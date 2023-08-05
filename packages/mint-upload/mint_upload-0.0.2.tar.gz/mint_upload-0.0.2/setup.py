import os
from setuptools import find_packages, setup

def find_package_data(dirname):
    def find_paths(dirname):
        items = []
        for fname in os.listdir(dirname):
            path = os.path.join(dirname, fname)
            if os.path.isdir(path):
                items += find_paths(path)
            elif not path.endswith(".py") and not path.endswith(".pyc"):
                items.append(path)
        return items

    items = find_paths(dirname)
    return [os.path.relpath(path, dirname) for path in items]

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()

install_requires = [
    "requests>=2.24.0",
    "boto3>=1.15.0"
]

version = {}
with open("src/mint_upload/__init__.py") as fp:
    exec(fp.read(), version)



# This call to setup_name() does all the work
setup(
    name="mint_upload",
    version=version["__version__"],
    description="Module to upload file into MIC",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/mintproject/mint_upload",
    author="Maximiliano Osorio",
    author_email="mosorio@isi.edu",
    license="Apache-2",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={"mint_upload": find_package_data("src/mint_upload")},
    zip_safe=False,
    install_requires=install_requires,
    python_requires=">=3.6.0",
)
