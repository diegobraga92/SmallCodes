"""
COMPREHENSIVE FLASK DATABASE/ORM TUTORIAL APPLICATION
This application demonstrates key Flask-SQLAlchemy concepts with detailed explanations.
"""

import os
from datetime import datetime
from typing import List, Optional
from contextlib import contextmanager

# Flask and related imports
from flask import Flask, request, jsonify, render_template_string, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, Index, text, func, create_engine
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from sqlalchemy.orm import Session, joinedload, selectinload, lazyload
from sqlalchemy.engine import Engine
import alembic.config
from werkzeug.exceptions import InternalServerError

# Initialize Flask app
app = Flask(__name__)

# Configure database - using SQLite for simplicity (can be changed to PostgreSQL/MySQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Show SQL queries in console for learning

# Initialize SQLAlchemy with Flask
db = SQLAlchemy(app)


# ============================================================================
# 1. DATABASE MODELS - DEFINING OUR SCHEMA
# ============================================================================

class User(db.Model):
    """
    User model demonstrating basic ORM features.
    
    In ORM (Object-Relational Mapping), we define Python classes that map to database tables.
    Each instance represents a row, and each attribute represents a column.
    """
    
    __tablename__ = 'users'
    
    # Primary key - auto-incrementing integer
    id = db.Column(db.Integer, primary_key=True)
    
    # String columns with constraints
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # DateTime column with default value
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to other tables
    # This establishes a one-to-many relationship with Post
    posts = db.relationship('Post', back_populates='author', 
                           cascade='all, delete-orphan', lazy='select')
    
    # One-to-one relationship with UserProfile
    profile = db.relationship('UserProfile', back_populates='user', 
                             uselist=False, cascade='all, delete-orphan')
    
    # Index on frequently queried columns for better performance
    __table_args__ = (
        Index('idx_user_username', 'username'),  # Index on username for faster lookups
        Index('idx_user_created', 'created_at'),  # Index on creation date for date range queries
    )
    
    def __repr__(self):
        return f'<User {self.username}>'


class UserProfile(db.Model):
    """One-to-one relationship example with User."""
    
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), 
                       unique=True, nullable=False)
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    
    # Back-reference to User
    user = db.relationship('User', back_populates='profile')
    
    def __repr__(self):
        return f'<UserProfile for User {self.user_id}>'


class Post(db.Model):
    """
    Post model demonstrating relationships and query patterns.
    """
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    author = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', 
                              cascade='all, delete-orphan', lazy='dynamic')
    tags = db.relationship('Tag', secondary='post_tags', back_populates='posts')
    
    # Indexes for query optimization
    __table_args__ = (
        Index('idx_post_user', 'user_id'),  # Foreign key index
        Index('idx_post_created', 'created_at'),  # For ordering/filtering by date
        Index('idx_post_title', 'title'),  # For title searches
    )
    
    def __repr__(self):
        return f'<Post {self.title}>'


class Comment(db.Model):
    """Comment model for demonstrating N+1 query problems."""
    
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    post = db.relationship('Post', back_populates='comments')
    author = db.relationship('User')
    
    __table_args__ = (
        Index('idx_comment_post', 'post_id'),  # Foreign key index
        Index('idx_comment_user', 'user_id'),  # Foreign key index
    )
    
    def __repr__(self):
        return f'<Comment {self.id}>'


class Tag(db.Model):
    """Tag model for many-to-many relationship demonstration."""
    
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Many-to-many relationship with Post
    posts = db.relationship('Post', secondary='post_tags', back_populates='tags')
    
    def __repr__(self):
        return f'<Tag {self.name}>'


# Association table for many-to-many relationship
class PostTag(db.Model):
    """Association table for Post-Tag many-to-many relationship."""
    
    __tablename__ = 'post_tags'
    
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    
    # Index on both columns for better join performance
    __table_args__ = (
        Index('idx_post_tag', 'post_id', 'tag_id'),
    )


