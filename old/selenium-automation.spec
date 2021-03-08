# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/Users/benjaminmurray/Projects/ClimbingSpots2'],
             binaries=[('driver/chromedriver', 'driver/')],
             datas=[('example.json', '.'), ('example.ini', '.')],
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='selenium-automation',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='selenium-automation.app',
             icon=None,
             bundle_identifier=None)

import shutil
shutil.copyfile('example.ini', '{0}/example.ini'.format(DISTPATH))
shutil.copyfile('example.json', '{0}/example.json'.format(DISTPATH))
