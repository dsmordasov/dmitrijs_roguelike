# -*- mode: python ; coding: utf-8 -*-
# pro tip: using >pyi-makespec --onefile main.py
#          to build the spec file <3
# w/ this spec file, to build locally for Windows, 
# > pyinstaller build.spec


from main import GAME_TITLE # works on LOCAL builds only!
#GAME_TITLE = "The Rat Catcher" # Uncomment before pushing 
block_cipher = None

a = Analysis(['main.py'], # remove pathex for portability
             binaries=[],
             datas=[("assets", "assets")], # must be exported to "assets" as that's where the code searches for them
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name=GAME_TITLE,
		  icon="assets/game_icon.ico",
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False, # disabled console, we don't need it
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
