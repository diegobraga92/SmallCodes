// =============================================================================
// event_store.rs — Event Store (Infrastructure Layer)
// =============================================================================
//
// WHAT IS AN EVENT STORE?
//   An event store is a database that stores events as the source of truth.
//   Unlike a traditional database where you UPDATE rows, an event store only
//   APPENDS new events. The current state is derived by replaying events.
//
// KEY OPERATIONS:
//   1. append_events: Add new events to the stream (with optimistic concurrency)
//   2. read_events: Load all events for a stream (for replay)
//   3. save_snapshot: Store a snapshot of the current state (performance)
//   4. load_latest_snapshot: Load the most recent snapshot (performance)
//
// OPTIMISTIC CONCURRENCY:
//   When appending events, we check that the stream version hasn't changed
//   since we last read it. If it has, another command was processed first
//   and we need to retry (or reject the command).
//
//   SQL: INSERT INTO events WHERE expected_version = ?
//   If the version doesn't match, the insert fails (via a UNIQUE constraint
//   on (stream_id, version) or a CHECK constraint).
//
// SNAPSHOTS:
//   Replaying 10,000 events every time you need the current state is slow.
//   Snapshots store the aggregate state at a specific version. To get the
//   current state:
//     1. Load the latest snapshot (e.g., at version 9,500)
//     2. Replay only events after that snapshot (events 9,501 to 10,000)
//   This reduces replay from 10,000 events to 500 events.
// =============================================================================

use crate::domain::{Account, AccountEvent};
use sqlx::SqlitePool;

/// The event store — append-only log of events with snapshot support.
///
/// WHY Arc<SqlitePool>?
///   SqlitePool is already Arc internally (it's a handle to a connection pool).
///   We wrap it in Arc for the blanket impl pattern (same as TaskFlow).
pub struct EventStore {
    pool: SqlitePool,
}

impl EventStore {
    /// Create a new event store with the given connection pool.
    pub fn new(pool: SqlitePool) -> Self {
        Self { pool }
    }

    /// Initialize the database tables.
    ///
    /// We create two tables:
    ///   1. events — the append-only event log
    ///   2. snapshots — cached aggregate states for performance
    ///
    /// WHY TWO TABLES?
    ///   Events are the source of truth. Snapshots are a cache that can be
    ///   rebuilt from events at any time. Keeping them separate makes this
    ///   relationship explicit.
    pub async fn init(&self) -> Result<(), sqlx::Error> {
        // The events table stores individual events.
        // Each event has:
        //   - id: unique identifier (for idempotency)
        //   - stream_id: which aggregate this event belongs to
        //   - version: position in the stream (1, 2, 3, ...)
        //   - event_type: the variant name (for deserialization)
        //   - data: JSON-serialized event payload
        //   - timestamp: when the event occurred
        //
        // UNIQUE(stream_id, version):
        //   This enforces optimistic concurrency. If two commands try to
        //   append at the same version, one will fail with a UNIQUE violation.
        sqlx::query(
            "CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                stream_id TEXT NOT NULL,
                version INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                data TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                UNIQUE(stream_id, version)
            )",
        )
        .execute(&self.pool)
        .await?;

        // Index for fast stream reads: "give me all events for account 123"
        sqlx::query(
            "CREATE INDEX IF NOT EXISTS idx_events_stream
             ON events(stream_id, version)",
        )
        .execute(&self.pool)
        .await?;

