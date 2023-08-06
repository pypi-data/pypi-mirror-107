from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md")) as f:  # PY3: encoding="utf-8"
    long_description = f.read()

setup(
    name="calver-pinning",
    description="Setuptools extension for CalVer package versions (fork)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/di/calver",
    author="Dustin Ingram",
    author_email="di@python.org",
    maintainer="Jamie Bliss",
    maintainer_email="jamie@ivyleav.es",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
    keywords="calver",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    # python_requires=">=3.5",
    entry_points={
        "distutils.setup_keywords": [
            "use_calver = calver.integration:version",
        ],
    },
    use_calver=True,
    setup_requires=["calver-pinning"],
    # XXX: What's the minimum version of setuptools?
    install_requires=["setuptools"],
)
