from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
        name='convx',
        version='0.0.2',
        description='A package for quickly converting binary, hex and decimal to one another.',
        py_modules=["convx"],
        package_dir={'': 'src'},
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"
        ],
        long_description=long_description,
        long_description_content_type="text/markdown",
        install_requires = [
            "riposte >= 0.4.1"
        ],
        extras_require = {
            "dev": [
                "pytest>=6.2.4"
            ]
        },
        url="https://github.com/The-Real-Thisas/convx",
        author="Thisas",
        author_email="thisas@thisas.dev"
)
