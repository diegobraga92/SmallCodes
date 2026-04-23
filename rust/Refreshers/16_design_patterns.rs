//// RUST DESIGN PATTERNS
/// Classic design patterns adapted for Rust's ownership and type system
/// Covers creational, structural, and behavioral patterns with idiomatic Rust

use std::rc::Rc;
use std::cell::RefCell;
use std::sync::{Arc, Mutex};

// ============================================================================
// 1. BUILDER PATTERN
// ============================================================================

/// Builder pattern for complex object construction
/// Rust-specific: Can enforce required fields at compile time

// Traditional builder
#[derive(Debug, Clone)]
struct User {
    id: u64,
    name: String,
    email: String,
    age: Option<u32>,
    role: String,
}

struct UserBuilder {
    id: u64,
    name: String,
    email: String,
    age: Option<u32>,
    role: String,
}

impl UserBuilder {
    fn new(id: u64, name: impl Into<String>) -> Self {
        Self {
            id,
            name: name.into(),
            email: String::new(),
            age: None,
            role: "user".to_string(),
        }
    }
    
    fn email(mut self, email: impl Into<String>) -> Self {
        self.email = email.into();
        self
    }
    
    fn age(mut self, age: u32) -> Self {
        self.age = Some(age);
        self
    }
    
    fn role(mut self, role: impl Into<String>) -> Self {
        self.role = role.into();
        self
    }
    
    fn build(self) -> User {
        User {
            id: self.id,
            name: self.name,
            email: self.email,
            age: self.age,
            role: self.role,
        }
    }
}

/// Type-state builder - enforces required fields at compile time
struct HttpRequestBuilder<Stage> {
    url: Option<String>,
    method: Option<String>,
    body: Option<String>,
    _stage: std::marker::PhantomData<Stage>,
}

struct NoUrl;
struct NoMethod;
struct Ready;

impl HttpRequestBuilder<NoUrl> {
    fn new() -> Self {
        Self {
            url: None,
            method: None,
            body: None,
            _stage: std::marker::PhantomData,
        }
    }
    
    fn url(self, url: impl Into<String>) -> HttpRequestBuilder<NoMethod> {
        HttpRequestBuilder {
            url: Some(url.into()),
            method: self.method,
            body: self.body,
            _stage: std::marker::PhantomData,
        }
    }
}

impl HttpRequestBuilder<NoMethod> {
    fn method(self, method: impl Into<String>) -> HttpRequestBuilder<Ready> {
        HttpRequestBuilder {
            url: self.url,
            method: Some(method.into()),
            body: self.body,
            _stage: std::marker::PhantomData,
        }
    }
}

impl HttpRequestBuilder<Ready> {
    fn body(mut self, body: impl Into<String>) -> Self {
        self.body = Some(body.into());
        self
    }
    
    fn build(self) -> HttpRequest {
        HttpRequest {
            url: self.url.unwrap(),
            method: self.method.unwrap(),
            body: self.body,
        }
    }
}

#[derive(Debug)]
struct HttpRequest {
    url: String,
    method: String,
    body: Option<String>,
}


// ============================================================================
// 2. FACTORY PATTERN
// ============================================================================

/// Factory pattern for creating objects based on input

trait Animal {
    fn speak(&self) -> String;
}

struct Dog;
struct Cat;
struct Bird;

impl Animal for Dog {
    fn speak(&self) -> String {
        "Woof!".to_string()
    }
}

impl Animal for Cat {
    fn speak(&self) -> String {
        "Meow!".to_string()
    }
}

impl Animal for Bird {
    fn speak(&self) -> String {
        "Tweet!".to_string()
    }
}

// Simple factory
fn create_animal(animal_type: &str) -> Option<Box<dyn Animal>> {
    match animal_type {
        "dog" => Some(Box::new(Dog)),
        "cat" => Some(Box::new(Cat)),
        "bird" => Some(Box::new(Bird)),
        _ => None,
    }
}

// Factory with enum (more Rust-idiomatic)
enum AnimalType {
    Dog,
    Cat,
    Bird,
}

