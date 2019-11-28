import os
from PIL import Image
from pathlib import Path
from core.wpg import WPGFile

opk_folder = Path(r'C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\game\opk')
edit_folder = Path(r'C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\textures')

#%% One
fpath = Path(r'C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\game\opk\title\spa\wpg\title_ID_2D_004.wpg')
texture_folder = edit_folder / fpath.relative_to(opk_folder).parent / fpath.stem
wpg = WPGFile(fpath)
# wpg.export_to_folder(texture_folder)
wpg.import_from_folder(texture_folder)
wpg.save()

#%% Multiple
# for fpath in opk_folder.glob('**/*.wpg'):
#     texture_folder = edit_folder / fpath.relative_to(opk_folder).parent / fpath.stem
#     wpg = WPGFile(fpath)
#     # wpg.export_to_folder(texture_folder)
#     wpg.import_from_folder(texture_folder)
#     wpg.save()