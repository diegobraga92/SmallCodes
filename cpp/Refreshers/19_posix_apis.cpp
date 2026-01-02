#include <iostream>
#include <string>
#include <vector>
#include <cstring>
#include <unistd.h>      // POSIX standard
#include <sys/types.h>   // Process types
#include <sys/stat.h>    // File status
#include <fcntl.h>       // File control
#include <dirent.h>      // Directory operations
#include <pwd.h>         // User info
#include <grp.h>         // Group info
#include <time.h>        // Time functions

void demonstrate_posix_apis() {
    std::cout << "\n=== POSIX APIs (Linux/macOS/Unix) ===\n";
    
    // ============================================================================
    // 1. PROCESS INFORMATION
    // ============================================================================
    
    std::cout << "\n1. Process Information:\n";
    
    // Get Process ID (PID)
    pid_t pid = getpid();
    pid_t ppid = getppid();  // Parent PID
    
    std::cout << "Current PID: " << pid << "\n";
    std::cout << "Parent PID: " << ppid << "\n";
    
    // Get User and Group IDs
    uid_t uid = getuid();     // Real user ID
    uid_t euid = geteuid();   // Effective user ID
    gid_t gid = getgid();     // Real group ID
    gid_t egid = getegid();   // Effective group ID
    
    std::cout << "User ID (real/effective): " << uid << "/" << euid << "\n";
    std::cout << "Group ID (real/effective): " << gid << "/" << egid << "\n";
    
    // Get user info
    struct passwd* pw = getpwuid(uid);
    if (pw) {
        std::cout << "Username: " << pw->pw_name << "\n";
        std::cout << "Home directory: " << pw->pw_dir << "\n";
        std::cout << "Shell: " << pw->pw_shell << "\n";
    }
    
    // ============================================================================
    // 2. FILE SYSTEM OPERATIONS
    // ============================================================================
    
    std::cout << "\n2. File System Operations:\n";
    
    // Create a directory
    if (mkdir("test_dir", 0755) == -1) {
        if (errno != EEXIST) {  // Ignore if already exists
            perror("mkdir failed");
        }
    } else {
        std::cout << "Directory created: test_dir\n";
    }
    
    // Get file status
    struct stat file_stat;
    if (stat(__FILE__, &file_stat) == 0) {
        std::cout << "\nFile: " << __FILE__ << "\n";
        std::cout << "Size: " << file_stat.st_size << " bytes\n";
        std::cout << "Permissions: " << std::oct << file_stat.st_mode << std::dec << "\n";
        std::cout << "Owner UID: " << file_stat.st_uid << "\n";
        std::cout << "Group GID: " << file_stat.st_gid << "\n";
        std::cout << "Last modified: " << ctime(&file_stat.st_mtime);
    }
    
    // List directory contents
    std::cout << "\nDirectory listing (current):\n";
    DIR* dir = opendir(".");
    if (dir) {
        struct dirent* entry;
        while ((entry = readdir(dir)) != nullptr) {
            // Skip . and ..
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
                continue;
            }
            
            // Get file type
            std::string type;
            switch (entry->d_type) {
                case DT_REG:  type = "File"; break;
                case DT_DIR:  type = "Directory"; break;
                case DT_LNK:  type = "Symlink"; break;
                case DT_FIFO: type = "FIFO"; break;
                case DT_SOCK: type = "Socket"; break;
                case DT_CHR:  type = "Character device"; break;
                case DT_BLK:  type = "Block device"; break;
                default:      type = "Unknown";
            }
            
            std::cout << "  " << entry->d_name << " [" << type << "]\n";
        }
        closedir(dir);
    }
    
    // Change directory
    char cwd[1024];
    if (getcwd(cwd, sizeof(cwd))) {
        std::cout << "\nCurrent directory: " << cwd << "\n";
    }
    
    // Change to test directory
    if (chdir("test_dir") == 0) {
        getcwd(cwd, sizeof(cwd));
        std::cout << "Changed to: " << cwd << "\n";
        chdir("..");  // Change back
    }
    
    // Remove directory
    rmdir("test_dir");
    std::cout << "Removed test_dir\n";
    
    // ============================================================================
    // 3. FILE I/O WITH POSIX (low-level)
    // ============================================================================
    
    std::cout << "\n3. Low-level File I/O:\n";
    
    // Create and write to file using POSIX
    int fd = open("posix_example.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd != -1) {
        const char* data = "Hello from POSIX file I/O!\n";
        ssize_t bytes_written = write(fd, data, strlen(data));
        std::cout << "Wrote " << bytes_written << " bytes\n";
        close(fd);
    }
    
    // Read from file
    fd = open("posix_example.txt", O_RDONLY);
    if (fd != -1) {
        char buffer[256];
        ssize_t bytes_read = read(fd, buffer, sizeof(buffer) - 1);
        if (bytes_read > 0) {
            buffer[bytes_read] = '\0';
            std::cout << "Read: " << buffer;
        }
        close(fd);
    }
    
    // File locking
    fd = open("locked_file.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd != -1) {
        // Set advisory lock
        struct flock lock;
        lock.l_type = F_WRLCK;    // Write lock
        lock.l_whence = SEEK_SET;
        lock.l_start = 0;
        lock.l_len = 0;           // Lock entire file
        
        if (fcntl(fd, F_SETLK, &lock) != -1) {
            std::cout << "File locked\n";
            
            // Write while locked
            write(fd, "Locked content\n", 15);
            
            // Unlock
            lock.l_type = F_UNLCK;
            fcntl(fd, F_SETLK, &lock);
            std::cout << "File unlocked\n";
        }
        close(fd);
    }
    
    // ============================================================================
    // 4. TIME AND DATE OPERATIONS
    // ============================================================================
    
    std::cout << "\n4. Time Operations:\n";
    
    // Get current time
    time_t now = time(nullptr);
    std::cout << "Current time (seconds since epoch): " << now << "\n";
    std::cout << "Formatted: " << ctime(&now);
    
    // Get high-resolution time
    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    std::cout << "Nanosecond precision: " << ts.tv_sec << "." 
              << ts.tv_nsec << " seconds\n";
    
    // Sleep operations
    std::cout << "Sleeping for 1 second...\n";
    sleep(1);  // Seconds
    
    std::cout << "Sleeping for 500 milliseconds...\n";
    usleep(500000);  // Microseconds
    
    // ============================================================================
    // 5. ENVIRONMENT VARIABLES
    // ============================================================================
    
    std::cout << "\n5. Environment Variables:\n";
    
    // Get environment variable
    const char* path = getenv("PATH");
    if (path) {
        std::cout << "PATH variable (first 100 chars): " 
                  << std::string(path, 0, 100) << "...\n";
    }
    
    const char* home = getenv("HOME");
    if (home) {
        std::cout << "Home directory: " << home << "\n";
    }
    
    // Set environment variable (affects current process and children)
    setenv("MY_VAR", "my_value", 1);  // Overwrite if exists
    
    // Check it was set
    const char* my_var = getenv("MY_VAR");
    if (my_var) {
        std::cout << "MY_VAR: " << my_var << "\n";
    }
    
    // ============================================================================
    // 6. SYSTEM RESOURCE INFORMATION
    // ============================================================================
    
    std::cout << "\n6. System Resource Information:\n";
    
    // Get system name
    char hostname[256];
    if (gethostname(hostname, sizeof(hostname)) == 0) {
        std::cout << "Hostname: " << hostname << "\n";
    }
    
    // Get page size (important for memory alignment)
    long page_size = sysconf(_SC_PAGESIZE);
    std::cout << "System page size: " << page_size << " bytes\n";
    
    // Get number of processors
    long num_processors = sysconf(_SC_NPROCESSORS_ONLN);
    std::cout << "Number of processors: " << num_processors << "\n";
    
    // Get maximum open files per process
    long max_files = sysconf(_SC_OPEN_MAX);
    std::cout << "Maximum open files per process: " << max_files << "\n";
    
    // Clean up
    unlink("posix_example.txt");
    unlink("locked_file.txt");
}