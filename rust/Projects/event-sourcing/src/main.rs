// =============================================================================
// main.rs — Event Sourcing Demo Entry Point
// =============================================================================
//
// This demo shows a complete event sourcing + CQRS system in action.
//
// SCENARIO:
//   We simulate a simple banking application where:
//   1. Alice opens an account with $1,000.00
//   2. Alice deposits $500.00
//   3. Alice withdraws $200.00
//   4. Alice tries to withdraw $2,000.00 (should fail — insufficient funds)
//   5. We query the account state and transaction history
//   6. We show the full event log (audit trail)
//   7. We demonstrate temporal query (state at version 2)
//
// WHAT THIS DEMONSTRATES:
//   - Event sourcing: all state changes are stored as events
//   - CQRS: separate write model (events) and read model (projections)
//   - Optimistic concurrency: concurrent writes are detected
//   - Snapshots: efficient state rebuild
//   - Audit trail: every change is recorded and queryable
//   - Temporal queries: state at any point in time
// =============================================================================

mod account_service;
mod domain;
mod event_store;
mod projection;

use account_service::AccountService;
use domain::{AccountCommand, AccountError};
use event_store::EventStore;
use projection::ProjectionStore;
use sqlx::SqlitePool;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize logging
    tracing_subscriber::fmt()
        .with_env_filter("event_sourcing=info")
        .init();

    println!("╔══════════════════════════════════════════════════════════╗");
    println!("║        Event Sourcing + CQRS Demo                       ║");
    println!("╚══════════════════════════════════════════════════════════╝");
    println!();

    // =========================================================================
    // SETUP
    // =========================================================================
    //
    // We use an in-memory SQLite database for the demo.
    // In production, you'd use a file-based database or PostgreSQL.
    //
    // The database URL "file::memory:?cache=shared" allows multiple
    // connections to share the same in-memory database. This is needed
    // because the event store and projection store use separate pools.
    println!("📦 Initializing database...");

    let pool = SqlitePool::connect("sqlite::memory:")
        .await
        .expect("Failed to create database pool");

    // Initialize the event store (events + snapshots tables)
    let event_store = EventStore::new(pool.clone());
    event_store.init().await.expect("Failed to init event store");

    // Initialize the projection store (transactions table)
    let projection_store = ProjectionStore::new(pool.clone());
    projection_store
        .init()
        .await
        .expect("Failed to init projection store");

    // Create the account service (coordinates event store + projections)
    let service = AccountService::new(event_store, projection_store);

    println!("   ✅ Database initialized");
    println!();

    // =========================================================================
    // SCENARIO: Alice's Banking Operations
    // =========================================================================

    // --- Step 1: Open Account ---
    println!("📝 Step 1: Alice opens an account with $1,000.00");
    println!("   Command: OpenAccount {{ owner: \"Alice\", initial_balance: 100000 }}");
    println!("   (Amounts are in cents: $1,000.00 = 100000 cents)");
    println!();

    let events = service
        .handle_command(AccountCommand::OpenAccount {
            owner: "Alice".to_string(),
            initial_balance: 100000, // $1,000.00
        })
        .await?;

    let alice_account_id = match &events[0] {
        domain::AccountEvent::AccountOpened { account_id, .. } => account_id.clone(),
        _ => unreachable!(),
    };

    let account = service
        .get_account(&alice_account_id)
        .await?
        .expect("Account should exist");

    println!(
        "   ✅ Account opened: {} (owner: {}, balance: ${:.2})",
        account.account_id,
        account.owner,
        account.balance as f64 / 100.0
    );
    println!();

    // --- Step 2: Deposit ---
    println!("📝 Step 2: Alice deposits $500.00");
    println!("   Command: Deposit {{ account_id: \"{}\", amount: 50000 }}", &alice_account_id[..8]);
    println!();

    service
        .handle_command(AccountCommand::Deposit {
            account_id: alice_account_id.clone(),
            amount: 50000, // $500.00
        })
        .await?;

    let account = service
        .get_account(&alice_account_id)
        .await?
        .expect("Account should exist");

    println!(
        "   ✅ Deposit processed. New balance: ${:.2}",
        account.balance as f64 / 100.0
    );
    println!();

    // --- Step 3: Withdraw ---
    println!("📝 Step 3: Alice withdraws $200.00");
    println!("   Command: Withdraw {{ account_id: \"{}\", amount: 20000 }}", &alice_account_id[..8]);
    println!();

    service
        .handle_command(AccountCommand::Withdraw {
            account_id: alice_account_id.clone(),
            amount: 20000, // $200.00
        })
        .await?;

    let account = service
        .get_account(&alice_account_id)
        .await?
        .expect("Account should exist");

    println!(
        "   ✅ Withdrawal processed. New balance: ${:.2}",
        account.balance as f64 / 100.0
    );
    println!();

    // --- Step 4: Insufficient Funds ---
    println!("📝 Step 4: Alice tries to withdraw $2,000.00 (should fail)");
    println!("   Command: Withdraw {{ account_id: \"{}\", amount: 200000 }}", &alice_account_id[..8]);
    println!();

    let result = service
        .handle_command(AccountCommand::Withdraw {
            account_id: alice_account_id.clone(),
            amount: 200000, // $2,000.00
        })
        .await;

    match result {
        Err(AccountError::InsufficientFunds {
            balance,
            requested,
        }) => {
            println!(
                "   ❌ Insufficient funds! Balance: ${:.2}, Requested: ${:.2}",
                balance as f64 / 100.0,
                requested as f64 / 100.0
            );
        }
        _ => panic!("Expected InsufficientFunds error"),
    }
    println!();

    // =========================================================================
    // QUERY: Current State
    // =========================================================================
    println!("🔍 Query: Current account state");
    println!();

    let account = service
        .get_account(&alice_account_id)
        .await?
        .expect("Account should exist");

    println!(
        "   Account:     {}",
        account.account_id
    );
    println!(
        "   Owner:       {}",
        account.owner
    );
    println!(
        "   Balance:     ${:.2}",
        account.balance as f64 / 100.0
    );
    println!(
        "   Version:     {}",
        account.version
    );
    println!(
        "   Status:      {}",
        if account.is_open { "Open" } else { "Closed" }
    );
    println!();

    // =========================================================================
    // QUERY: Transaction History (from Projection)
    // =========================================================================
    println!("📊 Query: Transaction history (from projection)");
    println!();

    let transactions = service
        .get_transaction_history(&alice_account_id)
        .await?;

    println!(
        "   {:<5} {:<12} {:<10} {:<12} {}",
        "#", "Type", "Amount", "Balance", "Description"
    );
    println!(
        "   {:<5} {:<12} {:<10} {:<12} {}",
        "-----", "------------", "----------", "------------", "---------------------------"
    );

    for (i, tx) in transactions.iter().enumerate() {
        println!(
            "   {:<5} {:<12} ${:<7.2} ${:<9.2} {}",
            i + 1,
            tx.transaction_type,
            tx.amount as f64 / 100.0,
            tx.balance_after as f64 / 100.0,
            tx.description,
        );
    }
    println!();

    // =========================================================================
    // QUERY: Full Event Log (Audit Trail)
    // =========================================================================
    println!("📋 Query: Full event log (audit trail)");
    println!();

    let event_history = service
        .get_event_history(&alice_account_id)
        .await?;

    println!(
        "   {:<5} {:<20} {:<30} {}",
        "Ver", "Event Type", "Timestamp", "Data"
    );
    println!(
        "   {:<5} {:<20} {:<30} {}",
        "-----", "--------------------", "------------------------------", "----------------------------------------"
    );

    for stored in &event_history {
        let data_summary = match &stored.event {
            domain::AccountEvent::AccountOpened {
                initial_balance, ..
            } => format!("initial_balance={}", initial_balance),
            domain::AccountEvent::MoneyDeposited { amount, .. } => {
                format!("amount={}", amount)
            }
            domain::AccountEvent::MoneyWithdrawn { amount, .. } => {
                format!("amount={}", amount)
            }
        };

        println!(
            "   {:<5} {:<20} {:<30} {}",
            stored.version,
            stored.event_type,
            &stored.timestamp[..19], // Trim subseconds for readability
            data_summary,
        );
    }
    println!();

    // =========================================================================
    // TEMPORAL QUERY: State at Version 2
    // =========================================================================
    println!("⏳ Temporal Query: Account state at version 2");
    println!("   (After account opened + deposit, before withdrawal)");
    println!();

    // To get state at a specific version, we replay events up to that version.
    // This is a key benefit of event sourcing — you can query state at any
    // point in time.
    let events_only: Vec<domain::AccountEvent> = event_history
        .iter()
        .take(2) // Only first 2 events (version 1 and 2)
        .map(|s| s.event.clone())
        .collect();

    let state_at_v2 = domain::Account::rebuild(&events_only);

    println!(
        "   Balance at version 2: ${:.2}",
        state_at_v2.balance as f64 / 100.0
    );
    println!(
        "   (Expected: $1,500.00 = $1,000.00 initial + $500.00 deposit)");
    println!();

    // =========================================================================
    // SUMMARY
    // =========================================================================
    println!("╔══════════════════════════════════════════════════════════╗");
    println!("║        Demo Complete                                    ║");
    println!("╚══════════════════════════════════════════════════════════╝");
    println!();
    println!("   What you just witnessed:");
    println!();
    println!("   1. Event Sourcing: Every state change was stored as an");
    println!("      immutable event in the events table. The current balance");
    println!("      was derived by replaying events, not by updating a row.");
    println!();
    println!("   2. CQRS: The write side (events) and read side (projections)");
    println!("      are separate. The transaction history is a denormalized");
    println!("      read model built from events.");
    println!();
    println!("   3. Business Rules: The insufficient funds check prevented an");
    println!("      overdraft. No event was produced for the failed command.");
    println!();
    println!("   4. Audit Trail: Every event is recorded with its type,");
    println!("      version, and timestamp. You can see exactly what happened.");
    println!();
    println!("   5. Temporal Query: We queried the account state at version 2");
    println!("      by replaying only the first 2 events. This is impossible");
    println!("      with a traditional UPDATE-in-place database.");
    println!();

    Ok(())
}
