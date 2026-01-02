#include <iostream>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <cstring>
#include <vector>
#include <csignal>

void demonstrate_process_management() {
    std::cout << "\n=== PROCESS MANAGEMENT ===\n";
    
    // ============================================================================
    // 1. FORK - CREATING NEW PROCESSES
    // ============================================================================
    
    std::cout << "\n1. fork() - Creating Child Processes:\n";
    
    pid_t pid = fork();  // Creates a copy of the current process
    
    if (pid == -1) {
        // fork() failed
        perror("fork failed");
        return;
    }
    else if (pid == 0) {
        // CHILD PROCESS
        std::cout << "Child process: PID = " << getpid() 
                  << ", Parent PID = " << getppid() << "\n";
        
        // Child process can execute different code
        for (int i = 0; i < 3; i++) {
            std::cout << "Child working... (" << i << ")\n";
            sleep(1);
        }
        
        // Child exits with status code
        std::cout << "Child exiting\n";
        exit(42);  // Exit with status 42
    }
    else {
        // PARENT PROCESS
        std::cout << "Parent process: PID = " << getpid() 
                  << ", Child PID = " << pid << "\n";
        
        // Wait for child to complete
        int status;
        pid_t child_pid = waitpid(pid, &status, 0);
        
        if (child_pid == -1) {
            perror("waitpid failed");
        }
        else if (WIFEXITED(status)) {
            std::cout << "Child exited with status: " << WEXITSTATUS(status) << "\n";
        }
        else if (WIFSIGNALED(status)) {
            std::cout << "Child killed by signal: " << WTERMSIG(status) << "\n";
        }
    }
    
    // ============================================================================
    // 2. EXEC FAMILY - REPLACING PROCESS IMAGE
    // ============================================================================
    
    std::cout << "\n2. exec() - Replacing Process Image:\n";
    
    pid = fork();
    
    if (pid == 0) {
        // Child process - replace with 'ls' command
        
        std::cout << "Child about to execute 'ls -la'\n";
        
        // Different exec variants:
        
        // execv - takes array of arguments
        char* args[] = {
            (char*)"/bin/ls",
            (char*)"-la",
            (char*)".",
            nullptr
        };
        
        // execl - takes list of arguments
        // execl("/bin/ls", "ls", "-la", ".", nullptr);
        
        // execvp - searches PATH for command
        // char* args[] = {(char*)"ls", (char*)"-la", (char*)".", nullptr};
        // execvp("ls", args);
        
        // execv replaces current process with ls
        execv("/bin/ls", args);
        
        // If exec succeeds, this code never runs
        perror("exec failed");
        exit(1);
    }
    else if (pid > 0) {
        // Parent waits for child
        waitpid(pid, nullptr, 0);
        std::cout << "Child 'ls' command completed\n";
    }
    
    // ============================================================================
    // 3. FORK + EXEC COMBINED
    // ============================================================================
    
    std::cout << "\n3. fork() + exec() Pattern:\n";
    
    std::vector<std::string> commands = {
        "echo Hello from child!",
        "sleep 2",
        "pwd",
        "whoami"
    };
    
    for (const auto& cmd : commands) {
        pid = fork();
        
        if (pid == 0) {
            // Child executes command using shell
            execl("/bin/sh", "sh", "-c", cmd.c_str(), nullptr);
            perror("exec failed");
            exit(1);
        }
        else if (pid > 0) {
            std::cout << "Parent launched: " << cmd << " (PID: " << pid << ")\n";
        }
    }
    
    // Wait for all children
    while (wait(nullptr) > 0) {
        // Wait for all child processes
    }
    std::cout << "All children completed\n";
    
    // ============================================================================
    // 4. ORPHAN PROCESSES
    // ============================================================================
    
    std::cout << "\n4. Orphan Process Demo:\n";
    
    pid = fork();
    
    if (pid == 0) {
        // Child becomes orphan
        std::cout << "Child (PID: " << getpid() << ") starting\n";
        std::cout << "Child parent (PPID): " << getppid() << "\n";
        
        // Make parent exit
        sleep(1);
        
        std::cout << "Child after parent exit - PPID: " << getppid() << "\n";
        std::cout << "Child now orphaned (PPID = 1)\n";
        
        // Orphan process continues
        for (int i = 0; i < 3; i++) {
            std::cout << "Orphan working...\n";
            sleep(1);
        }
        
        exit(0);
    }
    else {
        // Parent exits immediately
        std::cout << "Parent exiting, leaving child orphaned\n";
        exit(0);
    }
    
    // ============================================================================
    // 5. ZOMBIE PROCESSES
    // ============================================================================
    
    std::cout << "\n5. Zombie Process Demo:\n";
    
    pid = fork();
    
    if (pid == 0) {
        // Child exits immediately, becomes zombie
        std::cout << "Child (PID: " << getpid() << ") exiting\n";
        exit(0);
    }
    else {
        // Parent doesn't wait for child
        std::cout << "Parent (PID: " << getpid() << ") not waiting for child\n";
        std::cout << "Child (PID: " << pid << ") becomes zombie\n";
        
        // Show zombie with ps command
        std::cout << "Run 'ps aux | grep " << pid << "' to see zombie\n";
        
        // Sleep to keep zombie alive
        sleep(5);
        
        // Now wait to reap zombie
        waitpid(pid, nullptr, 0);
        std::cout << "Zombie reaped\n";
    }
    
    // ============================================================================
    // 6. PROCESS GROUPS AND SESSIONS
    // ============================================================================
    
    std::cout << "\n6. Process Groups and Sessions:\n";
    
    // Get process group ID
    pid_t pgid = getpgrp();
    std::cout << "Process Group ID: " << pgid << "\n";
    
    // Create new process group
    if (setsid() == -1) {
        perror("setsid failed");
    } else {
        std::cout << "Created new session, PGID: " << getpgrp() << "\n";
    }
    
    // Create background process group
    pid = fork();
    if (pid == 0) {
        // Child in background group
        setpgid(0, 0);  // Put in new process group
        std::cout << "Background process PGID: " << getpgrp() << "\n";
        sleep(2);
        exit(0);
    }
    
    // ============================================================================
    // 7. DAEMON PROCESSES
    // ============================================================================
    
    std::cout << "\n7. Creating a Daemon Process:\n";
    
    pid = fork();
    
    if (pid == 0) {
        // Step 1: Create new session
        if (setsid() == -1) {
            perror("setsid failed");
            exit(1);
        }
        
        // Step 2: Fork again to ensure not session leader
        pid_t pid2 = fork();
        if (pid2 == -1) {
            perror("second fork failed");
            exit(1);
        }
        else if (pid2 > 0) {
            // First child exits
            exit(0);
        }
        
        // Step 3: Change working directory to root
        if (chdir("/") == -1) {
            perror("chdir failed");
            exit(1);
        }
        
        // Step 4: Close standard file descriptors
        close(STDIN_FILENO);
        close(STDOUT_FILENO);
        close(STDERR_FILENO);
        
        // Step 5: Redirect file descriptors to /dev/null
        int devnull = open("/dev/null", O_RDWR);
        dup2(devnull, STDIN_FILENO);
        dup2(devnull, STDOUT_FILENO);
        dup2(devnull, STDERR_FILENO);
        close(devnull);
        
        // Daemon main loop
        for (int i = 0; i < 10; i++) {
            // Daemon would do its work here
            // For demo, just sleep
            sleep(1);
        }
        
        exit(0);
    }
    else {
        // Parent exits immediately
        waitpid(pid, nullptr, 0);
        std::cout << "Daemon created and parent exited\n";
    }
    
    // ============================================================================
    // 8. PROCESS PRIORITIES AND SCHEDULING
    // ============================================================================
    
    std::cout << "\n8. Process Priorities:\n";
    
    // Get current priority
    int priority = getpriority(PRIO_PROCESS, 0);
    std::cout << "Current process priority: " << priority << "\n";
    
    // Set priority (lower number = higher priority, range -20 to 19)
    if (setpriority(PRIO_PROCESS, 0, 10) == 0) {
        std::cout << "Priority set to 10\n";
    }
    
    // Get scheduler policy
    int policy = sched_getscheduler(0);
    std::cout << "Scheduler policy: ";
    switch (policy) {
        case SCHED_FIFO: std::cout << "SCHED_FIFO"; break;
        case SCHED_RR: std::cout << "SCHED_RR"; break;
        case SCHED_OTHER: std::cout << "SCHED_OTHER (default)"; break;
        default: std::cout << "Unknown";
    }
    std::cout << "\n";
}

