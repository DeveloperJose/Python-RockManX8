import os
for fname in os.listdir('.'):
    spl = fname.split('.')
    if len(spl) <= 1:
        continue

    ext = spl[-1]
    if ext != 'arc':
        continue

    print("[Python] Fixing ARC File ", fname)

    # ARCTool produces a 0x11 but a 0x07 is expected by the collection
    with open(fname, 'r+b') as file:
        file.seek(4)
        file.write(0x07.to_bytes(1, byteorder='little'))