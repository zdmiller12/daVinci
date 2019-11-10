# -*- mode: python ; coding: utf-8 -*-

import sys

block_cipher = None


a = Analysis(['launch_reps.py'],
             pathex=['C:\\Users\\miller\\reps\\reps'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
			 
a.datas += [('.\\resource\\dataEdit_base.ui',   '.\\resource\\dataEdit_base.ui',   'DATA'),
            ('.\\resource\\editPreferences.ui', '.\\resource\\editPreferences.ui', 'DATA'),
			('.\\resource\\mainWindow.ui',      '.\\resource\\mainWindow.ui',      'DATA'),
			('.\\resource\\userAction.ui',      '.\\resource\\userAction.ui',      'DATA')]
            
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

if sys.platform == 'win32' or sys.platform == 'win64' or sys.platform == 'linux':
    exe = EXE(pyz,
              a.scripts,
              a.binaries,
              a.zipfiles,
			  a.datas,
			  [],
			  name='launch_reps',
			  clean=True,
			  debug=False,
			  bootloader_ignore_signals=False,
			  strip=False,
			  upx=True,
			  upx_exclude=[],
			  runtime_tmpdir=None,
			  console=True 
	)