# ============================================================================
# 2. DATABASE SETUP AND MIGRATIONS (ALEMBIC)
# ============================================================================

def init_database():
    """
    Initialize the database and create tables.
    
    In production, we would use Alembic for migrations instead of db.create_all().
    db.create_all() is fine for development but doesn't handle:
    - Schema updates
    - Data migrations
    - Version control
    - Rollbacks
    """
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Add some sample data
        if not User.query.first():
            # Create users
            user1 = User(username='alice', email='alice@example.com')
            user2 = User(username='bob', email='bob@example.com')
            
            # Create profiles
            profile1 = UserProfile(bio='Python developer', location='NYC')
            profile2 = UserProfile(bio='Web designer', location='SF')
            user1.profile = profile1
            user2.profile = profile2
            
            # Create posts
            post1 = Post(title='First Post', content='Hello World!', author=user1)
            post2 = Post(title='Second Post', content='Another post', author=user1)
            post3 = Post(title='Bob\'s Post', content='My thoughts', author=user2)
            
            # Create tags
            tag1 = Tag(name='python')
            tag2 = Tag(name='flask')
            tag3 = Tag(name='database')
            
            # Associate tags with posts
            post1.tags.extend([tag1, tag2])
            post2.tags.append(tag3)
            post3.tags.extend([tag1, tag3])
            
            # Create comments
            comment1 = Comment(content='Great post!', post=post1, author=user2)
            comment2 = Comment(content='Thanks!', post=post1, author=user1)
            
            # Add to session and commit
            db.session.add_all([user1, user2, tag1, tag2, tag3])
            db.session.commit()
            
            print("Database initialized with sample data!")


# ============================================================================
# 3. SESSION MANAGEMENT AND LIFECYCLE
# ============================================================================

"""
SQLAlchemy SESSION LIFECYCLE:

1. Session Creation: Session is created (db.session in Flask-SQLAlchemy)
2. Adding Objects: Objects are added to session with db.session.add()
3. Flush: Changes are sent to database (transaction buffer)
4. Commit: Transaction is permanently saved to database
5. Rollback: Transaction is cancelled, changes are discarded
6. Close: Session is closed, connections returned to pool

Flask-SQLAlchemy automatically handles session scope per request.
Each request gets its own session that's closed at the end.
"""

