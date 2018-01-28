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
             excludes=['matplotlib', 'PIL', 'PyQt4', 'PyQt5', 'pydoc', 'pythoncom', 'pkg_resources', 'setuptools', 'sysconfig', 'xml.dom.domreg', 'Tkinter', 'rth_pkgres', 'scipy.linalg', 'scipy.io.matlab', 'distutils', 'lib2to3', 'llvmlite', 'IPython', 'pandas'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
# a.binaries = a.binaries - TOC([('mkl_avx512_mic.dll', 'mkl_avx512.dll', 'mkl_avx2.dll', 'mkl_mc3.dll', 'mkl_avx.dll', 'mkl_mc.dll', 'mkl_core.dll', 'mkl_def.dll', 'mkl_intel_thread.dll')])
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
          console=False )
