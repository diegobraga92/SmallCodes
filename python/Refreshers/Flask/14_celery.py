"""
Comprehensive Celery with Flask Implementation
===============================================
This code demonstrates Celery integration with Flask for background task processing,
covering everything from basic setup to advanced patterns.
"""

import os
import time
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from abc import ABC, abstractmethod
from functools import wraps

from flask import Flask, request, jsonify, current_app, g
from celery import Celery, Task, group, chain, chord, signature
from celery.result import AsyncResult, allow_join_result
from celery.schedules import crontab
from redis import Redis
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests

# ============================================================================
# PART 1: CELERY OVERVIEW
# ============================================================================

"""
What is Celery?
---------------
Celery is a distributed task queue that allows you to run background tasks
asynchronously. It's perfect for:
- Long-running operations (email sending, file processing)
- Scheduled tasks (cron jobs)
- Distributed computing across multiple workers
- Handling webhook callbacks
"""

"""
Core Components:
1. Broker: Message queue (Redis, RabbitMQ) - holds tasks
2. Worker: Processes tasks from the queue
3. Result Backend: Stores task results (Redis, database)
4. Beat Scheduler: For periodic/scheduled tasks
"""

# ============================================================================
# PART 2: CELERY USAGES WITH FLASK
# ============================================================================

# Initialize Flask application
app = Flask(__name__)

# Configuration
app.config.update(
    # Celery Configuration
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0',
    
    # Flask Configuration
    SECRET_KEY=os.getenv('SECRET_KEY', 'dev-key-123'),
    SQLALCHEMY_DATABASE_URI='sqlite:///tasks.db',
    
    # Task Configuration
    MAX_RETRIES=3,
    DEFAULT_RETRY_DELAY=60,  # seconds
    
    # Email Configuration (for examples)
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    
    # External APIs
    STRIPE_API_KEY=os.getenv('STRIPE_API_KEY'),
    AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY'),
    AWS_SECRET_KEY=os.getenv('AWS_SECRET_KEY'),
)

# --------------------------------------
# 2.1 CELERY SETUP WITH FLASK FACTORY PATTERN
# --------------------------------------

def make_celery(app: Flask) -> Celery:
    """
    Factory function to create Celery instance integrated with Flask.
    This pattern allows proper Flask context handling.
    """
    class FlaskTask(Task):
        """
        Custom Celery Task that runs within Flask application context.
        This ensures Flask extensions and configuration are available.
        """
        def __call__(self, *args, **kwargs):
            # Run task within Flask app context
            with app.app_context():
                return self.run(*args, **kwargs)
    
    # Create Celery instance
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND'],
        task_cls=FlaskTask  # Use our custom task class
    )
    
    # Configure Celery from Flask config
    celery.conf.update(app.config)
    
    # Additional Celery configuration
    celery.conf.update(
        # Task serialization
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        
        # Timezone
        timezone='UTC',
        enable_utc=True,
        
        # Worker settings
        worker_prefetch_multiplier=1,  # Fair task distribution
        worker_max_tasks_per_child=1000,  # Prevent memory leaks
        
        # Result expiration
        result_expires=3600,  # 1 hour
        
        # Task routing (optional)
        task_routes={
            'app.tasks.email.*': {'queue': 'email'},
            'app.tasks.reports.*': {'queue': 'reports'},
            'app.tasks.payments.*': {'queue': 'payments'},
        }
    )
    
    return celery

# Create Celery instance
celery = make_celery(app)

# Database setup for task tracking
Base = declarative_base()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
SessionLocal = sessionmaker(bind=engine)

class TaskModel(Base):
    """Database model for tracking Celery tasks"""
    __tablename__ = 'celery_tasks'
    
    id = Column(String(255), primary_key=True)  # Celery task ID
    name = Column(String(255))
    status = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    result = Column(String, nullable=True)  # JSON serialized result
    error = Column(String, nullable=True)
    user_id = Column(Integer, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'result': json.loads(self.result) if self.result else None,
            'error': self.error
        }

# Create tables
Base.metadata.create_all(bind=engine)

# --------------------------------------
# 2.2 BASIC TASK DEFINITIONS
# --------------------------------------

