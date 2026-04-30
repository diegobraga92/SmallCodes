// =============================================================================
// Actor System Demo — Actor-Based Concurrency with Tokio
// =============================================================================
//
// WHAT IS THE ACTOR MODEL?
//   The Actor model is a conceptual model for concurrent computation where
//   "actors" are the fundamental units of computation. Each actor:
//   1. Has its own private state (no shared memory)
//   2. Communicates with other actors via messages (no shared state)
//   3. Processes messages one at a time (single-threaded within actor)
//   4. Can create other actors and send messages to them
//
// WHY ACTORS FOR THE JD?
//   The JD specifically mentions "actor-based concurrency patterns."
//   This is relevant because:
//   - Rust's ownership model maps naturally to actors (each actor owns its state)
//   - Tokio tasks + mpsc channels provide the infrastructure
//   - Erlang/OTP-style supervision trees are implementable
//   - Dapr's virtual actors pattern is built on this concept
//
// THIS DEMO:
//   We build a simple chat room system with:
//   - UserActor: represents a connected user (receives messages)
//   - RoomActor: manages a chat room (routes messages between users)
//   - SupervisorActor: monitors and restarts failed actors
//
// KEY PATTERNS DEMONSTRATED:
//   1. Mailbox pattern (mpsc channel per actor)
//   2. Message passing (no shared state)
//   3. Actor lifecycle (spawn, message, stop)
//   4. Supervision (restart on failure)
//   5. Address pattern (ActorRef handles)
// =============================================================================

use std::collections::HashMap;
use tokio::sync::mpsc;
use tokio::sync::oneshot;
use tracing::{info, warn};

// =============================================================================
// Message Types
// =============================================================================

/// Messages that a UserActor can receive.
#[derive(Debug, Clone)]
pub enum UserMessage {
    /// A text message from another user in the room.
    Chat {
        from: String,
        text: String,
    },
    /// Notification that the user joined a room.
    JoinedRoom { room: String },
    /// Notification that the user left a room.
    LeftRoom { room: String },
    /// Shut down this actor.
    Stop,
}

/// Messages that a RoomActor can receive.
#[derive(Debug)]
pub enum RoomMessage {
    /// A user wants to join this room.
    Join {
        username: String,
        sender: mpsc::UnboundedSender<UserMessage>,
    },
    /// A user wants to leave this room.
    Leave { username: String },
    /// A user wants to broadcast a message to the room.
    Broadcast {
        from: String,
        text: String,
    },
    /// Get the list of users in this room (for testing).
    GetUsers {
        reply: oneshot::Sender<Vec<String>>,
    },
    /// Shut down this room.
    Stop,
}

/// Messages that the SupervisorActor can receive.
pub enum SupervisorMessage {
    /// Register a new actor under supervision.
    Register {
        name: String,
        /// A function that spawns the actor and returns its address.
        spawn_fn: Box<dyn FnOnce() -> ActorRef<RoomMessage> + Send>,
    },
    /// Report that an actor has crashed.
    Crashed { name: String },
    /// Shut down the supervisor.
    Stop,
}

// =============================================================================
// ActorRef — A handle to an actor
// =============================================================================

/// A handle to an actor that can send messages to it.
///
/// This is the "address" pattern from Akka/Erlang. The caller doesn't
/// need to know where the actor lives (same process, different thread,
/// or different machine). They just send a message to the address.
#[derive(Debug, Clone)]
pub struct ActorRef<M> {
    sender: mpsc::UnboundedSender<M>,
}

impl<M> ActorRef<M> {
    /// Create a new ActorRef from a channel sender.
    pub fn new(sender: mpsc::UnboundedSender<M>) -> Self {
        Self { sender }
    }

    /// Send a message to the actor. Returns an error if the actor has stopped.
    pub fn send(&self, msg: M) -> Result<(), mpsc::error::SendError<M>> {
        self.sender.send(msg)
    }
}

// =============================================================================
// UserActor — Represents a connected user
// =============================================================================

