#include <cstddef>
#include <cstring>

class Buffer {
private:
    size_t len;
    char* data;

// This example includes RAII in the constructor and destructor
public:
    Buffer(const size_t size): len(size) {}

    Buffer(const Buffer& buf) {
        len = buf.len;
        strcpy(data, buf.data);
    }

    Buffer(Buffer&& buf) {
        len = buf.len;
        data = buf.data;
        buf.data = nullptr;
    }

    Buffer& operator=(Buffer& buf) {
        len = buf.len;
        strcpy(data, buf.data);
    }

    Buffer& operator=(Buffer&& buf) {
        if (this != &buf) {
            len = buf.len;
            data = buf.data;
            buf.data = nullptr;
        }
    }

    ~Buffer() { delete[] data; }
};