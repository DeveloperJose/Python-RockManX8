from core.set import SetFile
set = SetFile(r'C:/Users/DevJ/Downloads/Set_08.set')
print(len(set.enemies))
print(set.enemies[0].id_bytes())
print(set.enemies[0].get_header())
set.enemies[0].print(0)

set.print()