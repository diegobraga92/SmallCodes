#ifndef PACKET_RECEIVER_H
#define PACKET_RECEIVER_H

#include <vector>
#include <string>
#include <cstddef>
#include <cstdint>

class PacketReceiver {
public:
    void StartPacket();

    bool ReceivePart(uint16_t id, size_t controlSum, const std::string& data);

    std::vector<std::string> GetCollectedPackets() const;

    size_t GetNumOfFailedParts() const;

private:
    struct Packet {
        std::vector<std::pair<uint16_t, std::string>> parts;
    };

    std::vector<Packet> packets_;
    bool packetStarted_{false};
    size_t failedParts_{0};
};

#endif // PACKET_RECEIVER_H
