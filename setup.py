from setuptools import setup

setup(
    name="console-examples",
    version="0.1.0",
    packages=["todolib"],
    install_requires=["docopt>=0.6.2", "click>=7.0"],
    tests_require=["pytest>=5.1.1"],
)
