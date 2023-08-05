import setuptools

setuptools.setup(
    name='import-submodules',
    version='2021.5.25',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
