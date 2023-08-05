from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ingotdr',
    version='0.0.2',
    description="INGOT-DR (INterpretable GrOup Testing for Drug Resistance)",
    author="Hooman Zabeti",
    author_email="hzabeti@sfu.ca",
    url="https://github.com/hoomanzabeti/ingotdr",
    py_modules=["ingot"],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['numpy', 'pandas', 'pulp', 'sklearn'],
    include_package_data=True
)
