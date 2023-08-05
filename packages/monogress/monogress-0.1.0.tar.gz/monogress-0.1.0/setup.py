import setuptools


setuptools.setup(
    name="monogress",
    version="0.1.0",
    author="Francis B. Lavoie",
    author_email="francis.b.lavoie@usherbrooke.ca",
    description="Monotonic univariate regression",
    long_description="Monotonic univariate regression",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["scipy"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ),
)