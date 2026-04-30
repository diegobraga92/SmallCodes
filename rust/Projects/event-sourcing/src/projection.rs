// =============================================================================
// projection.rs — Read-Side Projections (CQRS Read Model)
// =============================================================================
//
// WHAT IS A PROJECTION?
//   In CQRS, a projection is a read-optimized view of data that is built
//   from events. While the event store is the source of truth, projections
//   provide query-friendly representations of that data.
//
// WHY SEPARATE READ MODELS?
//   The event store is optimized for appending events and rebuilding state.
//   It's NOT optimized for queries like "show me the last 10 transactions."
//   Projections are:
//   - Optimized for specific query patterns
//   - Updated asynchronously (eventual consistency)
//   - Potentially denormalized for fast reads
//
// THIS PROJECTION: Transaction History
//   We maintain a `transactions` table that stores each financial transaction
//   as a separate row. This makes it easy to query:
//   - "Show me all transactions for account 123"
//   - "Show me the last 5 deposits"
//   - "What was the balance after each transaction?"
//
// EVENTUAL CONSISTENCY:
//   In a distributed system, projections might lag behind the event store.
//   A client that writes and immediately reads might not see their write.
//   In this demo, we update projections synchronously (same transaction),
//   so consistency is immediate. In production, you'd use async subscribers.
// =============================================================================

use crate::domain::AccountEvent;
use crate::event_store::StoredEvent;
use sqlx::SqlitePool;

/// A single transaction in the transaction history projection.
///
/// This is a denormalized read model — it combines data from multiple
/// event types into a single, query-friendly format.
#[derive(Clone, Debug, sqlx::FromRow)]
pub struct Transaction {
    /// Unique transaction ID (UUID v4).
    pub id: String,
    /// The account this transaction belongs to.
    pub account_id: String,
    /// The event version that produced this transaction.
    pub event_version: i64,
    /// Type of transaction: "deposit" or "withdrawal".
    pub transaction_type: String,
    /// Amount in cents.
    pub amount: i64,
    /// Running balance after this transaction (in cents).
    pub balance_after: i64,
    /// Description of the transaction.
    pub description: String,
    /// When the transaction occurred (ISO 8601).
    pub timestamp: String,
}

/// The projection store — maintains read-optimized views of event data.
pub struct ProjectionStore {
    pool: SqlitePool,
}

impl ProjectionStore {
    /// Create a new projection store.
    pub fn new(pool: SqlitePool) -> Self {
        Self { pool }
    }

    /// Initialize the projection tables.
    pub async fn init(&self) -> Result<(), sqlx::Error> {
        sqlx::query(
            "CREATE TABLE IF NOT EXISTS transactions (
                id TEXT PRIMARY KEY,
                account_id TEXT NOT NULL,
                event_version INTEGER NOT NULL,
                transaction_type TEXT NOT NULL,
                amount INTEGER NOT NULL,
                balance_after INTEGER NOT NULL,
                description TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )",
        )
        .execute(&self.pool)
        .await?;

        // Index for fast queries: "give me all transactions for account 123"
        sqlx::query(
            "CREATE INDEX IF NOT EXISTS idx_transactions_account
             ON transactions(account_id, event_version)",
        )
        .execute(&self.pool)
        .await?;