impl AnimalType {
    fn create(&self) -> Box<dyn Animal> {
        match self {
            AnimalType::Dog => Box::new(Dog),
            AnimalType::Cat => Box::new(Cat),
            AnimalType::Bird => Box::new(Bird),
        }
    }
}


// ============================================================================
// 3. SINGLETON PATTERN
// ============================================================================

/// Singleton in Rust using lazy_static or once_cell
/// Ensures only one instance exists

use std::sync::OnceLock;

struct Config {
    api_key: String,
    timeout: u64,
}

static CONFIG: OnceLock<Config> = OnceLock::new();

impl Config {
    fn global() -> &'static Config {
        CONFIG.get_or_init(|| {
            Config {
                api_key: "secret-key".to_string(),
                timeout: 30,
            }
        })
    }
}

// Thread-safe mutable singleton
static COUNTER: OnceLock<Mutex<i32>> = OnceLock::new();

fn get_counter() -> &'static Mutex<i32> {
    COUNTER.get_or_init(|| Mutex::new(0))
}


// ============================================================================
// 4. STRATEGY PATTERN
// ============================================================================

/// Strategy pattern for interchangeable algorithms
/// Rust uses traits naturally for this

trait CompressionStrategy {
    fn compress(&self, data: &str) -> Vec<u8>;
}

struct GzipCompression;
struct ZipCompression;
struct NoCompression;

impl CompressionStrategy for GzipCompression {
    fn compress(&self, data: &str) -> Vec<u8> {
        format!("GZIP:{}", data).into_bytes()
    }
}

impl CompressionStrategy for ZipCompression {
    fn compress(&self, data: &str) -> Vec<u8> {
        format!("ZIP:{}", data).into_bytes()
    }
}

impl CompressionStrategy for NoCompression {
    fn compress(&self, data: &str) -> Vec<u8> {
        data.as_bytes().to_vec()
    }
}

struct Compressor<S: CompressionStrategy> {
    strategy: S,
}

impl<S: CompressionStrategy> Compressor<S> {
    fn new(strategy: S) -> Self {
        Self { strategy }
    }
    
    fn compress_file(&self, data: &str) -> Vec<u8> {
        self.strategy.compress(data)
    }
}


// ============================================================================
// 5. OBSERVER PATTERN
// ============================================================================

/// Observer pattern for event notification
/// Rust uses callbacks or channels

trait Observer {
    fn update(&mut self, message: &str);
}

struct EmailNotifier {
    email: String,
}

impl Observer for EmailNotifier {
    fn update(&mut self, message: &str) {
        println!("Email to {}: {}", self.email, message);
    }
}

struct SmsNotifier {
    phone: String,
}

impl Observer for SmsNotifier {
    fn update(&mut self, message: &str) {
        println!("SMS to {}: {}", self.phone, message);
    }
}

struct Subject {
    observers: Vec<Box<dyn Observer>>,
}

impl Subject {
    fn new() -> Self {
        Self {
            observers: Vec::new(),
        }
    }
    
    fn attach(&mut self, observer: Box<dyn Observer>) {
        self.observers.push(observer);
    }
    
    fn notify(&mut self, message: &str) {
        for observer in &mut self.observers {
            observer.update(message);
        }
    }
}


// ============================================================================
// 6. DECORATOR PATTERN
// ============================================================================

/// Decorator pattern for adding behavior dynamically
/// Rust typically uses composition or trait objects

trait Coffee {
    fn cost(&self) -> f64;
    fn description(&self) -> String;
}

struct SimpleCoffee;

impl Coffee for SimpleCoffee {
    fn cost(&self) -> f64 {
        2.0
    }
    
    fn description(&self) -> String {
        "Simple coffee".to_string()
    }
}

struct MilkDecorator<C: Coffee> {
    coffee: C,
}

impl<C: Coffee> MilkDecorator<C> {
    fn new(coffee: C) -> Self {
        Self { coffee }
    }
}

impl<C: Coffee> Coffee for MilkDecorator<C> {
    fn cost(&self) -> f64 {
        self.coffee.cost() + 0.5
    }
    
