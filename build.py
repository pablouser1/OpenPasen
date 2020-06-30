# Crea los binarios .exe para Windows

# -*- coding: utf-8 -*-

import sys
from platform import system

from cx_Freeze import Executable, setup

base = None

build_exe_options = {
    'excludes': ['tkinter'],
    'include_files': ['assets', 'LICENSE'],
    'packages': ['gi'],
}

if system() == 'Windows':
    from build_windows_extras import include_files

    if sys.platform == 'win32':
        base = 'Win32GUI'

    elif sys.platform == 'win64':
        base = 'Win64GUI'

    build_exe_options['include_files'] = include_files
elif system() == 'Linux':
    pass

setup(
    name='OpenPasen',
    author='Pablo Ferreiro Romero',
    version='1.3',
    description='Programa de seguimiento escolar de la Junta de Andalucía no oficial',
    options={'build_exe': build_exe_options},
    executables=[
        Executable(
            'openpasen.py',
            base=base,
        ),
    ],
)