        Ok(())
    }

    /// Handle a batch of stored events, updating projections.
    ///
    /// This is called AFTER events are appended to the event store.
    /// It processes each event and updates the relevant projections.
    ///
    /// WHY TAKE StoredEvent INSTEAD OF AccountEvent?
    ///   StoredEvent has metadata (version, timestamp) that we need
    ///   for the projection. AccountEvent is the pure domain event.
    pub async fn handle_events(
        &self,
        events: &[StoredEvent],
    ) -> Result<(), sqlx::Error> {
        for stored in events {
            match &stored.event {
                AccountEvent::AccountOpened {
                    account_id,
                    initial_balance,
                    ..
                } => {
                    // Record the initial deposit as a transaction
                    self.insert_transaction(
                        account_id,
                        stored.version as i64,
                        "deposit",
                        *initial_balance,
                        *initial_balance,
                        "Initial deposit (account opened)",
                        &stored.timestamp,
                    )
                    .await?;
                }

                AccountEvent::MoneyDeposited {
                    account_id, amount, ..
                } => {
                    // Calculate the running balance by summing all previous
                    // transactions for this account, then adding this deposit.
                    let balance_before = self.get_current_balance(account_id).await?;
                    let balance_after = balance_before + amount;

                    self.insert_transaction(
                        account_id,
                        stored.version as i64,
                        "deposit",
                        *amount,
                        balance_after,
                        &format!("Deposit of ${:.2}", *amount as f64 / 100.0),
                        &stored.timestamp,
                    )
                    .await?;
                }

                AccountEvent::MoneyWithdrawn {
                    account_id, amount, ..
                } => {
                    let balance_before = self.get_current_balance(account_id).await?;
                    let balance_after = balance_before - amount;

                    self.insert_transaction(
                        account_id,
                        stored.version as i64,
                        "withdrawal",
                        *amount,
                        balance_after,
                        &format!("Withdrawal of ${:.2}", *amount as f64 / 100.0),
                        &stored.timestamp,
                    )
                    .await?;
                }
            }
        }

        Ok(())
    }

    /// Insert a single transaction into the projection table.
    async fn insert_transaction(
        &self,
        account_id: &str,
        event_version: i64,
        transaction_type: &str,
        amount: i64,
        balance_after: i64,
        description: &str,
        timestamp: &str,
    ) -> Result<(), sqlx::Error> {
        let id = uuid::Uuid::new_v4().to_string();

        sqlx::query(
            "INSERT INTO transactions (id, account_id, event_version, transaction_type,
             amount, balance_after, description, timestamp)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        )
        .bind(&id)
        .bind(account_id)
        .bind(event_version)
        .bind(transaction_type)
        .bind(amount)
        .bind(balance_after)
        .bind(description)
        .bind(timestamp)
        .execute(&self.pool)
        .await?;

        Ok(())
    }

    /// Get the current balance by summing all transactions for an account.
    ///
    /// This is an alternative to rebuilding from events — we use the
    /// projection to compute the balance. This is faster than replaying
    /// events because we only need to sum one column.
    ///
    /// WHY NOT JUST USE THE AGGREGATE?
    ///   The aggregate is rebuilt from events (snapshot + replay).
    ///   The projection is a pre-computed view. Both should agree.
    ///   Having both is a consistency check.
    async fn get_current_balance(&self, account_id: &str) -> Result<i64, sqlx::Error> {
        // Sum all deposits and subtract all withdrawals
        let deposits: Option<(Option<i64>,)> = sqlx::query_as(
            "SELECT SUM(amount) FROM transactions
             WHERE account_id = ? AND transaction_type = 'deposit'",
        )
        .bind(account_id)
        .fetch_optional(&self.pool)
        .await?;

        let withdrawals: Option<(Option<i64>,)> = sqlx::query_as(
            "SELECT SUM(amount) FROM transactions
             WHERE account_id = ? AND transaction_type = 'withdrawal'",
        )
        .bind(account_id)
        .fetch_optional(&self.pool)
        .await?;

        let total_deposits = deposits.and_then(|r| r.0).unwrap_or(0);
        let total_withdrawals = withdrawals.and_then(|r| r.0).unwrap_or(0);

        Ok(total_deposits - total_withdrawals)
    }

    /// Get all transactions for an account, ordered by version.
    pub async fn get_transactions(
        &self,
        account_id: &str,
    ) -> Result<Vec<Transaction>, sqlx::Error> {
        let transactions: Vec<Transaction> = sqlx::query_as(
            "SELECT id, account_id, event_version, transaction_type,
             amount, balance_after, description, timestamp
             FROM transactions
             WHERE account_id = ?
             ORDER BY event_version ASC",
        )
        .bind(account_id)
        .fetch_all(&self.pool)
        .await?;

        Ok(transactions)
    }
}

// =============================================================================
// Unit Tests
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::AccountEvent;

    /// Helper to create an in-memory SQLite database for testing.
    async fn create_test_store() -> ProjectionStore {
        let pool = SqlitePool::connect("sqlite::memory:")
            .await
            .expect("Failed to create in-memory SQLite");
        let store = ProjectionStore::new(pool);
        store.init().await.expect("Failed to init store");
        store
    }

    /// Helper to create a StoredEvent from an AccountEvent.
    fn make_stored_event(account_id: &str, version: u64, event: AccountEvent) -> StoredEvent {
        StoredEvent {
            id: uuid::Uuid::new_v4().to_string(),
            stream_id: account_id.to_string(),
            version,
            event_type: "test".to_string(),
            event,
            timestamp: chrono::Utc::now().to_rfc3339(),
        }
    }

    #[tokio::test]
    async fn test_account_opened_projection() {
        let store = create_test_store().await;

        let event = AccountEvent::AccountOpened {
            account_id: "test-1".to_string(),
            owner: "Alice".to_string(),
            initial_balance: 10000,
            opened_at: chrono::Utc::now().to_rfc3339(),
        };

        let stored = make_stored_event("test-1", 1, event);
        store.handle_events(&[stored]).await.expect("Failed to handle events");

        let transactions = store
            .get_transactions("test-1")
            .await
            .expect("Failed to get transactions");

        assert_eq!(transactions.len(), 1);
        assert_eq!(transactions[0].transaction_type, "deposit");
        assert_eq!(transactions[0].amount, 10000);
        assert_eq!(transactions[0].balance_after, 10000);
    }

    #[tokio::test]
    async fn test_multiple_transactions() {
        let store = create_test_store().await;

        let events = vec![
            make_stored_event("test-2", 1, AccountEvent::AccountOpened {
                account_id: "test-2".to_string(),
                owner: "Bob".to_string(),
                initial_balance: 10000,
                opened_at: chrono::Utc::now().to_rfc3339(),
            }),
            make_stored_event("test-2", 2, AccountEvent::MoneyDeposited {
                account_id: "test-2".to_string(),
                amount: 5000,
                deposited_at: chrono::Utc::now().to_rfc3339(),
            }),
            make_stored_event("test-2", 3, AccountEvent::MoneyWithdrawn {
                account_id: "test-2".to_string(),
                amount: 3000,
                withdrawn_at: chrono::Utc::now().to_rfc3339(),
            }),
        ];

        store.handle_events(&events).await.expect("Failed to handle events");

        let transactions = store
            .get_transactions("test-2")
            .await
            .expect("Failed to get transactions");

        assert_eq!(transactions.len(), 3);
        assert_eq!(transactions[0].balance_after, 10000);
        assert_eq!(transactions[1].balance_after, 15000);
        assert_eq!(transactions[2].balance_after, 12000);
    }
}
