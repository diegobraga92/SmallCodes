# Node.js Refreshers

Comprehensive Node.js guide for server-side JavaScript development.

## 📚 Topics Covered

### Fundamentals
- **00_node_basics.js** - Node.js runtime, modules, REPL
- **01_modules.js** - CommonJS, require/exports, ES modules
- **02_file_system.js** - fs module, read/write, streams
- **03_path_module.js** - Path manipulation, joining, resolving
- **04_events.js** - EventEmitter, custom events, listeners
- **05_streams.js** - Readable, Writable, Transform, Pipe

### HTTP & Networking
- **06_http_server.js** - Creating HTTP server, routing basics
- **07_http_client.js** - Making HTTP requests, fetch
- **08_url_module.js** - URL parsing, query strings
- **09_networking.js** - TCP, UDP, sockets

### Intermediate
- **10_npm_packages.js** - npm basics, package.json, dependencies
- **11_environment_vars.js** - process.env, dotenv, configuration
- **12_child_processes.js** - spawn, exec, fork, worker threads
- **13_buffers.js** - Binary data, encoding, manipulation
- **14_timers.js** - setTimeout, setInterval, setImmediate
- **15_error_handling.js** - Error types, try/catch, async errors

### Database Integration
- **16_mongodb.js** - MongoDB connection, CRUD operations
- **17_postgresql.js** - PostgreSQL with pg, queries, transactions
- **18_redis.js** - Redis client, caching, pub/sub
- **19_orm_prisma.js** - Prisma ORM, models, migrations

### Advanced
- **20_authentication.js** - JWT, sessions, bcrypt, security
- **21_middleware.js** - Middleware patterns, error handling
- **22_testing.js** - Jest, Mocha, integration tests
- **23_performance.js** - Clustering, caching, profiling
- **24_security.js** - Input validation, sanitization, helmet
- **25_deployment.js** - PM2, Docker, environment setup
- **26_websockets.js** - Real-time communication, Socket.IO
- **27_graphql.js** - GraphQL server, resolvers, schema
- **28_microservices.js** - Service architecture, message queues

## 🎯 Learning Path

1. **Core Node.js** (00-05)
2. **HTTP & Networking** (06-09)
3. **Package Management** (10-15)
4. **Database Integration** (16-19)
5. **Production Ready** (20-28)

## 💡 Best Practices

- Use async/await over callbacks
- Handle errors properly
- Use environment variables for config
- Implement proper logging
- Use streams for large files
- Cluster for multi-core usage
- Implement rate limiting
- Validate input data
- Use TypeScript for type safety
- Monitor application health

## 🚀 Quick Start

```bash
# Initialize new project
npm init -y

# Install common dependencies
npm install express dotenv

# Run Node.js file
node app.js

# With nodemon (auto-restart)
npm install -D nodemon
npx nodemon app.js
```

## 📖 Key Concepts

### Async Patterns
- Callbacks (legacy)
- Promises
- Async/await
- Event emitters
- Streams

### Common Modules
- **fs**: File system operations
- **http/https**: HTTP server/client
- **path**: Path manipulation
- **os**: Operating system info
- **crypto**: Encryption
- **stream**: Data streaming

### NPM Scripts
```json
{
  "scripts": {
    "start": "node app.js",
    "dev": "nodemon app.js",
    "test": "jest",
    "build": "tsc"
  }
}
```

---

Happy Node.js development! 🚀
