# Express.js Refreshers

Comprehensive Express.js guide for building REST APIs.

## 📚 Topics Covered

### Fundamentals
- **00_express_basics.js** - Setup, basic server, routing
- **01_routing.js** - Routes, route parameters, query strings
- **02_middleware.js** - Application, router, error middleware
- **03_request_response.js** - req, res objects, methods
- **04_static_files.js** - Serving static files, public directory
- **05_template_engines.js** - EJS, Pug, Handlebars

### API Development
- **06_rest_api.js** - RESTful design, CRUD operations
- **07_body_parsing.js** - JSON, URL-encoded, multipart
- **08_validation.js** - express-validator, Joi, custom validation
- **09_error_handling.js** - Error middleware, async errors, custom errors
- **10_authentication.js** - JWT, sessions, passport.js
- **11_authorization.js** - Role-based access, permissions
- **12_cors.js** - CORS configuration, preflight requests

### Database Integration
- **13_mongodb_mongoose.js** - Mongoose ODM, models, queries
- **14_postgresql.js** - pg library, query building
- **15_prisma.js** - Prisma ORM integration
- **16_redis.js** - Caching, session storage

### Advanced
- **17_file_upload.js** - multer, file handling, validation
- **18_rate_limiting.js** - Rate limiting, throttling
- **19_security.js** - helmet, sanitization, best practices
- **20_testing.js** - Jest, supertest, integration tests
- **21_logging.js** - winston, morgan, structured logging
- **22_performance.js** - Compression, caching, clustering
- **23_websockets.js** - Socket.IO integration
- **24_graphql.js** - GraphQL with Express
- **25_microservices.js** - Service communication, message queues
- **26_deployment.js** - PM2, Docker, environment management

## 🎯 Learning Path

1. **Express Basics** (00-05)
2. **API Development** (06-12)
3. **Database Integration** (13-16)
4. **Production Ready** (17-26)

## 💡 Best Practices

### Application Structure
```
project/
├── src/
│   ├── controllers/    # Route handlers
│   ├── models/         # Database models
│   ├── routes/         # Route definitions
│   ├── middleware/     # Custom middleware
│   ├── utils/          # Helper functions
│   ├── config/         # Configuration
│   └── app.js          # Express app
├── tests/              # Test files
└── server.js           # Entry point
```

### Middleware Order
1. Body parsers
2. CORS
3. Security headers (helmet)
4. Logger
5. Static files
6. Routes
7. Error handler (last)

### Error Handling
- Use async/await with try-catch
- Centralized error handling middleware
- Custom error classes
- Proper HTTP status codes
- Don't leak stack traces in production

## 🚀 Quick Start

```bash
# Initialize project
mkdir my-api && cd my-api
npm init -y

# Install Express
npm install express

# Install common dependencies
npm install dotenv cors helmet morgan

# Development dependencies
npm install -D nodemon

# Run server
node server.js

# Or with nodemon
npx nodemon server.js
```

## 📖 Key Concepts

### Basic Server
```javascript
const express = require('express');
const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.get('/', (req, res) => {
  res.json({ message: 'Hello World' });
});

// Error handling
app.use((err, req, res, next) => {
  res.status(500).json({ error: err.message });
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### REST API Routes
```javascript
app.get('/api/users', getAllUsers);       // Get all
app.get('/api/users/:id', getUser);       // Get one
app.post('/api/users', createUser);       // Create
app.put('/api/users/:id', updateUser);    // Update
app.delete('/api/users/:id', deleteUser); // Delete
```

### Middleware Pattern
```javascript
// Application-level
app.use((req, res, next) => {
  console.log('Time:', Date.now());
  next();
});

// Router-level
router.use('/admin', requireAuth);

// Error-handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});
```

---

Happy Express development! 🚂