        // The snapshots table stores cached aggregate states.
        //   - stream_id: which aggregate this snapshot is for
        //   - version: the aggregate version at snapshot time
        //   - data: JSON-serialized aggregate state
        //   - timestamp: when the snapshot was taken
        sqlx::query(
            "CREATE TABLE IF NOT EXISTS snapshots (
                stream_id TEXT PRIMARY KEY,
                version INTEGER NOT NULL,
                data TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )",
        )
        .execute(&self.pool)
        .await?;

        Ok(())
    }

    /// Append events to a stream with optimistic concurrency control.
    ///
    /// HOW IT WORKS:
    ///   1. We check the current version of the stream
    ///   2. We verify it matches the expected_version
    ///   3. We insert the new events with sequential versions
    ///   4. If the version doesn't match, we return a ConcurrencyConflict error
    ///
    /// WHY RETURN THE EVENTS BACK?
    ///   The caller needs the events with their assigned versions for
    ///   updating projections. Returning them avoids a second read.
    ///
    /// ATOMICITY:
    ///   All events are inserted in a single transaction. Either all succeed
    ///   or none do. This prevents partial updates.
    pub async fn append_events(
        &self,
        stream_id: &str,
        expected_version: u64,
        events: &[AccountEvent],
    ) -> Result<Vec<StoredEvent>, crate::domain::AccountError> {
        // Start a transaction for atomicity
        let mut tx = self
            .pool
            .begin()
            .await
            .map_err(|e| crate::domain::AccountError::Database(e.to_string()))?;

        // Check the current version of the stream
        let current_version: Option<(i64,)> = sqlx::query_as(
            "SELECT COALESCE(MAX(version), 0) FROM events WHERE stream_id = ?",
        )
        .bind(stream_id)
        .fetch_optional(&mut *tx)
        .await
        .map_err(|e| crate::domain::AccountError::Database(e.to_string()))?;

        let current_version = current_version.map(|v| v.0 as u64).unwrap_or(0);

        // Optimistic concurrency check
        if current_version != expected_version {
            return Err(crate::domain::AccountError::ConcurrencyConflict {
                expected: expected_version,
                actual: current_version,
            });
        }

        // Insert each event with sequential versions
        let mut stored_events = Vec::with_capacity(events.len());
        for (i, event) in events.iter().enumerate() {
            let version = expected_version + 1 + i as u64;
            let event_id = uuid::Uuid::new_v4().to_string();
            let event_type = event_type_name(event);
            let data = serde_json::to_string(event)
                .map_err(|e| crate::domain::AccountError::Database(e.to_string()))?;
            let timestamp = chrono::Utc::now().to_rfc3339();

            sqlx::query(
                "INSERT INTO events (id, stream_id, version, event_type, data, timestamp)
                 VALUES (?, ?, ?, ?, ?, ?)",
            )
            .bind(&event_id)
            .bind(stream_id)
            .bind(version as i64)
            .bind(&event_type)
            .bind(&data)
            .bind(&timestamp)
            .execute(&mut *tx)
            .await
            .map_err(|e| crate::domain::AccountError::Database(e.to_string()))?;

            stored_events.push(StoredEvent {
                id: event_id,
                stream_id: stream_id.to_string(),
                version,
                event_type,
                event: event.clone(),
                timestamp,
            });
        }

        // Commit the transaction
        tx.commit()
            .await
            .map_err(|e| crate::domain::AccountError::Database(e.to_string()))?;

        Ok(stored_events)
    }

    /// Read all events for a stream, ordered by version.
    ///
    /// This is used to rebuild the aggregate state by replaying events.
    /// The events are returned in order (version 1, 2, 3, ...).
    ///
    /// WHY READ ALL EVENTS?
    ///   For a full rebuild. In practice, you'd combine this with a snapshot
    ///   (see load_events_after_snapshot).
    pub async fn read_events(&self, stream_id: &str) -> Result<Vec<StoredEvent>, crate::domain::AccountError> {
        let rows: Vec<(String, String, i64, String, String, String)> = sqlx::query_as(
            "SELECT id, stream_id, version, event_type, data, timestamp
             FROM events
             WHERE stream_id = ?
             ORDER BY version ASC",
        )
        .bind(stream_id)
        .fetch_all(&self.pool)
        .await
        .map_err(|e| crate::domain::AccountError::Database(e.to_string()))?;

        let mut events = Vec::with_capacity(rows.len());
        for (id, stream_id, version, event_type, data, timestamp) in rows {
            let event: AccountEvent = serde_json::from_str(&data)
                .map_err(|e| crate::domain::AccountError::Database(e.to_string()))?;

            events.push(StoredEvent {
                id,
                stream_id,
                version: version as u64,
                event_type,
                event,
                timestamp,
            });
        }

        Ok(events)
    }

    /// Save a snapshot of the aggregate state.
    ///
    /// WHEN TO SNAPSHOT?
    ///   A common strategy is to snapshot every N events (e.g., every 100).
    ///   This limits replay to at most 99 events after the latest snapshot.
    ///
    /// UPSERT:
    ///   We use INSERT OR REPLACE because there's only one snapshot per stream.
    ///   The latest snapshot replaces any previous one.
    pub async fn save_snapshot(&self, account: &Account) -> Result<(), crate::domain::AccountError> {
        let data = serde_json::to_string(account)
            .map_err(|e| crate::domain::AccountError::Database(e.to_string()))?;
        let timestamp = chrono::Utc::now().to_rfc3339();

        sqlx::query(
            "INSERT OR REPLACE INTO snapshots (stream_id, version, data, timestamp)
             VALUES (?, ?, ?, ?)",
        )
        .bind(&account.account_id)
        .bind(account.version as i64)
        .bind(&data)
        .bind(&timestamp)
        .execute(&self.pool)
        .await
        .map_err(|e| crate::domain::AccountError::Database(e.to_string()))?;

        Ok(())
    }

    /// Load the latest snapshot for a stream.
    ///
    /// Returns None if no snapshot exists (e.g., first time loading).
    pub async fn load_latest_snapshot(
        &self,
        stream_id: &str,
    ) -> Result<Option<Account>, crate::domain::AccountError> {
        let row: Option<(String, i64, String, String)> = sqlx::query_as(
            "SELECT stream_id, version, data, timestamp
             FROM snapshots
             WHERE stream_id = ?",
        )
        .bind(stream_id)
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| crate::domain::AccountError::Database(e.to_string()))?;

        match row {
            Some((_, _, data, _)) => {
                let account: Account = serde_json::from_str(&data)
                    .map_err(|e| crate::domain::AccountError::Database(e.to_string()))?;
                Ok(Some(account))
            }
            None => Ok(None),
        }
    }

    /// Load the aggregate state using snapshot + event replay.
    ///
    /// This is the OPTIMIZED way to get the current state:
    ///   1. Load the latest snapshot (if any)
    ///   2. Load only events AFTER the snapshot version
    ///   3. Replay those events on top of the snapshot
    ///
    /// If no snapshot exists, it replays all events from scratch.
    pub async fn load_aggregate(
        &self,
        stream_id: &str,
    ) -> Result<Option<Account>, crate::domain::AccountError> {
        // Step 1: Load the latest snapshot
        let snapshot = self.load_latest_snapshot(stream_id).await?;

        let (mut state, snapshot_version) = match snapshot {
            Some(ref account) => (account.clone(), account.version),
            None => (Account::new(), 0),
        };

        // Step 2: Load events after the snapshot version
        let rows: Vec<(String, String, i64, String, String, String)> = sqlx::query_as(
            "SELECT id, stream_id, version, event_type, data, timestamp
             FROM events
             WHERE stream_id = ? AND version > ?
             ORDER BY version ASC",
        )
        .bind(stream_id)
        .bind(snapshot_version as i64)
        .fetch_all(&self.pool)
        .await
        .map_err(|e| crate::domain::AccountError::Database(e.to_string()))?;

        // Step 3: Replay events on top of the snapshot
        for (_id, _stream_id, _version, _event_type, data, _timestamp) in &rows {
            let event: AccountEvent = serde_json::from_str(data)
                .map_err(|e| crate::domain::AccountError::Database(e.to_string()))?;
            state = Account::apply(&event, &state);
        }

        if state.version == 0 {
            // No events found — account doesn't exist
            Ok(None)
        } else {
            Ok(Some(state))
        }
    }

    /// Get the total number of events for a stream.
    /// Useful for deciding when to snapshot (e.g., every 100 events).
    pub async fn event_count(&self, stream_id: &str) -> Result<u64, crate::domain::AccountError> {
        let count: (i64,) = sqlx::query_as(
            "SELECT COUNT(*) FROM events WHERE stream_id = ?",
        )
        .bind(stream_id)
        .fetch_one(&self.pool)
        .await
        .map_err(|e| crate::domain::AccountError::Database(e.to_string()))?;

        Ok(count.0 as u64)
    }
}

