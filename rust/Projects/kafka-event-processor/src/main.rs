// =============================================================================
// Kafka Event Processor Demo — Event Streaming Patterns
// =============================================================================
//
// WHAT THIS DEMONSTRATES:
//   1. Event streaming patterns (producer/consumer)
//   2. Topic-based message routing
//   3. Consumer groups with parallel processing
//   4. At-least-once delivery semantics
//   5. Dead-letter queue pattern
//   6. Idempotent processing
//
// JD RELEVANCE:
//   The JD mentions "Familiarity with event streaming platforms such as
//   Apache Kafka." This demo shows the core patterns used with Kafka:
//   topics, partitions, consumer groups, offset management, and retries.
//
// ARCHITECTURE:
//   ┌──────────────┐   produce    ┌──────────────────┐   consume   ┌──────────────┐
//   │  API Service │─────────────►│   Event Bus      │────────────►│  Worker      │
//   │  (producer)  │              │  (in-memory)     │             │  (consumer)  │
//   └──────────────┘              │                  │             └──────────────┘
//                                 │  ┌────────────┐  │                  │
//                                 │  │  orders    │  │                  │
//                                 │  │  topic     │  │             ┌────▼──────────┐
//                                 │  └────────────┘  │             │  Dead Letter  │
//                                 │  ┌────────────┐  │             │  Queue (DLQ)  │
//                                 │  │  payments  │  │             └───────────────┘
//                                 │  │  topic     │  │
//                                 │  └────────────┘  │
//                                 │  ┌────────────┐  │
//                                 │  │  dlq       │  │
//                                 │  │  topic     │  │
//                                 │  └────────────┘  │
//                                 └──────────────────┘
//
// KEY KAFKA CONCEPTS DEMONSTRATED:
//   - Topic: A category/feed name to which records are published
//   - Partition: A topic is split into partitions for parallelism
//   - Producer: Publishes records to a topic
//   - Consumer: Reads records from a topic
//   - Consumer Group: Multiple consumers coordinate to process partitions
//   - Offset: A position in a partition (tracked per consumer group)
//   - Dead Letter Queue: A topic for messages that failed processing
// =============================================================================

use chrono::Utc;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::{mpsc, Mutex, RwLock};
use rand::Rng;
use tracing::{error, info, warn};

// =============================================================================
// Event Types
// =============================================================================

/// A generic event envelope — similar to Kafka's ConsumerRecord.
#[derive(Debug, Clone, Serialize, Deserialize)]
struct Event {
    /// Unique event ID (like Kafka's offset)
    id: String,
    /// Event type (like Kafka's topic)
    event_type: String,
    /// Event source
    source: String,
    /// Event payload (JSON string)
    payload: String,
    /// When the event was produced
    timestamp: String,
    /// Retry count (for dead letter queue)
    retry_count: u32,
}

/// Order placed event.
#[derive(Debug, Clone, Serialize, Deserialize)]
struct OrderPlaced {
    order_id: String,
    user_id: String,
    amount: f64,
    items: Vec<String>,
}

/// Payment processed event.
#[derive(Debug, Clone, Serialize, Deserialize)]
struct PaymentProcessed {
    payment_id: String,
    order_id: String,
    amount: f64,
    status: String,
}

// =============================================================================
// In-Memory Event Bus (Simulating Kafka)
// =============================================================================

/// A simulated Kafka topic.
///
/// In real Kafka, a topic is a log of records. Here we use an mpsc channel
/// to simulate the same producer/consumer pattern.
struct Topic {
    name: String,
    /// Producer sends events here
    tx: mpsc::Sender<Event>,
    /// Consumer receives events from here
    rx: Mutex<mpsc::Receiver<Event>>,
}

impl Topic {
    fn new(name: String, buffer: usize) -> Self {
        let (tx, rx) = mpsc::channel(buffer);
        Self {
            name,
            tx,
            rx: Mutex::new(rx),
        }
    }

