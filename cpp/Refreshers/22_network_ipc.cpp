#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>
#include <thread>
#include <vector>
#include <poll.h>

void demonstrate_networking_basics() {
    std::cout << "\n=== NETWORKING BASICS ===\n";
    
    // ============================================================================
    // 1. SOCKET CREATION AND BASIC CONCEPTS
    // ============================================================================
    
    std::cout << "\n1. Socket Creation and Concepts:\n";
    
    // Socket types
    std::cout << "Socket types:\n";
    std::cout << "  SOCK_STREAM - TCP (reliable, connection-oriented)\n";
    std::cout << "  SOCK_DGRAM  - UDP (unreliable, connectionless)\n";
    std::cout << "  SOCK_RAW    - Raw sockets (direct IP access)\n";
    
    // Protocol families
    std::cout << "\nProtocol families:\n";
    std::cout << "  AF_INET     - IPv4\n";
    std::cout << "  AF_INET6    - IPv6\n";
    std::cout << "  AF_UNIX/AF_LOCAL - Unix domain sockets\n";
    
    // Create a TCP socket
    int tcp_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (tcp_socket == -1) {
        perror("socket() failed");
        return;
    }
    std::cout << "\nCreated TCP socket: fd=" << tcp_socket << "\n";
    
    // Create a UDP socket
    int udp_socket = socket(AF_INET, SOCK_DGRAM, 0);
    if (udp_socket != -1) {
        std::cout << "Created UDP socket: fd=" << udp_socket << "\n";
        close(udp_socket);
    }
    
    // ============================================================================
    // 2. SOCKET OPTIONS
    // ============================================================================
    
    std::cout << "\n2. Socket Options:\n";
    
    // Set socket options
    int reuse = 1;
    if (setsockopt(tcp_socket, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) == 0) {
        std::cout << "Set SO_REUSEADDR (allow immediate reuse of address)\n";
    }
    
    // Get socket buffer sizes
    int send_buffer, recv_buffer;
    socklen_t optlen = sizeof(send_buffer);
    
    getsockopt(tcp_socket, SOL_SOCKET, SO_SNDBUF, &send_buffer, &optlen);
    getsockopt(tcp_socket, SOL_SOCKET, SO_RCVBUF, &recv_buffer, &optlen);
    
    std::cout << "Send buffer size: " << send_buffer << " bytes\n";
    std::cout << "Receive buffer size: " << recv_buffer << " bytes\n";
    
    // Set non-blocking mode
    int flags = fcntl(tcp_socket, F_GETFL, 0);
    fcntl(tcp_socket, F_SETFL, flags | O_NONBLOCK);
    std::cout << "Set socket to non-blocking mode\n";
    
    // ============================================================================
    // 3. TCP SERVER
    // ============================================================================
    
    std::cout << "\n3. TCP Server Implementation:\n";
    
    // Server thread function
    auto server_thread = []() {
        // Create server socket
        int server_fd = socket(AF_INET, SOCK_STREAM, 0);
        if (server_fd == -1) {
            perror("server socket() failed");
            return;
        }
        
        // Set SO_REUSEADDR
        int reuse = 1;
        setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));
        
        // Bind to address
        struct sockaddr_in server_addr;
        memset(&server_addr, 0, sizeof(server_addr));
        server_addr.sin_family = AF_INET;
        server_addr.sin_addr.s_addr = INADDR_ANY;  // Bind to all interfaces
        server_addr.sin_port = htons(8080);        // Port 8080
        
        if (bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
            perror("bind() failed");
            close(server_fd);
            return;
        }
        
        // Listen for connections
        if (listen(server_fd, 5) == -1) {  // Backlog of 5 connections
            perror("listen() failed");
            close(server_fd);
            return;
        }
        
        std::cout << "TCP Server listening on port 8080...\n";
        
        // Accept one connection
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        
        int client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &client_len);
        if (client_fd == -1) {
            perror("accept() failed");
            close(server_fd);
            return;
        }
        
        // Get client info
        char client_ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, sizeof(client_ip));
        std::cout << "Server accepted connection from: " << client_ip 
                  << ":" << ntohs(client_addr.sin_port) << "\n";
        
        // Receive data from client
        char buffer[1024];
        ssize_t bytes_received = recv(client_fd, buffer, sizeof(buffer) - 1, 0);
        
        if (bytes_received > 0) {
            buffer[bytes_received] = '\0';
            std::cout << "Server received: " << buffer << "\n";
            
            // Send response
            const char* response = "Hello from TCP Server!\n";
            send(client_fd, response, strlen(response), 0);
        }
        
        // Close connections
        close(client_fd);
        close(server_fd);
    };
    
    // ============================================================================
    // 4. TCP CLIENT
    // ============================================================================
    
    std::cout << "\n4. TCP Client Implementation:\n";
    
    // Start server in background thread
    std::thread server(server_thread);
    sleep(1);  // Give server time to start
    
    // Create client socket
    int client_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (client_fd == -1) {
        perror("client socket() failed");
        server.join();
        return;
    }
    
    // Connect to server
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(8080);
    
    // Convert IP address from text to binary
    if (inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr) <= 0) {
        perror("inet_pton() failed");
        close(client_fd);
        server.join();
        return;
    }
    
    if (connect(client_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        perror("connect() failed");
        close(client_fd);
        server.join();
        return;
    }
    
    std::cout << "TCP Client connected to server\n";
    
    // Send data to server
    const char* message = "Hello from TCP Client!\n";
    send(client_fd, message, strlen(message), 0);
    
    // Receive response
    char buffer[1024];
    ssize_t bytes_received = recv(client_fd, buffer, sizeof(buffer) - 1, 0);
    
    if (bytes_received > 0) {
        buffer[bytes_received] = '\0';
        std::cout << "Client received: " << buffer << "\n";
    }
    
    // Clean up
    close(client_fd);
    server.join();
    
    // ============================================================================
    // 5. UDP SERVER AND CLIENT
    // ============================================================================
    
    std::cout << "\n5. UDP Communication:\n";
    
    // UDP Server thread
    auto udp_server_thread = []() {
        int server_fd = socket(AF_INET, SOCK_DGRAM, 0);
        if (server_fd == -1) {
            perror("UDP server socket() failed");
            return;
        }
        
        struct sockaddr_in server_addr;
        memset(&server_addr, 0, sizeof(server_addr));
        server_addr.sin_family = AF_INET;
        server_addr.sin_addr.s_addr = INADDR_ANY;
        server_addr.sin_port = htons(9090);
        
        if (bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
            perror("UDP bind() failed");
            close(server_fd);
            return;
        }
        
        std::cout << "UDP Server listening on port 9090...\n";
        
        // Receive datagram
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        char buffer[1024];
        
        ssize_t bytes_received = recvfrom(server_fd, buffer, sizeof(buffer) - 1, 0,
                                          (struct sockaddr*)&client_addr, &client_len);
        
        if (bytes_received > 0) {
            buffer[bytes_received] = '\0';
            
            char client_ip[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, sizeof(client_ip));
            
            std::cout << "UDP Server received from " << client_ip 
                      << ":" << ntohs(client_addr.sin_port) << ": " << buffer << "\n";
            
            // Send response back
            const char* response = "UDP Server response!\n";
            sendto(server_fd, response, strlen(response), 0,
                   (struct sockaddr*)&client_addr, client_len);
        }
        
        close(server_fd);
    };
    
    // Start UDP server
    std::thread udp_server(udp_server_thread);
    sleep(1);
    
    // UDP Client
    int udp_client_fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (udp_client_fd != -1) {
        struct sockaddr_in server_addr;
        memset(&server_addr, 0, sizeof(server_addr));
        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(9090);
        inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);
        
        // Send datagram (no connection needed)
        const char* message = "Hello UDP Server!\n";
        sendto(udp_client_fd, message, strlen(message), 0,
               (struct sockaddr*)&server_addr, sizeof(server_addr));
        
        std::cout << "UDP Client sent message\n";
        
        // Receive response
        struct sockaddr_in from_addr;
        socklen_t from_len = sizeof(from_addr);
        char buffer[1024];
        
        ssize_t bytes_received = recvfrom(udp_client_fd, buffer, sizeof(buffer) - 1, 0,
                                          (struct sockaddr*)&from_addr, &from_len);
        
        if (bytes_received > 0) {
            buffer[bytes_received] = '\0';
            std::cout << "UDP Client received: " << buffer << "\n";
        }
        
        close(udp_client_fd);
    }
    
    udp_server.join();
    
    // ============================================================================
    // 6. NETWORK ADDRESS FUNCTIONS
    // ============================================================================
    
    std::cout << "\n6. Network Address Functions:\n";
    
    // Convert IP address from text to binary
    struct in_addr ip_addr;
    if (inet_pton(AF_INET, "192.168.1.1", &ip_addr) > 0) {
        std::cout << "inet_pton: 192.168.1.1 -> " << ip_addr.s_addr << "\n";
    }
    
    // Convert binary to text
    char ip_str[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &ip_addr, ip_str, sizeof(ip_str));
    std::cout << "inet_ntop: " << ip_addr.s_addr << " -> " << ip_str << "\n";
    
    // Host byte order vs Network byte order
    uint16_t host_port = 8080;
    uint16_t net_port = htons(host_port);  // Host to Network (short)
    uint16_t back_to_host = ntohs(net_port);  // Network to Host
    
    std::cout << "Host order: " << host_port 
              << ", Network order: " << net_port
              << ", Back to host: " << back_to_host << "\n";
    
    // ============================================================================
    // 7. NON-BLOCKING I/O WITH POLL
    // ============================================================================
    
    std::cout << "\n7. Non-blocking I/O with poll():\n";
    
    int poll_socket = socket(AF_INET, SOCK_STREAM, 0);
    fcntl(poll_socket, F_SETFL, O_NONBLOCK);
    
    struct pollfd fds[1];
    fds[0].fd = poll_socket;
    fds[0].events = POLLIN;  // Check for readability
    
    std::cout << "Polling socket for 2 seconds (will timeout)...\n";
    
    int poll_result = poll(fds, 1, 2000);  // 2 second timeout
    
    if (poll_result == 0) {
        std::cout << "poll() timeout - no data available\n";
    } else if (poll_result > 0) {
        if (fds[0].revents & POLLIN) {
            std::cout << "Data available to read\n";
        }
    }
    
    close(poll_socket);
    
    // ============================================================================
    // 8. MULTIPLE CONNECTIONS WITH SELECT
    // ============================================================================
    
    std::cout << "\n8. Multiple Connections with select():\n";
    
    // Create listening socket
    int select_server = socket(AF_INET, SOCK_STREAM, 0);
    setsockopt(select_server, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));
    
    struct sockaddr_in select_addr;
    memset(&select_addr, 0, sizeof(select_addr));
    select_addr.sin_family = AF_INET;
    select_addr.sin_addr.s_addr = INADDR_ANY;
    select_addr.sin_port = htons(9999);
    
    bind(select_server, (struct sockaddr*)&select_addr, sizeof(select_addr));
    listen(select_server, 5);
    
    std::cout << "Server ready on port 9999 (run client to test select)\n";
    
    // Set up select()
    fd_set read_fds;
    FD_ZERO(&read_fds);
    FD_SET(select_server, &read_fds);
    
    int max_fd = select_server;
    
    struct timeval timeout;
    timeout.tv_sec = 1;
    timeout.tv_usec = 0;
    
    int select_result = select(max_fd + 1, &read_fds, nullptr, nullptr, &timeout);
    
    if (select_result == -1) {
        perror("select() failed");
    } else if (select_result == 0) {
        std::cout << "select() timeout - no connections\n";
    } else {
        if (FD_ISSET(select_server, &read_fds)) {
            std::cout << "New connection ready to accept\n";
        }
    }
    
    close(select_server);
    
    // ============================================================================
    // 9. DNS LOOKUP
    // ============================================================================
    
    std::cout << "\n9. DNS Lookup:\n";
    
    struct hostent* host = gethostbyname("google.com");
    if (host) {
        std::cout << "google.com resolves to:\n";
        for (int i = 0; host->h_addr_list[i] != nullptr; i++) {
            struct in_addr addr;
            memcpy(&addr, host->h_addr_list[i], sizeof(addr));
            char ip[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, &addr, ip, sizeof(ip));
            std::cout << "  " << ip << "\n";
        }
    }
    
    // ============================================================================
    // 10. SOCKET ERRORS
    // ============================================================================
    
    std::cout << "\n10. Socket Error Handling:\n";
    
    int error = 0;
    socklen_t errlen = sizeof(error);
    getsockopt(tcp_socket, SOL_SOCKET, SO_ERROR, &error, &errlen);
    
    if (error == 0) {
        std::cout << "Socket is in good state\n";
    } else {
        std::cout << "Socket error: " << strerror(error) << "\n";
    }
    
    // Common socket errors
    std::cout << "\nCommon socket errors:\n";
    std::cout << "  EAGAIN/EWOULDBLOCK - Resource temporarily unavailable\n";
    std::cout << "  ECONNREFUSED       - Connection refused\n";
    std::cout << "  ETIMEDOUT          - Connection timed out\n";
    std::cout << "  ECONNRESET         - Connection reset by peer\n";
    
    // Close TCP socket
    close(tcp_socket);
    
    std::cout << "\nNetworking Summary:\n";
    std::cout << "TCP: Reliable, ordered, connection-oriented\n";
    std::cout << "UDP: Unreliable, unordered, connectionless\n";
    std::cout << "Use TCP for: HTTP, FTP, SSH, email\n";
    std::cout << "Use UDP for: DNS, VoIP, video streaming, games\n";
}


