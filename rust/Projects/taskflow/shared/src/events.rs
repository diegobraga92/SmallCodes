// =============================================================================
// events.rs — Event-Driven Communication
// =============================================================================
//
// WHAT IS EVENT-DRIVEN ARCHITECTURE?
//   Instead of Service A calling Service B directly (synchronous coupling),
//   Service A publishes an "event" and Service B reacts to it asynchronously.
//   This decouples the producer from the consumer.
//
//   Example flow:
//   1. API service creates a task
//   2. API service publishes TaskEvent::Created
//   3. Worker service receives the event (maybe seconds later)
//   4. Worker processes the task
//
//   The API service doesn't know about the worker. It just publishes events.
//   The worker doesn't know about the API. It just listens for events.
//
// WHY EVENTS INSTEAD OF DIRECT FUNCTION CALLS?
//   - Decoupling: API and Worker can be deployed independently
//   - Resilience: If Worker is down, events queue up (with a real message broker)
//   - Scalability: Multiple workers can process events in parallel
//   - Audit trail: Events can be logged and replayed
//
// WHAT IS THE EVENT BUS PATTERN?
//   An Event Bus is a mediator that sits between publishers and subscribers.
//   Publishers call event_bus.publish(event)
//   Subscribers call event_bus.subscribe() and get a Receiver
//   The bus delivers events from publishers to all subscribers.
//
// IN-MEMORY VS MESSAGE BROKER:
//   We use an in-memory tokio broadcast channel. This is fine for local demos
//   but has limitations:
//   - Events are lost if the process crashes
//   - Events cannot be replayed
//   - Only works within a single process
//   In production, you'd use Kafka, RabbitMQ, or NATS.
//   The EventBus trait makes this swap straightforward.
// =============================================================================

use crate::domain::Task;
use tokio::sync::broadcast;

// =============================================================================
// TaskEvent — The Event Type
// =============================================================================
//
// An enum of all possible events in the system.
// Currently only one variant (Created), but this can grow:
//   - TaskEvent::Updated(Task) — task description changed
//   - TaskEvent::Deleted(String) — task was removed
//   - TaskEvent::Failed { task_id: String, error: String } — processing failed
//
// WHY AN ENUM INSTEAD OF SEPARATE TYPES?
//   An enum gives us a single channel type. All events flow through the same
//   bus. Subscribers can match on the variant they care about.
//   Tradeoff: Adding a new variant requires updating all match statements.
#[derive(Clone, Debug)]
pub enum TaskEvent {
    /// A new task was created and needs processing.
    Created(Task),
}

// =============================================================================
// EventBus Trait — The Contract
// =============================================================================
//
// WHY A TRAIT?
//   Dependency Inversion Principle (the "D" in SOLID):
//   High-level modules (application layer) should not depend on low-level
//   modules (infrastructure). Both should depend on abstractions.
//
//   The EventBus trait is the abstraction. The application layer depends on
//   this trait, not on InMemoryEventBus or KafkaEventBus. This means:
//   - We can swap implementations without changing application code
//   - We can mock the event bus in tests
//   - The application layer is framework-agnostic
//
// WHY Send + Sync?
//   - Send: The event bus can be sent between threads (needed for tokio::spawn)
//   - Sync: The event bus can be shared between threads (needed for Arc)
//   Most infrastructure types in Rust need these bounds.
pub trait EventBus: Send + Sync {
    /// Publish an event to all subscribers.
    /// This is non-blocking — it returns immediately after sending.
    fn publish(&self, event: TaskEvent);

    /// Subscribe to receive events.
    /// Returns a broadcast::Receiver that can be awaited in an async context.
    fn subscribe(&self) -> broadcast::Receiver<TaskEvent>;
}

// =============================================================================
// InMemoryEventBus — Concrete Implementation
// =============================================================================
//
// Uses tokio's broadcast channel under the hood.
//
// HOW BROADCAST CHANNELS WORK:
//   - Multiple senders can send messages
//   - Multiple receivers all receive the same messages
//   - Messages are buffered up to a capacity
//   - Slow receivers that fall behind get a Lagged error
//   - When all receivers are dropped, messages are discarded
//
// CAPACITY = 100:
//   If the worker is slow and 100 events queue up, the 101st send will fail.
//   In production, you'd use an unbounded channel or a message broker that
//   handles backpressure. For this demo, 100 is plenty.
pub struct InMemoryEventBus {
    tx: broadcast::Sender<TaskEvent>,
}

impl InMemoryEventBus {
    /// Create a new event bus with the given buffer capacity.
    /// Capacity is the maximum number of events that can be buffered before
    /// slow subscribers start missing messages.
    pub fn new(capacity: usize) -> Self {
        let (tx, _) = broadcast::channel(capacity);
        Self { tx }
    }
}

impl EventBus for InMemoryEventBus {
    fn publish(&self, event: TaskEvent) {
        // broadcast::Sender::send returns an error if there are no receivers.
        // We ignore this error with `let _ =` because it's not a problem —
        // it just means nobody is listening (e.g., worker hasn't started yet).
        let _ = self.tx.send(event);
    }

    fn subscribe(&self) -> broadcast::Receiver<TaskEvent> {
        self.tx.subscribe()
    }
}

// =============================================================================
// Arc Blanket Implementation
// =============================================================================
//
// WHY IS THIS NEEDED?
//   In Rust, you can't call trait methods through an Arc unless the trait
//   is object-safe or you have a blanket impl. This impl lets us use
//   `Arc<InMemoryEventBus>` anywhere an `EventBus` is expected.
//
//   Without this, we'd need to dereference the Arc every time:
//     (*event_bus).publish(event)
//   Or use a reference:
//     (&**event_bus).publish(event)
//
//   With this impl, we can just call:
//     event_bus.publish(event)
//
//   This is a common pattern in Rust for passing shared state.
impl<T: EventBus> EventBus for std::sync::Arc<T> {
    fn publish(&self, event: TaskEvent) {
        T::publish(self, event);
    }

    fn subscribe(&self) -> broadcast::Receiver<TaskEvent> {
        T::subscribe(self)
    }
}
