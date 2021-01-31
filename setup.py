import setuptools

from finanzen_base.Utils.requirements import read_requirements

required_packages = read_requirements('requirements/prod.txt')
extra_packages = read_requirements('requirements/dev.txt')

# Parse Readme for long_description
with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="finanzen_entgelt",
    version="0.0.1",
    author="Valentin Kuhn",
    author_email="valentin.gabriel.kuhn@outlook.de",
    description="Gather and process financial income information.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    install_requires=required_packages,
    extras_require={"dev": extra_packages}
)