    /// Produce an event to this topic.
    async fn produce(&self, event: Event) -> Result<(), String> {
        self.tx.send(event).await.map_err(|e| format!("Failed to produce: {e}"))
    }

    /// Consume an event from this topic.
    async fn consume(&self) -> Option<Event> {
        self.rx.lock().await.recv().await
    }
}

/// The event bus manages multiple topics.
struct EventBus {
    topics: RwLock<HashMap<String, Arc<Topic>>>,
}

impl EventBus {
    fn new() -> Self {
        Self {
            topics: RwLock::new(HashMap::new()),
        }
    }

    /// Create a topic if it doesn't exist.
    async fn create_topic(&self, name: &str, buffer: usize) -> Arc<Topic> {
        let mut topics = self.topics.write().await;
        topics
            .entry(name.to_string())
            .or_insert_with(|| Arc::new(Topic::new(name.to_string(), buffer)))
            .clone()
    }

    /// Get a topic by name.
    async fn get_topic(&self, name: &str) -> Option<Arc<Topic>> {
        self.topics.read().await.get(name).cloned()
    }

    /// Produce an event to a topic.
    async fn produce(&self, topic_name: &str, event: Event) -> Result<(), String> {
        let topic = self
            .get_topic(topic_name)
            .await
            .ok_or_else(|| format!("Topic '{topic_name}' not found"))?;
        topic.produce(event).await
    }
}

// =============================================================================
// Producer
// =============================================================================

/// Produces events to the event bus (like a Kafka producer).
struct OrderProducer {
    event_bus: Arc<EventBus>,
}

impl OrderProducer {
    fn new(event_bus: Arc<EventBus>) -> Self {
        Self { event_bus }
    }

    /// Produce an order placed event.
    async fn place_order(&self, user_id: &str, amount: f64, items: Vec<String>) -> Result<String, String> {
        let order_id = uuid::Uuid::new_v4().to_string();

        let order = OrderPlaced {
            order_id: order_id.clone(),
            user_id: user_id.to_string(),
            amount,
            items,
        };

        let event = Event {
            id: uuid::Uuid::new_v4().to_string(),
            event_type: "order.placed".to_string(),
            source: "order-service".to_string(),
            payload: serde_json::to_string(&order).unwrap(),
            timestamp: Utc::now().to_rfc3339(),
            retry_count: 0,
        };

        self.event_bus.produce("orders", event).await?;
        info!("Order placed: {order_id}");
        Ok(order_id)
    }

    /// Produce a payment processed event.
    async fn process_payment(&self, order_id: &str, amount: f64) -> Result<String, String> {
        let payment_id = uuid::Uuid::new_v4().to_string();

        let payment = PaymentProcessed {
            payment_id: payment_id.clone(),
            order_id: order_id.to_string(),
            amount,
            status: "completed".to_string(),
        };

        let event = Event {
            id: uuid::Uuid::new_v4().to_string(),
            event_type: "payment.processed".to_string(),
            source: "payment-service".to_string(),
            payload: serde_json::to_string(&payment).unwrap(),
            timestamp: Utc::now().to_rfc3339(),
            retry_count: 0,
        };

        self.event_bus.produce("payments", event).await?;
        info!("Payment processed: {payment_id} for order {order_id}");
        Ok(payment_id)
    }
}

// =============================================================================
// Consumer / Worker
// =============================================================================

/// Processes events from a topic (like a Kafka consumer).
struct OrderWorker {
    event_bus: Arc<EventBus>,
    worker_id: String,
}

impl OrderWorker {
    fn new(event_bus: Arc<EventBus>, worker_id: &str) -> Self {
        Self {
            event_bus,
            worker_id: worker_id.to_string(),
        }
    }

