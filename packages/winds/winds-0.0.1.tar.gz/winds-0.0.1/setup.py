from setuptools import find_packages, setup

with open('LICENSE.txt', 'r') as fh:
    long_description = fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'A conversion package'
LONG_DESCRIPTION = 'A package that makes it easy to convert values between several units of measurement'

setup(
    name="winds",
    version='0.0.1',
    description='Packages having functions that calculate wind regimes as well as other important features for wind turbine design',
    long_description='The package was created in an effort to facilitate the analysis of wind regimes and other important consideraion for wind turbines design, different function could be call and with the introduction of parameters can give the result of the needed fuction',
    author="Uel Palmer Kouame",
    authorEmail="kouame@purdue.edu",
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    keywords='conversion',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)

