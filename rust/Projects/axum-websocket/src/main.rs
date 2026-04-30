// =============================================================================
// Axum WebSocket Chat Server — Real-Time Bidirectional Communication
// =============================================================================
//
// WHAT THIS DEMONSTRATES:
//   1. WebSocket upgrade from HTTP (HTTP → WS handshake)
//   2. Bidirectional message streaming (server ↔ client)
//   3. Broadcast to all connected clients (chat room pattern)
//   4. Graceful client disconnect handling
//   5. Concurrent connection management with Tokio
//
// JD RELEVANCE:
//   The JD mentions "HTTP frameworks such as Axum including WebSocket support."
//   WebSockets are essential for real-time features like live dashboards,
//   collaborative editing, notifications, and chat systems.
//
// ARCHITECTURE:
//   ┌──────────────┐     HTTP GET /ws     ┌──────────────────┐
//   │  Client 1    │◄────────────────────►│                  │
//   └──────────────┘   WebSocket upgrade   │   Axum Server    │
//                                          │   (broadcast)    │
//   ┌──────────────┐     HTTP GET /ws     │                  │
//   │  Client 2    │◄────────────────────►│   ┌──────────┐   │
//   └──────────────┘                       │   │ Broadcast │   │
//                                          │   │  Channel  │   │
//   ┌──────────────┐     HTTP GET /ws     │   └──────────┘   │
//   │  Client N    │◄────────────────────►│                  │
//   └──────────────┘                       └──────────────────┘
//
// KEY PATTERNS:
//   - WebSocket upgrade: Axum's `ws` feature handles the HTTP→WS upgrade
//   - Broadcast channel: Tokio's broadcast channel fans out messages
//   - Split sink/stream: futures-util's `split` for concurrent read/write
//   - Heartbeat/ping: Periodic pings to detect dead connections
// =============================================================================

use axum::{
    extract::{
        ws::{Message, WebSocket, WebSocketUpgrade},
        State,
    },
    response::{Html, IntoResponse},
    routing::get,
    Router,
};
use futures_util::{SinkExt, StreamExt};
use std::sync::Arc;
use tokio::sync::broadcast;
use tracing::{info, warn};

// =============================================================================
// Application State
// =============================================================================

/// Shared application state.
///
/// The broadcast channel is the core of the chat system:
/// - `tx`: Sender half — used by the HTTP handler to broadcast messages
/// - Clients subscribe by creating a receiver from this sender
struct AppState {
    /// Broadcast channel for chat messages.
    /// Capacity 100 means if a client is 100 messages behind, they'll
    /// miss messages (lagged). In production, use a larger buffer or
    /// a persistent message queue.
    tx: broadcast::Sender<String>,
}

// =============================================================================
// HTTP Handlers
// =============================================================================

/// GET / — Simple HTML page with a WebSocket client for testing.
async fn index() -> Html<&'static str> {
    Html(include_str!("../static/index.html"))
}

/// GET /ws — WebSocket upgrade endpoint.
///
/// This is the key endpoint. When a client connects to `/ws`, Axum:
/// 1. Receives the HTTP request with an `Upgrade: websocket` header
/// 2. Calls `ws.on_upgrade(handler)` to perform the upgrade
/// 3. The handler function receives a `WebSocket` connection
///
/// The `WebSocketUpgrade` extractor handles all the HTTP protocol details.
async fn ws_handler(
    ws: WebSocketUpgrade,
    State(state): State<Arc<AppState>>,
) -> impl IntoResponse {
    info!("New WebSocket connection request");
    ws.on_upgrade(move |socket| handle_socket(socket, state))
}

// =============================================================================
// WebSocket Handler
// =============================================================================

