from setuptools import setup

setup(
    name="console-examples",
    version="0.1.0",
    packages=["todolib"],
    install_requires=[
        "docopt>=0.6.2",
        "click>=7.0",
        "fire>=0.2.1",
        "cement>=3.0.4",
        "cleo>=0.7.5",
        "cliff>=2.16.0",
        "plac>=1.1.0",
        "plumbum>=1.6.7",
        "cmd2>=0.8.9",
    ],
    tests_require=["pytest>=5.1.1"],
)
