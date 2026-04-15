#include <cstdint>
#include <cstring>
#include <iostream>
#include <vector>

/*
    We define a very simple custom image format:

    [ Header ][ Pixel Data ]

    Header layout (packed manually in memory, NOT using pragma pack):
    - 4 bytes: width  (uint32_t)
    - 4 bytes: height (uint32_t)
    - 1 byte : bits per pixel (bpp)

    Pixel data:
    - For bpp = 1 → each bit = one pixel
    - So 8 pixels per byte
*/

struct ImageHeader {
    uint32_t width;
    uint32_t height;
    uint8_t bpp;
};

/*
    Processes pixel data assuming 1-bit per pixel.

    pixels → pointer to start of pixel data
    size   → size of pixel buffer in bytes
*/
void processPixels(const uint8_t* pixels, size_t size, const ImageHeader& header) {
    // Total number of pixels in the image
    size_t totalPixels = static_cast<size_t>(header.width) * header.height;

    std::cout << "\nProcessed Image (inverted):\n";

    for (size_t i = 0; i < totalPixels; ++i) {

        // Each byte holds 8 pixels → find which byte this pixel belongs to
        size_t byteIndex = i / 8;

        // Which bit inside that byte (0–7)
        size_t bitIndex = i % 8;

        // Safety check (avoid reading out of bounds)
        if (byteIndex >= size) {
            std::cerr << "Error: pixel index out of bounds\n";
            return;
        }

        uint8_t byte = pixels[byteIndex];

        /*
            Extract the correct bit:

            Example:
                byte = 10101010
                bitIndex = 0 → we want the LEFTMOST bit (MSB)

            So we shift right by (7 - bitIndex):
                (byte >> (7 - bitIndex)) & 1
        */
        bool pixel = (byte >> (7 - bitIndex)) & 1;

        // Example processing: invert the pixel
        bool inverted = !pixel;

        // Print result (0 or 1)
        std::cout << inverted;

        // Newline at end of each row
        if ((i + 1) % header.width == 0)
            std::cout << "\n";
    }
}

/*
    Main processing function

    data → pointer to raw memory buffer
    size → total size of buffer
*/
void processImage(const uint8_t* data, size_t size) {

    // 1. Validate that we at least have enough bytes for a header
    if (size < sizeof(ImageHeader)) {
        std::cerr << "Invalid image: too small\n";
        return;
    }

    // 2. Copy header safely from raw memory
    //    (avoids alignment and strict aliasing issues)
    ImageHeader header;
    std::memcpy(&header, data, sizeof(ImageHeader));

    // 3. Print header info
    std::cout << "Image Info:\n";
    std::cout << "Width : " << header.width << "\n";
    std::cout << "Height: " << header.height << "\n";
    std::cout << "BPP   : " << static_cast<int>(header.bpp) << "\n";

    // 4. Validate supported format
    if (header.bpp != 1) {
        std::cerr << "Only 1-bit images supported in this example\n";
        return;
    }

    // 5. Compute where pixel data starts
    const uint8_t* pixels = data + sizeof(ImageHeader);

    // 6. Compute pixel data size
    size_t pixelDataSize = size - sizeof(ImageHeader);

    // 7. Process pixel data
    processPixels(pixels, pixelDataSize, header);
}

/*
    Helper function to build a fake image buffer in memory.

    This simulates what you might read from a file or network.
*/
std::vector<uint8_t> createTestImage() {
    std::vector<uint8_t> buffer;

    uint32_t width = 8;
    uint32_t height = 2;
    uint8_t bpp = 1;

    // --- Append header (little-endian) ---

    // Copy width (4 bytes)
    buffer.insert(buffer.end(),
                  reinterpret_cast<uint8_t*>(&width),
                  reinterpret_cast<uint8_t*>(&width) + sizeof(width));

    // Copy height (4 bytes)
    buffer.insert(buffer.end(),
                  reinterpret_cast<uint8_t*>(&height),
                  reinterpret_cast<uint8_t*>(&height) + sizeof(height));

    // Copy bpp (1 byte)
    buffer.push_back(bpp);

    /*
        Pixel data:

        Row 1: 10101010
        Row 2: 11001100

        Each row = 8 pixels = 1 byte
    */

    buffer.push_back(0b10101010);
    buffer.push_back(0b11001100);

    return buffer;
}

int main() {

    // Create fake image in memory
    std::vector<uint8_t> image = createTestImage();

    // Pass raw pointer + size to processing function
    processImage(image.data(), image.size());

    return 0;
}