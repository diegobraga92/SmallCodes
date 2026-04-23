"""
MESSAGE QUEUES - REDIS, RABBITMQ, KAFKA
========================================
Message queues enable asynchronous communication between services,
decoupling producers and consumers for scalable architectures.

Use Cases:
- Background job processing
- Microservices communication
- Event-driven architectures
- Load leveling
- Reliable message delivery
"""

print("=" * 80)
print("MESSAGE QUEUES - REDIS, RABBITMQ, KAFKA")
print("=" * 80)

# ============================================================================
# 1. MESSAGE QUEUE CONCEPTS
# ============================================================================

"""
MESSAGE QUEUE PATTERNS:

1. POINT-TO-POINT (Queue):
   - One producer → Queue → One consumer
   - Message consumed once
   - Example: Task queue

2. PUBLISH/SUBSCRIBE (Topic):
   - One producer → Topic → Multiple consumers
   - Message consumed by all subscribers
   - Example: Event notifications

3. REQUEST/REPLY:
   - Producer sends request
   - Consumer processes and replies
   - Example: RPC patterns

WHEN TO USE WHAT:

REDIS:
- Simple queues
- Fast, in-memory
- Pub/Sub patterns
- Caching + queuing
- Rate limiting

RABBITMQ:
- Complex routing
- Guaranteed delivery
- Multiple protocols
- Enterprise features
- Transaction support

KAFKA:
- High throughput
- Event streaming
- Log aggregation
- Real-time analytics
- Message replay
"""


# ============================================================================
# 2. REDIS AS MESSAGE QUEUE
# ============================================================================

"""
REDIS BASICS:
- In-memory data store
- Supports lists, sets, sorted sets, hashes
- Pub/Sub messaging
- Very fast (microsecond latency)

INSTALLATION:
pip install redis
"""

import redis
import json
import time
from typing import Dict, Any, Optional, List
from datetime import datetime

# ============================================================================
# Redis Simple Queue
# ============================================================================

class RedisQueue:
    """
    Simple queue implementation using Redis lists
    - LPUSH: Add to queue (left)
    - RPOP: Remove from queue (right)
    - BRPOP: Blocking pop (waits for item)
    """
    
    def __init__(self, name: str, host='localhost', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db)
        self.queue_name = name
    
    def push(self, item: Any):
        """Add item to queue"""
        data = json.dumps(item)
        self.redis.lpush(self.queue_name, data)
    
    def pop(self, block: bool = False, timeout: int = 0) -> Optional[Any]:
        """
        Remove and return item from queue
        
        block: Wait for item if queue empty
        timeout: Max wait time (0 = wait forever)
        """
        if block:
            result = self.redis.brpop(self.queue_name, timeout=timeout)
            if result:
                _, data = result
                return json.loads(data)
        else:
            data = self.redis.rpop(self.queue_name)
            if data:
                return json.loads(data)
        return None
    
    def size(self) -> int:
        """Get queue size"""
        return self.redis.llen(self.queue_name)
    
    def clear(self):
        """Clear all items from queue"""
        self.redis.delete(self.queue_name)


# Example usage
def demo_redis_queue():
    """Demonstrate Redis queue"""
    queue = RedisQueue('tasks')
    
    # Producer: Add tasks
    queue.push({'task': 'send_email', 'to': 'user@example.com'})
    queue.push({'task': 'process_image', 'id': 123})
    
    print(f"Queue size: {queue.size()}")
    
    # Consumer: Process tasks
    while queue.size() > 0:
        task = queue.pop()
        print(f"Processing: {task}")


# ============================================================================
# Redis Pub/Sub
# ============================================================================

class RedisPubSub:
    """
    Publish/Subscribe pattern with Redis
    - Multiple consumers can subscribe to channels
    - Messages sent to all subscribers
    """
    
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db)
        self.pubsub = self.redis.pubsub()
    
    def publish(self, channel: str, message: Any):
        """Publish message to channel"""
        data = json.dumps(message)
        self.redis.publish(channel, data)
    
    def subscribe(self, *channels: str):
        """Subscribe to channels"""
        self.pubsub.subscribe(*channels)
    
    def listen(self):
        """
        Listen for messages
        Generator that yields messages
        """
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                yield message['channel'].decode(), data


