import argparse
from distutils.dir_util import copy_tree
from pathlib import Path

from core.wpg import WPGFile

# https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration >= total:
        print()


def __main__():
    parser = argparse.ArgumentParser(description='Modify textures from Mega Man X8')
    parser.add_argument("option", type=str, help="Task for the editor. Either 'export' or 'import'")
    parser.add_argument("--import_folder", type=str, help="When importing, what folder you are importing")
    args = parser.parse_args()

    if args.option.lower() not in ['export', 'import']:
        print(f">> Invalid option '{args.option}' selected")
        return

    # Look for the opk
    opk_path = Path('opk')
    if not opk_path.exists():
        print(">> opk folder not found, please place this script in the root directory of the game files")
        return

    backup_opk = Path('backup_opk')
    if not backup_opk.exists():
        print(">> Making backup folder")
        copy_tree(str(opk_path), str(backup_opk))

    export_dir = Path('exported_textures')
    if not export_dir.exists():
        print(">> Creating 'exported_textures' folder")
        export_dir.mkdir()

    if args.option.lower() == 'export':
        all_wpg_files = list(backup_opk.rglob("*.wpg"))
        for idx, wpg_backup_path in enumerate(all_wpg_files):
            printProgressBar(idx, len(all_wpg_files), '>> Exporting all textures (*.wpg) to "exported_textures" directory')
            wpg = WPGFile(wpg_backup_path)
            texture_folder = export_dir / wpg_backup_path.relative_to(backup_opk).parent / wpg_backup_path.stem
            wpg.export_to_folder(texture_folder)
            wpg.close()

        print(">> Finished exporting!")

    elif args.option.lower() == 'import':
        if not args.import_folder:
            print(">> To import you need to specify the --input_folder parameter")
            return

        import_dir = export_dir / args.import_folder
        if not import_dir.exists():
            print(f">> The import path {import_dir} does not exist")
            return

        wpg_backup_path = (backup_opk / import_dir.relative_to(export_dir).parent / import_dir.stem).with_suffix(".wpg")
        if not wpg_backup_path.exists():
            print(">> Could not find the matching backup WPG file, did you rename any folders or files in the 'backup_opk' directory?")
            return

        wpg_real_path = (opk_path / import_dir.relative_to(export_dir).parent / import_dir.stem).with_suffix(".wpg")
        if not wpg_backup_path.exists():
            print(">> Could not find the matching real WPG file, did you rename any folders or files in the 'opk' directory?")
            return

        # Open WPG from backup so all the flags and texture counts are unchanged
        print(f">> Importing '{args.import_folder}' into '{wpg_real_path}'")
        wpg = WPGFile(wpg_backup_path)
        wpg.import_from_folder(import_dir)

        # Save to real game path
        wpg.save(wpg_real_path)
        wpg.close()
        print(">> Finished importing!")


if __name__ == "__main__":
    __main__()
