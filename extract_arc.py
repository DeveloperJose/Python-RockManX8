from src.main.python.x8_utils import MCBFile
import os
import subprocess

ARC_PATH = 'tools/arctool/USA ARCS'
MCB_PATH = os.path.join(ARC_PATH, 'X8', 'data', 'mes', 'USA')
ARC_TOOL = 'tools/arctool/arctool.exe'
FONT_PATH = 'tools/arctool/font.wpg'

#%% Extract MCBs
# for fname in os.listdir(ARC_PATH):
#     fpath = os.path.join(ARC_PATH, fname)
#     subprocess.call([ARC_TOOL, '-x', '-pc', '-noextractdir', fpath])

#%% Print MCB contents
# for fname in os.listdir(MCB_PATH):
#     fpath = os.path.join(MCB_PATH, fname)
#     mcb = MCBFile(fpath)
#     mcb.print()