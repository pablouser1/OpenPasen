import setuptools
from setuptools import setup

PACKAGE_NAME = "openpasen"
setup(
    name="OpenPasen",
    python_requires='>=3.6',
    version="1.2.5",
    url="https://github.com/pablouser1/OpenPasen",
    author="Pablo Ferreiro Romero",
    author_email="pferreiromero@gmail.com",
    description="Programa de seguimiento escolar de la Junta de Andalucía",
    long_description=open('README.md').read().decode('utf-8'),
    packages=setuptools.find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=[
        open('requierements.txt').read().decode('utf-8')
    ],
    package_data={},
    include_package_data=True,
    zip_safe=True,
)