    fn description(&self) -> String {
        format!("{}, milk", self.coffee.description())
    }
}

struct SugarDecorator<C: Coffee> {
    coffee: C,
}

impl<C: Coffee> SugarDecorator<C> {
    fn new(coffee: C) -> Self {
        Self { coffee }
    }
}

impl<C: Coffee> Coffee for SugarDecorator<C> {
    fn cost(&self) -> f64 {
        self.coffee.cost() + 0.3
    }
    
    fn description(&self) -> String {
        format!("{}, sugar", self.coffee.description())
    }
}


// ============================================================================
// 7. ADAPTER PATTERN
// ============================================================================

/// Adapter pattern for interface compatibility

// External library interface
struct LegacyRectangle {
    x1: f64,
    y1: f64,
    x2: f64,
    y2: f64,
}

impl LegacyRectangle {
    fn draw_legacy(&self) {
        println!("Drawing legacy rectangle from ({},{}) to ({},{})", 
                 self.x1, self.y1, self.x2, self.y2);
    }
}

// Our interface
trait Shape {
    fn draw(&self);
}

// Adapter
struct RectangleAdapter {
    rectangle: LegacyRectangle,
}

impl RectangleAdapter {
    fn new(x: f64, y: f64, width: f64, height: f64) -> Self {
        Self {
            rectangle: LegacyRectangle {
                x1: x,
                y1: y,
                x2: x + width,
                y2: y + height,
            },
        }
    }
}

impl Shape for RectangleAdapter {
    fn draw(&self) {
        self.rectangle.draw_legacy();
    }
}


// ============================================================================
// 8. COMMAND PATTERN
// ============================================================================

/// Command pattern for encapsulating actions

trait Command {
    fn execute(&mut self) -> Result<(), String>;
    fn undo(&mut self) -> Result<(), String>;
}

struct Document {
    content: String,
}

struct InsertTextCommand {
    document: Rc<RefCell<Document>>,
    text: String,
    position: usize,
}

impl Command for InsertTextCommand {
    fn execute(&mut self) -> Result<(), String> {
        let mut doc = self.document.borrow_mut();
        doc.content.insert_str(self.position, &self.text);
        println!("Inserted: '{}'", self.text);
        Ok(())
    }
    
    fn undo(&mut self) -> Result<(), String> {
        let mut doc = self.document.borrow_mut();
        let end = self.position + self.text.len();
        doc.content.replace_range(self.position..end, "");
        println!("Undid insert: '{}'", self.text);
        Ok(())
    }
}

struct CommandHistory {
    commands: Vec<Box<dyn Command>>,
    current: usize,
}

impl CommandHistory {
    fn new() -> Self {
        Self {
            commands: Vec::new(),
            current: 0,
        }
    }
    
    fn execute(&mut self, mut command: Box<dyn Command>) -> Result<(), String> {
        command.execute()?;
        self.commands.truncate(self.current);
        self.commands.push(command);
        self.current += 1;
        Ok(())
    }
    
    fn undo(&mut self) -> Result<(), String> {
        if self.current > 0 {
            self.current -= 1;
            self.commands[self.current].undo()?;
        }
        Ok(())
    }
}


// ============================================================================
// 9. STATE PATTERN
// ============================================================================

/// State pattern for state-dependent behavior
/// Rust can use enums or trait objects

// Enum-based (type-safe, preferred in Rust)
enum ConnectionState {
    Disconnected,
    Connecting,
    Connected { session_id: String },
    Error { message: String },
}

struct Connection {
    state: ConnectionState,
}

impl Connection {
    fn new() -> Self {
        Self {
            state: ConnectionState::Disconnected,
        }
    }
    
    fn connect(&mut self) -> Result<(), String> {
        match &self.state {
            ConnectionState::Disconnected => {
                println!("Connecting...");
                self.state = ConnectionState::Connecting;
                // Simulate connection
                self.state = ConnectionState::Connected {
                    session_id: "abc123".to_string(),
                };
                Ok(())
            }
            ConnectionState::Connected { .. } => {
                Err("Already connected".to_string())
            }
            _ => Err("Cannot connect from current state".to_string()),
        }
    }
    
