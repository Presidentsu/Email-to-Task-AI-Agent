
# agentic_ai.spec - Spec file for PyInstaller
# Run with: pyinstaller agentic_ai.spec

block_cipher = None

a = Analysis(
    ['agentic_ai.py'],
    pathex=[],
    binaries=[],
    datas=[],  # No credentials.json included, user will provide path
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='agentic_ai',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # CLI tool — keep console window
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='agentic_ai'
)
