import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="projpicker",
    version="0.1.1",
    author="Huidae Cho",
    author_email="grass4u@gmail.com",
    description="ProjPicker (projection picker) allows the user to select all projections whose extent completely contains given points, polylines, polygons, and bounding boxes. The goal is to make it easy and visual to select a desired projection by location.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HuidaeCho/projpicker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
