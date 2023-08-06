from setuptools import setup

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name='zeplyn',
    version='0.1.0',
    description='Upload and reitarate on your packages',
    py_modules=['zeplyn'],
    package_dir={'':'src'},
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url='https://github.com/ssantoshp/zeplyn',
    author = "Santosh Passoubady",
    author_email = "santoshpassoubady@gmail.com",
    license='MIT',
    install_requires=[
          'twine',
      ],
)
