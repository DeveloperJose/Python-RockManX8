from core.set import SetFile, SetEnemy

s1 = SetFile(
    r"C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\backup\set\Set02_00.set"
)
names = set()
enemies = []

x = 0.0
y = 0.0

for enemy in s1.enemies:
    if enemy.type in names:
        continue

    names.add(enemy.type)
    enemy.x = x
    enemy.y = y
    x += 1
    y += 0.5
    enemies.append(enemy)

enemies.sort()

print("There are", len(names), "unique enemies in", s1.stage_name)
print(enemies)

s1.enemies = enemies
s1.save(
    r"C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\game\set\Set02_00.set"
)