#include <iostream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/msg.h>
#include <sys/sem.h>
#include <cstring>
#include <vector>
#include <thread>
#include <fcntl.h>
#include <sys/stat.h>

// Union for semaphore operations
union semun {
    int val;
    struct semid_ds* buf;
    unsigned short* array;
    struct seminfo* __buf;
};

void demonstrate_ipc() {
    std::cout << "\n=== INTER-PROCESS COMMUNICATION (IPC) ===\n";
    
    // ============================================================================
    // 1. PIPES (UNNAMED PIPES)
    // ============================================================================
    
    std::cout << "\n1. Unnamed Pipes:\n";
    
    int pipe_fds[2];  // pipe_fds[0] = read, pipe_fds[1] = write
    
    if (pipe(pipe_fds) == -1) {
        perror("pipe() failed");
        return;
    }
    
    std::cout << "Created pipe: read_fd=" << pipe_fds[0] 
              << ", write_fd=" << pipe_fds[1] << "\n";
    
    pid_t pid = fork();
    
    if (pid == 0) {
        // Child process - reads from pipe
        close(pipe_fds[1]);  // Close write end
        
        char buffer[100];
        ssize_t bytes_read = read(pipe_fds[0], buffer, sizeof(buffer) - 1);
        
        if (bytes_read > 0) {
            buffer[bytes_read] = '\0';
            std::cout << "Child read from pipe: " << buffer << "\n";
        }
        
        close(pipe_fds[0]);
        exit(0);
    }
    else {
        // Parent process - writes to pipe
        close(pipe_fds[0]);  // Close read end
        
        const char* message = "Hello from parent via pipe!\n";
        write(pipe_fds[1], message, strlen(message));
        
        close(pipe_fds[1]);
        waitpid(pid, nullptr, 0);
    }
    
    // ============================================================================
    // 2. NAMED PIPES (FIFOs)
    // ============================================================================
    
    std::cout << "\n2. Named Pipes (FIFOs):\n";
    
    const char* fifo_path = "/tmp/myfifo";
    
    // Create FIFO (named pipe)
    if (mkfifo(fifo_path, 0666) == -1 && errno != EEXIST) {
        perror("mkfifo failed");
    } else {
        std::cout << "Created FIFO at: " << fifo_path << "\n";
        
        pid = fork();
        
        if (pid == 0) {
            // Child writes to FIFO
            int fd = open(fifo_path, O_WRONLY);
            if (fd != -1) {
                const char* msg = "Data through FIFO\n";
                write(fd, msg, strlen(msg));
                close(fd);
                std::cout << "Child wrote to FIFO\n";
            }
            exit(0);
        }
        else {
            // Parent reads from FIFO
            int fd = open(fifo_path, O_RDONLY);
            if (fd != -1) {
                char buffer[100];
                ssize_t bytes = read(fd, buffer, sizeof(buffer) - 1);
                if (bytes > 0) {
                    buffer[bytes] = '\0';
                    std::cout << "Parent read from FIFO: " << buffer << "\n";
                }
                close(fd);
            }
            waitpid(pid, nullptr, 0);
            
            // Clean up
            unlink(fifo_path);
        }
    }
    
    // ============================================================================
    // 3. SHARED MEMORY
    // ============================================================================
    
    std::cout << "\n3. Shared Memory:\n";
    
    // Generate a key for shared memory
    key_t shm_key = ftok("/tmp", 'S');
    if (shm_key == -1) {
        perror("ftok failed");
    } else {
        std::cout << "Generated key: " << shm_key << "\n";
        
        // Create shared memory segment
        int shm_id = shmget(shm_key, 1024, IPC_CREAT | 0666);
        if (shm_id == -1) {
            perror("shmget failed");
        } else {
            std::cout << "Shared memory ID: " << shm_id << "\n";
            
            pid = fork();
            
            if (pid == 0) {
                // Child attaches and writes
                char* shm_ptr = (char*)shmat(shm_id, nullptr, 0);
                if (shm_ptr != (char*)-1) {
                    strcpy(shm_ptr, "Shared memory data from child");
                    std::cout << "Child wrote to shared memory\n";
                    shmdt(shm_ptr);  // Detach
                }
                exit(0);
            }
            else {
                // Parent attaches and reads
                sleep(1);  // Wait for child to write
                
                char* shm_ptr = (char*)shmat(shm_id, nullptr, 0);
                if (shm_ptr != (char*)-1) {
                    std::cout << "Parent read from shared memory: " << shm_ptr << "\n";
                    shmdt(shm_ptr);
                }
                
                waitpid(pid, nullptr, 0);
                
                // Clean up
                shmctl(shm_id, IPC_RMID, nullptr);
                std::cout << "Shared memory removed\n";
            }
        }
    }
    
    // ============================================================================
    // 4. MESSAGE QUEUES
    // ============================================================================
    
    std::cout << "\n4. Message Queues:\n";
    
    // Generate key
    key_t msg_key = ftok("/tmp", 'M');
    if (msg_key == -1) {
        perror("ftok for message queue failed");
    } else {
        // Create message queue
        int msg_id = msgget(msg_key, IPC_CREAT | 0666);
        if (msg_id == -1) {
            perror("msgget failed");
        } else {
            std::cout << "Message queue ID: " << msg_id << "\n";
            
            // Define message structure
            struct msgbuf {
                long mtype;
                char mtext[100];
            };
            
            pid = fork();
            
            if (pid == 0) {
                // Child sends message
                struct msgbuf msg;
                msg.mtype = 1;  // Message type
                strcpy(msg.mtext, "Hello from child process!");
                
                if (msgsnd(msg_id, &msg, strlen(msg.mtext) + 1, 0) == 0) {
                    std::cout << "Child sent message\n";
                }
                
                exit(0);
            }
            else {
                // Parent receives message
                sleep(1);
                
                struct msgbuf msg;
                ssize_t bytes = msgrcv(msg_id, &msg, sizeof(msg.mtext), 1, 0);
                
                if (bytes > 0) {
                    std::cout << "Parent received message (type=" << msg.mtype 
                              << "): " << msg.mtext << "\n";
                }
                
                waitpid(pid, nullptr, 0);
                
                // Clean up
                msgctl(msg_id, IPC_RMID, nullptr);
                std::cout << "Message queue removed\n";
            }
        }
    }
    
    // ============================================================================
    // 5. SEMAPHORES
    // ============================================================================
    
    std::cout << "\n5. Semaphores:\n";
    
    key_t sem_key = ftok("/tmp", 'E');
    if (sem_key == -1) {
        perror("ftok for semaphore failed");
    } else {
        // Create semaphore set with 1 semaphore
        int sem_id = semget(sem_key, 1, IPC_CREAT | 0666);
        if (sem_id == -1) {
            perror("semget failed");
        } else {
            std::cout << "Semaphore ID: " << sem_id << "\n";
            
            // Initialize semaphore to 1 (binary semaphore)
            union semun sem_union;
            sem_union.val = 1;
            if (semctl(sem_id, 0, SETVAL, sem_union) == -1) {
                perror("semctl SETVAL failed");
            }
            
            pid = fork();
            
            if (pid == 0) {
                // Child waits for semaphore
                std::cout << "Child waiting for semaphore...\n";
                
                struct sembuf sem_op;
                sem_op.sem_num = 0;
                sem_op.sem_op = -1;  // Wait (decrement)
                sem_op.sem_flg = 0;
                
                semop(sem_id, &sem_op, 1);
                std::cout << "Child acquired semaphore\n";
                
                // Critical section
                sleep(2);
                std::cout << "Child in critical section\n";
                
                // Release semaphore
                sem_op.sem_op = 1;  // Signal (increment)
                semop(sem_id, &sem_op, 1);
                std::cout << "Child released semaphore\n";
                
                exit(0);
            }
            else {
                // Parent waits for semaphore
                std::cout << "Parent waiting for semaphore...\n";
                
                struct sembuf sem_op;
                sem_op.sem_num = 0;
                sem_op.sem_op = -1;
                sem_op.sem_flg = 0;
                
                semop(sem_id, &sem_op, 1);
                std::cout << "Parent acquired semaphore\n";
                
                // Critical section
                sleep(1);
                std::cout << "Parent in critical section\n";
                
                // Release semaphore
                sem_op.sem_op = 1;
                semop(sem_id, &sem_op, 1);
                std::cout << "Parent released semaphore\n";
                
                waitpid(pid, nullptr, 0);
                
                // Clean up
                semctl(sem_id, 0, IPC_RMID);
                std::cout << "Semaphore removed\n";
            }
        }
    }
    
    // ============================================================================
    // 6. UNIX DOMAIN SOCKETS
    // ============================================================================
    
    std::cout << "\n6. Unix Domain Sockets:\n";
    
    const char* socket_path = "/tmp/mysocket";
    
    // Remove socket file if exists
    unlink(socket_path);
    
    // Create socket
    int sock_fd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (sock_fd == -1) {
        perror("socket() failed");
    } else {
        // Bind socket to file
        struct sockaddr_un addr;
        memset(&addr, 0, sizeof(addr));
        addr.sun_family = AF_UNIX;
        strcpy(addr.sun_path, socket_path);
        
        if (bind(sock_fd, (struct sockaddr*)&addr, sizeof(addr)) == -1) {
            perror("bind() failed");
            close(sock_fd);
        } else {
            listen(sock_fd, 5);
            
            pid = fork();
            
            if (pid == 0) {
                // Child connects to socket
                sleep(1);
                
                int client_fd = socket(AF_UNIX, SOCK_STREAM, 0);
                struct sockaddr_un server_addr;
                memset(&server_addr, 0, sizeof(server_addr));
                server_addr.sun_family = AF_UNIX;
                strcpy(server_addr.sun_path, socket_path);
                
                if (connect(client_fd, (struct sockaddr*)&server_addr, 
                           sizeof(server_addr)) == 0) {
                    const char* msg = "Hello via Unix socket!\n";
                    send(client_fd, msg, strlen(msg), 0);
                    close(client_fd);
                    std::cout << "Child sent data via Unix socket\n";
                }
                
                exit(0);
            }
            else {
                // Parent accepts connection
                struct sockaddr_un client_addr;
                socklen_t client_len = sizeof(client_addr);
                
                int client_fd = accept(sock_fd, (struct sockaddr*)&client_addr, 
                                      &client_len);
                
                if (client_fd != -1) {
                    char buffer[100];
                    ssize_t bytes = recv(client_fd, buffer, sizeof(buffer) - 1, 0);
                    if (bytes > 0) {
                        buffer[bytes] = '\0';
                        std::cout << "Parent received via Unix socket: " << buffer << "\n";
                    }
                    close(client_fd);
                }
                
                waitpid(pid, nullptr, 0);
                close(sock_fd);
                unlink(socket_path);
            }
        }
    }
    
    // ============================================================================
    // 7. MEMORY-MAPPED FILES FOR IPC (REVISITED)
    // ============================================================================
    
    std::cout << "\n7. Memory-Mapped Files for IPC:\n";
    
    const char* mmap_file = "/tmp/ipc_mmap";
    int fd = open(mmap_file, O_RDWR | O_CREAT | O_TRUNC, 0666);
    
    if (fd != -1) {
        // Extend file
        ftruncate(fd, 4096);
        
        // Map file
        void* shared = mmap(nullptr, 4096, PROT_READ | PROT_WRITE, 
                           MAP_SHARED, fd, 0);
        
        if (shared != MAP_FAILED) {
            pid = fork();
            
            if (pid == 0) {
                // Child writes
                char* data = (char*)shared;
                strcpy(data, "IPC via memory-mapped file");
                std::cout << "Child wrote to mapped memory\n";
                exit(0);
            }
            else {
                // Parent reads
                sleep(1);
                char* data = (char*)shared;
                std::cout << "Parent read from mapped memory: " << data << "\n";
                
                waitpid(pid, nullptr, 0);
                
                // Clean up
                munmap(shared, 4096);
            }
        }
        
        close(fd);
        unlink(mmap_file);
    }
    
    // ============================================================================
    // 8. SIGNALS AS IPC (SIMPLIFIED)
    // ============================================================================
    
    std::cout << "\n8. Signals as IPC:\n";
    
    pid = fork();
    
    if (pid == 0) {
        // Child waits for signal
        std::cout << "Child waiting for signal...\n";
        pause();  // Wait for signal
        std::cout << "Child received signal!\n";
        exit(0);
    }
    else {
        // Parent sends signal
        sleep(1);
        std::cout << "Parent sending SIGUSR1 to child...\n";
        kill(pid, SIGUSR1);
        
        waitpid(pid, nullptr, 0);
    }
    
    // ============================================================================
    // 9. COMPARISON OF IPC METHODS
    // ============================================================================
    
    std::cout << "\n9. IPC Method Comparison:\n\n";
    
    std::cout << "Method           | Data Type       | Relationship  | Complexity\n";
    std::cout << "-----------------|-----------------|--------------|------------\n";
    std::cout << "Pipe             | Byte stream     | Parent-Child | Low\n";
    std::cout << "Named Pipe (FIFO)| Byte stream     | Any processes| Low\n";
    std::cout << "Shared Memory    | Random access   | Any processes| Medium\n";
    std::cout << "Message Queue    | Structured      | Any processes| Medium\n";
    std::cout << "Semaphore        | Synchronization | Any processes| Medium\n";
    std::cout << "Unix Socket      | Byte/structured | Any processes| High\n";
    std::cout << "Signal           | Notification    | Any processes| Low\n";
    std::cout << "Memory-Mapped    | Random access   | Any processes| Medium\n";
    
    std::cout << "\nWhen to use:\n";
    std::cout << "- Pipe: Simple parent-child communication\n";
    std::cout << "- FIFO: Persistent communication between unrelated processes\n";
    std::cout << "- Shared Memory: High-speed data sharing\n";
    std::cout << "- Message Queue: Structured message passing\n";
    std::cout << "- Semaphore: Process synchronization\n";
    std::cout << "- Unix Socket: Most flexible, network-like API\n";
    std::cout << "- Signal: Simple notifications\n";
    std::cout << "- Memory-Mapped: File-based shared memory\n";
}