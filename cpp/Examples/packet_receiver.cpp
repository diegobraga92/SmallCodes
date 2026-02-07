/*
Task Description:

Implement a PacketReceiver class that receives packet parts, verifies them,
and merges them into final messages.

Each message (packet) consists of multiple parts. Parts:
- Arrive after a StartPacket() call
- May arrive in any order
- Are identified by an id (their order in the final packet)
- Contain a string payload
- Include a controlSum that must match std::hash<std::string>(data)

Requirements:
- StartPacket() begins collecting a new packet
- Calling StartPacket() twice without receiving parts creates an empty packet
- ReceivePart():
  - Returns false if StartPacket() was never called
  - Verifies checksum; invalid parts are counted as failed
  - Overwrites parts with the same id
- GetCollectedPackets():
  - Returns all fully built packets so far
  - Does not modify internal state
  - Is idempotent if called repeatedly
- GetNumOfFailedParts():
  - Returns total number of rejected parts across all packets
*/

#include "packet_receiver.h"
#include <algorithm>
#include <functional>

void PacketReceiver::StartPacket() {
    packets_.push_back(Packet{});
    packetStarted_ = true;
}

bool PacketReceiver::ReceivePart(uint16_t id, size_t controlSum, const std::string& data) {
    if (!packetStarted_ || packets_.empty()) {
        ++failedParts_;
        return false;
    }

    if (std::hash<std::string>{}(data) != controlSum) {
        ++failedParts_;
        return false;
    }

    Packet& pkt = packets_.back();

    // Overwrite part if id already exists
    for (auto& part : pkt.parts) {
        if (part.first == id) {
            part.second = data;
            return true;
        }
    }

    pkt.parts.emplace_back(id, data);
    return true;
}

std::vector<std::string> PacketReceiver::GetCollectedPackets() const {
    std::vector<std::string> result;

    for (const auto& pkt : packets_) {
        if (pkt.parts.empty()) {
            result.emplace_back("");
            continue;
        }

        std::vector<std::pair<uint16_t, std::string>> ordered = pkt.parts;
        std::sort(ordered.begin(), ordered.end(),
                  [](const auto& a, const auto& b) {
                      return a.first < b.first;
                  });

        std::string combined;
        for (const auto& part : ordered) {
            combined += part.second;
        }

        result.push_back(combined);
    }

    return result;
}

size_t PacketReceiver::GetNumOfFailedParts() const {
    return failedParts_;
}