# Example usage
def demo_redis_pubsub():
    """Demonstrate Redis Pub/Sub"""
    import threading
    
    pubsub = RedisPubSub()
    
    # Subscriber (runs in thread)
    def subscriber():
        sub = RedisPubSub()
        sub.subscribe('notifications', 'alerts')
        
        for channel, message in sub.listen():
            print(f"[{channel}] Received: {message}")
    
    # Start subscriber thread
    thread = threading.Thread(target=subscriber, daemon=True)
    thread.start()
    
    time.sleep(1)  # Let subscriber start
    
    # Publisher: Send messages
    pubsub.publish('notifications', {'type': 'info', 'msg': 'Hello!'})
    pubsub.publish('alerts', {'type': 'warning', 'msg': 'Check this'})
    
    time.sleep(1)  # Let messages process


# ============================================================================
# 3. RABBITMQ MESSAGE QUEUE
# ============================================================================

"""
RABBITMQ:
- AMQP protocol (Advanced Message Queuing Protocol)
- Message broker with routing
- Guaranteed delivery
- Complex routing patterns

INSTALLATION:
pip install pika

CONCEPTS:
- Producer: Sends messages
- Exchange: Routes messages
- Queue: Stores messages
- Consumer: Receives messages
- Binding: Connection between exchange and queue
"""

import pika

# ============================================================================
# RabbitMQ Simple Queue
# ============================================================================

class RabbitMQProducer:
    """
    RabbitMQ message producer
    """
    
    def __init__(self, host='localhost', queue='tasks'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )
        self.channel = self.connection.channel()
        self.queue = queue
        
        # Declare queue (create if doesn't exist)
        self.channel.queue_declare(queue=queue, durable=True)
    
    def send(self, message: Any):
        """
        Send message to queue
        
        durable: Message survives broker restart
        persistent: Message written to disk
        """
        data = json.dumps(message)
        
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            body=data,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )
        print(f"Sent: {message}")
    
    def close(self):
        """Close connection"""
        self.connection.close()


class RabbitMQConsumer:
    """
    RabbitMQ message consumer
    """
    
    def __init__(self, host='localhost', queue='tasks'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )
        self.channel = self.connection.channel()
        self.queue = queue
        
        # Declare queue
        self.channel.queue_declare(queue=queue, durable=True)
        
        # Fair dispatch: Don't give more than one message at a time
        self.channel.basic_qos(prefetch_count=1)
    
    def callback(self, ch, method, properties, body):
        """
        Process message
        Override this in subclass
        """
        message = json.loads(body)
        print(f"Received: {message}")
        
        # Simulate work
        time.sleep(1)
        
        # Acknowledge message (manual ack)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    def start(self):
        """Start consuming messages"""
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.callback,
            auto_ack=False  # Manual acknowledgment
        )
        
        print('Waiting for messages...')
        self.channel.start_consuming()
    
    def close(self):
        """Close connection"""
        self.connection.close()


# Example usage
def demo_rabbitmq():
    """Demonstrate RabbitMQ"""
    # Producer
    producer = RabbitMQProducer(queue='tasks')
    producer.send({'task': 'send_email', 'to': 'user@example.com'})
    producer.send({'task': 'process_image', 'id': 123})
    producer.close()
    
    # Consumer (would run in separate process)
    # consumer = RabbitMQConsumer(queue='tasks')
    # consumer.start()


# ============================================================================
# RabbitMQ Pub/Sub (Fanout Exchange)
# ============================================================================

