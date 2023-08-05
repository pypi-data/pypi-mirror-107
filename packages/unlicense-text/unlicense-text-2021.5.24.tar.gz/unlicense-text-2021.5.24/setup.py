import setuptools

setuptools.setup(
    name='unlicense-text',
    version='2021.5.24',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages(),
    scripts=['bin/unlicense-text']
)
