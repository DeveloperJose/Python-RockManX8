# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['src\\main.py'],
             pathex=['C:\\Users\\xeroj\\Desktop\\Local_Programming\\Python-RockManX8'],
             binaries=[],
             datas=[('resources/font.wpg', 'resources/font.wpg'), ('resources/mugshots.npz', 'resources/mugshots.npz'), ('resources/ARCtool.exe', 'resources/ARCtool.exe')],
             hiddenimports=['sentry_sdk.integrations.logging', 'sentry_sdk.integrations.stdlib', 'sentry_sdk.integrations.excepthook'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