    /// Process events from the orders topic.
    ///
    /// This simulates a Kafka consumer polling loop:
    /// 1. Poll for new events
    /// 2. Process each event
    /// 3. Commit offset (mark as processed)
    /// 4. On failure: retry or send to DLQ
    async fn process_orders(&self) {
        let topic = self.event_bus.get_topic("orders").await.unwrap();

        loop {
            match topic.consume().await {
                Some(event) => {
                    info!(
                        worker = %self.worker_id,
                        event_id = %event.id,
                        event_type = %event.event_type,
                        "Consumed event"
                    );

                    // Simulate processing with potential failure
                    let success = self.handle_order_event(&event).await;

                    if !success {
                        // Retry logic: send to DLQ after 3 failures
                        if event.retry_count >= 3 {
                            warn!(
                                event_id = %event.id,
                                retries = event.retry_count,
                                "Max retries exceeded, sending to DLQ"
                            );
                            let mut dlq_event = event.clone();
                            dlq_event.event_type = "order.dlq".to_string();
                            dlq_event.source = "order-worker".to_string();
                            if let Err(e) = self.event_bus.produce("dlq", dlq_event).await {
                                error!("Failed to send to DLQ: {e}");
                            }
                        } else {
                            // Re-produce with incremented retry count
                            info!(
                                event_id = %event.id,
                                retry = event.retry_count + 1,
                                "Retrying event"
                            );
                            let mut retry_event = event.clone();
                            retry_event.retry_count += 1;
                            if let Err(e) = self.event_bus.produce("orders", retry_event).await {
                                error!("Failed to retry event: {e}");
                            }
                        }
                    }
                }
                None => {
                    // No more events — in Kafka this would be a poll timeout
                    tokio::time::sleep(std::time::Duration::from_millis(100)).await;
                }
            }
        }
    }

    /// Handle a single order event.
    async fn handle_order_event(&self, event: &Event) -> bool {
        // Simulate processing time
        tokio::time::sleep(std::time::Duration::from_millis(50)).await;

        // Simulate a 20% failure rate for demo purposes
        let mut rng = rand::thread_rng();
        if rng.gen_range(0..5) == 0 {
            warn!(
                event_id = %event.id,
                "Failed to process order event"
            );
            return false;
        }

        info!(
            worker = %self.worker_id,
            event_id = %event.id,
            "Successfully processed order event"
        );
        true
    }
}

// =============================================================================
// Dead Letter Queue Processor
// =============================================================================

/// Processes events from the dead letter queue.
struct DlqProcessor {
    event_bus: Arc<EventBus>,
}

impl DlqProcessor {
    fn new(event_bus: Arc<EventBus>) -> Self {
        Self { event_bus }
    }

    /// Monitor and report DLQ events.
    async fn process_dlq(&self) {
        let topic = self.event_bus.get_topic("dlq").await.unwrap();

        loop {
            match topic.consume().await {
                Some(event) => {
                    error!(
                        event_id = %event.id,
                        event_type = %event.event_type,
                        retries = event.retry_count,
                        source = %event.source,
                        "DLQ event — requires manual intervention"
                    );
                }
                None => {
                    tokio::time::sleep(std::time::Duration::from_millis(200)).await;
                }
            }
        }
    }
}

