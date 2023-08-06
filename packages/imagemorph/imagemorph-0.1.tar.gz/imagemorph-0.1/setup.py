import setuptools
from pathlib import Path
from setuptools import setup, Extension

here = Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='imagemorph',
    version='0.1',
    description=('Program to apply random elastic rubbersheet transforms to '
                 'images for augmenting training sets in machine learning/deep '
                 'learning.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tobiasvanderwerff/imagemorph',
    install_requires=['numpy', 'opencv-python'],
    package_dir={'': 'src/python'},
    py_modules=['imagemorph'],
    python_requires='>=3.6',
    ext_modules=[Extension('libimagemorph', ['src/C/imagemorph.c'])]
)
