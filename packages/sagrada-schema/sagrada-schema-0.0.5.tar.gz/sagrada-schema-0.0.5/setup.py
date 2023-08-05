# Always prefer setuptools over distutils
from setuptools import setup  # , find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='sagrada-schema',  # Required

    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    version='0.0.5',
    # https://packaging.python.org/specifications/core-metadata/#summary
    description='A sample Python project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Neon Chip Ltd',  # Optional
    author_email='info@neonchip.co.uk',

    # When your source code is in a subdirectory under the project root, e.g.
    # `src/`, it is necessary to specify the `package_dir` argument.
    # package_dir={'': 'schema'},  # Optional
    # packages=find_packages(where='schema'),  # Required
    packages=['schema'],
    python_requires='>=3.6, <4',

)
