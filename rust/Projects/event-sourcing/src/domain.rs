// =============================================================================
// domain.rs — Core Business Entities (Domain Layer)
// =============================================================================
//
// WHAT IS THE DOMAIN LAYER?
//   The innermost layer of Clean Architecture. It contains:
//   - Events: facts that have happened (past tense, immutable)
//   - Commands: intents that may or may not succeed (imperative tense)
//   - Aggregate: the current state rebuilt from events
//
// CLEAN ARCHITECTURE RULE:
//   Domain layer has ZERO external dependencies beyond serde.
//   No database, no async runtime, no HTTP framework.
//   This makes it testable in isolation and framework-agnostic.
//
// EVENT SOURCING KEY CONCEPTS:
//   1. Events are the source of truth — never deleted, never mutated
//   2. Current state is derived by replaying events
//   3. Commands are validated against current state before producing events
//   4. Events are named in past tense (AccountOpened, MoneyDeposited)
// =============================================================================

use serde::{Deserialize, Serialize};

// =============================================================================
// AccountEvent — The Event Types
// =============================================================================
//
// WHY PAST TENSE?
//   Events represent facts that have already happened. They cannot be
//   changed or undone. If a mistake is made, you append a compensating
//   event (e.g., MoneyWithdrawn in error → MoneyDeposited correction).
//
// WHY AN ENUM?
//   All account events flow through the same event store. The enum
//   variant determines the event type. This is simpler than separate
//   tables per event type for a demo.
//
// WHY SERIALIZE/DESERIALIZE?
//   Events are stored as JSON in SQLite. serde enables this.
//   In production, you might use protobuf or Avro for schema evolution.
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub enum AccountEvent {
    /// An account was opened with an initial deposit.
    AccountOpened {
        account_id: String,
        owner: String,
        initial_balance: i64, // Amount in cents (avoid floats for money)
        opened_at: String,    // ISO 8601 timestamp
    },

    /// Money was deposited into an account.
    MoneyDeposited {
        account_id: String,
        amount: i64,          // Amount in cents
        deposited_at: String, // ISO 8601 timestamp
    },

    /// Money was withdrawn from an account.
    MoneyWithdrawn {
        account_id: String,
        amount: i64,          // Amount in cents
        withdrawn_at: String, // ISO 8601 timestamp
    },
}

// =============================================================================
// AccountCommand — The Command Types
// =============================================================================
//
// WHY IMPERATIVE TENSE?
//   Commands represent intents. They may be rejected if business rules
//   are violated (e.g., insufficient funds). If accepted, they produce
//   one or more events.
//
// COMMAND vs EVENT:
//   Command: "Withdraw $30 from account 123"
//     → Validated against current state
//     → If balance >= 30, produces MoneyWithdrawn event
//     → If balance < 30, returns error (no event produced)
//
//   Event: "MoneyWithdrawn { account: 123, amount: 30 }"
//     → A fact that happened
//     → Cannot be rejected
//     → Stored permanently
#[derive(Clone, Debug)]
pub enum AccountCommand {
    /// Open a new account with an initial deposit.
    OpenAccount { owner: String, initial_balance: i64 },

    /// Deposit money into an existing account.
    Deposit { account_id: String, amount: i64 },

    /// Withdraw money from an existing account.
    Withdraw { account_id: String, amount: i64 },
}

// =============================================================================
// Account — The Aggregate (Current State)
// =============================================================================
//
// WHAT IS AN AGGREGATE?
//   In Domain-Driven Design (DDD), an Aggregate is a cluster of domain
//   objects that are treated as a single unit. The Account aggregate
//   includes the account state and all events that have happened to it.
//
// WHY IS THIS CALLED AN AGGREGATE AND NOT JUST A STRUCT?
//   - It has an identity (account_id)
//   - It has a version number for optimistic concurrency
//   - Its state is derived from events (not stored directly)
//   - It enforces invariants (balance cannot go negative)
//
// VERSION FIELD:
//   The version tracks how many events have been applied. When we save
//   new events, we check that the version hasn't changed (optimistic
//   concurrency). This prevents lost updates when two commands race.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Account {
    /// Unique identifier for the account.
    pub account_id: String,

    /// Account owner's name.
    pub owner: String,

    /// Current balance in cents. Never negative.
    pub balance: i64,

    /// Number of events applied to this aggregate.
    /// Used for optimistic concurrency control.
    pub version: u64,

    /// Whether the account is open.
    pub is_open: bool,
}

