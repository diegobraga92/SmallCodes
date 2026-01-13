#include <unistd.h>   // close
#include <utility>    // std::exchange
#include <stdexcept>

class UniqueFD {
public:
    // Construct empty (no fd)
    UniqueFD() noexcept = default;

    // Take ownership of an existing fd
    explicit UniqueFD(int fd) noexcept
        : fd_(fd) {}

    // Non-copyable (unique ownership)
    UniqueFD(const UniqueFD&) = delete;
    UniqueFD& operator=(const UniqueFD&) = delete;

    // Movable
    UniqueFD(UniqueFD&& other) noexcept
        : fd_(std::exchange(other.fd_, -1)) {}

    UniqueFD& operator=(UniqueFD&& other) noexcept {
        if (this != &other) {
            reset();
            fd_ = std::exchange(other.fd_, -1);
        }
        return *this;
    }

    // Destructor releases the resource
    ~UniqueFD() {
        reset();
    }

    // Access underlying fd
    int get() const noexcept {
        return fd_;
    }

    // Release ownership without closing
    int release() noexcept {
        return std::exchange(fd_, -1);
    }

    // Replace managed fd
    void reset(int new_fd = -1) noexcept {
        if (fd_ != -1) {
            ::close(fd_);
        }
        fd_ = new_fd;
    }

    // Check validity
    explicit operator bool() const noexcept {
        return fd_ != -1;
    }

private:
    int fd_{-1};
};