class RabbitMQPublisher:
    """
    Publisher using fanout exchange
    Sends message to all bound queues
    """
    
    def __init__(self, host='localhost', exchange='logs'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )
        self.channel = self.connection.channel()
        self.exchange = exchange
        
        # Declare fanout exchange
        self.channel.exchange_declare(
            exchange=exchange,
            exchange_type='fanout'
        )
    
    def publish(self, message: Any):
        """Publish message to all subscribers"""
        data = json.dumps(message)
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key='',  # Ignored for fanout
            body=data
        )
        print(f"Published: {message}")
    
    def close(self):
        self.connection.close()


class RabbitMQSubscriber:
    """
    Subscriber to fanout exchange
    """
    
    def __init__(self, host='localhost', exchange='logs'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )
        self.channel = self.connection.channel()
        self.exchange = exchange
        
        # Declare exchange
        self.channel.exchange_declare(
            exchange=exchange,
            exchange_type='fanout'
        )
        
        # Create exclusive queue (deleted when consumer disconnects)
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue = result.method.queue
        
        # Bind queue to exchange
        self.channel.queue_bind(
            exchange=exchange,
            queue=self.queue
        )
    
    def callback(self, ch, method, properties, body):
        """Process message"""
        message = json.loads(body)
        print(f"Received: {message}")
    
    def start(self):
        """Start consuming"""
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.callback,
            auto_ack=True
        )
        
        print('Waiting for logs...')
        self.channel.start_consuming()


# ============================================================================
# 4. APACHE KAFKA
# ============================================================================

"""
KAFKA:
- Distributed streaming platform
- High throughput, low latency
- Horizontal scalability
- Message retention (replay messages)
- Distributed, fault-tolerant

INSTALLATION:
pip install kafka-python

CONCEPTS:
- Topic: Category/feed of messages
- Partition: Ordered, immutable sequence of messages
- Producer: Publishes messages to topics
- Consumer: Reads messages from topics
- Consumer Group: Load balancing across consumers
- Broker: Kafka server
"""

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

# ============================================================================
# Kafka Producer
# ============================================================================

class KafkaMessageProducer:
    """
    Kafka message producer
    """
    
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            # Optional: Delivery guarantees
            acks='all',  # Wait for all replicas
            retries=3
        )
    
    def send(self, topic: str, message: Any, key: Optional[str] = None):
        """
        Send message to topic
        
        topic: Topic name
        message: Message data
        key: Optional key (for partitioning)
        """
        try:
            # Async send
            future = self.producer.send(
                topic,
                value=message,
                key=key.encode('utf-8') if key else None
            )
            
            # Wait for result (optional)
            record_metadata = future.get(timeout=10)
            
            print(f"Sent to {record_metadata.topic} "
                  f"partition {record_metadata.partition} "
                  f"offset {record_metadata.offset}")
        
        except KafkaError as e:
            print(f"Failed to send message: {e}")
    
    def close(self):
        """Flush and close producer"""
        self.producer.flush()
        self.producer.close()


# ============================================================================
# Kafka Consumer
# ============================================================================

class KafkaMessageConsumer:
    """
    Kafka message consumer
    """
    
    def __init__(
        self,
        topics: List[str],
        group_id: str,
        bootstrap_servers='localhost:9092'
    ):
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            # Start from beginning if no offset
            auto_offset_reset='earliest',
            # Commit offsets automatically
            enable_auto_commit=True
        )
    
    def consume(self):
        """
        Consume messages
        Generator that yields messages
        """
        try:
            for message in self.consumer:
                yield {
                    'topic': message.topic,
                    'partition': message.partition,
                    'offset': message.offset,
                    'key': message.key.decode('utf-8') if message.key else None,
                    'value': message.value,
                    'timestamp': message.timestamp
                }
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()


# Example usage
def demo_kafka():
    """Demonstrate Kafka"""
    # Producer
    producer = KafkaMessageProducer()
    
    producer.send('events', {
        'event': 'user_signup',
        'user_id': 123,
        'timestamp': datetime.now().isoformat()
    })
    
    producer.send('events', {
        'event': 'order_placed',
        'order_id': 456,
        'timestamp': datetime.now().isoformat()
    }, key='order')
    
    producer.close()
    
    # Consumer (would run in separate process)
    # consumer = KafkaMessageConsumer(['events'], group_id='processors')
    # for message in consumer.consume():
    #     print(f"Processing: {message['value']}")


