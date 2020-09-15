import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OpenPasen", # Replace with your own username
    version="1.4.3",
    author="Pablo Ferreiro",
    author_email="pferreiromero@gmail.com",
    description="Cliente Open-Source no oficial del programa de seguimiento escolar de la Junta de Andalucía",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pablouser1/OpenPasen",
    include_package_data = True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