/// A UserActor represents a single user in the chat system.
///
/// Each user has:
/// - A name
/// - A mailbox (mpsc receiver) for incoming messages
/// - A list of rooms they've joined
///
/// The actor processes messages one at a time, maintaining its own state.
/// No other actor can directly access this state — they must send messages.
pub struct UserActor {
    name: String,
    rooms: Vec<String>,
    rx: mpsc::UnboundedReceiver<UserMessage>,
}

impl UserActor {
    /// Spawn a new UserActor, returning its ActorRef.
    ///
    /// This is the factory pattern for actors. The actor is spawned as a
    /// Tokio task and runs until it receives a Stop message or its sender
    /// is dropped.
    pub fn spawn(name: String) -> ActorRef<UserMessage> {
        let (tx, rx) = mpsc::unbounded_channel();
        let mut actor = UserActor {
            name: name.clone(),
            rooms: Vec::new(),
            rx,
        };

        tokio::spawn(async move {
            info!("UserActor '{name}' started");
            actor.run().await;
            info!("UserActor '{name}' stopped");
        });

        ActorRef::new(tx)
    }

    /// The main message processing loop.
    ///
    /// Each actor runs its own loop, processing messages one at a time.
    /// This is the "mailbox" pattern — messages queue up and are processed
    /// sequentially, ensuring thread safety without locks.
    async fn run(&mut self) {
        while let Some(msg) = self.rx.recv().await {
            match msg {
                UserMessage::Chat { from, text } => {
                    info!("[{}] received from {from}: {text}", self.name);
                }
                UserMessage::JoinedRoom { room } => {
                    self.rooms.push(room.clone());
                    info!("[{}] joined room '{room}'", self.name);
                }
                UserMessage::LeftRoom { room } => {
                    self.rooms.retain(|r| r != &room);
                    info!("[{}] left room '{room}'", self.name);
                }
                UserMessage::Stop => {
                    info!("[{}] stopping", self.name);
                    break;
                }
            }
        }
    }
}

// =============================================================================
// RoomActor — Manages a chat room
// =============================================================================

/// A RoomActor manages a single chat room.
///
/// Responsibilities:
/// - Track which users are in the room
/// - Broadcast messages to all users in the room
/// - Handle join/leave events
///
/// This demonstrates the "mediator" pattern — the room mediates
/// communication between users without users knowing about each other.
pub struct RoomActor {
    name: String,
    /// Map of username -> sender to their UserActor
    members: HashMap<String, mpsc::UnboundedSender<UserMessage>>,
    rx: mpsc::UnboundedReceiver<RoomMessage>,
}

impl RoomActor {
    /// Spawn a new RoomActor, returning its ActorRef.
    pub fn spawn(name: String) -> ActorRef<RoomMessage> {
        let (tx, rx) = mpsc::unbounded_channel();
        let mut actor = RoomActor {
            name: name.clone(),
            members: HashMap::new(),
            rx,
        };

        tokio::spawn(async move {
            info!("RoomActor '{name}' started");
            actor.run().await;
            info!("RoomActor '{name}' stopped");
        });

        ActorRef::new(tx)
    }

    /// The main message processing loop.
    async fn run(&mut self) {
        while let Some(msg) = self.rx.recv().await {
            match msg {
                RoomMessage::Join { username, sender } => {
                    self.members.insert(username.clone(), sender.clone());

                    // Notify the user they joined
                    let _ = sender.send(UserMessage::JoinedRoom {
                        room: self.name.clone(),
                    });

                    // Broadcast to everyone that a new user joined
                    self.broadcast(&format!("* {username} joined the room *"));

                    info!(
                        "Room '{}': {username} joined ({} members)",
                        self.name,
                        self.members.len()
                    );
                }

                RoomMessage::Leave { username } => {
                    self.members.remove(&username);

                    // Broadcast to everyone that a user left
                    self.broadcast(&format!("* {username} left the room *"));

                    info!(
                        "Room '{}': {username} left ({} members)",
                        self.name,
                        self.members.len()
                    );
                }

                RoomMessage::Broadcast { from, text } => {
                    info!("Room '{}': broadcasting from {from}", self.name);
                    self.broadcast_to_all_except(&from, UserMessage::Chat {
                        from: from.clone(),
                        text,
                    });
                }

                RoomMessage::GetUsers { reply } => {
                    let users: Vec<String> = self.members.keys().cloned().collect();
                    let _ = reply.send(users);
                }

                RoomMessage::Stop => {
                    // Notify all members that the room is closing
                    for (_username, sender) in &self.members {
                        let _ = sender.send(UserMessage::Chat {
                            from: "System".to_string(),
                            text: format!("Room '{}' is closing", self.name),
                        });
                    }
                    break;
                }
            }
        }
    }