# ============================================================================
# 5. MESSAGE QUEUE PATTERNS
# ============================================================================

"""
COMMON PATTERNS:

1. WORK QUEUE (Task Queue):
   - Distribute time-consuming tasks
   - Multiple workers process queue
   - Load balancing

2. PUBLISH/SUBSCRIBE:
   - Broadcast messages to multiple consumers
   - Event-driven architecture
   - Decoupled services

3. REQUEST/REPLY:
   - RPC over message queue
   - Async request-response
   - Correlation IDs

4. PRIORITY QUEUE:
   - Different priority levels
   - High-priority messages processed first

5. DEAD LETTER QUEUE:
   - Failed messages sent to DLQ
   - Retry logic
   - Error handling

6. SAGA PATTERN:
   - Distributed transactions
   - Compensating transactions
   - Event choreography
"""


# ============================================================================
# 6. CELERY - DISTRIBUTED TASK QUEUE
# ============================================================================

"""
CELERY:
- Distributed task queue
- Works with Redis, RabbitMQ, SQS
- Task scheduling
- Task routing
- Result backend

INSTALLATION:
pip install celery[redis]  # With Redis
pip install celery[amqp]   # With RabbitMQ

BASIC SETUP:

from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def add(x, y):
    return x + y

# Call task
result = add.delay(4, 4)
print(result.get(timeout=1))

RUN WORKER:
celery -A tasks worker --loglevel=info
"""


# ============================================================================
# 7. BEST PRACTICES
# ============================================================================

"""
MESSAGE QUEUE BEST PRACTICES:

1. IDEMPOTENCY:
   - Messages may be delivered multiple times
   - Ensure operations are idempotent
   - Use unique message IDs

2. ERROR HANDLING:
   - Retry failed messages
   - Dead letter queues
   - Error logging
   - Circuit breakers

3. MESSAGE DESIGN:
   - Keep messages small
   - Include timestamps
   - Versioning for schema changes
   - Include correlation IDs

4. MONITORING:
   - Queue depth
   - Processing rate
   - Error rate
   - Consumer lag

5. SCALABILITY:
   - Multiple consumers
   - Partitioning (Kafka)
   - Connection pooling
   - Batch processing

6. RELIABILITY:
   - Message persistence
   - Acknowledgments
   - Replication
   - Backups

7. SECURITY:
   - Authentication
   - Encryption (TLS)
   - Authorization
   - Network isolation

8. TESTING:
   - Mock message queues
   - Integration tests
   - Load testing
   - Chaos engineering
"""


# ============================================================================
# 8. COMPARISON MATRIX
# ============================================================================

"""
REDIS vs RABBITMQ vs KAFKA:

REDIS:
✓ Very fast (in-memory)
✓ Simple setup
✓ Good for caching + queuing
✗ No guarantee of delivery
✗ Limited persistence
Use: Simple queues, real-time, ephemeral data

RABBITMQ:
✓ Reliable delivery
✓ Flexible routing
✓ Multiple protocols
✓ Enterprise features
✗ Lower throughput than Kafka
✗ More complex setup
Use: Task queues, RPC, complex routing

KAFKA:
✓ Very high throughput
✓ Horizontal scalability
✓ Message replay
✓ Stream processing
✗ Complex setup/operations
✗ Higher latency than Redis
Use: Event streaming, logs, analytics, high volume
"""

print("\n=== Message Queues Complete ===")

"""
KEY TAKEAWAYS:

1. Redis: Fast, simple queues and pub/sub
2. RabbitMQ: Reliable, flexible message broker
3. Kafka: High-throughput event streaming
4. Celery: Python-native distributed tasks
5. Choose based on requirements:
   - Speed → Redis
   - Reliability → RabbitMQ
   - Scale → Kafka
6. Always handle failures and retries
7. Monitor queue depth and processing
8. Design for idempotency
9. Use dead letter queues
10. Test at scale
"""
