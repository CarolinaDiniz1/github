"""Script to generate placeholder PNG icons for the extension."""
import struct
import zlib
import os

def create_png(size, color=(10, 102, 194)):
    """Creates a solid-color PNG."""
    w = h = size
    raw = b''
    for _ in range(h):
        raw += b'\x00'  # filter type
        for _ in range(w):
            raw += bytes(color) + b'\xff'  # RGBA

    def chunk(tag, data):
        c = struct.pack('>I', len(data)) + tag + data
        return c + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)

    ihdr_data = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    idat_data = zlib.compress(raw)

    return (b'\x89PNG\r\n\x1a\n' +
            chunk(b'IHDR', ihdr_data) +
            chunk(b'IDAT', idat_data) +
            chunk(b'IEND', b''))

os.makedirs('icons', exist_ok=True)
for size in [16, 48, 128]:
    with open(f'icons/icon{size}.png', 'wb') as f:
        f.write(create_png(size))
    print(f'Created icons/icon{size}.png')

print('Icons created successfully.')
