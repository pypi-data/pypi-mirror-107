import setuptools

description = "KeysManagemets is a layer tool to ease the usage of application secret keys. \n" \
              "It allows to define multiple secret key,  from various sources if required, for each use case " \
              "After keys definitions, the tool provides methods to support secret keys rotation when needed."

setuptools.setup(
    name="keys_management",
    version="0.0.3",
    author="Ofek Israel",
    author_email="ofek.israel@nielsen.com",
    long_description=description,
    description="A small example package",
    packages=setuptools.find_packages(exclude=('tests*',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
