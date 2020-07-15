import os
from PIL import Image
from pathlib import Path
from core.wpg import WPGFile

backup_opk_folder_path = Path(r'C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\backup\opk')
opk_folder_path = Path(r'C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\game\opk')
edit_folder_path = Path(r'C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\textures')

#%% One
# fpath = Path(r'C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\game\opk\title\spa\wpg\title_ID_2D_004.wpg')
# texture_folder = edit_folder / fpath.relative_to(opk_folder).parent / fpath.stem
# wpg = WPGFile(fpath)
# # wpg.export_to_folder(texture_folder)
# wpg.import_from_folder(texture_folder)
# wpg.save()


#%% Multiple
def export_all():
    for wpg_path in backup_opk_folder_path.rglob("*.wpg"):
        wpg = WPGFile(wpg_path)
        texture_folder = edit_folder_path / wpg_path.relative_to(backup_opk_folder_path).parent / wpg_path.stem
        wpg.export_to_folder(texture_folder)
        wpg.close()


def import_all():
    for wpg_path in opk_folder_path.rglob("*.wpg"):
        wpg_local_filename = wpg_path.relative_to(opk_folder_path).parent / wpg_path.name
        texture_folder = edit_folder_path / wpg_path.relative_to(opk_folder_path).parent / wpg_path.stem

        # Open WPG from backup so all the flags and texture counts are unchanged
        wpg = WPGFile(backup_opk_folder_path / wpg_local_filename)
        wpg.import_from_folder(texture_folder)

        # Save to real game path
        wpg.save(wpg_path)
        wpg.close()
