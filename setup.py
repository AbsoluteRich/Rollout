from setuptools import setup, find_packages

from rollout import __version__

setup(
    name="rollout",
    version=__version__,
    install_requires=[
        "Click",
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "rollout = rollout:cli",
        ],
    },
)
