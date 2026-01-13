void* memset_aligned(void* dst, int value, std::size_t n) {
    auto* d = static_cast<unsigned char*>(dst);
    unsigned char byte = static_cast<unsigned char>(value);

    // 1. Fill byte-by-byte until aligned
    while (n > 0 &&
           (reinterpret_cast<std::uintptr_t>(d) % alignof(std::size_t)) != 0) {
        *d++ = byte;
        --n;
    }

    // 2. Build word-sized fill pattern
    std::size_t pattern = 0;
    for (std::size_t i = 0; i < sizeof(std::size_t); ++i) {
        pattern = (pattern << 8) | byte;
    }

    // 3. Fill word-sized chunks
    auto* dw = reinterpret_cast<std::size_t*>(d);
    while (n >= sizeof(std::size_t)) {
        *dw++ = pattern;
        n -= sizeof(std::size_t);
    }

    // 4. Fill remaining bytes
    d = reinterpret_cast<unsigned char*>(dw);
    while (n--) {
        *d++ = byte;
    }

    return dst;
}
