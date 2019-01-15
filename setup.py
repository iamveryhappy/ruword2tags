import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ruword2tags",
    version="0.0.3",
    author="Ilya Koziev",
    author_email="inkoziev@gmail.com",
    description="Russian morphology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Koziev/ruword2tags",
    packages=setuptools.find_packages(),
    package_data={'ruword2tags': ['*.dat']},
    include_package_data=True,
)