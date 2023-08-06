from setuptools import setup

setup(
    name='RNAtweaks',
    version='0.0.2',
    author='Dominik Rabsch',
    author_email='rabsch@informatik.uni-freiburg.de',
    packages=['RNAtweaks'],
    scripts=[],
    license='LICENSE.txt',
    url="https://github.com/domonik/RNAtweaks",
    long_description_content_type="text/markdown",
    description='Package including ViennaRNA helper functions and classes',
    long_description=open('README.md').read(),
    include_package_data=False,
    install_requires=[
        "numpy"
    ],
)
