# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['D:\\workspace\\project\\guqin-pitch-recognizer'],
             binaries=[],
             hiddenimports=['scipy._lib.messagestream', 'sklearn.neighbors.typedefs', 
             'sklearn.neighbors.quad_tree',
             'sklearn.tree',
             'sklearn.tree._utils'],
             datas=[('D:\\tools\\dev\\miniconda3\\Lib\\site-packages\\resampy\\data\\*', 'resampy/data')],
             hookspath=[],
             runtime_hooks=[],
             excludes=['matplotlib', 'PIL', 'PyQt4', 'PyQt5', 'lib2to3' 'IPython', 'pandas'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main',
          debug=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=True )
