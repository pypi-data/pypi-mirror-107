import pathlib as pa

import pkg_resources
import setuptools

import rocshelf

with pa.Path('requirements.txt').open() as requirements_txt:
    install_requirements = [
        str(requirement) for requirement in pkg_resources.parse_requirements(requirements_txt)
    ]

long_description = pa.Path('readme.md').read_text()

setuptools.setup(
    name='rocshelf',
    version='.'.join(map(str, rocshelf.__version__[:3])),

    packages=setuptools.find_packages(include=('rocshelf', )),
    install_requires=install_requirements,
    python_requires='>=3.9',

    author='rocshers',
    author_email='prog.rocshers@gmail.com',

    description=rocshelf.__doc__,
    long_description=long_description,
    long_description_content_type='text/markdown',

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
)