impl Account {
    /// Create a new, empty account (zero state).
    /// This is the starting point before any events are applied.
    pub fn new() -> Self {
        Self {
            account_id: String::new(),
            owner: String::new(),
            balance: 0,
            version: 0,
            is_open: false,
        }
    }

    /// Apply an event to the aggregate, returning the new state.
    ///
    /// This is the CORE of event sourcing. Instead of mutating state
    /// directly, we apply events to derive the new state. This function
    /// is a pure function: given a state and an event, it returns a new state.
    ///
    /// WHY IS THIS A PURE FUNCTION?
    ///   - No side effects (no database writes, no I/O)
    ///   - Deterministic (same input always produces same output)
    ///   - Testable in isolation (no mocks needed)
    ///   - Replayable (can rebuild state from any point in time)
    ///
    /// WHY DOESN'T THIS MUTATE self?
    ///   Immutability makes reasoning about state changes easier.
    ///   In practice, you might mutate for performance, but the pure
    ///   function approach is clearer for learning.
    pub fn apply(event: &AccountEvent, state: &Account) -> Account {
        match event {
            AccountEvent::AccountOpened {
                account_id,
                owner,
                initial_balance,
                ..
            } => Account {
                account_id: account_id.clone(),
                owner: owner.clone(),
                balance: *initial_balance,
                version: state.version + 1,
                is_open: true,
            },

            AccountEvent::MoneyDeposited { amount, .. } => Account {
                balance: state.balance + amount,
                version: state.version + 1,
                ..state.clone()
            },

            AccountEvent::MoneyWithdrawn { amount, .. } => Account {
                balance: state.balance - amount,
                version: state.version + 1,
                ..state.clone()
            },
        }
    }

    /// Rebuild the aggregate state by replaying all events from scratch.
    ///
    /// This is how you get the current state in event sourcing:
    ///   1. Start with an empty aggregate (Account::new())
    ///   2. Apply each event in order
    ///   3. The result is the current state
    ///
    /// WHY REPLAY FROM SCRATCH INSTEAD OF STORING CURRENT STATE?
    ///   - You can rebuild state at any point in time (temporal query)
    ///   - You can fix bugs by replaying with corrected event handlers
    ///   - You can add new projections by replaying all events
    ///
    /// PERFORMANCE NOTE:
    ///   Replaying 10 events is instant. Replaying 10 million events
    ///   is slow. That's why we use snapshots (see event_store.rs).
    pub fn rebuild(events: &[AccountEvent]) -> Self {
        let mut state = Account::new();
        for event in events {
            state = Account::apply(event, &state);
        }
        state
    }
}

impl Default for Account {
    fn default() -> Self {
        Self::new()
    }
}

// =============================================================================
// Error Types
// =============================================================================

/// Errors that can occur when handling commands.
/// Using thiserror for ergonomic error types with Display/Error derives.
#[derive(Debug, thiserror::Error)]
pub enum AccountError {
    /// Account doesn't exist (tried to deposit/withdraw from unknown account).
    #[error("Account {0} not found")]
    AccountNotFound(String),

    /// Account is closed (tried to deposit/withdraw from closed account).
    #[error("Account {0} is closed")]
    AccountClosed(String),

    /// Insufficient funds for withdrawal.
    #[error("Insufficient funds: balance={balance}, requested={requested}")]
    InsufficientFunds {
        /// Current balance in cents.
        balance: i64,
        /// Requested withdrawal amount in cents.
        requested: i64,
    },

