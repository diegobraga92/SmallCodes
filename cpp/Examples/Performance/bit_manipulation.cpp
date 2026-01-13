#include <cstdint>
#include <iostream>
#include <bit>
#include <arpa/inet.h> // htonl / ntohl (POSIX)

/* ============================================================
   SECTION 1: FLAGS AND MASKS
   ============================================================ */

// Flags are usually powers of two
enum Permissions : uint32_t {
    READ  = 1u << 0,  // 0001
    WRITE = 1u << 1,  // 0010
    EXEC  = 1u << 2   // 0100
};

/* ============================================================
   SECTION 2: BASIC BIT OPERATIONS
   ============================================================ */

inline void set_bit(uint32_t& x, int bit) {
    x |= (1u << bit);
}

inline void clear_bit(uint32_t& x, int bit) {
    x &= ~(1u << bit);
}

inline void toggle_bit(uint32_t& x, int bit) {
    x ^= (1u << bit);
}

inline bool test_bit(uint32_t x, int bit) {
    return (x >> bit) & 1u;
}

/* ============================================================
   SECTION 3: BIT FIELD EXTRACTION / INSERTION
   ============================================================ */

// Extract bits [shift, shift + width)
inline uint32_t extract_field(uint32_t value, int shift, uint32_t mask) {
    return (value >> shift) & mask;
}

// Insert field into value
inline void insert_field(uint32_t& value, uint32_t field,
                         int shift, uint32_t mask) {
    value &= ~(mask << shift);            // clear field
    value |= (field & mask) << shift;     // insert new value
}

/* ============================================================
   SECTION 4: PACKING / UNPACKING DATA
   ============================================================ */

// Pack two 16-bit values into one 32-bit value
uint32_t pack_u16(uint16_t hi, uint16_t lo) {
    return (uint32_t(hi) << 16) | lo;
}

void unpack_u16(uint32_t v, uint16_t& hi, uint16_t& lo) {
    hi = uint16_t(v >> 16);
    lo = uint16_t(v & 0xFFFF);
}

/* ============================================================
   SECTION 5: MANUAL BITFIELD PACKING (PORTABLE)
   ============================================================ */

// Layout: [ version:4 | flags:4 | length:8 ]
struct Header {
    uint16_t raw{0};

    uint8_t version() const { return (raw >> 12) & 0xF; }
    uint8_t flags()   const { return (raw >> 8)  & 0xF; }
    uint8_t length()  const { return raw & 0xFF; }

    void set_version(uint8_t v) {
        raw = (raw & 0x0FFF) | ((v & 0xF) << 12);
    }

    void set_flags(uint8_t f) {
        raw = (raw & 0xF0FF) | ((f & 0xF) << 8);
    }

    void set_length(uint8_t l) {
        raw = (raw & 0xFF00) | l;
    }
};

/* ============================================================
   SECTION 6: C++ BITFIELDS (NON-PORTABLE, EDUCATIONAL)
   ============================================================ */

// ⚠ Layout is compiler- and endian-dependent
struct BitfieldExample {
    uint8_t a : 3;
    uint8_t b : 5;
};

/* ============================================================
   SECTION 7: ENDIANNESS
   ============================================================ */

constexpr bool is_little_endian() {
    return uint16_t{1} ==
           *reinterpret_cast<const uint8_t*>(&uint16_t{1});
}

// Manual byte swap
uint32_t bswap32(uint32_t x) {
    return (x >> 24) |
          ((x >> 8)  & 0x0000FF00) |
          ((x << 8)  & 0x00FF0000) |
           (x << 24);
}

/* ============================================================
   SECTION 8: ALIGNMENT HELPERS
   ============================================================ */

uint32_t align_up(uint32_t x, uint32_t alignment) {
    return (x + alignment - 1) & ~(alignment - 1);
}

/* ============================================================
   SECTION 9: READ-MODIFY-WRITE SAFE PATTERNS
   ============================================================ */

void set_bits(uint32_t& x, uint32_t mask) {
    x |= mask;
}

void clear_bits(uint32_t& x, uint32_t mask) {
    x &= ~mask;
}

/* ============================================================
   SECTION 10: DEMO / MAIN
   ============================================================ */

int main() {
    std::cout << "=== FLAGS ===\n";
    uint32_t perms = 0;
    perms |= READ | WRITE;
    std::cout << "READ? " << bool(perms & READ) << "\n";
    clear_bits(perms, WRITE);
    std::cout << "WRITE? " << bool(perms & WRITE) << "\n";

    std::cout << "\n=== BIT OPERATIONS ===\n";
    uint32_t x = 0;
    set_bit(x, 3);
    toggle_bit(x, 3);
    std::cout << "Bit 3 set? " << test_bit(x, 3) << "\n";

    std::cout << "\n=== PACK / UNPACK ===\n";
    uint32_t packed = pack_u16(0xABCD, 0x1234);
    uint16_t hi, lo;
    unpack_u16(packed, hi, lo);
    std::cout << std::hex << hi << " " << lo << "\n";

    std::cout << "\n=== MANUAL BITFIELD ===\n";
    Header h;
    h.set_version(3);
    h.set_flags(5);
    h.set_length(128);
    std::cout << "version=" << int(h.version())
              << " flags=" << int(h.flags())
              << " length=" << int(h.length()) << "\n";

    std::cout << "\n=== ENDIANNESS ===\n";
    std::cout << "Little endian? " << is_little_endian() << "\n";

    uint32_t v = 0x12345678;
    std::cout << "bswap32: 0x" << std::hex << bswap32(v) << "\n";

    uint32_t net = htonl(v);
    std::cout << "htonl: 0x" << net << "\n";
    std::cout << "ntohl: 0x" << ntohl(net) << "\n";

    std::cout << "\n=== ALIGNMENT ===\n";
    std::cout << "align 13 to 8: " << align_up(13, 8) << "\n";

    std::cout << "\n=== BIT COUNT ===\n";
    std::cout << "popcount(0b10110110) = "
              << std::popcount(0b10110110) << "\n";
}
