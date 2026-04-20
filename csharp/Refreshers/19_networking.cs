/*
    C# NETWORKING
    File: 19_networking.cs
    
    Comprehensive guide to network programming in C#.
    Covers HTTP clients, TCP/UDP sockets, WebSocket, gRPC,
    network protocols, async patterns, error handling, and best practices.
*/

using System;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Net.Sockets;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Security.Cryptography.X509Certificates;
using System.Linq;

namespace CSharpRefresher.Networking
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Networking ===\n");
            
            DemonstrateHttpClients();
            DemonstrateTcpSockets();
            DemonstrateUdpSockets();
            DemonstrateWebSockets();
            DemonstrateGrpcAndProtocols();
            DemonstrateNetworkUtilities();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstrateHttpClients()
        {
            Console.WriteLine("=== 1. HTTP Clients ===\n");
            
            // 1. HttpClient (modern, recommended)
            Console.WriteLine("1. HttpClient (Modern):");
            
            // Create HttpClient with custom handler
            using (var handler = new HttpClientHandler())
            {
                // Configure handler
                handler.UseCookies = true;
                handler.AllowAutoRedirect = true;
                handler.MaxAutomaticRedirections = 5;
                
                using (var client = new HttpClient(handler))
                {
                    // Configure client
                    client.Timeout = TimeSpan.FromSeconds(30);
                    client.DefaultRequestHeaders.Add("User-Agent", "CSharpRefresher/1.0");
                    
                    // GET request
                    async Task GetExample()
                    {
                        try
                        {
                            HttpResponseMessage response = await client.GetAsync("https://httpbin.org/get");
                            response.EnsureSuccessStatusCode();
                            string content = await response.Content.ReadAsStringAsync();
                            Console.WriteLine($"GET response: {content.Substring(0, Math.Min(100, content.Length))}...");
                            Console.WriteLine($"Status: {response.StatusCode}, Headers: {response.Headers.Count}");
                        }
                        catch (HttpRequestException ex)
                        {
                            Console.WriteLine($"HTTP error: {ex.Message}");
                        }
                    }
                    GetExample().Wait();
                    
                    // POST request with JSON
                    async Task PostExample()
                    {
                        var data = new { Name = "Test", Value = 42 };
                        string json = System.Text.Json.JsonSerializer.Serialize(data);
                        var content = new StringContent(json, Encoding.UTF8, "application/json");
                        
                        HttpResponseMessage response = await client.PostAsync("https://httpbin.org/post", content);
                        response.EnsureSuccessStatusCode();
                        Console.WriteLine($"POST completed: {response.StatusCode}");
                    }
                    PostExample().Wait();
                    
                    // PUT and DELETE
                    async Task PutDeleteExample()
                    {
                        var putContent = new StringContent("{\"key\":\"value\"}", Encoding.UTF8, "application/json");
                        var putResponse = await client.PutAsync("https://httpbin.org/put", putContent);
                        Console.WriteLine($"PUT: {putResponse.StatusCode}");
                        
                        var deleteResponse = await client.DeleteAsync("https://httpbin.org/delete");
                        Console.WriteLine($"DELETE: {deleteResponse.StatusCode}");
                    }
                    PutDeleteExample().Wait();
                    
                    // Send custom request
                    async Task CustomRequest()
                    {
                        var request = new HttpRequestMessage(HttpMethod.Head, "https://httpbin.org/headers");
                        var response = await client.SendAsync(request);
                        Console.WriteLine($"HEAD: {response.StatusCode}, Content length: {response.Content.Headers.ContentLength}");
                    }
                    CustomRequest().Wait();
                }
            }
            
            // 2. HttpClient with dependency injection
            Console.WriteLine("\n2. HttpClient with Dependency Injection:");
            Console.WriteLine("""
                In ASP.NET Core, register HttpClient:
                
                services.AddHttpClient("NamedClient", client =>
                {
                    client.BaseAddress = new Uri("https://api.example.com");
                    client.DefaultRequestHeaders.Add("Accept", "application/json");
                });
                
                Then inject IHttpClientFactory.
                """);
            
            // 3. HttpClientFactory patterns
            Console.WriteLine("\n3. HttpClientFactory Patterns:");
            Console.WriteLine("""
                Benefits over new HttpClient():
                • Connection pooling
                • DNS refresh
                • Circuit breaker integration
                • Configuration management
                • Lifecycle management
                
                Patterns:
                • Named clients
                • Typed clients
                • Generated clients (Refit, NSwag)
                """);
            
            // 4. Advanced HTTP features
            Console.WriteLine("\n4. Advanced HTTP Features:");
            
            // Compression
            async Task CompressionExample()
            {
                using (var client = new HttpClient())
                {
                    client.DefaultRequestHeaders.AcceptEncoding.Add(new System.Net.Http.Headers.StringWithQualityHeaderValue("gzip"));
                    client.DefaultRequestHeaders.AcceptEncoding.Add(new System.Net.Http.Headers.StringWithQualityHeaderValue("deflate"));
                    
                    var response = await client.GetAsync("https://httpbin.org/gzip");
                    Console.WriteLine($"Compressed response: {response.Content.Headers.ContentEncoding}");
                }
            }
            CompressionExample().Wait();
            
            // Timeouts and cancellation
            async Task TimeoutExample()
            {
                using (var cts = new CancellationTokenSource(TimeSpan.FromSeconds(2)))
                using (var client = new HttpClient() { Timeout = Timeout.InfiniteTimeSpan })
                {
                    try
                    {
                        var response = await client.GetAsync("https://httpbin.org/delay/5", cts.Token);
                    }
                    catch (TaskCanceledException)
                    {
                        Console.WriteLine("Request cancelled due to timeout");
                    }
                }
            }
            TimeoutExample().Wait();
            
            // 5. HTTP/2 and HTTP/3
            Console.WriteLine("\n5. HTTP/2 and HTTP/3:");
            Console.WriteLine("""
                HTTP/2 (default in .NET Core 3.0+):
                • Multiplexing
                • Header compression
                • Server push
                
                HTTP/3 (QUIC) in .NET 5+:
                • UDP-based
                • Built-in encryption
                • Faster connection establishment
                
                Enable in HttpClient:
                var client = new HttpClient()
                {
                    DefaultRequestVersion = HttpVersion.Version20,
                    DefaultVersionPolicy = HttpVersionPolicy.RequestVersionOrHigher
                };
                """);
            
            // 6. Polly for resilience
            Console.WriteLine("\n6. Polly for Resilience:");
            Console.WriteLine("""
                Common patterns:
                • Retry with exponential backoff
                • Circuit breaker
                • Timeout policy
                • Bulkhead isolation
                • Fallback strategies
                
                Example with HttpClientFactory:
                services.AddHttpClient("ResilientClient")
                    .AddTransientHttpErrorPolicy(policy => 
                        policy.WaitAndRetryAsync(3, retryAttempt => 
                            TimeSpan.FromSeconds(Math.Pow(2, retryAttempt))));
                """);
        }
        
        static void DemonstrateTcpSockets()
        {
            Console.WriteLine("\n=== 2. TCP Sockets ===\n");
            
            // 1. TCP Client
            Console.WriteLine("1. TCP Client:");
            
            async Task TcpClientExample()
            {
                using (var client = new TcpClient())
                {
                    // Connect with timeout
                    var connectTask = client.ConnectAsync("httpbin.org", 80);
                    var timeoutTask = Task.Delay(TimeSpan.FromSeconds(5));
                    
                    if (await Task.WhenAny(connectTask, timeoutTask) == timeoutTask)
                    {
                        Console.WriteLine("Connection timeout");
                        return;
                    }
                    
                    Console.WriteLine($"Connected: {client.Connected}, Local: {client.Client.LocalEndPoint}, Remote: {client.Client.RemoteEndPoint}");
                    
                    // Get stream
                    using (var stream = client.GetStream())
                    using (var writer = new StreamWriter(stream, Encoding.ASCII) { AutoFlush = true })
                    using (var reader = new StreamReader(stream, Encoding.ASCII))
                    {
                        // Send HTTP request
                        await writer.WriteLineAsync("GET / HTTP/1.1");
                        await writer.WriteLineAsync("Host: httpbin.org");
                        await writer.WriteLineAsync("Connection: close");
                        await writer.WriteLineAsync();
                        
                        // Read response
                        string response = await reader.ReadToEndAsync();
                        Console.WriteLine($"TCP response (first 200 chars):\n{response.Substring(0, Math.Min(200, response.Length))}...");
                    }
                }
            }
            TcpClientExample().Wait();
            
            // 2. TCP Listener (server)
            Console.WriteLine("\n2. TCP Listener (Server):");
            
            async Task TcpServerExample()
            {
                var listener = new TcpListener(IPAddress.Loopback, 0); // Random port
                listener.Start();
                int port = ((IPEndPoint)listener.LocalEndpoint).Port;
                
                Console.WriteLine($"Server listening on port {port}");
                
                // Start accepting in background
                var acceptTask = listener.AcceptTcpClientAsync();
                
                // Connect client in parallel
                async Task ConnectClient()
                {
                    using (var client = new TcpClient())
                    {
                        await client.ConnectAsync(IPAddress.Loopback, port);
                        using (var stream = client.GetStream())
                        using (var writer = new StreamWriter(stream) { AutoFlush = true })
                        {
                            await writer.WriteLineAsync("Hello Server!");
                        }
                    }
                }
                
                var clientTask = ConnectClient();
                var serverClient = await acceptTask;
                
                using (serverClient)
                using (var stream = serverClient.GetStream())
                using (var reader = new StreamReader(stream))
                {
                    string message = await reader.ReadLineAsync();
                    Console.WriteLine($"Server received: {message}");
                    
                    // Send response
                    using (var writer = new StreamWriter(stream) { AutoFlush = true })
                    {
                        await writer.WriteLineAsync("Hello Client!");
                    }
                }
                
                await clientTask;
                listener.Stop();
            }
            TcpServerExample().Wait();
            
            // 3. Async socket operations
            Console.WriteLine("\n3. Async Socket Operations:");
            
            async Task AsyncSocketExample()
            {
                var socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                
                try
                {
                    // Async connect
                    await socket.ConnectAsync("httpbin.org", 80);
                    
                    // Send data
                    string request = "GET / HTTP/1.1\r\nHost: httpbin.org\r\nConnection: close\r\n\r\n";
                    byte[] requestBytes = Encoding.ASCII.GetBytes(request);
                    await socket.SendAsync(requestBytes, SocketFlags.None);
                    
                    // Receive data with buffer
                    byte[] buffer = new byte[4096];
                    var response = new StringBuilder();
                    
                    while (true)
                    {
                        int bytesReceived = await socket.ReceiveAsync(buffer, SocketFlags.None);
                        if (bytesReceived == 0) break;
                        response.Append(Encoding.ASCII.GetString(buffer, 0, bytesReceived));
                    }
                    
                    Console.WriteLine($"Async socket response length: {response.Length}");
                }
                finally
                {
                    socket.Close();
                }
            }
            AsyncSocketExample().Wait();
            
            // 4. Socket options and configuration
            Console.WriteLine("\n4. Socket Options:");
            
            var socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
            socket.SetSocketOption(SocketOptionLevel.Tcp, SocketOptionName.NoDelay, true); // Disable Nagle's algorithm
            socket.ReceiveTimeout = 5000;
            socket.SendTimeout = 5000;
            socket.ReceiveBufferSize = 8192;
            socket.SendBufferSize = 8192;
            socket.LingerState = new LingerOption(true, 5); // Wait 5 seconds on close
            
            Console.WriteLine("""
                Common socket options:
                • NoDelay: Disable Nagle's algorithm (reduce latency)
                • ReuseAddress: Allow address reuse
                • Receive/Send timeout: Operation timeouts
                • Receive/Send buffer size: Performance tuning
                • Linger: Control socket close behavior
                • KeepAlive: Maintain connection
                """);
            
            // 5. NetworkStream
            Console.WriteLine("\n5. NetworkStream:");
            Console.WriteLine("""
                NetworkStream wraps socket for stream operations:
                
                using (var client = new TcpClient())
                {
                    await client.ConnectAsync(host, port);
                    using (var stream = client.GetStream())
                    {
                        // Stream operations (Read/Write, async versions)
                        // Can wrap with StreamReader/StreamWriter for text
                        // Or BinaryReader/BinaryWriter for binary data
                    }
                }
                
                Features:
                • Read/Write timeouts
                • DataAvailable property
                • CanRead/CanWrite/CanSeek properties
                """);
            
            // 6. Socket performance
            Console.WriteLine("\n6. Socket Performance Tips:");
            Console.WriteLine("""
                • Use async/await for scalability
                • Consider SocketAsyncEventArgs for high-performance scenarios
                • Buffer management (pool buffers)
                • Set appropriate buffer sizes
                • Use NoDelay for low-latency applications
                • Monitor connections and dispose properly
                """);
        }
        
        static void DemonstrateUdpSockets()
        {
            Console.WriteLine("\n=== 3. UDP Sockets ===\n");
            
            // 1. UDP Client
            Console.WriteLine("1. UDP Client:");
            
            async Task UdpClientExample()
            {
                using (var client = new UdpClient())
                {
                    // Connect to DNS server for query
                    await client.ConnectAsync("8.8.8.8", 53);
                    
                    // Send DNS query (simplified)
                    byte[] dnsQuery = CreateDnsQuery("example.com");
                    await client.SendAsync(dnsQuery, dnsQuery.Length);
                    
                    // Receive response with timeout
                    var receiveTask = client.ReceiveAsync();
                    var timeoutTask = Task.Delay(TimeSpan.FromSeconds(2));
                    
                    if (await Task.WhenAny(receiveTask, timeoutTask) == receiveTask)
                    {
                        UdpReceiveResult result = receiveTask.Result;
                        Console.WriteLine($"UDP received {result.Buffer.Length} bytes from {result.RemoteEndPoint}");
                    }
                    else
                    {
                        Console.WriteLine("UDP receive timeout");
                    }
                }
            }
            
            // Helper for DNS query
            byte[] CreateDnsQuery(string domain)
            {
                // Simplified DNS query (just for demonstration)
                var query = new byte[512];
                query[0] = 0xAA; // Transaction ID
                query[1] = 0xAA;
                query[2] = 0x01; // Flags: standard query
                query[3] = 0x00;
                query[4] = 0x00; // Questions: 1
                query[5] = 0x01;
                // ... domain encoding would go here
                return query;
            }
            
            UdpClientExample().Wait();
            
            // 2. UDP Server (listener)
            Console.WriteLine("\n2. UDP Server:");
            
            async Task UdpServerExample()
            {
                using (var server = new UdpClient(12345)) // Listen on port 12345
                {
                    Console.WriteLine($"UDP server listening on port {((IPEndPoint)server.Client.LocalEndPoint).Port}");
                    
                    // Receive in background
                    var receiveTask = server.ReceiveAsync();
                    
                    // Send test message
                    using (var client = new UdpClient())
                    {
                        byte[] message = Encoding.ASCII.GetBytes("Hello UDP Server!");
                        await client.SendAsync(message, message.Length, "127.0.0.1", 12345);
                    }
                    
                    // Receive the message
                    UdpReceiveResult result = await receiveTask;
                    string received = Encoding.ASCII.GetString(result.Buffer);
                    Console.WriteLine($"Server received: {received} from {result.RemoteEndPoint}");
                    
                    // Send response
                    byte[] response = Encoding.ASCII.GetBytes("Hello UDP Client!");
                    await server.SendAsync(response, response.Length, result.RemoteEndPoint);
                }
            }
            UdpServerExample().Wait();
            
            // 3. UDP multicast
            Console.WriteLine("\n3. UDP Multicast:");
            
            async Task MulticastExample()
            {
                // Join multicast group
                using (var client = new UdpClient(12346))
                {
                    client.JoinMulticastGroup(IPAddress.Parse("224.0.0.1"));
                    
                    // Send multicast message
                    byte[] message = Encoding.ASCII.GetBytes("Multicast test");
                    await client.SendAsync(message, message.Length, "224.0.0.1", 12346);
                    
                    // Receive multicast (with timeout)
                    var cts = new CancellationTokenSource(TimeSpan.FromSeconds(1));
                    try
                    {
                        var result = await client.ReceiveAsync().WithCancellation(cts.Token);
                        Console.WriteLine($"Multicast received: {Encoding.ASCII.GetString(result.Buffer)}");
                    }
                    catch (OperationCanceledException)
                    {
                        Console.WriteLine("Multicast receive timeout");
                    }
                    
                    client.DropMulticastGroup(IPAddress.Parse("224.0.0.1"));
                }
            }
            
            // Extension method for cancellation
            public static async Task<T> WithCancellation<T>(this Task<T> task, CancellationToken cancellationToken)
            {
                var tcs = new TaskCompletionSource<bool>();
                using (cancellationToken.Register(s => ((TaskCompletionSource<bool>)s).TrySetResult(true), tcs))
                {
                    if (task != await Task.WhenAny(task, tcs.Task))
                        throw new OperationCanceledException(cancellationToken);
                }
                return await task;
            }
            
            MulticastExample().Wait();
            
            // 4. UDP broadcast
            Console.WriteLine("\n4. UDP Broadcast:");
            
            async Task BroadcastExample()
            {
                using (var client = new UdpClient())
                {
                    client.EnableBroadcast = true;
                    
                    byte[] message = Encoding.ASCII.GetBytes("Broadcast message");
                    await client.SendAsync(message, message.Length, "255.255.255.255", 12345);
                    Console.WriteLine("Broadcast sent");
                }
            }
            BroadcastExample().Wait();
            
            // 5. UDP vs TCP considerations
            Console.WriteLine("\n5. UDP vs TCP Considerations:");
            Console.WriteLine("""
                UDP Characteristics:
                • Connectionless
                • No guarantees (no ACK, no retransmission)
                • No ordering guarantees
                • Lower overhead
                • Can broadcast/multicast
                
                Use cases:
                • DNS queries
                • VoIP/Video streaming
                • Game networking
                • Service discovery
                • IoT sensor data
                
                TCP Characteristics:
                • Connection-oriented
                • Reliable, ordered delivery
                • Flow control
                • Congestion control
                • Higher overhead
                
                Implement on UDP if needed:
                • Reliability (acknowledgments, retransmission)
                • Ordering (sequence numbers)
                • Congestion control
                """);
            
            // 6. Real-time protocols
            Console.WriteLine("\n6. Real-time Protocols:");
            Console.WriteLine("""
                Common UDP-based protocols:
                • DNS (Domain Name System)
                • DHCP (Dynamic Host Configuration)
                • SNMP (Simple Network Management)
                • RTP/RTCP (Real-time Transport)
                • QUIC (HTTP/3 transport)
                • Custom game protocols
                
                Considerations:
                • Packet loss handling
                • Jitter buffering
                • Latency requirements
                • Bandwidth usage
                """);
        }
        
        static void DemonstrateWebSockets()
        {
            Console.WriteLine("\n=== 4. WebSockets ===\n");
            
            // 1. WebSocket client
            Console.WriteLine("1. WebSocket Client:");
            
            async Task WebSocketClientExample()
            {
                using (var client = new ClientWebSocket())
                {
                    // Configure options
                    client.Options.KeepAliveInterval = TimeSpan.FromSeconds(30);
                    client.Options.SetRequestHeader("User-Agent", "CSharpRefresher");
                    
                    // Connect
                    await client.ConnectAsync(new Uri("wss://echo.websocket.events"), CancellationToken.None);
                    Console.WriteLine($"WebSocket connected: {client.State}");
                    
                    // Send message
                    string message = "Hello WebSocket!";
                    byte[] messageBytes = Encoding.UTF8.GetBytes(message);
                    await client.SendAsync(new ArraySegment<byte>(messageBytes), 
                        WebSocketMessageType.Text, true, CancellationToken.None);
                    
                    // Receive echo
                    byte[] buffer = new byte[1024];
                    var result = await client.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);
                    string response = Encoding.UTF8.GetString(buffer, 0, result.Count);
                    Console.WriteLine($"Received: {response}, Message type: {result.MessageType}, End: {result.EndOfMessage}");
                    
                    // Close
                    await client.CloseAsync(WebSocketCloseStatus.NormalClosure, "Goodbye", CancellationToken.None);
                    Console.WriteLine($"WebSocket closed: {client.State}");
                }
            }
            
            try
            {
                WebSocketClientExample().Wait();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"WebSocket error: {ex.Message}");
            }
            
            // 2. WebSocket server (ASP.NET Core)
            Console.WriteLine("\n2. WebSocket Server (ASP.NET Core):");
            Console.WriteLine("""
                In Startup.cs:
                
                app.UseWebSockets();
                
                In controller/middleware:
                
                if (context.WebSockets.IsWebSocketRequest)
                {
                    var webSocket = await context.WebSockets.AcceptWebSocketAsync();
                    await HandleWebSocket(webSocket);
                }
                
                Handling method:
                async Task HandleWebSocket(WebSocket webSocket)
                {
                    var buffer = new byte[1024];
                    while (webSocket.State == WebSocketState.Open)
                    {
                        var result = await webSocket.ReceiveAsync(buffer, CancellationToken.None);
                        if (result.MessageType == WebSocketMessageType.Close)
                        {
                            await webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, 
                                "Closed by client", CancellationToken.None);
                        }
                        else
                        {
                            // Process message
                            await webSocket.SendAsync(buffer, result.MessageType, 
                                result.EndOfMessage, CancellationToken.None);
                        }
                    }
                }
                """);
            
            // 3. WebSocket message types
            Console.WriteLine("\n3. WebSocket Message Types:");
            Console.WriteLine("""
                • Text: UTF-8 encoded text
                • Binary: Arbitrary binary data
                • Close: Connection close notification
                
                Fragmentation:
                • Large messages can be split across multiple frames
                • Use result.EndOfMessage to detect complete messages
                • WebSocketMessageType indicates text vs binary
                """);
            
            // 4. SignalR (abstraction over WebSockets)
            Console.WriteLine("\n4. SignalR:");
            Console.WriteLine("""
                SignalR provides:
                • Automatic transport fallback (WebSocket -> ServerSentEvents -> LongPolling)
                • Connection management
                • Group messaging
                • Client-to-server and server-to-client RPC
                
                Setup:
                services.AddSignalR();
                
                app.UseEndpoints(endpoints =>
                {
                    endpoints.MapHub<ChatHub>("/chat");
                });
                
                Client (JavaScript, .NET, Java, etc.):
                var connection = new HubConnectionBuilder()
                    .WithUrl("/chat")
                    .Build();
                
                await connection.StartAsync();
                await connection.InvokeAsync("SendMessage", user, message);
                """);
            
            // 5. WebSocket subprotocols
            Console.WriteLine("\n5. WebSocket Subprotocols:");
            Console.WriteLine("""
                Common subprotocols:
                • wamp (Web Application Messaging Protocol)
                • soap (SOAP over WebSocket)
                • mqtt (MQTT over WebSocket)
                • stomp (Simple Text Oriented Messaging Protocol)
                
                Setting subprotocol:
                client.Options.AddSubProtocol("custom-protocol");
                
                Server checks:
                if (context.WebSockets.WebSocketRequestedProtocols.Contains("myproto"))
                {
                    webSocket = await context.WebSockets.AcceptWebSocketAsync("myproto");
                }
                """);
            
            // 6. WebSocket security
            Console.WriteLine("\n6. WebSocket Security:");
            Console.WriteLine("""
                Considerations:
                • Use wss:// (WebSocket Secure)
                • Validate origin headers
                • Implement authentication/authorization
                • Limit message sizes
                • Sanitize input
                • Rate limiting
                • Monitor connections
                """);
        }
        
        static void DemonstrateGrpcAndProtocols()
        {
            Console.WriteLine("\n=== 5. gRPC and Protocols ===\n");
            
            // 1. gRPC overview
            Console.WriteLine("1. gRPC Overview:");
            Console.WriteLine("""
                gRPC features:
                • HTTP/2 based
                • Protocol Buffers for serialization
                • Bidirectional streaming
                • Pluggable authentication
                • Cancellation and timeout
                
                proto file example:
                syntax = "proto3";
                
                service Greeter {
                  rpc SayHello (HelloRequest) returns (HelloReply);
                  rpc StreamMessages (stream Message) returns (stream Response);
                }
                
                message HelloRequest {
                  string name = 1;
                }
                
                message HelloReply {
                  string message = 1;
                }
                """);
            
            // 2. gRPC client
            Console.WriteLine("\n2. gRPC Client:");
            Console.WriteLine("""
                // Generated client from proto file
                using var channel = GrpcChannel.ForAddress("https://localhost:5001");
                var client = new Greeter.GreeterClient(channel);
                
                // Unary call
                var reply = await client.SayHelloAsync(new HelloRequest { Name = "World" });
                Console.WriteLine($"Greeting: {reply.Message}");
                
                // Server streaming
                using var call = client.StreamMessages(new MessageRequest());
                await foreach (var response in call.ResponseStream.ReadAllAsync())
                {
                    Console.WriteLine($"Streamed: {response.Text}");
                }
                
                // Client streaming
                using var clientStream = client.ClientStreamingCall();
                await clientStream.RequestStream.WriteAsync(new Message { Text = "Message 1" });
                await clientStream.RequestStream.CompleteAsync();
                var clientStreamResponse = await clientStream.ResponseAsync;
                
                // Bidirectional streaming
                using var duplex = client.DuplexStreamingCall();
                // Read and write concurrently
                """);
            
            // 3. gRPC server
            Console.WriteLine("\n3. gRPC Server:");
            Console.WriteLine("""
                In Startup.cs:
                services.AddGrpc();
                
                app.UseEndpoints(endpoints =>
                {
                    endpoints.MapGrpcService<GreeterService>();
                });
                
                Service implementation:
                public class GreeterService : Greeter.GreeterBase
                {
                    public override async Task<HelloReply> SayHello(HelloRequest request, 
                        ServerCallContext context)
                    {
                        return new HelloReply 
                        { 
                            Message = "Hello " + request.Name 
                        };
                    }
                    
                    public override async Task StreamMessages(IAsyncStreamReader<Message> requestStream,
                        IServerStreamWriter<Response> responseStream,
                        ServerCallContext context)
                    {
                        await foreach (var message in requestStream.ReadAllAsync())
                        {
                            await responseStream.WriteAsync(new Response 
                            { 
                                Text = "Echo: " + message.Text 
                            });
                        }
                    }
                }
                """);
            
            // 4. REST APIs vs gRPC
            Console.WriteLine("\n4. REST APIs vs gRPC:");
            Console.WriteLine("""
                REST (HTTP/JSON):
                • Human-readable
                • Browser-friendly
                • Cacheable
                • Stateless
                • Wide tooling support
                
                gRPC (HTTP/2/Protobuf):
                • High performance
                • Strongly-typed
                • Streaming support
                • Code generation
                • Smaller payloads
                
                gRPC-Web for browser clients:
                • Browser-compatible gRPC
                • Proxy required for HTTP/2
                """);
            
            // 5. Other protocols
            Console.WriteLine("\n5. Other Network Protocols:");
            Console.WriteLine("""
                • FTP/FTPS: File transfer
                • SMTP: Email sending
                • POP3/IMAP: Email retrieval
                • LDAP: Directory services
                • SSH: Secure shell
                • MQTT: IoT messaging
                • AMQP: Message queuing
                
                Libraries:
                • MailKit for email (SMTP, POP3, IMAP)
                • SSH.NET for SSH
                • MQTTnet for MQTT
                • RabbitMQ.Client for AMQP
                """);
            
            // 6. Protocol selection guide
            Console.WriteLine("\n6. Protocol Selection Guide:");
            Console.WriteLine("""
                Choose based on requirements:
                
                Web APIs:
                • Public API: REST/JSON
                • Internal microservices: gRPC
                • Real-time updates: WebSocket/SignalR
                
                File transfer:
                • Large files: FTP/FTPS
                • Simple: HTTP with chunked encoding
                
                Messaging:
                • Enterprise: AMQP (RabbitMQ)
                • IoT: MQTT
                • Real-time: WebSocket
                
                Remote procedure calls:
                • Performance: gRPC
                • Simplicity: REST
                • Legacy: SOAP
                """);
        }
        
        static void DemonstrateNetworkUtilities()
        {
            Console.WriteLine("\n=== 6. Network Utilities ===\n");
            
            // 1. DNS resolution
            Console.WriteLine("1. DNS Resolution:");
            
            try
            {
                IPHostEntry hostEntry = Dns.GetHostEntry("google.com");
                Console.WriteLine($"Host: {hostEntry.HostName}");
                Console.WriteLine("IP addresses:");
                foreach (IPAddress address in hostEntry.AddressList)
                {
                    Console.WriteLine($"  {address} ({address.AddressFamily})");
                }
                
                Console.WriteLine("Aliases:");
                foreach (string alias in hostEntry.Aliases)
                {
                    Console.WriteLine($"  {alias}");
                }
            }
            catch (SocketException ex)
            {
                Console.WriteLine($"DNS error: {ex.Message}");
            }
            
            // Async DNS
            async Task AsyncDnsExample()
            {
                IPHostEntry hostEntry = await Dns.GetHostEntryAsync("microsoft.com");
                Console.WriteLine($"Async DNS: {hostEntry.HostName}, {hostEntry.AddressList.Length} addresses");
            }
            AsyncDnsExample().Wait();
            
            // 2. IP address parsing and manipulation
            Console.WriteLine("\n2. IP Address Utilities:");
            
            // Parse IP addresses
            IPAddress ip1 = IPAddress.Parse("192.168.1.1");
            IPAddress ip2 = IPAddress.Parse("2001:0db8:85a3:0000:0000:8a2e:0370:7334");
            Console.WriteLine($"IPv4: {ip1}, IPv6: {ip2}");
            
            // Check private IP
            bool isPrivate = IsPrivateIP(ip1);
            Console.WriteLine($"Is private IP: {isPrivate}");
            
            // Network address
            IPAddress network = CalculateNetworkAddress(ip1, 24);
            Console.WriteLine($"Network address: {network}/24");
            
            // 3. Port and endpoint utilities
            Console.WriteLine("\n3. Port and Endpoint Utilities:");
            
            var endpoint = new IPEndPoint(IPAddress.Loopback, 8080);
            Console.WriteLine($"Endpoint: {endpoint}, Address: {endpoint.Address}, Port: {endpoint.Port}");
            
            // Parse endpoint from string
            if (IPEndPoint.TryParse("127.0.0.1:80", out IPEndPoint parsedEndpoint))
            {
                Console.WriteLine($"Parsed endpoint: {parsedEndpoint}");
            }
            
            // 4. Network interfaces
            Console.WriteLine("\n4. Network Interfaces:");
            
            var interfaces = System.Net.NetworkInformation.NetworkInterface.GetAllNetworkInterfaces();
            foreach (var ni in interfaces.Take(3)) // Show first 3
            {
                Console.WriteLine($"Interface: {ni.Name} ({ni.NetworkInterfaceType})");
                Console.WriteLine($"  Description: {ni.Description}");
                Console.WriteLine($"  Status: {ni.OperationalStatus}");
                Console.WriteLine($"  Speed: {ni.Speed / 1_000_000} Mbps");
                
                var ipProps = ni.GetIPProperties();
                foreach (var address in ipProps.UnicastAddresses.Take(2))
                {
                    Console.WriteLine($"  Address: {address.Address}/{address.PrefixLength}");
                }
            }
            
            // 5. Ping utility
            Console.WriteLine("\n5. Ping Utility:");
            
            async Task PingExample()
            {
                using (var ping = new System.Net.NetworkInformation.Ping())
                {
                    try
                    {
                        var reply = await ping.SendPingAsync("8.8.8.8", 1000);
                        Console.WriteLine($"Ping: {reply.Status}, Time: {reply.RoundtripTime}ms, TTL: {reply.Options?.Ttl}");
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"Ping error: {ex.Message}");
                    }
                }
            }
            PingExample().Wait();
            
            // 6. Network information
            Console.WriteLine("\n6. Network Information:");
            
            var hostName = Dns.GetHostName();
            Console.WriteLine($"Host name: {hostName}");
            
            var localIPs = Dns.GetHostAddresses(hostName);
            Console.WriteLine("Local IP addresses:");
            foreach (var ip in localIPs.Take(3))
            {
                Console.WriteLine($"  {ip}");
            }
            
            // 7. Best practices summary
            Console.WriteLine("\n=== Network Programming Best Practices ===");
            Console.WriteLine("""
                1. Always Use Async/Await:
                   • Don't block on network operations
                   • Use cancellation tokens
                   • Handle timeouts gracefully
                
                2. Connection Management:
                   • Use connection pooling (HttpClientFactory)
                   • Implement retry logic with backoff
                   • Consider circuit breakers
                   • Monitor connection counts
                
                3. Error Handling:
                   • Catch specific exceptions (HttpRequestException, SocketException)
                   • Implement fallback strategies
                   • Log network errors with context
                   • User-friendly error messages
                
                4. Security:
                   • Use TLS/SSL for sensitive data
                   • Validate certificates
                   • Sanitize network input
                   • Implement authentication/authorization
                   • Use secure protocols (HTTPS, WSS, FTPS)
                
                5. Performance:
                   • Reuse connections when possible
                   • Compress large payloads
                   • Use appropriate buffer sizes
                   • Consider protocol choice (gRPC vs REST)
                   • Monitor network usage
                
                6. Testing:
                   • Mock network dependencies
                   • Test error scenarios (timeout, DNS failure)
                   • Load test network code
                   • Test with different network conditions
                
                7. Monitoring:
                   • Log request/response times
                   • Track error rates
                   • Monitor connection counts
                   • Alert on abnormal patterns
                
                Remember: Network is unreliable. Design for failure.
                """);
        }
        
        // Helper methods
        static bool IsPrivateIP(IPAddress ip)
        {
            if (ip.AddressFamily == System.Net.Sockets.AddressFamily.InterNetwork)
            {
                byte[] bytes = ip.GetAddressBytes();
                // 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
                return bytes[0] == 10 ||
                       (bytes[0] == 172 && bytes[1] >= 16 && bytes[1] <= 31) ||
                       (bytes[0] == 192 && bytes[1] == 168);
            }
            return false;
        }
        
        static IPAddress CalculateNetworkAddress(IPAddress ip, int prefixLength)
        {
            byte[] ipBytes = ip.GetAddressBytes();
            byte[] maskBytes = new byte[ipBytes.Length];
            
            for (int i = 0; i < ipBytes.Length; i++)
            {
                int bits = Math.Min(8, prefixLength - i * 8);
                if (bits > 0)
                {
                    maskBytes[i] = (byte)(0xFF << (8 - bits));
                }
                ipBytes[i] &= maskBytes[i];
            }
            
            return new IPAddress(ipBytes);
        }
    }
}