    fn disconnect(&mut self) -> Result<(), String> {
        match &self.state {
            ConnectionState::Connected { session_id } => {
                println!("Disconnecting session: {}", session_id);
                self.state = ConnectionState::Disconnected;
                Ok(())
            }
            _ => Err("Not connected".to_string()),
        }
    }
}


// ============================================================================
// 10. VISITOR PATTERN
// ============================================================================

/// Visitor pattern for operations on object structures
/// Rust uses double dispatch with traits

trait ShapeVisitor {
    fn visit_circle(&mut self, circle: &Circle);
    fn visit_rectangle(&mut self, rectangle: &Rectangle);
}

trait Visitable {
    fn accept(&self, visitor: &mut dyn ShapeVisitor);
}

struct Circle {
    radius: f64,
}

impl Visitable for Circle {
    fn accept(&self, visitor: &mut dyn ShapeVisitor) {
        visitor.visit_circle(self);
    }
}

struct Rectangle {
    width: f64,
    height: f64,
}

impl Visitable for Rectangle {
    fn accept(&self, visitor: &mut dyn ShapeVisitor) {
        visitor.visit_rectangle(self);
    }
}

struct AreaCalculator {
    total_area: f64,
}

impl ShapeVisitor for AreaCalculator {
    fn visit_circle(&mut self, circle: &Circle) {
        self.total_area += std::f64::consts::PI * circle.radius * circle.radius;
    }
    
    fn visit_rectangle(&mut self, rectangle: &Rectangle) {
        self.total_area += rectangle.width * rectangle.height;
    }
}


// ============================================================================
// 11. NEWTYPE PATTERN (RUST-SPECIFIC)
// ============================================================================

/// Newtype pattern for type safety and trait implementation

struct UserId(u64);
struct ProductId(u64);

// Can't accidentally mix different ID types
fn get_user(id: UserId) -> String {
    format!("User {}", id.0)
}

fn get_product(id: ProductId) -> String {
    format!("Product {}", id.0)
}

// Implement traits for external types
struct Meters(f64);

impl std::ops::Add for Meters {
    type Output = Self;
    
    fn add(self, other: Self) -> Self {
        Meters(self.0 + other.0)
    }
}


// ============================================================================
// 12. TYPE STATE PATTERN (RUST-SPECIFIC)
// ============================================================================

/// Type state pattern enforces states at compile time

struct FileHandle<State> {
    path: String,
    _state: std::marker::PhantomData<State>,
}

struct Closed;
struct Open;

impl FileHandle<Closed> {
    fn new(path: impl Into<String>) -> Self {
        Self {
            path: path.into(),
            _state: std::marker::PhantomData,
        }
    }
    
    fn open(self) -> FileHandle<Open> {
        println!("Opening file: {}", self.path);
        FileHandle {
            path: self.path,
            _state: std::marker::PhantomData,
        }
    }
}

impl FileHandle<Open> {
    fn write(&self, data: &str) {
        println!("Writing to {}: {}", self.path, data);
    }
    
    fn close(self) -> FileHandle<Closed> {
        println!("Closing file: {}", self.path);
        FileHandle {
            path: self.path,
            _state: std::marker::PhantomData,
        }
    }
}


// ============================================================================
// 13. EXTENSION TRAIT PATTERN (RUST-SPECIFIC)
// ============================================================================

/// Extension trait for adding methods to existing types

trait StringExt {
    fn truncate_to(&self, max_len: usize) -> String;
}

impl StringExt for String {
    fn truncate_to(&self, max_len: usize) -> String {
        if self.len() <= max_len {
            self.clone()
        } else {
            format!("{}...", &self[..max_len])
        }
    }
}

impl StringExt for &str {
    fn truncate_to(&self, max_len: usize) -> String {
        if self.len() <= max_len {
            self.to_string()
        } else {
            format!("{}...", &self[..max_len])
        }
    }
}