#include <iostream>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <cstring>
#include <vector>

void demonstrate_file_descriptors() {
    std::cout << "\n=== FILE DESCRIPTORS ===\n";
    
    // ============================================================================
    // 1. STANDARD FILE DESCRIPTORS
    // ============================================================================
    
    std::cout << "\n1. Standard File Descriptors:\n";
    
    std::cout << "STDIN_FILENO  = " << STDIN_FILENO << "  (Standard Input)\n";
    std::cout << "STDOUT_FILENO = " << STDOUT_FILENO << "  (Standard Output)\n";
    std::cout << "STDERR_FILENO = " << STDERR_FILENO << "  (Standard Error)\n";
    
    // Test writing to stdout using file descriptor
    const char* msg = "Hello via file descriptor!\n";
    write(STDOUT_FILENO, msg, strlen(msg));
    
    // ============================================================================
    // 2. OPENING FILES AND GETTING DESCRIPTORS
    // ============================================================================
    
    std::cout << "\n2. Opening Files and File Descriptors:\n";
    
    // Open file for writing
    int fd1 = open("test1.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd1 == -1) {
        perror("open test1.txt failed");
    } else {
        std::cout << "test1.txt opened with fd: " << fd1 << "\n";
        
        const char* data = "Data for test1.txt\n";
        write(fd1, data, strlen(data));
        
        close(fd1);
        std::cout << "test1.txt closed\n";
    }
    
    // Open multiple files
    int fd2 = open("test2.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    int fd3 = open("test3.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    
    std::cout << "test2.txt fd: " << fd2 << "\n";
    std::cout << "test3.txt fd: " << fd3 << "\n";
    
    // File descriptors are usually the lowest available number
    close(fd2);
    close(fd3);
    
    // ============================================================================
    // 3. DUP AND DUP2 - DUPLICATING FILE DESCRIPTORS
    // ============================================================================
    
    std::cout << "\n3. dup() and dup2() - Duplicating File Descriptors:\n";
    
    // Open a file
    int original_fd = open("original.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    write(original_fd, "Original data\n", 14);
    
    // dup() - duplicates to lowest available fd
    int dup_fd = dup(original_fd);
    std::cout << "Original fd: " << original_fd << ", dup() fd: " << dup_fd << "\n";
    
    // Both fds point to same file
    write(dup_fd, "Written via dup fd\n", 19);
    
    // dup2() - duplicates to specific fd
    // Close stdout and redirect to file
    int saved_stdout = dup(STDOUT_FILENO);  // Save stdout
    
    int file_fd = open("output.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    dup2(file_fd, STDOUT_FILENO);  // Redirect stdout to file
    
    // Now cout goes to file!
    std::cout << "This goes to output.txt, not screen!\n";
    
    // Restore stdout
    dup2(saved_stdout, STDOUT_FILENO);
    std::cout << "Back to normal stdout\n";
    
    close(original_fd);
    close(dup_fd);
    close(file_fd);
    close(saved_stdout);
    
    // ============================================================================
    // 4. FILE DESCRIPTOR FLAGS
    // ============================================================================
    
    std::cout << "\n4. File Descriptor Flags:\n";
    
    int fd = open("flags.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    
    // Get file descriptor flags
    int flags = fcntl(fd, F_GETFD);
    std::cout << "File descriptor flags: " << std::hex << flags << std::dec << "\n";
    
    // Set FD_CLOEXEC flag (close-on-exec)
    flags |= FD_CLOEXEC;
    fcntl(fd, F_SETFD, flags);
    std::cout << "Set FD_CLOEXEC flag\n";
    
    // Get file status flags
    int status_flags = fcntl(fd, F_GETFL);
    std::cout << "File status flags: " << std::hex << status_flags << std::dec << "\n";
    
    // Check access mode
    int access_mode = status_flags & O_ACCMODE;
    std::cout << "Access mode: ";
    if (access_mode == O_RDONLY) std::cout << "O_RDONLY";
    else if (access_mode == O_WRONLY) std::cout << "O_WRONLY";
    else if (access_mode == O_RDWR) std::cout << "O_RDWR";
    std::cout << "\n";
    
    close(fd);
    
    // ============================================================================
    // 5. NON-BLOCKING I/O
    // ============================================================================
    
    std::cout << "\n5. Non-blocking I/O:\n";
    
    // Open file in non-blocking mode
    fd = open("nonblock.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    
    // Get current flags
    flags = fcntl(fd, F_GETFL);
    
    // Add O_NONBLOCK flag
    flags |= O_NONBLOCK;
    fcntl(fd, F_SETFL, flags);
    
    std::cout << "Set O_NONBLOCK flag\n";
    
    // Non-blocking write would return immediately if buffer full
    const char* nb_data = "Non-blocking write\n";
    ssize_t written = write(fd, nb_data, strlen(nb_data));
    
    if (written == -1 && errno == EAGAIN) {
        std::cout << "Write would block (buffer full)\n";
    } else {
        std::cout << "Wrote " << written << " bytes\n";
    }
    
    close(fd);
    
    // ============================================================================
    // 6. FILE DESCRIPTOR LIMITS
    // ============================================================================
    
    std::cout << "\n6. File Descriptor Limits:\n";
    
    // Get system limit for open files
    struct rlimit rlim;
    if (getrlimit(RLIMIT_NOFILE, &rlim) == 0) {
        std::cout << "Soft limit (current max): " << rlim.rlim_cur << "\n";
        std::cout << "Hard limit (absolute max): " << rlim.rlim_max << "\n";
    }
    
    // Try to open many files (until limit reached)
    std::vector<int> fds;
    std::cout << "\nOpening files until limit...\n";
    
    for (int i = 0; i < 1000; i++) {
        std::string filename = "temp_" + std::to_string(i) + ".txt";
        int temp_fd = open(filename.c_str(), O_WRONLY | O_CREAT | O_TRUNC, 0644);
        
        if (temp_fd == -1) {
            std::cout << "Failed to open file #" << i << ": " << strerror(errno) << "\n";
            break;
        }
        
        fds.push_back(temp_fd);
        
        if (i % 100 == 0) {
            std::cout << "Opened " << i << " files\n";
        }
    }
    
    std::cout << "Successfully opened " << fds.size() << " files\n";
    
    // Close all files
    for (int fd : fds) {
        close(fd);
    }
    
    // ============================================================================
    // 7. FILE DESCRIPTOR INHERITANCE
    // ============================================================================
    
    std::cout << "\n7. File Descriptor Inheritance:\n";
    
    // Create a pipe
    int pipe_fds[2];
    if (pipe(pipe_fds) == 0) {
        std::cout << "Created pipe: read_fd=" << pipe_fds[0] 
                  << ", write_fd=" << pipe_fds[1] << "\n";
        
        pid_t pid = fork();
        
        if (pid == 0) {
            // Child process inherits file descriptors
            close(pipe_fds[1]);  // Close write end
            
            char buffer[100];
            ssize_t n = read(pipe_fds[0], buffer, sizeof(buffer) - 1);
            if (n > 0) {
                buffer[n] = '\0';
                std::cout << "Child received: " << buffer << "\n";
            }
            
            close(pipe_fds[0]);
            exit(0);
        }
        else {
            // Parent writes to pipe
            close(pipe_fds[0]);  // Close read end
            
            const char* msg = "Hello from parent via inherited fd!\n";
            write(pipe_fds[1], msg, strlen(msg));
            
            close(pipe_fds[1]);
            waitpid(pid, nullptr, 0);
        }
    }
    
    // ============================================================================
    // 8. FILE DESCRIPTOR PASSING BETWEEN PROCESSES
    // ============================================================================
    
    std::cout << "\n8. Advanced: Passing File Descriptors Between Processes:\n";
    
    // This requires UNIX domain sockets and is advanced
    // Basic concept: sendmsg()/recvmsg() with ancillary data
    
    // ============================================================================
    // 9. SECURING FILE DESCRIPTORS
    // ============================================================================
    
    std::cout << "\n9. Securing File Descriptors:\n";
    
    // Open sensitive file
    fd = open("sensitive.txt", O_WRONLY | O_CREAT | O_TRUNC, 0600);  // Owner RW only
    
    // Lower privileges if running as root
    if (geteuid() == 0) {
        // Drop root privileges
        if (setuid(1000) == 0) {  // Change to normal user
            std::cout << "Dropped root privileges\n";
        }
    }
    
    // File descriptor is still open even after privilege drop
    write(fd, "Sensitive data\n", 15);
    
    // Important: close file descriptors before exec
    fcntl(fd, F_SETFD, FD_CLOEXEC);  // Auto-close on exec
    
    close(fd);
    
    // Clean up
    unlink("test1.txt");
    unlink("test2.txt");
    unlink("test3.txt");
    unlink("original.txt");
    unlink("output.txt");
    unlink("flags.txt");
    unlink("nonblock.txt");
    unlink("sensitive.txt");
    
    for (int i = 0; i < 1000; i++) {
        std::string filename = "temp_" + std::to_string(i) + ".txt";
        unlink(filename.c_str());
    }
}

#include <iostream>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <cstring>
#include <vector>
#include <random>
#include <algorithm>

void demonstrate_memory_mapped_files() {
    std::cout << "\n=== MEMORY-MAPPED FILES ===\n";
    
    const char* filename = "memory_mapped_example.dat";
    size_t file_size = 1024 * 1024;  // 1MB
    
    // ============================================================================
    // 1. BASIC MEMORY MAPPING
    // ============================================================================
    
    std::cout << "\n1. Basic Memory Mapping:\n";
    
    // Create or open file
    int fd = open(filename, O_RDWR | O_CREAT | O_TRUNC, 0644);
    if (fd == -1) {
        perror("open failed");
        return;
    }
    
    // Extend file to desired size
    if (ftruncate(fd, file_size) == -1) {
        perror("ftruncate failed");
        close(fd);
        return;
    }
    
    // Map file into memory
    void* mapped = mmap(
        nullptr,            // Let OS choose address
        file_size,          // Map entire file
        PROT_READ | PROT_WRITE,  // Read/write access
        MAP_SHARED,         // Changes visible to other processes
        fd,                 // File descriptor
        0                   // Offset from start
    );
    
    if (mapped == MAP_FAILED) {
        perror("mmap failed");
        close(fd);
        return;
    }
    
    std::cout << "File mapped at address: " << mapped << "\n";
    std::cout << "File size: " << file_size << " bytes\n";
    
    // Use mapped memory like regular memory
    char* data = static_cast<char*>(mapped);
    
    // Write data directly to memory (automatically goes to file)
    const char* message = "Hello from memory-mapped file!\n";
    strcpy(data, message);
    
    // Read from memory (reads from file)
    std::cout << "Read from memory map: " << data;
    
    // ============================================================================
    // 2. LARGE FILE PROCESSING
    // ============================================================================
    
    std::cout << "\n2. Processing Large Files:\n";
    
    // Fill file with random data
    std::mt19937 rng(std::random_device{}());
    std::uniform_int_distribution<int> dist(0, 255);
    
    for (size_t i = 0; i < file_size; i++) {
        data[i] = static_cast<char>(dist(rng));
    }
    
    // Process data in memory (very fast!)
    size_t count_zeros = 0;
    for (size_t i = 0; i < file_size; i++) {
        if (data[i] == 0) {
            count_zeros++;
        }
    }
    
    std::cout << "Found " << count_zeros << " zero bytes in " 
              << file_size << " bytes\n";
    
    // Search for pattern
    const char* pattern = "PATTERN";
    char* found = static_cast<char*>(memmem(data, file_size, pattern, strlen(pattern)));
    if (found) {
        std::cout << "Found pattern at offset: " << (found - data) << "\n";
    } else {
        std::cout << "Pattern not found\n";
    }
    
    // ============================================================================
    // 3. PARTIAL MAPPING (WINDOWING)
    // ============================================================================
    
    std::cout << "\n3. Partial File Mapping (Windowing):\n";
    
    // Unmap entire file first
    munmap(mapped, file_size);
    
    // Map only part of file (64KB window)
    size_t window_size = 64 * 1024;  // 64KB
    size_t window_offset = 512 * 1024;  // Start at 512KB
    
    // Ensure offset is page-aligned
    size_t page_size = sysconf(_SC_PAGESIZE);
    window_offset = (window_offset / page_size) * page_size;
    
    mapped = mmap(
        nullptr,
        window_size,
        PROT_READ | PROT_WRITE,
        MAP_SHARED,
        fd,
        window_offset
    );
    
    if (mapped != MAP_FAILED) {
        std::cout << "Mapped 64KB window at offset " << window_offset 
                  << ", address: " << mapped << "\n";
        
        // Process this window
        data = static_cast<char*>(mapped);
        data[0] = 'W';
        data[1] = 'I';
        data[2] = 'N';
        data[3] = '\0';
        
        std::cout << "Window starts with: " << data << "\n";
        
        munmap(mapped, window_size);
    }
    
    // ============================================================================
    // 4. SHARED MEMORY BETWEEN PROCESSES
    // ============================================================================
    
    std::cout << "\n4. Shared Memory Between Processes:\n";
    
    pid_t pid = fork();
    
    if (pid == 0) {
        // Child process
        
        // Re-open and map the same file
        int child_fd = open(filename, O_RDWR);
        void* child_mapped = mmap(
            nullptr,
            file_size,
            PROT_READ | PROT_WRITE,
            MAP_SHARED,
            child_fd,
            0
        );
        
        if (child_mapped != MAP_FAILED) {
            char* child_data = static_cast<char*>(child_mapped);
            
            // Read what parent wrote
            std::cout << "Child sees: " << child_data << "\n";
            
            // Write something for parent
            strcpy(child_data + 100, "Child was here!\n");
            
            // Force changes to disk
            msync(child_mapped, file_size, MS_SYNC);
            
            munmap(child_mapped, file_size);
            close(child_fd);
        }
        
        exit(0);
    }
    else {
        // Parent process
        
        // Re-map file
        mapped = mmap(
            nullptr,
            file_size,
            PROT_READ | PROT_WRITE,
            MAP_SHARED,
            fd,
            0
        );
        
        if (mapped != MAP_FAILED) {
            data = static_cast<char*>(mapped);
            
            // Write initial data
            strcpy(data, "Parent initial data\n");
            
            // Wait for child to write
            sleep(1);
            
            // Read child's message
            std::cout << "Parent reads from offset 100: " << (data + 100);
            
            // Synchronize changes to disk
            msync(mapped, file_size, MS_SYNC);
            
            munmap(mapped, file_size);
        }
        
        waitpid(pid, nullptr, 0);
    }
    
    // ============================================================================
    // 5. ANONYMOUS MAPPING (NOT BACKED BY FILE)
    // ============================================================================
    
    std::cout << "\n5. Anonymous Memory Mapping:\n";
    
    size_t anon_size = 1024 * 1024;  // 1MB
    
    void* anon_mapped = mmap(
        nullptr,
        anon_size,
        PROT_READ | PROT_WRITE,
        MAP_PRIVATE | MAP_ANONYMOUS,  // Not backed by file
        -1,                           // No file descriptor
        0
    );
    
    if (anon_mapped != MAP_FAILED) {
        std::cout << "Anonymous memory mapped at: " << anon_mapped << "\n";
        
        // Use as regular memory
        int* numbers = static_cast<int*>(anon_mapped);
        for (size_t i = 0; i < anon_size / sizeof(int); i++) {
            numbers[i] = i * 2;
        }
        
        // Check some values
        std::cout << "numbers[0] = " << numbers[0] << "\n";
        std::cout << "numbers[100] = " << numbers[100] << "\n";
        
        // Clean up
        munmap(anon_mapped, anon_size);
    }
    
    // ============================================================================
    // 6. MEMORY PROTECTION
    // ============================================================================
    
    std::cout << "\n6. Memory Protection:\n";
    
    // Map with read-only protection
    void* ro_mapped = mmap(
        nullptr,
        4096,
        PROT_READ,           // Read only
        MAP_PRIVATE | MAP_ANONYMOUS,
        -1,
        0
    );
    
    if (ro_mapped != MAP_FAILED) {
        std::cout << "Read-only memory mapped\n";
        
        // Try to write (should fail)
        char* ro_data = static_cast<char*>(ro_mapped);
        
        // This would cause segmentation fault
        // ro_data[0] = 'X';  // DON'T UNCOMMENT - would crash
        
        // Change protection to read-write
        if (mprotect(ro_mapped, 4096, PROT_READ | PROT_WRITE) == 0) {
            std::cout << "Changed protection to read-write\n";
            ro_data[0] = 'X';  // Now safe to write
            std::cout << "Successfully wrote to memory\n";
        }
        
        munmap(ro_mapped, 4096);
    }
    
    // ============================================================================
    // 7. MEMORY ADVICE (MADVISE)
    // ============================================================================
    
    std::cout << "\n7. Memory Advice (madvise):\n";
    
    void* advised_mapped = mmap(
        nullptr,
        1024 * 1024,
        PROT_READ | PROT_WRITE,
        MAP_PRIVATE | MAP_ANONYMOUS,
        -1,
        0
    );
    
    if (advised_mapped != MAP_FAILED) {
        // Give advice to kernel about memory usage
        
        // Will need soon
        madvise(advised_mapped, 1024 * 1024, MADV_WILLNEED);
        std::cout << "MADV_WILLNEED: Pages will be needed soon\n";
        
        // Random access pattern
        madvise(advised_mapped, 1024 * 1024, MADV_RANDOM);
        std::cout << "MADV_RANDOM: Expect random page references\n";
        
        // Sequential access pattern
        madvise(advised_mapped, 1024 * 1024, MADV_SEQUENTIAL);
        std::cout << "MADV_SEQUENTIAL: Expect sequential access\n";
        
        // Don't need these pages anymore
        madvise(advised_mapped, 1024 * 1024, MADV_DONTNEED);
        std::cout << "MADV_DONTNEED: Pages can be freed\n";
        
        munmap(advised_mapped, 1024 * 1024);
    }
    
    // ============================================================================
    // 8. MEMORY LOCKING (PREVENTING SWAPPING)
    // ============================================================================
    
    std::cout << "\n8. Memory Locking (mlock):\n";
    
    void* locked_mapped = mmap(
        nullptr,
        4096,
        PROT_READ | PROT_WRITE,
        MAP_PRIVATE | MAP_ANONYMOUS,
        -1,
        0
    );
    
    if (locked_mapped != MAP_FAILED) {
        // Lock pages in memory (prevent swapping)
        if (mlock(locked_mapped, 4096) == 0) {
            std::cout << "Memory locked in RAM (won't be swapped)\n";
            
            // Use for real-time or security-sensitive data
            
            // Unlock when done
            munlock(locked_mapped, 4096);
            std::cout << "Memory unlocked\n";
        }
        
        munmap(locked_mapped, 4096);
    }
    
    // ============================================================================
    // 9. PERFORMANCE COMPARISON
    // ============================================================================
    
    std::cout << "\n9. Performance Comparison:\n";
    
    size_t large_size = 100 * 1024 * 1024;  // 100MB
    
    // Traditional file I/O
    std::cout << "Traditional file I/O...\n";
    
    int trad_fd = open("traditional.dat", O_RDWR | O_CREAT | O_TRUNC, 0644);
    ftruncate(trad_fd, large_size);
    
    char* trad_buffer = new char[large_size];
    
    // Write using write() system call
    auto start = std::chrono::high_resolution_clock::now();
    write(trad_fd, trad_buffer, large_size);
    auto end = std::chrono::high_resolution_clock::now();
    
    auto trad_time = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "Traditional write: " << trad_time.count() << " ms\n";
    
    delete[] trad_buffer;
    close(trad_fd);
    
    // Memory-mapped I/O
    std::cout << "Memory-mapped I/O...\n";
    
    int mmap_fd = open("mmap.dat", O_RDWR | O_CREAT | O_TRUNC, 0644);
    ftruncate(mmap_fd, large_size);
    
    start = std::chrono::high_resolution_clock::now();
    void* perf_mapped = mmap(nullptr, large_size, PROT_READ | PROT_WRITE, 
                             MAP_SHARED, mmap_fd, 0);
    
    if (perf_mapped != MAP_FAILED) {
        char* perf_data = static_cast<char*>(perf_mapped);
        
        // Write to memory (automatically goes to file)
        memset(perf_data, 'X', large_size);
        
        // Sync to ensure written
        msync(perf_mapped, large_size, MS_SYNC);
        
        end = std::chrono::high_resolution_clock::now();
        
        auto mmap_time = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        std::cout << "Memory-mapped write: " << mmap_time.count() << " ms\n";
        
        munmap(perf_mapped, large_size);
    }
    
    close(mmap_fd);
    
    // Clean up
    close(fd);
    unlink(filename);
    unlink("traditional.dat");
    unlink("mmap.dat");
    
    std::cout << "\nMemory-mapped files provide:\n";
    std::cout << "1. Zero-copy I/O (no buffer copying)\n";
    std::cout << "2. Direct memory access to file data\n";
    std::cout << "3. Efficient sharing between processes\n";
    std::cout << "4. Lazy loading (pages loaded on demand)\n";
    std::cout << "5. Automatic synchronization with file\n";
}

#include <iostream>
#include <csignal>
#include <unistd.h>
#include <cstring>
#include <sys/types.h>
#include <sys/wait.h>
#include <atomic>
#include <thread>

// Global flag for signal handler
std::atomic<bool> g_signal_received(false);

// ============================================================================
// SIGNAL HANDLERS
// ============================================================================

// Signal handler for SIGINT (Ctrl+C)
void sigint_handler(int signum) {
    std::cout << "\nCaught SIGINT (Signal " << signum << ")\n";
    std::cout << "Setting global flag...\n";
    g_signal_received = true;
}

// Signal handler for SIGTERM
void sigterm_handler(int signum) {
    std::cout << "\nCaught SIGTERM (Signal " << signum << ")\n";
    std::cout << "Performing cleanup...\n";
    
    // Async-signal-safe operations only!
    const char* msg = "Cleanup completed\n";
    write(STDOUT_FILENO, msg, strlen(msg));
    
    exit(0);
}

// Signal handler with context information
void sigaction_handler(int signum, siginfo_t* info, void* context) {
    std::cout << "\nAdvanced handler caught signal " << signum << "\n";
    
    // Get information about signal
    std::cout << "Signal information:\n";
    std::cout << "  PID of sender: " << info->si_pid << "\n";
    std::cout << "  UID of sender: " << info->si_uid << "\n";
    
    if (info->si_code == SI_USER) {
        std::cout << "  Sent by kill()\n";
    } else if (info->si_code == SI_QUEUE) {
        std::cout << "  Sent by sigqueue()\n";
        std::cout << "  Signal value: " << info->si_value.sival_int << "\n";
    }
    
    g_signal_received = true;
}

// ============================================================================
// ASYNC-SIGNAL-SAFE FUNCTIONS DEMONSTRATION
// ============================================================================

// List of async-signal-safe functions
void list_async_signal_safe_functions() {
    std::cout << "\nAsync-signal-safe functions (can be called from signal handlers):\n";
    std::cout << "------------------------------------------------------------------\n";
    std::cout << "  _Exit()           - Immediate termination\n";
    std::cout << "  _exit()           - Immediate termination\n";
    std::cout << "  abort()           - Abnormal termination\n";
    std::cout << "  accept()          - Accept connection\n";
    std::cout << "  access()          - Check file accessibility\n";
    std::cout << "  aio_error()       - Asynchronous I/O error status\n";
    std::cout << "  aio_return()      - Asynchronous I/O return status\n";
    std::cout << "  aio_suspend()     - Wait for async I/O\n";
    std::cout << "  alarm()           - Set alarm clock\n";
    std::cout << "  bind()            - Bind socket\n";
    std::cout << "  cfgetispeed()     - Get input baud rate\n";
    std::cout << "  cfgetospeed()     - Get output baud rate\n";
    std::cout << "  cfsetispeed()     - Set input baud rate\n";
    std::cout << "  cfsetospeed()     - Set output baud rate\n";
    std::cout << "  chdir()           - Change directory\n";
    std::cout << "  chmod()           - Change file mode\n";
    std::cout << "  chown()           - Change file owner\n";
    std::cout << "  clock_gettime()   - Get clock time\n";
    std::cout << "  close()           - Close file descriptor\n";
    std::cout << "  connect()         - Connect socket\n";
    std::cout << "  creat()           - Create file\n";
    std::cout << "  dup()             - Duplicate file descriptor\n";
    std::cout << "  dup2()            - Duplicate file descriptor to specific number\n";
    std::cout << "  execle()          - Execute program\n";
    std::cout << "  execve()          - Execute program\n";
    std::cout << "  fchmod()          - Change file mode\n";
    std::cout << "  fchown()          - Change file owner\n";
    std::cout << "  fcntl()           - File control\n";
    std::cout << "  fdatasync()       - Synchronize file data\n";
    std::cout << "  fork()            - Create process\n";
    std::cout << "  fpathconf()       - Get configurable path variables\n";
    std::cout << "  fstat()           - Get file status\n";
    std::cout << "  fsync()           - Synchronize file\n";
    std::cout << "  ftruncate()       - Truncate file\n";
    std::cout << "  getegid()         - Get effective group ID\n";
    std::cout << "  geteuid()         - Get effective user ID\n";
    std::cout << "  getgid()          - Get real group ID\n";
    std::cout << "  getgroups()       - Get supplementary group IDs\n";
    std::cout << "  getpeername()     - Get peer socket name\n";
    std::cout << "  getpgrp()         - Get process group ID\n";
    std::cout << "  getpid()          - Get process ID\n";
    std::cout << "  getppid()         - Get parent process ID\n";
    std::cout << "  getsockname()     - Get socket name\n";
    std::cout << "  getsockopt()      - Get socket options\n";
    std::cout << "  getuid()          - Get real user ID\n";
    std::cout << "  kill()            - Send signal\n";
    std::cout << "  link()            - Create link\n";
    std::cout << "  listen()          - Listen for socket connections\n";
    std::cout << "  lseek()           - Reposition file offset\n";
    std::cout << "  lstat()           - Get file status (symbolic link)\n";
    std::cout << "  mkdir()           - Create directory\n";
    std::cout << "  mkfifo()          - Create FIFO\n";
    std::cout << "  open()            - Open file\n";
    std::cout << "  pathconf()        - Get configurable path variables\n";
    std::cout << "  pause()           - Wait for signal\n";
    std::cout << "  pipe()            - Create pipe\n";
    std::cout << "  poll()            - Wait for I/O events\n";
    std::cout << "  posix_trace_event()- Trace event\n";
    std::cout << "  pselect()         - Synchronous I/O multiplexing\n";
    std::cout << "  raise()           - Send signal to self\n";
    std::cout << "  read()            - Read from file descriptor\n";
    std::cout << "  readlink()        - Read symbolic link\n";
    std::cout << "  recv()            - Receive message\n";
    std::cout << "  recvfrom()        - Receive message\n";
    std::cout << "  recvmsg()         - Receive message\n";
    std::cout << "  rename()           - Rename file\n";
    std::cout << "  rmdir()            - Remove directory\n";
    std::cout << "  select()          - Synchronous I/O multiplexing\n";
    std::cout << "  sem_post()        - Unlock semaphore\n";
    std::cout << "  send()            - Send message\n";
    std::cout << "  sendmsg()         - Send message\n";
    std::cout << "  sendto()          - Send message\n";
    std::cout << "  setgid()          - Set group ID\n";
    std::cout << "  setpgid()         - Set process group ID\n";
    std::cout << "  setsid()          - Create session\n";
    std::cout << "  setsockopt()      - Set socket options\n";
    std::cout << "  setuid()          - Set user ID\n";
    std::cout << "  shutdown()        - Shutdown socket\n";
    std::cout << "  sigaction()       - Examine/change signal action\n";
    std::cout << "  sigaddset()       - Add signal to set\n";
    std::cout << "  sigdelset()       - Delete signal from set\n";
    std::cout << "  sigemptyset()     - Initialize empty signal set\n";
    std::cout << "  sigfillset()      - Initialize full signal set\n";
    std::cout << "  sigismember()     - Test for signal in set\n";
    std::cout << "  signal()          - Signal handling (obsolescent)\n";
    std::cout << "  sigpause()        - Wait for signal\n";
    std::cout << "  sigpending()      - Examine pending signals\n";
    std::cout << "  sigprocmask()     - Examine/change blocked signals\n";
    std::cout << "  sigqueue()        - Queue signal with data\n";
    std::cout << "  sigset()          - Signal handling\n";
    std::cout << "  sigsuspend()      - Wait for signal\n";
    std::cout << "  sleep()           - Sleep for seconds\n";
    std::cout << "  sockatmark()      - Test socket at out-of-band mark\n";
    std::cout << "  socket()          - Create socket\n";
    std::cout << "  socketpair()      - Create pair of sockets\n";
    std::cout << "  stat()            - Get file status\n";
    std::cout << "  symlink()         - Create symbolic link\n";
    std::cout << "  sysconf()         - Get system configuration\n";
    std::cout << "  tcdrain()         - Wait for transmission completion\n";
    std::cout << "  tcflow()          - Suspend/resume transmission\n";
    std::cout << "  tcflush()         - Flush terminal I/O\n";
    std::cout << "  tcgetattr()       - Get terminal attributes\n";
    std::cout << "  tcgetpgrp()       - Get foreground process group ID\n";
    std::cout << "  tcsendbreak()     - Send break\n";
    std::cout << "  tcsetattr()       - Set terminal attributes\n";
    std::cout << "  tcsetpgrp()       - Set foreground process group ID\n";
    std::cout << "  time()            - Get time\n";
    std::cout << "  timer_getoverrun()- Get timer overrun count\n";
    std::cout << "  timer_gettime()   - Get timer value\n";
    std::cout << "  timer_settime()   - Set timer\n";
    std::cout << "  times()           - Get process times\n";
    std::cout << "  umask()           - Set file mode creation mask\n";
    std::cout << "  uname()           - Get system name\n";
    std::cout << "  unlink()          - Remove directory entry\n";
    std::cout << "  utime()           - Set file access/modification times\n";
    std::cout << "  wait()            - Wait for process termination\n";
    std::cout << "  waitpid()         - Wait for specific process\n";
    std::cout << "  write()           - Write to file descriptor\n";
    std::cout << "------------------------------------------------------------------\n";
}

void demonstrate_signals() {
    std::cout << "\n=== SIGNALS AND SIGNAL HANDLING ===\n";
    
    // ============================================================================
    // 1. BASIC SIGNAL HANDLING WITH signal()
    // ============================================================================
    
    std::cout << "\n1. Basic Signal Handling (signal()):\n";
    
    // Install signal handler for SIGINT (Ctrl+C)
    if (signal(SIGINT, sigint_handler) == SIG_ERR) {
        perror("signal() failed");
    } else {
        std::cout << "SIGINT handler installed. Press Ctrl+C to test...\n";
        
        // Wait for signal
        for (int i = 0; i < 10 && !g_signal_received; i++) {
            std::cout << "Waiting... (" << i << ")\n";
            sleep(1);
        }
        
        if (g_signal_received) {
            std::cout << "Signal was received!\n";
        } else {
            std::cout << "No signal received\n";
        }
        
        g_signal_received = false;
    }
    
    // ============================================================================
    // 2. ADVANCED SIGNAL HANDLING WITH sigaction()
    // ============================================================================
    
    std::cout << "\n2. Advanced Signal Handling (sigaction()):\n";
    
    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));
    
    // Use SA_SIGINFO to get additional information
    sa.sa_sigaction = sigaction_handler;
    sa.sa_flags = SA_SIGINFO | SA_RESTART;  // SA_RESTART restarts interrupted syscalls
    
    // Block other signals while handler runs
    sigemptyset(&sa.sa_mask);
    sigaddset(&sa.sa_mask, SIGTERM);
    
    if (sigaction(SIGUSR1, &sa, nullptr) == -1) {
        perror("sigaction() failed");
    } else {
        std::cout << "SIGUSR1 handler installed with SA_SIGINFO\n";
        
        // Test sending signal with data
        pid_t pid = getpid();
        
        union sigval value;
        value.sival_int = 42;
        
        if (sigqueue(pid, SIGUSR1, value) == 0) {
            std::cout << "Sent SIGUSR1 with value 42\n";
        }
        
        // Give handler time to run
        sleep(1);
    }
    
    // ============================================================================
    // 3. SIGNAL MASK AND BLOCKING
    // ============================================================================
    
    std::cout << "\n3. Signal Mask and Blocking:\n";
    
    sigset_t block_set, old_set;
    
    // Create empty signal set
    sigemptyset(&block_set);
    
    // Add signals to block
    sigaddset(&block_set, SIGINT);
    sigaddset(&block_set, SIGTERM);
    
    // Block signals
    if (sigprocmask(SIG_BLOCK, &block_set, &old_set) == -1) {
        perror("sigprocmask() failed");
    } else {
        std::cout << "Blocked SIGINT and SIGTERM\n";
        std::cout << "Press Ctrl+C now (signal will be blocked)...\n";
        sleep(3);
        
        // Check pending signals
        sigset_t pending;
        sigpending(&pending);
        
        if (sigismember(&pending, SIGINT)) {
            std::cout << "SIGINT is pending (blocked but received)\n";
        }
        
        // Unblock signals
        std::cout << "Unblocking signals...\n";
        sigprocmask(SIG_SETMASK, &old_set, nullptr);
        
        // Pending signal will be delivered now
        sleep(1);
    }
    
    // ============================================================================
    // 4. SIGNAL SAFE HANDLER
    // ============================================================================
    
    std::cout << "\n4. Async-Signal-Safe Handler:\n";
    
    // Install handler for SIGTERM
    struct sigaction sa_safe;
    memset(&sa_safe, 0, sizeof(sa_safe));
    sa_safe.sa_handler = sigterm_handler;
    
    if (sigaction(SIGTERM, &sa_safe, nullptr) == 0) {
        std::cout << "SIGTERM handler installed (uses write() not cout)\n";
        
        // Send SIGTERM to ourselves
        kill(getpid(), SIGTERM);
        
        // This won't execute because exit() is called in handler
        sleep(1);
    }
    
    // ============================================================================
    // 5. SIGCHLD AND ZOMBIE PROCESS PREVENTION
    // ============================================================================
    
    std::cout << "\n5. SIGCHLD and Zombie Prevention:\n";
    
    // Handler for SIGCHLD (child process terminated)
    auto sigchld_handler = [](int signum) {
        // Reap all terminated children
        pid_t pid;
        int status;
        
        while ((pid = waitpid(-1, &status, WNOHANG)) > 0) {
            const char* msg = "Child process reaped\n";
            write(STDOUT_FILENO, msg, strlen(msg));
        }
    };
    
    struct sigaction sa_chld;
    memset(&sa_chld, 0, sizeof(sa_chld));
    sa_chld.sa_handler = sigchld_handler;
    sa_chld.sa_flags = SA_RESTART | SA_NOCLDSTOP;
    
    if (sigaction(SIGCHLD, &sa_chld, nullptr) == 0) {
        std::cout << "SIGCHLD handler installed\n";
        
        // Create child that exits immediately
        pid_t pid = fork();
        
        if (pid == 0) {
            // Child
            std::cout << "Child process exiting\n";
            exit(0);
        } else {
            // Parent
            std::cout << "Parent waiting for SIGCHLD...\n";
            sleep(2);
        }
    }
    
    // ============================================================================
    // 6. SIGNAL IGNORING AND DEFAULT ACTIONS
    // ============================================================================
    
    std::cout << "\n6. Ignoring Signals and Default Actions:\n";
    
    // Ignore SIGPIPE (broken pipe)
    signal(SIGPIPE, SIG_IGN);
    std::cout << "SIGPIPE set to SIG_IGN (ignore)\n";
    
    // Restore default action
    signal(SIGPIPE, SIG_DFL);
    std::cout << "SIGPIPE restored to SIG_DFL (default)\n";
    
    // Default actions for common signals
    std::cout << "\nDefault signal actions:\n";
    std::cout << "  SIGINT  - Terminate          (Ctrl+C)\n";
    std::cout << "  SIGTERM - Terminate          (kill default)\n";
    std::cout << "  SIGKILL - Terminate (cannot catch)\n";
    std::cout << "  SIGSTOP - Stop (cannot catch)\n";
    std::cout << "  SIGCONT - Continue           (resume)\n";
    std::cout << "  SIGCHLD - Ignore             (child status change)\n";
    std::cout << "  SIGPIPE - Terminate          (broken pipe)\n";
    std::cout << "  SIGALRM - Terminate          (alarm clock)\n";
    std::cout << "  SIGUSR1 - Terminate          (user-defined)\n";
    std::cout << "  SIGUSR2 - Terminate          (user-defined)\n";
    
    // ============================================================================
    // 7. SIGALRM FOR TIMEOUTS
    // ============================================================================
    
    std::cout << "\n7. SIGALRM for Timeouts:\n";
    
    // Handler for alarm
    auto alarm_handler = [](int signum) {
        const char* msg = "ALARM! Timeout reached\n";
        write(STDOUT_FILENO, msg, strlen(msg));
    };
    
    signal(SIGALRM, alarm_handler);
    
    // Set alarm for 3 seconds
    std::cout << "Setting alarm for 3 seconds...\n";
    alarm(3);
    
    // Do some work
    std::cout << "Working...\n";
    for (int i = 0; i < 5; i++) {
        std::cout << "Step " << i << "\n";
        sleep(1);
    }
    
    // Cancel alarm
    alarm(0);
    
    // ============================================================================
    // 8. SIGNAL RESTART FLAG
    // ============================================================================
    
    std::cout << "\n8. SA_RESTART Flag:\n";
    
    struct sigaction sa_restart;
    memset(&sa_restart, 0, sizeof(sa_restart));
    sa_restart.sa_handler = [](int) { std::cout << "Signal received\n"; };
    sa_restart.sa_flags = SA_RESTART;
    
    if (sigaction(SIGUSR2, &sa_restart, nullptr) == 0) {
        std::cout << "Handler with SA_RESTART installed\n";
        std::cout << "System calls interrupted by this signal will be restarted\n";
    }
    
    // ============================================================================
    // 9. SIGSEGV AND SIGFPE HANDLING
    // ============================================================================
    
    std::cout << "\n9. Handling Fatal Signals (SIGSEGV, SIGFPE):\n";
    
    // Handler for segmentation fault
    auto segv_handler = [](int signum) {
        const char* msg = "Segmentation fault! Attempting cleanup...\n";
        write(STDERR_FILENO, msg, strlen(msg));
        
        // Attempt emergency cleanup
        const char* cleanup_msg = "Emergency cleanup complete\n";
        write(STDERR_FILENO, cleanup_msg, strlen(cleanup_msg));
        
        // Exit or do longjmp to recover
        _exit(1);
    };
    
    // Handler for floating point exception
    auto fpe_handler = [](int signum) {
        const char* msg = "Floating point exception\n";
        write(STDERR_FILENO, msg, strlen(msg));
        
        // Could set flag and use siglongjmp to recover
        _exit(1);
    };
    
    signal(SIGSEGV, segv_handler);
    signal(SIGFPE, fpe_handler);
    
    std::cout << "SIGSEGV and SIGFPE handlers installed\n";
    std::cout << "Note: Some signals are difficult to recover from\n";
    
    // ============================================================================
    // 10. SIGNAL SAFE FUNCTIONS DEMONSTRATION
    // ============================================================================
    
    std::cout << "\n10. Async-Signal-Safe Functions:\n";
    
    list_async_signal_safe_functions();
    
    // Demonstrate safe vs unsafe operations
    std::cout << "\nExample: Safe vs Unsafe Signal Handler\n";
    std::cout << "----------------------------------------\n";
    
    std::cout << "UNSAFE (DO NOT DO THIS):\n";
    std::cout << "void handler(int sig) {\n";
    std::cout << "    std::cout << \"Signal \" << sig << std::endl;  // UNSAFE!\n";
    std::cout << "    std::vector<int> v;                         // UNSAFE!\n";
    std::cout << "    v.push_back(42);                           // UNSAFE!\n";
    std::cout << "    malloc(100);                               // UNSAFE!\n";
    std::cout << "}\n\n";
    
    std::cout << "SAFE (CORRECT):\n";
    std::cout << "void handler(int sig) {\n";
    std::cout << "    const char* msg = \"Signal received\\n\";\n";
    std::cout << "    write(STDOUT_FILENO, msg, strlen(msg));    // SAFE!\n";
    std::cout << "    volatile sig_atomic_t flag = 1;            // SAFE!\n";
    std::cout << "    _exit(1);                                  // SAFE!\n";
    std::cout << "}\n";
    
    // ============================================================================
    // 11. SIGACTION WITH SIGINFO EXAMPLE
    // ============================================================================
    
    std::cout << "\n11. Real-world Example: Signal with Data:\n";
    
    struct sigaction sa_example;
    memset(&sa_example, 0, sizeof(sa_example));
    
    sa_example.sa_sigaction = [](int sig, siginfo_t* info, void* context) {
        const char* msg = "Real-time signal with data: ";
        write(STDOUT_FILENO, msg, strlen(msg));
        
        char buffer[20];
        int len = snprintf(buffer, sizeof(buffer), "%d\n", info->si_value.sival_int);
        write(STDOUT_FILENO, buffer, len);
    };
    
    sa_example.sa_flags = SA_SIGINFO;
    
    if (sigaction(SIGRTMIN, &sa_example, nullptr) == 0) {
        // Send signal with data
        union sigval value;
        value.sival_int = 12345;
        
        if (sigqueue(getpid(), SIGRTMIN, value) == 0) {
            std::cout << "Sent real-time signal with data 12345\n";
            sleep(1);
        }
    }
    
    // ============================================================================
    // 12. SIGNAL BEST PRACTICES
    // ============================================================================
    
    std::cout << "\n12. Signal Handling Best Practices:\n";
    std::cout << "------------------------------------\n";
    
    std::cout << "1. Use sigaction() instead of signal()\n";
    std::cout << "2. Keep signal handlers short and simple\n";
    std::cout << "3. Use only async-signal-safe functions\n";
    std::cout << "4. Set SA_RESTART flag for most handlers\n";
    std::cout << "5. Block signals during critical sections\n";
    std::cout << "6. Use sig_atomic_t for flags shared with handlers\n";
    std::cout << "7. Re-install handlers that get reset\n";
    std::cout << "8. Handle EINTR from system calls\n";
    std::cout << "9. Use SIGCHLD to reap child processes\n";
    std::cout << "10. Be careful with signals in multithreaded programs\n";
    
    // Clean up signal handlers
    signal(SIGINT, SIG_DFL);
    signal(SIGTERM, SIG_DFL);
    signal(SIGUSR1, SIG_DFL);
    signal(SIGUSR2, SIG_DFL);
    signal(SIGALRM, SIG_DFL);
    signal(SIGCHLD, SIG_DFL);
    signal(SIGSEGV, SIG_DFL);
    signal(SIGFPE, SIG_DFL);
    
    std::cout << "\nAll signal handlers restored to default\n";
}

int main() {
    std::cout << "=== SYSTEM PROGRAMMING IN C++ - COMPLETE GUIDE ===\n";
    
    demonstrate_posix_apis();
    
    #ifdef _WIN32
    demonstrate_windows_apis();
    #endif
    
    demonstrate_process_management();
    demonstrate_file_descriptors();
    demonstrate_memory_mapped_files();
    demonstrate_networking_basics();
    demonstrate_ipc();
    demonstrate_signals();
    
    std::cout << "\n=== ALL DEMONSTRATIONS COMPLETED ===\n";
    
    return 0;
}