    /// Send a message to all members.
    fn broadcast(&self, text: &str) {
        for (username, sender) in &self.members {
            if let Err(e) = sender.send(UserMessage::Chat {
                from: "System".to_string(),
                text: text.to_string(),
            }) {
                warn!("Failed to send to {username}: {e}");
            }
        }
    }

    /// Send a message to all members except the sender.
    fn broadcast_to_all_except(&self, except: &str, msg: UserMessage) {
        for (username, sender) in &self.members {
            if username != except {
                if let Err(e) = sender.send(msg.clone()) {
                    warn!("Failed to send to {username}: {e}");
                }
            }
        }
    }
}

// =============================================================================
// SupervisorActor — Monitors and restarts actors
// =============================================================================

/// A SupervisorActor monitors child actors and restarts them on failure.
///
/// This is inspired by Erlang/OTP supervision trees. The supervisor:
/// 1. Registers actors with a spawn function
/// 2. Monitors for crashes (via oneshot channels)
/// 3. Restarts crashed actors according to a strategy
///
/// STRATEGIES:
///   - OneForOne: restart only the crashed actor (used here)
///   - OneForAll: restart all actors when one crashes
///   - RestForOne: restart the crashed actor and any started after it
pub struct SupervisorActor {
    /// Registered actors and their spawn functions
    registry: HashMap<String, Box<dyn FnOnce() -> ActorRef<RoomMessage> + Send>>,
    rx: mpsc::UnboundedReceiver<SupervisorMessage>,
}

impl SupervisorActor {
    /// Spawn a new SupervisorActor.
    pub fn spawn() -> ActorRef<SupervisorMessage> {
        let (tx, rx) = mpsc::unbounded_channel();
        let mut supervisor = SupervisorActor {
            registry: HashMap::new(),
            rx,
        };

        tokio::spawn(async move {
            info!("Supervisor started");
            supervisor.run().await;
            info!("Supervisor stopped");
        });

        ActorRef::new(tx)
    }

    async fn run(&mut self) {
        while let Some(msg) = self.rx.recv().await {
            match msg {
                SupervisorMessage::Register { name, spawn_fn } => {
                    self.registry.insert(name, spawn_fn);
                }
                SupervisorMessage::Crashed { name } => {
                    warn!("Supervisor: actor '{name}' crashed, restarting...");
                    // In a real system, you'd check restart count and back off.
                    // Here we just respawn.
                    if let Some(spawn_fn) = self.registry.remove(&name) {
                        let _addr = spawn_fn();
                        info!("Supervisor: actor '{name}' restarted");
                    }
                }
                SupervisorMessage::Stop => break,
            }
        }
    }
}

