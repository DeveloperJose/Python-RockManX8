import time
import random

import pyMeow as pm
import kaitaistruct
from kaitaistruct import KaitaiStream, BytesIO

from set_file import SetFile

# Read original set file
with KaitaiStream(open("Set08_00.set", 'rb')) as _io:
    booster_forest = SetFile(True, _io)
    booster_forest._read()

# Make changes to SetFile 
idx = 0
current_enemy: SetFile.Enemy = booster_forest.enemies[idx]
# current_enemy.enemy_type = "Prm0139"
current_enemy.enemy_type = random.choice(["Prm0139", "Prm0541", "Prm0227", "Prm0017"])
current_enemy.angle = -45
current_enemy.y += 1
# current_enemy.category = bytearray({ 0x45, 0x00, 0x00, 0x00 })
print(current_enemy.enemy_type)
print(current_enemy.category)
print(current_enemy.pad6)
# print(f"Original: {booster_forest.num_enemies}")

# Prepare to read game memory
proc = pm.open_process("RXC2.exe")
base = pm.get_module(proc, "RXC2.exe")["base"]
set_offset = 0x323F968

# Read set file from game memory                                                                                                        
# set_size = 0x50
# in_game_bytes = pm.r_bytes(proc, set_offset + base, booster_forest.header.file_size)
# in_game_forest = SetFile(False, KaitaiStream(BytesIO(in_game_bytes)))
# in_game_forest._read()
# in_game_forest._check()

# with open("NewSet", 'wb') as f:
#     f.write(in_game_bytes)
# print(in_game_forest.num_enemies)
# print(in_game_forest.enemies[0].enemy_type)

# Convert original SetFile to in-game SetFile
booster_forest.is_file = False
booster_forest.header2 = booster_forest.header2[-20:]
for enemy in booster_forest.enemies:
    enemy.state = SetFile.EnemyState.active

booster_forest._check()

# Convert Kaitai Struct to bytes
_io = KaitaiStream(BytesIO(bytearray(booster_forest.header.file_size)))

booster_forest._write(_io)
# print(_io.to_byte_array())

# Write changes back to memory
pm.w_bytes(proc, set_offset + base, _io.to_byte_array())

# Player manip
x, y, z  = pm.r_floats(proc, base + 0x42E19C0, 3)
camera_zoom = pm.r_float(proc, 0x047767C8)
pm.w_bool(proc, base + 0x420A888, False)
pm.w_floats(proc, base + 0x42E19C0, [-x, -y-100, -z])
# pm.w_bool(proc, base + 0x420A888, True)
# time.sleep(1)
# pm.w_floats(proc, base + 0x42E19C0, [x, y, z])
pm.w_float(proc, 0x047767C8, 40)
time.sleep(0.1)
pm.w_float(proc, 0x047767C8, camera_zoom)
pm.w_bool(proc, base + 0x420A888, True)
pm.w_floats(proc, base + 0x42E19C0, [current_enemy.x, current_enemy.y, current_enemy.z])

# Unhide player
pm.w_bool(proc, base + 0x420B66C, False)
for i in range(50):
    pm.w_floats(proc, base + 0x42E19C0, [current_enemy.x, current_enemy.y, current_enemy.z])
    time.sleep(.01) 
# pm.w_bool(proc, base + 0x420B66C, True)

# Final
idx = 0
while True:
    pm.w_floats(proc, base + 0x42E19C0, [current_enemy.x, current_enemy.y, current_enemy.z])
    idx += 1
    if idx == 10000:
        break

time.sleep(1)
x, y, z  = pm.r_floats(proc, base + 0x42E19C0, 3)
diff_x = abs(x - current_enemy.x)
diff_y = abs(y - current_enemy.y)
diff_z = abs(z - current_enemy.z)
print("Player", x, y, z)
print("Enemy1", current_enemy.x, current_enemy.y, current_enemy.z)
print("Difference", diff_x, diff_y, diff_z)
print("Done")