from setuptools import setup, find_packages

VERSION = '0.1.3'
DESCRIPTION = 'A core with all my useful functions.'

# Setting up
setup(
    name="xyndra_function_core",
    version=VERSION,
    author="Xyndra",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['python', 'arrays', 'easy function'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)