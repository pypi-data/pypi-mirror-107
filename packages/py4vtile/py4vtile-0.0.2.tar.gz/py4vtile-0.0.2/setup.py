import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py4vtile",
    version="0.0.2",
    author="Manuele Pesenti",
    author_email="manuele@inventati.org",
    description="Tools that helps you to develop web service for distributing vector tiles.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manuelep/py4vtile",
    project_urls={
        "Bug Tracker": "https://github.com/manuelep/py4vtile/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        # "Framework :: Py4web",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        # Requirements goes here
        # Eg.: "caldav == 0.1.4",
        "mptools",
        "shapely",
        "mercantile",
        "pyproj",
        "py4web>=1.20210522.2",
        "mapbox_vector_tile"
    ]
)