// =============================================================================
// StoredEvent — An event with its metadata
// =============================================================================

/// An event as stored in the database, with metadata.
///
/// WHY SEPARATE FROM AccountEvent?
///   AccountEvent is the domain event (pure data).
///   StoredEvent adds metadata: database ID, version, timestamp.
///   This separation keeps the domain clean of infrastructure concerns.
#[derive(Clone, Debug)]
pub struct StoredEvent {
    /// Unique database ID (UUID v4).
    pub id: String,
    /// The aggregate this event belongs to.
    pub stream_id: String,
    /// Position in the event stream (1, 2, 3, ...).
    pub version: u64,
    /// The event type name (for debugging and deserialization).
    pub event_type: String,
    /// The actual domain event.
    pub event: AccountEvent,
    /// When the event was stored (ISO 8601).
    pub timestamp: String,
}

// =============================================================================
// Helper Functions
// =============================================================================

/// Get the variant name of an AccountEvent as a string.
/// Used for the event_type column in the database.
fn event_type_name(event: &AccountEvent) -> String {
    match event {
        AccountEvent::AccountOpened { .. } => "AccountOpened",
        AccountEvent::MoneyDeposited { .. } => "MoneyDeposited",
        AccountEvent::MoneyWithdrawn { .. } => "MoneyWithdrawn",
    }
    .to_string()
}