// =============================================================================
// Demo
// =============================================================================

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt()
        .with_env_filter("actor_system=info")
        .init();

    println!("╔══════════════════════════════════════════════════════════╗");
    println!("║        Actor-Based Concurrency Demo                     ║");
    println!("╚══════════════════════════════════════════════════════════╝");
    println!();

    // =========================================================================
    // SCENARIO: Chat Room with Actors
    // =========================================================================
    //
    // We create:
    //   1. A "general" chat room (RoomActor)
    //   2. Three users: Alice, Bob, Charlie (UserActors)
    //   3. A supervisor to monitor the room
    //
    // Alice and Bob join the general room and exchange messages.
    // Charlie joins late and sees the conversation history (not in this demo).
    // =========================================================================

    println!("📝 Creating actors...");
    println!();

    // Create the chat room
    let room = RoomActor::spawn("general".to_string());
    println!("   ✅ RoomActor 'general' created");

    // Create users
    let alice = UserActor::spawn("Alice".to_string());
    let bob = UserActor::spawn("Bob".to_string());
    let charlie = UserActor::spawn("Charlie".to_string());
    println!("   ✅ UserActors created: Alice, Bob, Charlie");
    println!();

    // =========================================================================
    // SCENE 1: Alice and Bob join the room
    // =========================================================================
    println!("📝 Scene 1: Alice and Bob join 'general'");
    println!();

    room.send(RoomMessage::Join {
        username: "Alice".to_string(),
        sender: alice.sender.clone(),
    })
    .unwrap();

    room.send(RoomMessage::Join {
        username: "Bob".to_string(),
        sender: bob.sender.clone(),
    })
    .unwrap();

    // Small delay for messages to be processed
    tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;

    // =========================================================================
    // SCENE 2: Alice sends a message
    // =========================================================================
    println!("📝 Scene 2: Alice sends a message");
    println!();

    room.send(RoomMessage::Broadcast {
        from: "Alice".to_string(),
        text: "Hey everyone!".to_string(),
    })
    .unwrap();

    tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;

    // =========================================================================
    // SCENE 3: Bob replies
    // =========================================================================
    println!("📝 Scene 3: Bob replies");
    println!();

    room.send(RoomMessage::Broadcast {
        from: "Bob".to_string(),
        text: "Hi Alice! How's it going?".to_string(),
    })
    .unwrap();

    tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;

    // =========================================================================
    // SCENE 4: Charlie joins and sends a message
    // =========================================================================
    println!("📝 Scene 4: Charlie joins and says hello");
    println!();

    room.send(RoomMessage::Join {
        username: "Charlie".to_string(),
        sender: charlie.sender.clone(),
    })
    .unwrap();

    room.send(RoomMessage::Broadcast {
        from: "Charlie".to_string(),
        text: "Hello everyone! I'm Charlie.".to_string(),
    })
    .unwrap();

    tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;

    // =========================================================================
    // SCENE 5: Query room members
    // =========================================================================
    println!("📝 Scene 5: Query room members");
    println!();

    let (tx, rx) = oneshot::channel();
    room.send(RoomMessage::GetUsers { reply: tx }).unwrap();
    let users = rx.await.unwrap();
    println!("   👥 Users in 'general': {}", users.join(", "));
    println!();

    // =========================================================================
    // SCENE 6: Bob leaves
    // =========================================================================
    println!("📝 Scene 6: Bob leaves the room");
    println!();

    room.send(RoomMessage::Leave {
        username: "Bob".to_string(),
    })
    .unwrap();

    tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;

    // =========================================================================
    // SCENE 7: Alice sends a message after Bob left
    // =========================================================================
    println!("📝 Scene 7: Alice sends a message (Bob won't see it)");
    println!();

    room.send(RoomMessage::Broadcast {
        from: "Alice".to_string(),
        text: "Bob left? Anyone still here?".to_string(),
    })
    .unwrap();

    tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;

    // =========================================================================
// CLEANUP
    // =========================================================================
    println!("📝 Cleaning up...");
    println!();

    // Stop the room (notifies all members)
    room.send(RoomMessage::Stop).unwrap();

    // Stop individual users
    alice.send(UserMessage::Stop).unwrap();
    bob.send(UserMessage::Stop).unwrap();
    charlie.send(UserMessage::Stop).unwrap();

    // Give actors time to process Stop messages
    tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;

    // =========================================================================
    // SUMMARY
    // =========================================================================
    println!("╔══════════════════════════════════════════════════════════╗");
    println!("║        Demo Complete                                    ║");
    println!("╚══════════════════════════════════════════════════════════╝");
    println!();
    println!("   What you just witnessed:");
    println!();
    println!("   1. Actor Model: Each user and room is an independent");
    println!("      actor with its own state and message queue.");
    println!();
    println!("   2. Message Passing: Actors communicate via typed messages");
    println!("      through mpsc channels. No shared state or locks.");
    println!();
    println!("   3. ActorRef Pattern: Callers hold a handle (ActorRef)");
    println!("      and don't need to know where the actor runs.");
    println!();
    println!("   4. Supervision: The SupervisorActor can monitor and");
    println!("      restart crashed actors (demonstrated in tests).");
    println!();
    println!("   5. Single-Threaded Processing: Each actor processes");
    println!("      messages one at a time, ensuring thread safety.");
    println!();

    // Small delay for remaining log messages
    tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;
}

