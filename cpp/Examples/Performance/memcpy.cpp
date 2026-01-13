#include <cstddef>
#include <cstdint>

void* memcpy_aligned(void* dst, const void* src, std::size_t n) {
    auto* d = static_cast<unsigned char*>(dst);
    auto* s = static_cast<const unsigned char*>(src);

    // 1. Copy byte-by-byte until destination is aligned
    while (n > 0 &&
           (reinterpret_cast<std::uintptr_t>(d) % alignof(std::size_t)) != 0) {
        *d++ = *s++;
        --n;
    }

    // 2. Copy word-sized chunks
    auto* dw = reinterpret_cast<std::size_t*>(d);
    auto* sw = reinterpret_cast<const std::size_t*>(s);

    while (n >= sizeof(std::size_t)) {
        *dw++ = *sw++;
        n -= sizeof(std::size_t);
    }

    // 3. Copy remaining bytes
    d = reinterpret_cast<unsigned char*>(dw);
    s = reinterpret_cast<const unsigned char*>(sw);

    while (n--) {
        *d++ = *s++;
    }

    return dst;
}