// =============================================================================
// Unit Tests
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::AccountEvent;

    /// Helper to create an in-memory SQLite database for testing.
    async fn create_test_store() -> EventStore {
        let pool = SqlitePool::connect("sqlite::memory:")
            .await
            .expect("Failed to create in-memory SQLite");
        let store = EventStore::new(pool);
        store.init().await.expect("Failed to init store");
        store
    }

    #[tokio::test]
    async fn test_append_and_read_events() {
        let store = create_test_store().await;

        let events = vec![
            AccountEvent::AccountOpened {
                account_id: "test-1".to_string(),
                owner: "Alice".to_string(),
                initial_balance: 10000,
                opened_at: chrono::Utc::now().to_rfc3339(),
            },
        ];

        let stored = store
            .append_events("test-1", 0, &events)
            .await
            .expect("Failed to append events");

        assert_eq!(stored.len(), 1);
        assert_eq!(stored[0].version, 1);

        let read = store
            .read_events("test-1")
            .await
            .expect("Failed to read events");

        assert_eq!(read.len(), 1);
        assert_eq!(read[0].version, 1);
    }

    #[tokio::test]
    async fn test_optimistic_concurrency() {
        let store = create_test_store().await;

        let events = vec![
            AccountEvent::AccountOpened {
                account_id: "test-2".to_string(),
                owner: "Bob".to_string(),
                initial_balance: 5000,
                opened_at: chrono::Utc::now().to_rfc3339(),
            },
        ];

        // First append succeeds (expected_version = 0)
        store
            .append_events("test-2", 0, &events)
            .await
            .expect("First append should succeed");

        // Second append with wrong version fails
        let result = store
            .append_events("test-2", 0, &events)
            .await;

        assert!(result.is_err());
        match result.unwrap_err() {
            crate::domain::AccountError::ConcurrencyConflict {
                expected: _,
                actual: 1,
            } => {} // Expected: actual version is 1, not 0
            other => panic!("Expected ConcurrencyConflict, got: {:?}", other),
        }
    }

    #[tokio::test]
    async fn test_snapshot_and_replay() {
        let store = create_test_store().await;

        // Append 3 events
        let events = vec![
            AccountEvent::AccountOpened {
                account_id: "test-3".to_string(),
                owner: "Charlie".to_string(),
                initial_balance: 10000,
                opened_at: chrono::Utc::now().to_rfc3339(),
            },
            AccountEvent::MoneyDeposited {
                account_id: "test-3".to_string(),
                amount: 5000,
                deposited_at: chrono::Utc::now().to_rfc3339(),
            },
            AccountEvent::MoneyWithdrawn {
                account_id: "test-3".to_string(),
                amount: 3000,
                withdrawn_at: chrono::Utc::now().to_rfc3339(),
            },
        ];

        store
            .append_events("test-3", 0, &events)
            .await
            .expect("Failed to append events");

        // Load aggregate (no snapshot yet — replays all 3 events)
        let account = store
            .load_aggregate("test-3")
            .await
            .expect("Failed to load aggregate")
            .expect("Aggregate should exist");

        assert_eq!(account.balance, 12000);
        assert_eq!(account.version, 3);

        // Save a snapshot at version 3
        store
            .save_snapshot(&account)
            .await
            .expect("Failed to save snapshot");

        // Append another event
        let more_events = vec![AccountEvent::MoneyDeposited {
            account_id: "test-3".to_string(),
            amount: 2000,
            deposited_at: chrono::Utc::now().to_rfc3339(),
        }];

        store
            .append_events("test-3", 3, &more_events)
            .await
            .expect("Failed to append more events");

        // Load aggregate (uses snapshot at version 3 + replays 1 event)
        let account = store
            .load_aggregate("test-3")
            .await
            .expect("Failed to load aggregate")
            .expect("Aggregate should exist");

        assert_eq!(account.balance, 14000); // 12000 + 2000
        assert_eq!(account.version, 4);
    }

    #[tokio::test]
    async fn test_nonexistent_account() {
        let store = create_test_store().await;

        let account = store
            .load_aggregate("nonexistent")
            .await
            .expect("Failed to load aggregate");

        assert!(account.is_none());
    }
}