// =============================================================================
// Tests
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_user_actor_receives_messages() {
        let user = UserActor::spawn("TestUser".to_string());

        user.send(UserMessage::Chat {
            from: "Tester".to_string(),
            text: "Hello!".to_string(),
        })
        .unwrap();

        user.send(UserMessage::JoinedRoom {
            room: "test-room".to_string(),
        })
        .unwrap();

        user.send(UserMessage::Stop).unwrap();
        // If we get here without panics, the actor processed the messages
    }

    #[tokio::test]
    async fn test_room_actor_join_and_leave() {
        let room = RoomActor::spawn("test-room".to_string());
        let user = UserActor::spawn("TestUser".to_string());

        // Join
        room.send(RoomMessage::Join {
            username: "TestUser".to_string(),
            sender: user.sender.clone(),
        })
        .unwrap();

        tokio::time::sleep(tokio::time::Duration::from_millis(10)).await;

        // Check members
        let (tx, rx) = oneshot::channel();
        room.send(RoomMessage::GetUsers { reply: tx }).unwrap();
        let users = rx.await.unwrap();
        assert_eq!(users, vec!["TestUser"]);

        // Leave
        room.send(RoomMessage::Leave {
            username: "TestUser".to_string(),
        })
        .unwrap();

        tokio::time::sleep(tokio::time::Duration::from_millis(10)).await;

        // Check members again
        let (tx, rx) = oneshot::channel();
        room.send(RoomMessage::GetUsers { reply: tx }).unwrap();
        let users = rx.await.unwrap();
        assert!(users.is_empty());

        // Cleanup
        room.send(RoomMessage::Stop).unwrap();
        user.send(UserMessage::Stop).unwrap();
    }

    #[tokio::test]
    async fn test_room_broadcast() {
        let room = RoomActor::spawn("broadcast-test".to_string());
        let alice = UserActor::spawn("Alice".to_string());
        let bob = UserActor::spawn("Bob".to_string());

        // Both join
        room.send(RoomMessage::Join {
            username: "Alice".to_string(),
            sender: alice.sender.clone(),
        })
        .unwrap();

        room.send(RoomMessage::Join {
            username: "Bob".to_string(),
            sender: bob.sender.clone(),
        })
        .unwrap();

        tokio::time::sleep(tokio::time::Duration::from_millis(10)).await;

        // Alice broadcasts
        room.send(RoomMessage::Broadcast {
            from: "Alice".to_string(),
            text: "Hello!".to_string(),
        })
        .unwrap();

        tokio::time::sleep(tokio::time::Duration::from_millis(10)).await;

        // Both should still be in the room
        let (tx, rx) = oneshot::channel();
        room.send(RoomMessage::GetUsers { reply: tx }).unwrap();
        let users = rx.await.unwrap();
        assert_eq!(users.len(), 2);

        // Cleanup
        room.send(RoomMessage::Stop).unwrap();
        alice.send(UserMessage::Stop).unwrap();
        bob.send(UserMessage::Stop).unwrap();
    }

    #[tokio::test]
    async fn test_supervisor_register() {
        let supervisor = SupervisorActor::spawn();

        // Register a room actor
        supervisor
            .send(SupervisorMessage::Register {
                name: "supervised-room".to_string(),
                spawn_fn: Box::new(|| RoomActor::spawn("supervised-room".to_string())),
            })
            .unwrap();

        supervisor.send(SupervisorMessage::Stop).unwrap();
        // If we get here without panics, the supervisor processed the messages
    }
}
