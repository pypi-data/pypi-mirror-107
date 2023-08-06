from setuptools import setup, find_packages

setup(
    name="mlmd-dataset-management",
    version="0.1.0",
    description="MLMD Dataset Management",
    long_description="MLMD Dataset Management",
    long_description_content_type="text/markdown",
    url="",
    author="Thinh Nguyen",
    author_email="nguyenlongthinh@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["mlmd"],
    include_package_data=True,
    install_requires=["azure-storage-blob","requests","ml-metadata","python-dotenv","google-cloud-storage"]
)