@celery.task(bind=True)  # bind=True gives access to self (task instance)
def add_numbers(self, a: int, b: int) -> int:
    """
    Simple task demonstrating basic Celery functionality.
    Use cases: Any CPU-bound or quick operation.
    """
    try:
        result = a + b
        current_app.logger.info(f"Adding {a} + {b} = {result}")
        return result
    except Exception as e:
        current_app.logger.error(f"Task failed: {str(e)}")
        raise

@celery.task(bind=True, max_retries=3, default_retry_delay=30)
def send_email(self, recipient: str, subject: str, body: str) -> Dict[str, Any]:
    """
    Email sending task with retry logic.
    Use cases: User notifications, marketing emails, alerts.
    """
    try:
        # Simulate email sending (replace with actual SMTP/API)
        current_app.logger.info(f"Sending email to {recipient}: {subject}")
        
        # Simulate potential failure (for demonstration)
        if "fail" in recipient:
            raise ConnectionError("SMTP server unavailable")
        
        # In real implementation:
        # msg = Message(subject, recipients=[recipient])
        # msg.body = body
        # mail.send(msg)
        
        time.sleep(2)  # Simulate network delay
        
        return {
            'status': 'sent',
            'recipient': recipient,
            'message_id': f'msg_{int(time.time())}',
            'timestamp': datetime.utcnow().isoformat()
        }
        
    except ConnectionError as exc:
        # Retry on connection errors
        current_app.logger.warning(f"Email failed, retrying: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)
    
    except Exception as exc:
        current_app.logger.error(f"Email failed permanently: {str(exc)}")
        return {
            'status': 'failed',
            'error': str(exc),
            'recipient': recipient
        }

# --------------------------------------
# 2.3 TASK DECORATORS AND CONFIGURATION
# --------------------------------------

# Custom decorator for task logging
def task_logger(func):
    """Decorator to add logging to Celery tasks"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        task_name = func.__name__
        current_app.logger.info(f"Starting task: {task_name}")
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            current_app.logger.info(f"Task {task_name} completed in {elapsed:.2f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            current_app.logger.error(f"Task {task_name} failed after {elapsed:.2f}s: {str(e)}")
            raise
    
    return wrapper

@celery.task(
    bind=True,
    name='app.tasks.generate_report',  # Explicit task name
    max_retries=2,
    default_retry_delay=300,  # 5 minutes
    acks_late=True,  # Don't acknowledge until task completes
    reject_on_worker_lost=True,  # Re-queue if worker dies
    time_limit=300,  # 5 minute time limit
    soft_time_limit=240,  # 4 minute soft limit (raises SoftTimeLimitExceeded)
)
@task_logger
def generate_report(self, report_type: str, user_id: int, date_range: Tuple[str, str]) -> Dict[str, Any]:
    """
    Long-running report generation with time limits and retry configuration.
    Use cases: Data analysis, PDF generation, complex calculations.
    """
    try:
        current_app.logger.info(f"Generating {report_type} report for user {user_id}")
        
        # Simulate long processing
        time.sleep(10)
        
        # Simulate data processing
        report_data = {
            'type': report_type,
            'user_id': user_id,
            'period': date_range,
            'generated_at': datetime.utcnow().isoformat(),
            'metrics': {
                'revenue': 15000.50,
                'users': 245,
                'growth': 15.3
            }
        }
        
        # Store report (simulated)
        report_id = f"report_{int(time.time())}"
        
        return {
            'success': True,
            'report_id': report_id,
            'download_url': f'/reports/{report_id}.pdf',
            'data': report_data
        }
        
    except Exception as exc:
        current_app.logger.error(f"Report generation failed: {str(exc)}")
        raise self.retry(exc=exc)

# --------------------------------------
# 2.4 PERIODIC TASKS (CELERY BEAT)
# --------------------------------------

# Configure periodic tasks
celery.conf.beat_schedule = {
    # Daily database backup at 2 AM
    'backup-database-daily': {
        'task': 'app.tasks.backup_database',
        'schedule': crontab(hour=2, minute=0),
        'args': (),
        'kwargs': {'backup_type': 'full'}
    },
    
    # Cleanup old sessions every hour
    'cleanup-sessions-hourly': {
        'task': 'app.tasks.cleanup_old_sessions',
        'schedule': crontab(minute=0),  # Every hour at minute 0
        'args': (),
        'kwargs': {'max_age_days': 7}
    },
    
    # Generate weekly report every Monday at 3 AM
    'weekly-report-monday': {
        'task': 'app.tasks.generate_weekly_report',
        'schedule': crontab(day_of_week=1, hour=3, minute=0),  # Monday=1
        'args': (),
    },
    
    # Health check every 5 minutes
    'health-check': {
        'task': 'app.tasks.system_health_check',
        'schedule': timedelta(minutes=5),
        'args': (),
    },
}

@celery.task
def backup_database(backup_type: str = 'full') -> Dict[str, Any]:
    """Periodic database backup task"""
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    filename = f"backup_{backup_type}_{timestamp}.sql"
    
    # Simulate backup (in real app, use pg_dump, mysqldump, etc.)
    current_app.logger.info(f"Creating {backup_type} database backup: {filename}")
    time.sleep(5)
    
    return {
        'success': True,
        'filename': filename,
        'size': '150MB',  # Simulated
        'created_at': datetime.utcnow().isoformat()
    }

@celery.task
def cleanup_old_sessions(max_age_days: int = 7) -> Dict[str, Any]:
    """Cleanup expired sessions"""
    # Simulate cleanup
    deleted_count = 42  # In real app, actual DB query
    current_app.logger.info(f"Cleaned up {deleted_count} old sessions")
    
    return {
        'success': True,
        'deleted_sessions': deleted_count,
        'max_age_days': max_age_days
    }

# ============================================================================
# PART 3: CELERY EXAMPLES WITH FLASK
# ============================================================================

# --------------------------------------
# 3.1 BASIC FLASK ROUTES WITH CELERY
# --------------------------------------

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Endpoint that offloads calculation to Celery"""
    data = request.get_json()
    a = data.get('a', 0)
    b = data.get('b', 0)
    
    # Start Celery task asynchronously
    task = add_numbers.delay(a, b)
    
    return jsonify({
        'task_id': task.id,
        'status': 'processing',
        'check_status': f'/api/task/{task.id}'
    }), 202  # 202 Accepted

@app.route('/api/task/<task_id>', methods=['GET'])
def get_task_status(task_id: str):
    """Check status of a Celery task"""
    task_result = AsyncResult(task_id, app=celery)
    
    response = {
        'task_id': task_id,
        'status': task_result.status,
        'result': None,
        'error': None
    }
    
    if task_result.ready():
        if task_result.successful():
            response['result'] = task_result.result
        else:
            response['error'] = str(task_result.result)
    
    return jsonify(response)

# --------------------------------------
# 3.2 EMAIL WORKFLOW EXAMPLE
# --------------------------------------

@dataclass
class EmailTemplate:
    """Data class for email templates"""
    name: str
    subject: str
    body_template: str
    
    def render(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Render template with context"""
        body = self.body_template
        for key, value in context.items():
            body = body.replace(f'{{{{{key}}}}}', str(value))
        
        return {
            'subject': self.subject,
            'body': body
        }

class EmailService:
    """Service for managing email workflows"""
    
    # Template definitions
    TEMPLATES = {
        'welcome': EmailTemplate(
            name='welcome',
            subject='Welcome to Our Service!',
            body_template='Hello {{name}}, welcome to our platform!'
        ),
        'password_reset': EmailTemplate(
            name='password_reset',
            subject='Password Reset Request',
            body_template='Click here to reset: {{reset_url}}'
        ),
        'order_confirmation': EmailTemplate(
            name='order_confirmation',
            subject='Order #{{order_id}} Confirmed',
            body_template='Thank you for your order of {{product_name}}'
        )
    }
    
    @staticmethod
    def send_bulk_emails(recipients: List[Dict], template_name: str) -> str:
        """
        Send bulk emails using Celery group for parallel processing.
        Use cases: Newsletters, user notifications, announcements.
        """
        # Create group of tasks for parallel execution
        tasks = []
        
        for recipient in recipients:
            template = EmailService.TEMPLATES[template_name]
            rendered = template.render(recipient)
            
            # Queue email task
            task = send_email.delay(
                recipient=recipient['email'],
                subject=rendered['subject'],
                body=rendered['body']
            )
            tasks.append(task)
        
        # Return a task group ID (we'll track this separately)
        return f"bulk_email_{int(time.time())}"
    
    @staticmethod
    def send_welcome_series(user_id: int, email: str, name: str) -> List[str]:
        """
        Send a series of welcome emails using Celery chain.
        Use cases: User onboarding sequences, drip campaigns.
        """
        # Define the sequence of emails
        welcome_chain = chain(
            send_email.s(
                recipient=email,
                subject=f"Welcome {name}!",
                body=f"Hi {name}, welcome to day 1!"
            ),
            send_email.s(
                recipient=email,
                subject=f"Getting Started, {name}",
                body=f"Hi {name}, here are some tips for day 2!"
            ),
            send_email.s(
                recipient=email,
                subject=f"Advanced Features, {name}",
                body=f"Hi {name}, check out these advanced features for day 3!"
            )
        )
        
        # Start the chain
        result = welcome_chain.apply_async()
        return [result.parent.id]  # Chain creates a group of tasks

@app.route('/api/send-welcome-email', methods=['POST'])
def send_welcome_email():
    """Endpoint to trigger welcome email workflow"""
    data = request.get_json()
    user_id = data['user_id']
    email = data['email']
    name = data['name']
    
    # Queue the welcome email series
    task_ids = EmailService.send_welcome_series(user_id, email, name)
    
    return jsonify({
        'success': True,
        'task_ids': task_ids,
        'message': 'Welcome email series started'
    })

# --------------------------------------
# 3.3 PAYMENT PROCESSING WORKFLOW
# --------------------------------------

class PaymentStatus(Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'

@dataclass
class Payment:
    """Payment domain object"""
    id: str
    user_id: int
    amount: float
    currency: str
    description: str
    status: PaymentStatus = PaymentStatus.PENDING
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()

@celery.task(bind=True, max_retries=3)
def process_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Complete payment processing workflow.
    Use cases: E-commerce transactions, subscription billing.
    """
    try:
        payment = Payment(**payment_data)
        
        # Step 1: Validate payment
        current_app.logger.info(f"Validating payment {payment.id}")
        time.sleep(1)
        
        # Step 2: Charge credit card (simulated)
        current_app.logger.info(f"Charging ${payment.amount} to user {payment.user_id}")
        
        # Simulate API call to payment gateway
        if payment.amount > 1000:
            raise ValueError("Amount exceeds limit")
        
        time.sleep(2)
        
        # Step 3: Update order status
        current_app.logger.info(f"Updating order for payment {payment.id}")
        
        # Step 4: Send confirmation
        send_email.delay(
            recipient=f"user{payment.user_id}@example.com",
            subject=f"Payment Confirmation #{payment.id}",
            body=f"Your payment of ${payment.amount} has been processed."
        )
        
        return {
            'success': True,
            'payment_id': payment.id,
            'transaction_id': f'txn_{int(time.time())}',
            'charged_amount': payment.amount,
            'timestamp': datetime.utcnow().isoformat()
        }
        
    except Exception as exc:
        current_app.logger.error(f"Payment processing failed: {str(exc)}")
        
        # Send failure notification
        send_email.delay(
            recipient=f"user{payment_data['user_id']}@example.com",
            subject=f"Payment Failed #{payment_data['id']}",
            body=f"Your payment of ${payment_data['amount']} could not be processed."
        )
        
        raise self.retry(exc=exc, countdown=60)

@app.route('/api/process-payment', methods=['POST'])
def process_payment_endpoint():
    """Endpoint to process payment asynchronously"""
    data = request.get_json()
    
    # Create payment record
    payment = Payment(
        id=f"pay_{int(time.time())}",
        user_id=data['user_id'],
        amount=data['amount'],
        currency=data.get('currency', 'USD'),
        description=data.get('description', 'Purchase')
    )
    
    # Start payment processing task
    task = process_payment.delay(asdict(payment))
    
    # Store task reference in database
    db_session = SessionLocal()
    task_record = TaskModel(
        id=task.id,
        name='process_payment',
        status='PENDING',
        user_id=data['user_id'],
        created_at=datetime.utcnow()
    )
    db_session.add(task_record)
    db_session.commit()
    db_session.close()
    
    return jsonify({
        'payment_id': payment.id,
        'task_id': task.id,
        'status': 'processing',
        'message': 'Payment is being processed'
    }), 202

# --------------------------------------
# 3.4 FILE PROCESSING PIPELINE
# --------------------------------------

@celery.task
def validate_file(file_path: str) -> Dict[str, Any]:
    """Validate uploaded file"""
    time.sleep(1)
    return {'valid': True, 'file_path': file_path}

@celery.task
def process_csv(file_path: str) -> Dict[str, Any]:
    """Process CSV file"""
    time.sleep(3)
    return {'processed': True, 'rows': 150, 'file_path': file_path}

@celery.task
def generate_summary(processing_result: Dict[str, Any]) -> Dict[str, Any]:
    """Generate summary from processed data"""
    time.sleep(2)
    return {
        'summary': True,
        'total_rows': processing_result['rows'],
        'generated_at': datetime.utcnow().isoformat()
    }

@celery.task
def cleanup_files(*file_paths: str) -> Dict[str, Any]:
    """Cleanup temporary files"""
    time.sleep(1)
    return {'cleaned': True, 'files': len(file_paths)}

@app.route('/api/upload-csv', methods=['POST'])
def upload_csv():
    """
    Endpoint demonstrating complex workflow with chord.
    Chord = group + callback (all tasks complete before callback)
    """
    # Simulate file upload
    file_path = f"/tmp/uploads/{int(time.time())}.csv"
    
    # Define workflow using chord
    workflow = chord(
        group(
            validate_file.s(file_path),
            process_csv.s(file_path)
        ),
        generate_summary.s()
    )
    
    # Add cleanup as a follow-up task
    full_workflow = chain(
        workflow,
        cleanup_files.s(file_path)
    )
    
    # Execute the workflow
    result = full_workflow.apply_async()
    
    return jsonify({
        'workflow_id': result.id,
        'status': 'processing',
        'steps': ['validate', 'process', 'summarize', 'cleanup'],
        'check_status': f'/api/workflow/{result.id}'
    }), 202

# --------------------------------------
# 3.5 MONITORING AND ERROR HANDLING
# --------------------------------------

class TaskTracker:
    """Utility for tracking Celery task execution"""
    
    @staticmethod
    def log_task_start(task_id: str, task_name: str, user_id: Optional[int] = None):
        """Log task start in database"""
        db_session = SessionLocal()
        
        task_record = TaskModel(
            id=task_id,
            name=task_name,
            status='STARTED',
            user_id=user_id,
            created_at=datetime.utcnow()
        )
        
        db_session.add(task_record)
        db_session.commit()
        db_session.close()
    
    @staticmethod
    def log_task_completion(task_id: str, result: Any = None, error: str = None):
        """Log task completion in database"""
        db_session = SessionLocal()
        
        task_record = db_session.query(TaskModel).filter_by(id=task_id).first()
        if task_record:
            task_record.status = 'COMPLETED' if not error else 'FAILED'
            task_record.completed_at = datetime.utcnow()
            task_record.result = json.dumps(result) if result else None
            task_record.error = error
            
            db_session.commit()
        
        db_session.close()

# Custom task base class with tracking
class TrackedTask(Task):
    """Base task class with automatic tracking"""
    abstract = True
    
    def on_success(self, retval, task_id, args, kwargs):
        """Called when task succeeds"""
        TaskTracker.log_task_completion(task_id, result=retval)
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Called when task fails"""
        TaskTracker.log_task_completion(task_id, error=str(exc))
    
    def __call__(self, *args, **kwargs):
        """Wrap task execution with tracking"""
        TaskTracker.log_task_start(self.request.id, self.name, kwargs.get('user_id'))
        return super().__call__(*args, **kwargs)

# Register the custom task class
celery.Task = TrackedTask

# --------------------------------------
# 3.6 TASK PRIORITIZATION AND QUEUES
# --------------------------------------

@celery.task(
    bind=True,
    queue='high_priority',
    priority=0  # Highest priority (0-9, 0 is highest)
)
def process_urgent_order(self, order_id: str):
    """High priority task for urgent orders"""
    current_app.logger.info(f"Processing urgent order: {order_id}")
    time.sleep(2)
    return {'order_id': order_id, 'status': 'urgent_processed'}

@celery.task(
    bind=True,
    queue='low_priority',
    priority=9  # Lowest priority
)
def generate_monthly_analytics(self, month: str):
    """Low priority task for analytics"""
    current_app.logger.info(f"Generating analytics for {month}")
    time.sleep(30)  # Long-running
    return {'month': month, 'status': 'analytics_generated'}

# ============================================================================
# PART 4: ADVANCED PATTERNS
# ============================================================================

# --------------------------------------
# 4.1 TASK RATE LIMITING
# --------------------------------------

class RateLimitedTask(Task):
    """Task with rate limiting"""
    abstract = True
    rate_limit = '10/m'  # 10 tasks per minute
    
    def __init__(self):
        self.last_run = None

@celery.task(base=RateLimitedTask, bind=True)
def call_external_api(self, endpoint: str, data: Dict):
    """Task with rate limiting for external API calls"""
    # Simulate API call
    time.sleep(1)
    return {'endpoint': endpoint, 'success': True}

# --------------------------------------
# 4.2 TASK CACHING
# --------------------------------------

from celery.contrib import rdc

@celery.task(bind=True)
@rdc.redis_cache(backend=Redis(), timeout=3600)  # Cache for 1 hour
def expensive_calculation(self, x: int, y: int) -> int:
    """Task with result caching"""
    current_app.logger.info(f"Calculating (cache miss): {x} * {y}")
    time.sleep(5)  # Expensive operation
    return x * y

# --------------------------------------
# 4.3 DYNAMIC TASK GENERATION
# --------------------------------------

def create_dynamic_task(task_name: str, func_code: str):
    """Dynamically create a Celery task at runtime"""
    
    # WARNING: Executing dynamic code is dangerous!
    # Only use with trusted input in controlled environments
    
    # Create function from code
    namespace = {}
    exec(func_code, namespace)
    task_func = namespace.get('task_function')
    
    if not task_func:
        raise ValueError("Function 'task_function' not found in code")
    
    # Register as Celery task
    task_decorator = celery.task(name=f"dynamic.{task_name}", bind=True)
    dynamic_task = task_decorator(task_func)
    
    return dynamic_task

# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@app.route('/api/celery/stats', methods=['GET'])
def celery_stats():
    """Get Celery worker statistics"""
    try:
        # Get active workers
        inspector = celery.control.inspect()
        
        stats = {
            'active_workers': inspector.active() or {},
            'scheduled_tasks': inspector.scheduled() or {},
            'registered_tasks': list(celery.tasks.keys()),
            'broker_url': app.config['CELERY_BROKER_URL'],
            'result_backend': app.config['CELERY_RESULT_BACKEND'],
            'beat_schedule': list(celery.conf.beat_schedule.keys())
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/history', methods=['GET'])
def task_history():
    """Get task execution history from database"""
    db_session = SessionLocal()
    
    # Get recent tasks
    tasks = db_session.query(TaskModel)\
        .order_by(TaskModel.created_at.desc())\
        .limit(50)\
        .all()
    
    db_session.close()
    
    return jsonify({
        'tasks': [task.to_dict() for task in tasks],
        'count': len(tasks)
    })

# ============================================================================
# CELERY WORKER CONFIGURATION EXAMPLES
# ============================================================================

"""
Running Celery Workers:
----------------------

# Basic worker
celery -A app.celery worker --loglevel=info

# Worker with concurrency
celery -A app.celery worker --loglevel=info --concurrency=4

# Worker for specific queue
celery -A app.celery worker --loglevel=info --queues=email,high_priority

# Beat scheduler for periodic tasks
celery -A app.celery beat --loglevel=info

# Flower for monitoring (optional)
flower -A app.celery --port=5555
"""

"""
docker-compose.yml example:
--------------------------
version: '3.8'
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  flask:
    build: .
    ports:
      - "5000:5000"
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    depends_on:
      - redis
  
  celery_worker:
    build: .
    command: celery -A app.celery worker --loglevel=info --concurrency=4
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    depends_on:
      - redis
      - flask
  
  celery_beat:
    build: .
    command: celery -A app.celery beat --loglevel=info
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - redis
      - flask
"""

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )