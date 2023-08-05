from pathlib import Path
from setuptools import setup, find_packages


setup(
    name="dendrodict",
    version="0.0.0",
    packages=find_packages("source"),
    author="Sixty North AS",
    author_email="rob@sixty-north.com",
    description="Dict type that makes it easier to work with deeply nested dicts.",
    license="MIT",
    keywords="",
    url="http://bitbucket.org/sixty-north/dendrodict",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
    ],
    platforms="any",
    include_package_data=True,
    package_dir={"": "source"},
    # package_data={'dendrodict': . . .},
    install_requires=[],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax, for
    # example: $ pip install -e .[dev,test]
    extras_require={
        "dev": ["black", "bump2version"],
        # 'doc': ['sphinx', 'cartouche'],
        "test": ["hypothesis", "pytest"],
    },
    entry_points={
        # 'console_scripts': [
        #    'dendrodict = dendrodict.cli:main',
        # ],
    },
    long_description=Path("README.rst").read_text(encoding="utf-8"),
)
