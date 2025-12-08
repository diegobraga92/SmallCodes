// simple_binary_parser.cpp
// Compile: g++ -std=c++17 simple_binary_parser.cpp -o simple_binary_parser
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>

// --- Utilities: safe read helpers (little-endian) ---
static void read_or_throw(std::istream& in, void* dest, std::size_t bytes) {
    in.read(reinterpret_cast<char*>(dest), bytes);
    if (static_cast<std::size_t>(in.gcount()) != bytes) {
        throw std::runtime_error("unexpected EOF while reading binary data");
    }
}

static uint8_t read_u8(std::istream& in) {
    uint8_t v;
    read_or_throw(in, &v, sizeof(v));
    return v;
}

static uint16_t read_u16_le(std::istream& in) {
    uint8_t b[2];
    read_or_throw(in, b, 2);
    return static_cast<uint16_t>(b[0]) | (static_cast<uint16_t>(b[1]) << 8);
}

static uint32_t read_u32_le(std::istream& in) {
    uint8_t b[4];
    read_or_throw(in, b, 4);
    return static_cast<uint32_t>(b[0])
         | (static_cast<uint32_t>(b[1]) << 8)
         | (static_cast<uint32_t>(b[2]) << 16)
         | (static_cast<uint32_t>(b[3]) << 24);
}

static uint64_t read_u64_le(std::istream& in) {
    uint8_t b[8];
    read_or_throw(in, b, 8);
    uint64_t v = 0;
    for (int i = 0; i < 8; ++i) v |= (static_cast<uint64_t>(b[i]) << (8*i));
    return v;
}

static std::vector<uint8_t> read_bytes(std::istream& in, std::size_t len) {
    std::vector<uint8_t> v(len);
    if (len == 0) return v;
    read_or_throw(in, v.data(), len);
    return v;
}

// --- Format types ---
struct FileHeader {
    char magic[4]; // 'B','I','N','F'
    uint8_t version;
    uint8_t reserved[3];
    uint32_t record_count;
};

struct Record {
    uint32_t id;
    uint64_t timestamp;
    std::vector<uint8_t> payload;
};

// --- Parser implementation ---
class BinaryParseError : public std::runtime_error {
public:
    explicit BinaryParseError(const std::string& msg) : std::runtime_error(msg) {}
};

std::vector<Record> parse_binary_stream(std::istream& in) {
    // Read header
    char magic[4];
    read_or_throw(in, magic, 4);
    if (std::memcmp(magic, "BINF", 4) != 0) {
        throw BinaryParseError("bad magic (not BINF)");
    }

    uint8_t version = read_u8(in);
    // accept only version 1 for this simple parser
    if (version != 1) {
        throw BinaryParseError("unsupported version: " + std::to_string(version));
    }

    // skip reserved 3 bytes
    uint8_t reserved[3];
    read_or_throw(in, reserved, 3);

    uint32_t record_count = read_u32_le(in);

    // Safety: protect against absurd record_count
    const uint32_t MAX_RECORDS = 1'000'000;
    if (record_count > MAX_RECORDS) {
        throw BinaryParseError("record_count too large");
    }

    std::vector<Record> records;
    records.reserve(static_cast<std::size_t>(record_count));

    for (uint32_t i = 0; i < record_count; ++i) {
        Record r;
        r.id = read_u32_le(in);
        r.timestamp = read_u64_le(in);
        uint16_t payload_len = read_u16_le(in);

        // Safety: limit payload length (avoid allocating huge memory)
        const uint32_t MAX_PAYLOAD = 10 * 1024 * 1024; // 10 MB
        if (payload_len > MAX_PAYLOAD) {
            throw BinaryParseError("payload length too large for record " + std::to_string(i));
        }

        r.payload = read_bytes(in, payload_len);
        records.push_back(std::move(r));
    }

    // Optionally: ensure we've consumed exactly the file (or ignore trailing data)
    // if (in.peek() != EOF) { ... }

    return records;
}

// --- Helpers to write a test binary file (for demo) ---
void write_sample_file(const std::string& path) {
    std::ofstream out(path, std::ios::binary);
    if (!out) throw std::runtime_error("failed to open file for writing: " + path);

    // header
    out.write("BINF", 4);                 // magic
    uint8_t version = 1; out.put(static_cast<char>(version));
    out.put(0); out.put(0); out.put(0);   // reserved bytes
    auto write_u32_le = [&](uint32_t v){
        char b[4];
        b[0] = static_cast<char>(v & 0xff);
        b[1] = static_cast<char>((v>>8) & 0xff);
        b[2] = static_cast<char>((v>>16) & 0xff);
        b[3] = static_cast<char>((v>>24) & 0xff);
        out.write(b,4);
    };
    // We'll write 3 records
    write_u32_le(3);

    // record 1
    write_u32_le(100); // id
    auto write_u64_le = [&](uint64_t v){
        char b[8];
        for (int i=0;i<8;++i) b[i] = static_cast<char>((v >> (8*i)) & 0xff);
        out.write(b,8);
    };
    write_u64_le(1650000000000ULL);
    uint16_t payload1_len = 5;
    out.put(static_cast<char>(payload1_len & 0xff));
    out.put(static_cast<char>((payload1_len >> 8) & 0xff));
    out.write("Hello", 5);

    // record 2
    write_u32_le(200);
    write_u64_le(1650000001000ULL);
    const char* s2 = "BinaryPayload";
    uint16_t payload2_len = static_cast<uint16_t>(std::strlen(s2));
    out.put(static_cast<char>(payload2_len & 0xff));
    out.put(static_cast<char>((payload2_len >> 8) & 0xff));
    out.write(s2, payload2_len);

    // record 3 (empty payload)
    write_u32_le(300);
    write_u64_le(1650000002000ULL);
    uint16_t payload3_len = 0;
    out.put(static_cast<char>(payload3_len & 0xff));
    out.put(static_cast<char>((payload3_len >> 8) & 0xff));
    // no payload bytes

    out.close();
}

// --- Pretty print records (demo) ---
void print_records(const std::vector<Record>& recs) {
    std::cout << "Parsed " << recs.size() << " records\n";
    for (const auto& r : recs) {
        std::cout << "Record id=" << r.id << " ts=" << r.timestamp
                  << " payload_len=" << r.payload.size() << " payload=";
        // try to print printable payload as text; otherwise hex
        bool printable = true;
        for (auto b : r.payload) if (b < 0x20 || b > 0x7e) { printable = false; break; }
        if (printable && !r.payload.empty()) {
            std::string s(r.payload.begin(), r.payload.end());
            std::cout << '"' << s << '"';
        } else {
            std::cout << std::hex << std::setfill('0');
            for (auto b : r.payload) std::cout << std::setw(2) << static_cast<int>(b);
            std::cout << std::dec << std::setfill(' ');
        }
        std::cout << '\n';
    }
}

// --- Demo main: write file, read it, parse it ---
int main() {
    try {
        const std::string path = "sample.bin";
        write_sample_file(path);
        std::ifstream in(path, std::ios::binary);
        if (!in) {
            std::cerr << "failed to open " << path << '\n';
            return 1;
        }
        auto recs = parse_binary_stream(in);
        print_records(recs);
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "parse failed: " << e.what() << '\n';
        return 2;
    }
}
