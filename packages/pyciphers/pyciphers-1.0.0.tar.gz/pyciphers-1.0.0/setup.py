import pathlib
from setuptools import setup
# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pyciphers",
    version="1.0.0",
    description="The Hill cipher Encryption algorithm is one of the symmetric key algorithms that have several "
                "advantages in "
                "data encryption.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Yashmodi59/Cipher_Python_Package",
    author="Yash Modi",
    author_email="yashmodi2059@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pyciphers"],
    include_package_data=True,
    install_requires=["numpy"],
    entry_points={
        "console_scripts": [
            "pyciphers=pyciphers.__main__:main",
        ]
    },
)
