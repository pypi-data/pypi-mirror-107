import setuptools
import pathlib


setuptools.setup(
    name='goatherd',
    version='0.1.0',
    description='Partially-observed visual reinforcement learning domain.',
    url='http://github.com/danijar/goatherd',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=['goatherd'],
    package_data={'goatherd': ['data.yaml', 'assets/*']},
    entry_points={'console_scripts': ['goatherd=goatherd.run_gui:main']},
    install_requires=['numpy', 'imageio', 'pillow', 'ruamel.yaml'],
    extras_require={'gui': ['pygame']},
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Games/Entertainment',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
