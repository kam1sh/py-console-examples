from setuptools import setup

setup(
    name="console-examples",
    version="0.2.0",
    packages=["todolib"],
    install_requires=[
        "cliff==2.16.0",
        "plac==1.1.0",
        "plumbum==1.6.7",
        "cmd2==0.8.9",
        "urwid==2.0.1",
    ],
    tests_require=["pytest>=5.1.1"],
)
