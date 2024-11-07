from PIL import Image
import struct

borzoi = Image.open("borzoi.png")


BLACK = (0, 0, 0)
TAN1 = (216,206,203)
TAN2 = (186,150,123)
BLUE = (173,216,230)
COLORS = [BLACK, TAN1, TAN2, BLUE]

pal_image = Image.new("P", (1,1))
pal_image.putpalette( 
    tuple(v for c in COLORS for v in c)
     + (0,0,0)*252)
im1 = borzoi.convert("RGB").resize((64, 64)).quantize(3, method=2, palette=pal_image)
im1.show()
borzoi.close()


def pack_bits(bits):
    n = 0
    for b in range(8):
        n = n + (bits[7 - b] << b)
    return n

out = bytearray()

def get_tile(sprite_row, sprite_col):
    out = bytearray()
    left, right = bytearray(), bytearray()

    for row in range(0, 8):
        cs = [
            im1.getpixel((8 * sprite_col + col, 8 * sprite_row + row))
                    for col in range(0, 8)
        ]
        l, r = pack_bits(list(map(lambda x: x >> 1, cs))), pack_bits(list(map(lambda x: x & 1, cs)))

        left.append(l)
        right.append(r)
        # print(cs, f"{l:02X}", f"{r:02X}")


    out.extend(left)
    out.extend(right)

    return out

print(get_tile(0,1))

dump = bytearray()

with open('borzoi.bin', 'wb') as f:
    for row in range(0, 8):
        for col in range(0, 8):
            t = get_tile(row, col)
            print(t.hex(' '))
            f.write(t)