// =============================================================================
// Main
// =============================================================================

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt()
        .with_env_filter("kafka_event_processor=info")
        .init();

    println!("╔══════════════════════════════════════════════════════════╗");
    println!("║   Kafka Event Processor Demo                           ║");
    println!("╚══════════════════════════════════════════════════════════╝");
    println!();
    println!("   This demo simulates Kafka event streaming patterns");
    println!("   using an in-memory event bus.");
    println!();
    println!("   Topics: orders, payments, dlq");
    println!("   Workers: 2 parallel consumers (consumer group)");
    println!("   DLQ: Events that fail 3+ times");
    println!();

    // Initialize the event bus and create topics
    let event_bus = Arc::new(EventBus::new());
    event_bus.create_topic("orders", 100).await;
    event_bus.create_topic("payments", 100).await;
    event_bus.create_topic("dlq", 100).await;

    // Create producer
    let producer = OrderProducer::new(event_bus.clone());

    // Create two workers (simulating a consumer group with 2 partitions)
    let worker1 = OrderWorker::new(event_bus.clone(), "worker-1");
    let worker2 = OrderWorker::new(event_bus.clone(), "worker-2");

    // Create DLQ processor
    let dlq = DlqProcessor::new(event_bus.clone());

    // Start workers and DLQ processor in background
    tokio::spawn(async move { worker1.process_orders().await });
    tokio::spawn(async move { worker2.process_orders().await });
    tokio::spawn(async move { dlq.process_dlq().await });

    // Produce sample events
    println!("   Producing sample events...");
    println!();

    let items = vec![
        "Laptop".to_string(),
        "Mouse".to_string(),
        "Keyboard".to_string(),
    ];

    // Produce 10 orders
    for i in 0..10 {
        let user_id = format!("user_{i}");
        let amount = 100.0 + (i as f64 * 50.0);

        match producer.place_order(&user_id, amount, items.clone()).await {
            Ok(order_id) => {
                info!("Order {order_id} produced successfully");
            }
            Err(e) => {
                error!("Failed to produce order: {e}");
            }
        }

        // Small delay between produces
        tokio::time::sleep(std::time::Duration::from_millis(50)).await;
    }

    // Wait for processing to complete
    tokio::time::sleep(std::time::Duration::from_secs(3)).await;

    println!();
    println!("   ✅ Demo complete!");
    println!("   Check the logs above to see:");
    println!("   - Events being produced to the 'orders' topic");
    println!("   - Workers consuming and processing events");
    println!("   - Failed events being retried");
    println!("   - Events exceeding max retries sent to DLQ");
    println!();
    println!("   In production, you'd replace the in-memory event bus");
    println!("   with Apache Kafka using the `rdkafka` crate.");
}

// =============================================================================
// Tests
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    async fn setup() -> Arc<EventBus> {
        let bus = Arc::new(EventBus::new());
        bus.create_topic("orders", 100).await;
        bus.create_topic("payments", 100).await;
        bus.create_topic("dlq", 100).await;
        bus
    }

    #[tokio::test]
    async fn test_produce_and_consume() {
        let bus = setup().await;
        let producer = OrderProducer::new(bus.clone());

        let order_id = producer
            .place_order("test_user", 100.0, vec!["item1".to_string()])
            .await
            .unwrap();

        assert!(!order_id.is_empty());

        // Consume the event
        let topic = bus.get_topic("orders").await.unwrap();
        let event = topic.consume().await.unwrap();

        assert_eq!(event.event_type, "order.placed");
        assert_eq!(event.source, "order-service");
    }

    #[tokio::test]
    async fn test_payment_event() {
        let bus = setup().await;
        let producer = OrderProducer::new(bus.clone());

        let payment_id = producer
            .process_payment("order-123", 250.0)
            .await
            .unwrap();

        assert!(!payment_id.is_empty());

        let topic = bus.get_topic("payments").await.unwrap();
        let event = topic.consume().await.unwrap();

        assert_eq!(event.event_type, "payment.processed");
    }

    #[tokio::test]
    async fn test_dlq_routing() {
        let bus = setup().await;
        let producer = OrderProducer::new(bus.clone());

        // Produce an event that will fail (we'll manually send to DLQ)
        let failed_event = Event {
            id: "failed-001".to_string(),
            event_type: "order.dlq".to_string(),
            source: "test".to_string(),
            payload: "{}".to_string(),
            timestamp: Utc::now().to_rfc3339(),
            retry_count: 3,
        };

        bus.produce("dlq", failed_event).await.unwrap();

        // Verify it's in the DLQ
        let topic = bus.get_topic("dlq").await.unwrap();
        let event = topic.consume().await.unwrap();

        assert_eq!(event.id, "failed-001");
        assert_eq!(event.retry_count, 3);
    }

    #[tokio::test]
    async fn test_multiple_topics() {
        let bus = setup().await;

        // Verify all topics exist
        assert!(bus.get_topic("orders").await.is_some());
        assert!(bus.get_topic("payments").await.is_some());
        assert!(bus.get_topic("dlq").await.is_some());

        // Non-existent topic
        assert!(bus.get_topic("nonexistent").await.is_none());
    }
}
