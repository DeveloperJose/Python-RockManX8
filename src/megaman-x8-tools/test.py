from core.set import SetFile
import numpy as np

set = SetFile(
    r"C:\Users\DevJ\Downloads\original_Set08_00\X8\data\Set\Set08_00.31BF570E"
)
print(len(set.enemies))
print(set.enemies[0].id_bytes())
print(set.enemies[0].get_header())
set.enemies[0].print(0)
set.print()
print(np.unique([e.type for e in set.enemies]))
