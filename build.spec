# -*- mode: python ; coding: utf-8 -*-
# pro tip: using >pyi-makespec --onefile main.py
#          to build the spec file <3

from main import GAME_TITLE # because that is still up for change

def asset_path(relative_path):
    """Get absolute path to the asset, for pyinstaller"""
    try:
        # pyinstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

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