@app.route('/session-demo')
def session_demo():
    """
    Demonstrate session lifecycle and transactions.
    """
    try:
        # Start of a transaction (implicitly started by SQLAlchemy)
        print("1. Starting new transaction...")
        
        # Create a new user object (in transient state)
        new_user = User(username='charlie', email='charlie@example.com')
        print(f"2. Created user object (state: {db.session.query(User).get(new_user.id)})")
        
        # Add to session (now in pending state)
        db.session.add(new_user)
        print(f"3. Added to session (state: {new_user in db.session})")
        
        # Flush - sends INSERT to database but doesn't commit
        db.session.flush()
        print("4. Flushed to database (transaction not committed yet)")
        
        # At this point, new_user.id is available even though not committed
        print(f"5. User ID assigned: {new_user.id}")
        
        # Now commit the transaction
        db.session.commit()
        print("6. Transaction committed - user saved to database")
        
        return jsonify({
            'message': 'Session lifecycle demonstrated',
            'user_id': new_user.id,
            'state': 'committed'
        })
        
    except Exception as e:
        # Rollback on error
        db.session.rollback()
        print(f"7. Error occurred, rolled back: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# 4. TRANSACTIONS AND ROLLBACKS
# ============================================================================

@app.route('/transaction-demo', methods=['POST'])
def transaction_demo():
    """
    Demonstrate atomic transactions with rollback on failure.
    
    Transactions ensure that either ALL operations succeed or NONE do.
    This maintains database consistency.
    """
    data = request.get_json()
    
    try:
        # Begin transaction (implicit in Flask-SQLAlchemy)
        print("Starting transaction...")
        
        # Create user
        username = data.get('username')
        email = data.get('email')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            raise ValueError(f"Username '{username}' already exists")
        
        # Create user and profile in single transaction
        user = User(username=username, email=email)
        profile = UserProfile(bio=data.get('bio', ''), location=data.get('location', ''))
        user.profile = profile
        
        db.session.add(user)
        
        # Create a post for the user
        post = Post(
            title=data.get('title', 'First Post'),
            content=data.get('content', 'Hello!'),
            author=user
        )
        db.session.add(post)
        
        # Try to create a tag with a duplicate name (will fail due to unique constraint)
        # This simulates a business logic error
        duplicate_tag = Tag(name='python')  # 'python' already exists in our seed data
        db.session.add(duplicate_tag)
        
        # This will raise IntegrityError because 'python' tag already exists
        # The entire transaction should roll back
        
        db.session.commit()  # This will fail
        
        return jsonify({'message': 'Transaction completed successfully'})
        
    except (IntegrityError, ValueError) as e:
        # Rollback the entire transaction
        db.session.rollback()
        print(f"Transaction rolled back: {e}")
        
        # Verify that user was NOT saved
        user_exists = User.query.filter_by(username=username).first()
        
        return jsonify({
            'error': 'Transaction failed and rolled back',
            'reason': str(e),
            'user_saved': user_exists is not None
        }), 400
        
    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# 5. N+1 QUERY PROBLEM DEMONSTRATION
# ============================================================================

@app.route('/nplusone-problem')
def nplusone_problem():
    """
    Demonstrate and solve the N+1 query problem.
    
    PROBLEM: When fetching posts and their authors separately,
    we make 1 query for posts + N queries for authors = N+1 queries.
    
    SOLUTION: Use eager loading (joinedload, selectinload) to fetch
    related data in a single query.
    """
    
    # ========== THE PROBLEM: N+1 QUERIES ==========
    print("\n=== N+1 QUERY PROBLEM ===")
    
    # Query 1: Get all posts
    posts = Post.query.all()
    
    # For each post, access author (triggers N additional queries!)
    post_data_problem = []
    for post in posts:
        # Each post.author access triggers a new query!
        post_data_problem.append({
            'title': post.title,
            'author': post.author.username,  # N queries here!
            'comments_count': post.comments.count()  # Another N queries if lazy!
        })
    
    print(f"Made approximately {len(posts) + 1} queries (N+1 problem)")
    
    # ========== SOLUTION 1: JOINED LOADING ==========
    print("\n=== SOLUTION: JOINED LOADING ===")
    
    # Single query with JOIN
    posts_joined = Post.query.options(
        joinedload(Post.author)  # Load author in same query using JOIN
    ).all()
    
    post_data_solution1 = []
    for post in posts_joined:
        # No additional query for author
        post_data_solution1.append({
            'title': post.title,
            'author': post.author.username,
            'comments_count': post.comments.count()  # Still N queries for comments!
        })
    
    print("Made 1 query for posts + authors")
    
    # ========== SOLUTION 2: SELECTIN LOADING (for collections) ==========
    print("\n=== SOLUTION: SELECTIN LOADING FOR COMMENTS ===")
    
    posts_with_comments = Post.query.options(
        joinedload(Post.author),
        selectinload(Post.comments)  # Load comments in separate but efficient query
    ).all()
    
    post_data_solution2 = []
    for post in posts_with_comments:
        # No additional queries for author or comments
        post_data_solution2.append({
            'title': post.title,
            'author': post.author.username,
            'comments_count': len(post.comments)  # Already loaded!
        })
    
    print("Made 2 queries total (1 for posts+authors, 1 for all comments)")
    
    return jsonify({
        'nplusone_problem': {
            'posts_count': len(post_data_problem),
            'query_count': len(posts) + 1,
            'message': 'Inefficient: made N+1 queries'
        },
        'solution_joined': {
            'posts_count': len(post_data_solution1),
            'query_count': 1,
            'message': 'Better: used joinedload for authors'
        },
        'solution_selectin': {
            'posts_count': len(post_data_solution2),
            'query_count': 2,
            'message': 'Best: used joinedload + selectinload'
        }
    })


# ============================================================================
# 6. LAZY VS EAGER LOADING
# ============================================================================

@app.route('/loading-strategies')
def loading_strategies():
    """
    Demonstrate different loading strategies in SQLAlchemy.
    
    LAZY LOADING: Load related objects only when accessed (default)
    EAGER LOADING: Load related objects immediately with the parent
    
    Tradeoffs:
    - Lazy: Less initial data, but potential N+1 problems
    - Eager: More initial data, but fewer queries
    """
    
    # Clear any existing queries for demonstration
    db.session.expunge_all()
    
    print("\n=== LAZY LOADING (default) ===")
    user = User.query.filter_by(username='alice').first()
    
    # posts are not loaded yet (lazy='select' by default)
    print(f"User loaded: {user.username}")
    print(f"Posts loaded yet? {'No' if user.posts is None else 'Yes'}")
    
    # Accessing posts triggers a query
    posts = user.posts  # Query executed here!
    print(f"After accessing posts: {len(posts)} posts loaded")
    
    print("\n=== EAGER LOADING (joinedload) ===")
    db.session.expunge_all()  # Clear session
    
    # Load user with posts eagerly
    user_eager = User.query.options(
        joinedload(User.posts)  # Eager load posts
    ).filter_by(username='alice').first()
    
    print(f"User loaded: {user_eager.username}")
    # Posts are already loaded (no additional query)
    print(f"Posts loaded with user: {len(user_eager.posts)}")
    
    print("\n=== DYNAMIC LOADING ===")
    # Dynamic relationship returns a query instead of loading
    post = Post.query.first()
    comments_query = post.comments  # Returns BaseQuery, not loaded list
    print(f"Comments query object: {comments_query}")
    print(f"Can filter dynamically: {comments_query.filter_by(user_id=1).all()}")
    
    return jsonify({
        'lazy_loading': {
            'description': 'Related objects loaded on access',
            'queries': 'Multiple queries (N+1 potential)',
            'use_case': 'When you might not need related data'
        },
        'eager_loading': {
            'description': 'Related objects loaded immediately',
            'queries': 'Single query with JOIN',
            'use_case': 'When you know you need related data'
        },
        'dynamic_loading': {
            'description': 'Returns query object for further filtering',
            'queries': 'Controlled by programmer',
            'use_case': 'When you need to filter/sort related data'
        }
    })


# ============================================================================
# 7. INDEXING BASICS DEMONSTRATION
# ============================================================================

@app.route('/indexing-demo')
def indexing_demo():
    """
    Demonstrate the importance of database indexes.
    
    Indexes are data structures that improve query speed at the cost of:
    - Additional storage
    - Slower INSERT/UPDATE/DELETE (indexes must be updated)
    
    Common index types:
    - B-tree: Default, good for equality and range queries
    - Hash: Only equality queries, faster than B-tree
    - GiST, GIN: For full-text search, arrays, JSON
    """
    
    # Explain queries to show index usage
    from sqlalchemy.dialects import sqlite
    
    print("\n=== QUERY WITHOUT INDEX (FULL TABLE SCAN) ===")
    
    # Query on non-indexed column (email has no index in our schema)
    query_no_index = User.query.filter(User.email.like('%@example.com'))
    explain_no_index = str(query_no_index.statement.compile(
        dialect=sqlite.dialect(),
        compile_kwargs={"literal_binds": True}
    ))
    print(f"Query: {explain_no_index}")
    print("This requires scanning all rows in users table")
    
    print("\n=== QUERY WITH INDEX (INDEX SEEK) ===")
    
    # Query on indexed column (username has index)
    query_with_index = User.query.filter(User.username == 'alice')
    explain_with_index = str(query_with_index.statement.compile(
        dialect=sqlite.dialect(),
        compile_kwargs={"literal_binds": True}
    ))
    print(f"Query: {explain_with_index}")
    print("This can use the idx_user_username index")
    
    print("\n=== COMPOSITE INDEX DEMONSTRATION ===")
    
    # Our PostTag table has composite index on (post_id, tag_id)
    # This helps queries filtering on both columns or just post_id
    composite_query = PostTag.query.filter_by(post_id=1).all()
    print(f"Composite index helps queries on post_id or (post_id, tag_id)")
    
    return jsonify({
        'indexing_importance': {
            'without_index': 'Full table scan - O(n) complexity',
            'with_index': 'Index seek - O(log n) complexity',
            'tradeoffs': 'Faster reads vs slower writes, more storage'
        },
        'index_types': {
            'single_column': 'For queries filtering on one column',
            'composite': 'For queries filtering on multiple columns',
            'unique': 'For enforcing uniqueness (already created by unique=True)',
            'covering': 'Index that includes all queried columns'
        }
    })


# ============================================================================
# 8. ORM VS CORE SQL TRADEOFFS
# ============================================================================

@app.route('/orm-vs-sql')
def orm_vs_sql():
    """
    Demonstrate tradeoffs between ORM and raw SQL.
    
    ORM PROS:
    - Object-oriented interface
    - Database abstraction
    - Automatic query building
    - Relationships and lazy loading
    - Security (parameterized queries)
    
    ORM CONS:
    - Overhead for complex queries
    - Less control over SQL
    - Can generate inefficient queries
    - Learning curve
    
    RAW SQL PROS:
    - Full control
    - Complex queries easier
    - Can use database-specific features
    - Sometimes faster
    
    RAW SQL CONS:
    - SQL injection risk if not careful
    - Database coupling
    - Manual mapping to objects
    - More verbose
    """
    
    # ========== ORM APPROACH ==========
    print("\n=== ORM QUERY ===")
    
    # Complex query using ORM
    orm_results = db.session.query(
        User.username,
        func.count(Post.id).label('post_count'),
        func.group_concat(Post.title).label('titles')
    ).join(Post, User.id == Post.user_id) \
     .group_by(User.id) \
     .having(func.count(Post.id) > 0) \
     .all()
    
    orm_data = []
    for row in orm_results:
        orm_data.append({
            'username': row.username,
            'post_count': row.post_count,
            'titles': row.titles
        })
    
    print(f"ORM generated SQL: {db.session.query(User).statement}")
    
    # ========== RAW SQL APPROACH ==========
    print("\n=== RAW SQL QUERY ===")
    
    raw_sql = """
    SELECT 
        u.username,
        COUNT(p.id) as post_count,
        GROUP_CONCAT(p.title) as titles
    FROM users u
    JOIN posts p ON u.id = p.user_id
    GROUP BY u.id
    HAVING COUNT(p.id) > 0
    """
    
    raw_results = db.session.execute(text(raw_sql)).fetchall()
    
    raw_data = []
    for row in raw_results:
        raw_data.append({
            'username': row.username,
            'post_count': row.post_count,
            'titles': row.titles
        })
    
    print(f"Raw SQL used: {raw_sql[:100]}...")
    
    # ========== HYBRID APPROACH ==========
    print("\n=== HYBRID APPROACH (SQL Expression) ===")
    
    # Using SQLAlchemy Core (not ORM)
    from sqlalchemy import select, join
    
    users = User.__table__
    posts = Post.__table__
    
    stmt = select([
        users.c.username,
        func.count(posts.c.id).label('post_count')
    ]).select_from(
        join(users, posts, users.c.id == posts.c.user_id)
    ).group_by(users.c.id)
    
    hybrid_results = db.session.execute(stmt).fetchall()
    
    return jsonify({
        'orm_approach': {
            'results': orm_data,
            'advantages': [
                'Type-safe',
                'Automatic parameter escaping',
                'Database agnostic',
                'Object mapping'
            ],
            'disadvantages': [
                'Can be slower for complex queries',
                'Less control over SQL',
                'Learning curve'
            ]
        },
        'raw_sql_approach': {
            'results': raw_data,
            'advantages': [
                'Full control over SQL',
                'Can use database-specific features',
                'Sometimes faster for complex queries'
            ],
            'disadvantages': [
                'SQL injection risk if not careful',
                'Database coupling',
                'Manual result mapping'
            ]
        },
        'recommendation': {
            'simple_crud': 'Use ORM',
            'complex_reporting': 'Consider raw SQL or hybrid',
            'security_critical': 'ORM with parameterized queries',
            'performance_critical': 'Benchmark both approaches'
        }
    })


# ============================================================================
# 9. GRACEFUL ERROR HANDLING
# ============================================================================

@app.route('/error-handling-demo')
def error_handling_demo():
    """
    Demonstrate graceful error handling for database operations.
    """
    
    user_id = request.args.get('user_id', 'invalid')
    
    try:
        # Attempt to query database
        if user_id == 'invalid':
            # Simulate invalid input
            raise ValueError("Invalid user ID format")
        
        user = User.query.get(int(user_id))
        
        if not user:
            # Handle not found gracefully
            return jsonify({
                'error': 'User not found',
                'error_code': 'NOT_FOUND'
            }), 404
        
        # Access related data (might cause other errors)
        post_count = len(user.posts)
        
        return jsonify({
            'username': user.username,
            'post_count': post_count
        })
        
    except ValueError as e:
        # Handle client input errors
        return jsonify({
            'error': 'Invalid input',
            'details': str(e),
            'error_code': 'INVALID_INPUT'
        }), 400
        
    except OperationalError as e:
        # Handle database connection errors
        app.logger.error(f"Database connection error: {e}")
        
        # Could implement retry logic here
        return jsonify({
            'error': 'Database temporarily unavailable',
            'error_code': 'DB_UNAVAILABLE',
            'retry_after': 30
        }), 503
        
    except SQLAlchemyError as e:
        # Catch all SQLAlchemy errors
        app.logger.error(f"Database error: {e}")
        db.session.rollback()  # Always rollback on error
        
        return jsonify({
            'error': 'Database operation failed',
            'error_code': 'DB_ERROR'
        }), 500
        
    except Exception as e:
        # Catch any other unexpected errors
        app.logger.exception(f"Unexpected error: {e}")
        
        return jsonify({
            'error': 'Internal server error',
            'error_code': 'INTERNAL_ERROR'
        }), 500


# ============================================================================
# 10. MIGRATIONS WITH ALEMBIC (DEMONSTRATION)
# ============================================================================

"""
ALEMBIC MIGRATIONS:

Alembic is a database migration tool for SQLAlchemy.
It handles schema changes over time.

Typical workflow:
1. alembic init migrations
2. Edit alembic.ini to point to your database
3. alembic revision --autogenerate -m "description"
4. Review and edit the generated migration script
5. alembic upgrade head

Key commands:
- alembic current: Show current revision
- alembic history: Show migration history
- alembic upgrade +2: Upgrade 2 revisions
- alembic downgrade -1: Downgrade 1 revision
"""

def demonstrate_migrations():
    """
    This function shows how migrations would work with Alembic.
    In practice, you'd use alembic commands in terminal.
    """
    
    print("\n=== ALEMBIC MIGRATION EXAMPLE ===")
    
    # Example of what a migration file might look like
    migration_example = """
    '''Example migration file: add_phone_number_to_users.py'''
    
    from alembic import op
    import sqlalchemy as sa
    
    def upgrade():
        # Add new column
        op.add_column('users', sa.Column('phone_number', sa.String(20)))
        
        # Create index on new column
        op.create_index('idx_user_phone', 'users', ['phone_number'])
        
        # Data migration: set default values
        op.execute("UPDATE users SET phone_number = 'unknown'")
        
    def downgrade():
        # Remove index
        op.drop_index('idx_user_phone', 'users')
        
        # Remove column
        op.drop_column('users', 'phone_number')
    """
    
    print(migration_example)
    
    return jsonify({
        'migration_tools': {
            'alembic': 'Most common for SQLAlchemy',
            'flask_migrate': 'Flask wrapper for Alembic',
            'sqlalchemy_migrate': 'Alternative (older)'
        },
        'best_practices': [
            'Always review auto-generated migrations',
            'Test migrations on development database first',
            'Backup production database before migrating',
            'Use transactions for data migrations when possible',
            'Write reversible migrations (implement downgrade)'
        ]
    })


# ============================================================================
# 11. CONTEXT MANAGER FOR TRANSACTIONS
# ============================================================================

@contextmanager
def transaction_context():
    """
    Custom context manager for database transactions.
    
    This pattern ensures transactions are always properly committed or rolled back.
    """
    try:
        yield db.session
        db.session.commit()
        print("Transaction committed successfully")
    except Exception as e:
        db.session.rollback()
        print(f"Transaction rolled back: {e}")
        raise
    finally:
        db.session.close()  # In Flask-SQLAlchemy, this just removes session


@app.route('/context-manager-demo')
def context_manager_demo():
    """
    Demonstrate using context managers for database operations.
    """
    
    try:
        with transaction_context() as session:
            # All operations in this block are in a transaction
            new_user = User(username='david', email='david@example.com')
            session.add(new_user)
            
            # If any operation fails, everything rolls back
            new_post = Post(title='Context Post', content='Demo', author=new_user)
            session.add(new_post)
            
            # No explicit commit needed - context manager handles it
            
        return jsonify({'message': 'Transaction completed via context manager'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# 12. PERFORMANCE OPTIMIZATION DEMONSTRATION
# ============================================================================

@app.route('/performance-tips')
def performance_tips():
    """
    Demonstrate common performance optimizations.
    """
    
    tips = {
        'query_optimization': [
            'Use .only() or .options(load_only()) to load only needed columns',
            'Avoid SELECT * in production',
            'Use pagination for large result sets'
        ],
        'indexing_strategy': [
            'Index foreign keys',
            'Index columns used in WHERE, ORDER BY, JOIN',
            'Consider composite indexes for multi-column queries',
            'Monitor slow queries and add indexes as needed'
        ],
        'session_management': [
            'Keep sessions short-lived',
            'Use scoped sessions in web applications',
            'Expunge objects from session when done with them',
            'Avoid long-running transactions'
        ],
        'connection_pooling': {
            'pool_size': '5-20 connections typically',
            'max_overflow': 'Allow some overflow for spikes',
            'pool_recycle': 'Recycle connections periodically (3600 seconds)',
            'pool_pre_ping': 'Test connections before using'
        }
    }
    
    # Demonstrate query optimization
    print("\n=== QUERY OPTIMIZATION DEMONSTRATION ===")
    
    # BAD: Loads all columns
    bad_query = User.query.all()
    
    # BETTER: Load only needed columns
    good_query = User.query.options(db.load_only(User.username, User.email)).all()
    
    # BEST: Use pagination for large datasets
    paginated = User.query.paginate(page=1, per_page=20, error_out=False)
    
    return jsonify({
        'performance_tips': tips,
        'query_comparison': {
            'bad_query': 'SELECT * FROM users',
            'good_query': 'SELECT username, email FROM users',
            'paginated_query': 'SELECT * FROM users LIMIT 20 OFFSET 0'
        }
    })


# ============================================================================
# 13. MAIN APPLICATION ROUTES
# ============================================================================

@app.route('/')
def index():
    """Main page with links to all demonstrations."""
    
    html = """
    <html>
        <head>
            <title>Flask Database/ORM Tutorial</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #333; }
                .demo { margin: 20px 0; padding: 15px; border-left: 4px solid #007bff; background: #f8f9fa; }
                a { color: #007bff; text-decoration: none; }
                a:hover { text-decoration: underline; }
                code { background: #e9ecef; padding: 2px 5px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h1>Flask Database & ORM Concepts Demo</h1>
            <p>Click on any demo to see the concept in action:</p>
            
            <div class="demo">
                <h2>📚 Core Concepts</h2>
                <ul>
                    <li><a href="/session-demo">Session Lifecycle & Management</a></li>
                    <li><a href="/transaction-demo" target="_blank">Transactions & Rollbacks</a> (POST endpoint)</li>
                    <li><a href="/orm-vs-sql">ORM vs Raw SQL Tradeoffs</a></li>
                </ul>
            </div>
            
            <div class="demo">
                <h2>⚡ Performance Concepts</h2>
                <ul>
                    <li><a href="/nplusone-problem">N+1 Query Problem & Solutions</a></li>
                    <li><a href="/loading-strategies">Lazy vs Eager Loading</a></li>
                    <li><a href="/indexing-demo">Database Indexing Basics</a></li>
                    <li><a href="/performance-tips">Performance Optimization Tips</a></li>
                </ul>
            </div>
            
            <div class="demo">
                <h2>🛡️ Reliability</h2>
                <ul>
                    <li><a href="/error-handling-demo?user_id=1">Graceful Error Handling</a></li>
                    <li><a href="/error-handling-demo?user_id=invalid">Error Handling with Invalid Input</a></li>
                    <li><a href="/context-manager-demo">Transaction Context Managers</a></li>
                </ul>
            </div>
            
            <div class="demo">
                <h2>📝 Database Models</h2>
                <p>Models defined in code:</p>
                <ul>
                    <li><code>User</code> with one-to-many <code>Post</code> relationship</li>
                    <li><code>UserProfile</code> with one-to-one relationship</li>
                    <li><code>Comment</code> and <code>Tag</code> with many-to-many relationships</li>
                    <li>Indexes on frequently queried columns</li>
                </ul>
            </div>
            
            <div class="demo">
                <h2>🔄 Migration Info</h2>
                <p>Check the console output for Alembic migration examples.</p>
                <p>In production, use: <code>flask db migrate</code> and <code>flask db upgrade</code></p>
            </div>
        </body>
    </html>
    """
    
    return render_template_string(html)


# ============================================================================
# 14. DATABASE EVENT LISTENERS (ADVANCED)
# ============================================================================

# Event listeners for database operations
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable foreign key constraints in SQLite."""
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


@event.listens_for(User, 'before_insert')
def hash_password_before_insert(mapper, connection, target):
    """
    Example of using ORM events.
    In real apps, you might hash passwords here.
    """
    print(f"Before inserting user: {target.username}")


@event.listens_for(Session, 'after_commit')
def after_commit_listener(session):
    """Example post-commit hook."""
    print("Transaction was committed successfully")


# ============================================================================
# 15. APPLICATION STARTUP
# ============================================================================

if __name__ == '__main__':
    # Initialize database
    print("Initializing database...")
    init_database()
    
    # Show all registered routes
    print("\n=== AVAILABLE ENDPOINTS ===")
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            print(f"{rule.endpoint}: {rule.rule}")
    
    print("\n" + "="*60)
    print("Flask Database/ORM Tutorial Application")
    print("="*60)
    print("\nKey concepts covered:")
    print("1. Database Models & Relationships")
    print("2. ORM vs Core SQL Tradeoffs")
    print("3. Session Scope & Lifecycle")
    print("4. Transactions & Rollbacks")
    print("5. N+1 Query Problems & Solutions")
    print("6. Lazy vs Eager Loading")
    print("7. Indexing Basics")
    print("8. Migrations (Alembic concepts)")
    print("9. Graceful Error Handling")
    print("\nVisit http://localhost:5000 to see all demos")
    print("="*60 + "\n")
    
    # Run the application
    app.run(debug=True, port=5000)