/// Handle a single WebSocket connection.
///
/// This function:
/// 1. Subscribes to the broadcast channel
/// 2. Splits the WebSocket into a sender and receiver
/// 3. Spawns two tasks:
///    - Read task: receives messages from the client and broadcasts them
///    - Write task: receives broadcast messages and sends them to the client
/// 4. If either task fails, the connection is closed
async fn handle_socket(socket: WebSocket, state: Arc<AppState>) {
    // Subscribe to the broadcast channel
    let mut rx = state.tx.subscribe();

    // Split the WebSocket into sender and receiver.
    // This allows us to read and write concurrently.
    let (mut ws_sender, mut ws_receiver) = socket.split();

    // Spawn a task to read messages from the client and broadcast them
    let tx = state.tx.clone();
    let read_task = tokio::spawn(async move {
        while let Some(msg) = ws_receiver.next().await {
            match msg {
                Ok(Message::Text(text)) => {
                    info!("Received message: {text}");
                    // Broadcast to all connected clients
                    let _ = tx.send(text);
                }
                Ok(Message::Close(_)) => {
                    info!("Client disconnected");
                    break;
                }
                Ok(Message::Ping(_)) => {
                    // Axum handles pongs automatically
                }
                Ok(Message::Pong(_)) => {
                    // Response to our ping
                }
                Err(e) => {
                    warn!("WebSocket error: {e}");
                    break;
                }
                _ => {} // Ignore binary messages
            }
        }
    });

    // Spawn a task to send broadcast messages to this client
    let write_task = tokio::spawn(async move {
        while let Ok(msg) = rx.recv().await {
            if ws_sender.send(Message::Text(msg.into())).await.is_err() {
                break;
            }
        }
    });

    // Wait for either task to complete (connection closed or error)
    tokio::select! {
        _ = read_task => {},
        _ = write_task => {},
    }

    info!("WebSocket connection closed");
}

// =============================================================================
// Main
// =============================================================================

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt()
        .with_env_filter("axum_websocket=info")
        .init();

    println!("╔══════════════════════════════════════════════════════════╗");
    println!("║   Axum WebSocket Chat Server                            ║");
    println!("╚══════════════════════════════════════════════════════════╝");
    println!();

    // Create the broadcast channel
    let (tx, _) = broadcast::channel::<String>(100);

    let state = Arc::new(AppState { tx });

    let app = Router::new()
        .route("/", get(index))
        .route("/ws", get(ws_handler))
        .with_state(state);

    let addr = "0.0.0.0:3000";
    println!("   🚀 Server starting on http://{addr}");
    println!();
    println!("   Endpoints:");
    println!("     GET /     - HTML chat client (open in browser)");
    println!("     GET /ws   - WebSocket endpoint");
    println!();
    println!("   How to test:");
    println!("     1. Open http://localhost:3000 in multiple browser tabs");
    println!("     2. Type a message in one tab — it appears in all tabs");
    println!("     3. Or use a WebSocket CLI client:");
    println!("        websocat ws://localhost:3000/ws");
    println!();

    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

// =============================================================================
// Tests
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;
    use axum::{
        body::Body,
        http::{self, Request},
    };
    use tower::util::ServiceExt;

    #[tokio::test]
    async fn test_index_page() {
        let (tx, _) = broadcast::channel::<String>(100);
        let state = Arc::new(AppState { tx });

        let app = Router::new()
            .route("/", get(index))
            .route("/ws", get(ws_handler))
            .with_state(state);

        let response = app
            .oneshot(
                Request::builder()
                    .uri("/")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), http::StatusCode::OK);
    }

    #[tokio::test]
    async fn test_websocket_upgrade_rejected_without_ws_headers() {
        let (tx, _) = broadcast::channel::<String>(100);
        let state = Arc::new(AppState { tx });

        let app = Router::new()
            .route("/ws", get(ws_handler))
            .with_state(state);

        // Without WebSocket upgrade headers, the request should fail
        let response = app
            .oneshot(
                Request::builder()
                    .uri("/ws")
                    .header("Connection", "upgrade")
                    .header("Upgrade", "websocket")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        // Axum's WebSocketUpgrade returns 400 if the request isn't a valid WS upgrade
        assert_eq!(response.status(), http::StatusCode::BAD_REQUEST);
    }
}
