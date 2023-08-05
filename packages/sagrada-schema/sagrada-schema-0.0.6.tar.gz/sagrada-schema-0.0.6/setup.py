# Always prefer setuptools over distutils
from setuptools import setup  # , find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='sagrada-schema',  # Required

    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    version='0.0.6',
    # https://packaging.python.org/specifications/core-metadata/#summary
    description='A sample Python project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Neon Chip Ltd',  # Optional
    author_email='info@neonchip.co.uk',

    # package_dir={'': 'schema'},  # Optional
    packages=['schema'],
    python_requires='>=3.6, <4',

)
