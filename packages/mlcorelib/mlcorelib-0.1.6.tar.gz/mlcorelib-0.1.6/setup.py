import setuptools

long_description = "Helper library for common ML functions" 

setuptools.setup(
    name="mlcorelib",                     # This is the name of the package
    version="0.1.6",                        # The initial release version
    author="Avinash Saxena",                     # Full name of the author
    description="Provides library for ML",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["mlcorelib"],             # Name of the python package
    package_dir={'':'mlcorelib/src'},     # Directory of the source code of the package
    install_requires=["transformers", "sklearn", "numpy"]                     # Install other dependencies if any
)
