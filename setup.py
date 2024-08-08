from setuptools import setup, find_packages

setup(
    name='asm.py',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'run_emulator=examples.run_emulator:main',
            'os_builder=simple_emulator.os_builder:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
