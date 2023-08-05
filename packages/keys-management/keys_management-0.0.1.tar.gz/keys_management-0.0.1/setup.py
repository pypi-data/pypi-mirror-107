import setuptools

setuptools.setup(
    name="keys_management",
    version="0.0.1",
    author="Ofek Israel",
    author_email="ofek.israel@nielsen.com",
    description="A small example package",
    packages=setuptools.find_packages(exclude=('tests*',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
