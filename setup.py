import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

about = dict()
with open(os.path.join(here, "style", "__version__.py"), "r") as f:
    exec(f.read(), about)

with open("README.md", "r") as fh:
    long_description = fh.read()

reqs = [line.strip() for line in open("requirements.txt")]
dev_reqs = [line.strip() for line in open("requirements_dev.txt")]

setup(
    name="pysld",
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__email__"],
    description="Package for SLD generator",
    py_modules=["pysld"],
    # package_dir={'':'src'},
    license="MIT License",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iamtekson/pysld",
    packages=["pysld"],
    keywords=[
        "pysld",
        'sld',
        'style',
        'cartography',
        'geoserver',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=reqs,
    extras_require={"dev": dev_reqs},
    python_requires=">=3.6",
)
