/*
Task Description:

Implement a class that helps with reading and processing image files.

Image format:
- Header consists of 5 bytes:
  - Byte 0 must be 0xFF
  - Byte 1 must be 0xAA
  - Bytes 2, 3, 4 represent the number of pixels as a 24-bit integer:
    (header[2] << 16) | (header[3] << 8) | header[4]
- Pixel data follows the header.
- Each pixel is one byte (8-bit grayscale).

Requirements:
1. Implement ImageData class that uses only the IFile interface.
2. No dynamic memory allocation (no new, malloc, etc.).
3. ParseHeaderInfo():
   - returns ImageStatus::NullFile if file pointer is null
   - returns ImageStatus::UnknownHeader if header cannot be fully read
   - returns ImageStatus::WrongHeaderTag if signature bytes are wrong
   - returns ImageStatus::ValidHeader if header is valid
4. ComputeHistogram():
   - returns ImageStatus::NullOutput if output pointer is null
   - returns ImageStatus::NullFile if file pointer is null
   - returns ImageStatus::UnknownHeader if header is not validated
   - returns ImageStatus::MissingData if pixel data is incomplete
   - returns ImageStatus::Success on success
5. Histogram size is 256 entries (0–255).
*/

#pragma once

#include <array>
#include <cstdint>
#include <cstddef>

class IFile {
public:
    virtual ~IFile() = default;
    virtual size_t Read(uint8_t* buf, size_t size) = 0;
    virtual size_t Size() const = 0;
    virtual bool SetPos(size_t pos) = 0;
    virtual bool IsEof() const = 0;
};

enum class ImageStatus {
    Unknown,
    Success,
    NullFile,
    NullOutput,
    UnknownHeader,
    WrongHeaderTag,
    ValidHeader,
    MissingData
};

class ImageData {
    static constexpr size_t HEADER_SIZE = 5;
    static constexpr size_t HIST_SIZE   = 256;
    static constexpr uint8_t HEADER_SIGNATURE[2] = {0xFF, 0xAA};

    IFile* file_{nullptr};
    bool headerValid_{false};
    size_t numPixels_{0};

public:
    explicit ImageData(IFile* newFile)
        : file_(newFile) {}

    ImageStatus ParseHeaderInfo() {
        if (!file_) {
            return ImageStatus::NullFile;
        }

        if (!file_->SetPos(0)) {
            return ImageStatus::UnknownHeader;
        }

        uint8_t header[HEADER_SIZE] = {};
        size_t readBytes = file_->Read(header, HEADER_SIZE);

        if (readBytes != HEADER_SIZE) {
            return ImageStatus::UnknownHeader;
        }

        if (header[0] != HEADER_SIGNATURE[0] ||
            header[1] != HEADER_SIGNATURE[1]) {
            return ImageStatus::WrongHeaderTag;
        }

        numPixels_ =
            (static_cast<size_t>(header[2]) << 16) |
            (static_cast<size_t>(header[3]) << 8)  |
            static_cast<size_t>(header[4]);

        headerValid_ = true;
        return ImageStatus::ValidHeader;
    }

    size_t GetNumPixels() const {
        return headerValid_ ? numPixels_ : static_cast<size_t>(-1);
    }

    ImageStatus ComputeHistogram(std::array<uint32_t, HIST_SIZE>* pOut) {
        if (!pOut) {
            return ImageStatus::NullOutput;
        }

        if (!file_) {
            return ImageStatus::NullFile;
        }

        if (!headerValid_) {
            return ImageStatus::UnknownHeader;
        }

        // Clear histogram
        for (size_t i = 0; i < HIST_SIZE; ++i) {
            (*pOut)[i] = 0;
        }

        if (!file_->SetPos(HEADER_SIZE)) {
            return ImageStatus::MissingData;
        }

        size_t pixelsRead = 0;
        uint8_t pixel = 0;

        while (pixelsRead < numPixels_) {
            size_t r = file_->Read(&pixel, 1);
            if (r != 1) {
                return ImageStatus::MissingData;
            }

            (*pOut)[pixel]++;
            pixelsRead++;
        }

        return ImageStatus::Success;
    }
};