    /// Invalid amount (negative or zero).
    #[error("Invalid amount: {0}")]
    InvalidAmount(i64),

    /// Optimistic concurrency conflict.
    #[error("Concurrency conflict: expected version {expected}, actual version {actual}")]
    ConcurrencyConflict {
        /// The version we expected when reading.
        expected: u64,
        /// The actual version in the database.
        actual: u64,
    },

    /// Database error.
    #[error("Database error: {0}")]
    Database(String),
}

impl From<sqlx::Error> for AccountError {
    fn from(error: sqlx::Error) -> Self {
        AccountError::Database(error.to_string())
    }
}

impl From<serde_json::Error> for AccountError {
    fn from(error: serde_json::Error) -> Self {
        AccountError::Database(error.to_string())
    }
}

// =============================================================================
// Unit Tests
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_empty_account() {
        let account = Account::new();
        assert_eq!(account.balance, 0);
        assert!(!account.is_open);
        assert_eq!(account.version, 0);
    }

    #[test]
    fn test_open_account() {
        let event = AccountEvent::AccountOpened {
            account_id: "123".to_string(),
            owner: "Alice".to_string(),
            initial_balance: 10000, // $100.00
            opened_at: "2024-01-01T00:00:00Z".to_string(),
        };

        let account = Account::apply(&event, &Account::new());
        assert_eq!(account.balance, 10000);
        assert!(account.is_open);
        assert_eq!(account.version, 1);
        assert_eq!(account.owner, "Alice");
    }

    #[test]
    fn test_deposit() {
        let opened = AccountEvent::AccountOpened {
            account_id: "123".to_string(),
            owner: "Alice".to_string(),
            initial_balance: 10000,
            opened_at: "2024-01-01T00:00:00Z".to_string(),
        };

        let deposit = AccountEvent::MoneyDeposited {
            account_id: "123".to_string(),
            amount: 5000, // $50.00
            deposited_at: "2024-01-02T00:00:00Z".to_string(),
        };

        let state = Account::apply(&opened, &Account::new());
        let state = Account::apply(&deposit, &state);

        assert_eq!(state.balance, 15000);
        assert_eq!(state.version, 2);
    }

    #[test]
    fn test_withdraw() {
        let opened = AccountEvent::AccountOpened {
            account_id: "123".to_string(),
            owner: "Alice".to_string(),
            initial_balance: 10000,
            opened_at: "2024-01-01T00:00:00Z".to_string(),
        };

        let withdraw = AccountEvent::MoneyWithdrawn {
            account_id: "123".to_string(),
            amount: 3000, // $30.00
            withdrawn_at: "2024-01-02T00:00:00Z".to_string(),
        };

        let state = Account::apply(&opened, &Account::new());
        let state = Account::apply(&withdraw, &state);

        assert_eq!(state.balance, 7000);
        assert_eq!(state.version, 2);
    }

    #[test]
    fn test_rebuild_from_events() {
        let events = vec![
            AccountEvent::AccountOpened {
                account_id: "123".to_string(),
                owner: "Alice".to_string(),
                initial_balance: 10000,
                opened_at: "2024-01-01T00:00:00Z".to_string(),
            },
            AccountEvent::MoneyDeposited {
                account_id: "123".to_string(),
                amount: 5000,
                deposited_at: "2024-01-02T00:00:00Z".to_string(),
            },
            AccountEvent::MoneyWithdrawn {
                account_id: "123".to_string(),
                amount: 3000,
                withdrawn_at: "2024-01-03T00:00:00Z".to_string(),
            },
        ];

        let account = Account::rebuild(&events);
        assert_eq!(account.balance, 12000); // 10000 + 5000 - 3000
        assert_eq!(account.version, 3);
        assert!(account.is_open);
    }

    #[test]
    fn test_rebuild_empty_events() {
        let account = Account::rebuild(&[]);
        assert_eq!(account.balance, 0);
        assert_eq!(account.version, 0);
        assert!(!account.is_open);
    }
}
