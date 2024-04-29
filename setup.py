from setuptools import setup

from rollout import __version__

setup(
    name="rollout",
    version=__version__,
    install_requires=[
        "Click",
    ],
    packages=["rollout"],
    entry_points={
        "console_scripts": [
            "rollout = rollout:cli",
        ],
    },
)