// ============================================================================
// 14. RAII PATTERN (RUST-SPECIFIC)
// ============================================================================

/// Resource Acquisition Is Initialization
/// Automatic cleanup via Drop trait

struct DatabaseConnection {
    connected: bool,
}

impl DatabaseConnection {
    fn new() -> Self {
        println!("Opening database connection");
        Self { connected: true }
    }
}

impl Drop for DatabaseConnection {
    fn drop(&mut self) {
        if self.connected {
            println!("Closing database connection");
        }
    }
}


// ============================================================================
// MAIN DEMONSTRATION
// ============================================================================

fn main() {
    println!("=== RUST DESIGN PATTERNS ===\n");
    
    println!("--- Builder Pattern ---");
    let user = UserBuilder::new(1, "Alice")
        .email("alice@example.com")
        .age(30)
        .role("admin")
        .build();
    println!("{:?}", user);
    
    let request = HttpRequestBuilder::new()
        .url("https://api.example.com")
        .method("POST")
        .body("{\"key\": \"value\"}")
        .build();
    println!("{:?}", request);
    
    println!("\n--- Factory Pattern ---");
    if let Some(animal) = create_animal("dog") {
        println!("{}", animal.speak());
    }
    
    println!("\n--- Singleton Pattern ---");
    let config = Config::global();
    println!("API Key: {}", config.api_key);
    
    println!("\n--- Strategy Pattern ---");
    let compressor = Compressor::new(GzipCompression);
    let compressed = compressor.compress_file("Hello World");
    println!("Compressed: {:?}", String::from_utf8_lossy(&compressed));
    
    println!("\n--- Observer Pattern ---");
    let mut subject = Subject::new();
    subject.attach(Box::new(EmailNotifier {
        email: "user@example.com".to_string(),
    }));
    subject.attach(Box::new(SmsNotifier {
        phone: "+1234567890".to_string(),
    }));
    subject.notify("Important event occurred!");
    
    println!("\n--- Decorator Pattern ---");
    let coffee = SimpleCoffee;
    let coffee = MilkDecorator::new(coffee);
    let coffee = SugarDecorator::new(coffee);
    println!("{}: ${:.2}", coffee.description(), coffee.cost());
    
    println!("\n--- State Pattern ---");
    let mut conn = Connection::new();
    let _ = conn.connect();
    let _ = conn.disconnect();
    
    println!("\n--- Newtype Pattern ---");
    let user_id = UserId(42);
    let _product_id = ProductId(42);
    println!("{}", get_user(user_id));
    // println!("{}", get_user(product_id)); // Compile error!
    
    println!("\n--- Type State Pattern ---");
    let file = FileHandle::<Closed>::new("data.txt");
    let file = file.open();
    file.write("Hello");
    let _file = file.close();
    // file.write("World"); // Compile error!
    
    println!("\n--- Extension Trait ---");
    let long_string = "This is a very long string";
    println!("{}", long_string.truncate_to(10));
    
    println!("\n--- RAII Pattern ---");
    {
        let _db = DatabaseConnection::new();
        // Connection automatically closed when dropped
    }
    
    println!("\n=== Complete ===");
}

/// KEY TAKEAWAYS:
/// 
/// RUST-SPECIFIC PATTERNS:
/// ✓ Newtype: Type safety wrapper
/// ✓ Type State: Compile-time state enforcement
/// ✓ Extension Trait: Add methods to existing types
/// ✓ RAII: Automatic resource management
/// 
/// ADAPTED CLASSIC PATTERNS:
/// ✓ Builder: Often uses type state
/// ✓ Strategy: Natural fit with traits
/// ✓ Factory: Use enums instead of inheritance
/// ✓ State: Prefer enums over trait objects
/// 
/// ANTI-PATTERNS TO AVOID:
/// ✗ Deref polymorphism
/// ✗ Excessive cloning
/// ✗ String typing
/// ✗ Panic in library code
/// 
/// RUST ENCOURAGES:
/// - Composition over inheritance
/// - Zero-cost abstractions
/// - Compile-time guarantees
/// - Explicit error handling
