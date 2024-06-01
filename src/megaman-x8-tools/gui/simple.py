import PySimpleGUI as sg

from core.set import SetFile, SetEnemy

set_file = SetFile(
    r"C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\game\set\Set11_00.set"
)

"""
    Demo - Drag a rectangle to draw it

    This demo shows how to use a Graph Element to (optionally) display an image and then use the
    mouse to "drag a rectangle".  This is sometimes called a rubber band and is an operation you
    see in things like editors
"""

layout = [
    [
        sg.Graph(
            canvas_size=(500, 500),
            graph_bottom_left=(-100, -100),
            graph_top_right=(1000, 1000),
            key="-GRAPH-",
            change_submits=True,  # mouse click events
            drag_submits=True,
        ),
    ],
    [sg.Text(key="info", size=(60, 1))],
    [sg.Button(key="undo")],
]

im1 = r"C:\Users\xeroj\Downloads\2_2.png"

window = sg.Window("Set Editor", layout, finalize=True)
graph: sg.Graph = window["-GRAPH-"]

grabbed_idx = None
dragging = False
start_point = end_point = None

enemy_sprites = []

for enemy in set_file.enemies:
    x = enemy.x * 5
    y = enemy.y * 5
    idx = graph.draw_circle((x, y), 4, "red")
    enemy_sprites.append([idx, enemy, x, y])

while True:
    event, values = window.read()

    if event is None:
        break  # exit

    if event == "-GRAPH-":  # if there's a "Graph" event, then it's a mouse
        x, y = values["-GRAPH-"]
        if not dragging:
            start_point = (x, y)
            # Find nearest neighbor
            closest_dist = 1000000000000000000
            grabbed_idx = -1
            for enemy_data in enemy_sprites:
                idx = enemy_data[0]
                e = enemy_data[1]
                x2 = enemy_data[2]
                y2 = enemy_data[3]
                dist = (x**2 - x2**2) + (y**2 - y2**2)
                if dist < closest_dist:
                    closest_dist = dist
                    grabbed_idx = idx

            dragging = True
        else:
            end_point = (x, y)

        if grabbed_idx and dragging:
            graph.relocate_figure(grabbed_idx, x, y)

    elif event.endswith("+UP"):  # The drawing has ended because mouse up
        info = window["info"]
        info.update(value=f"grabbed rectangle from {start_point} to {end_point}")
        start_point, end_point, grabbed_idx = (
            None,
            None,
            None,
        )  # enable grabbing a new rect
        dragging = False

    elif event == "undo":
        print("ye")

    else:
        print("unhandled event", event, values)
