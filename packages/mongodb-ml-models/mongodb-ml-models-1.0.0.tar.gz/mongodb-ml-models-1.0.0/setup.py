import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mongodb-ml-models",
    version="1.0.0",
    author="Mohammed Jassim",
    author_email="mohammedjassim.jasmir@gmail.com",
    description="For handling binary machine learning models in mongodb",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='pymongo pymongo-ml-model ml-model',
    url="https://github.com/jassim-jasmin/mongodb_model",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=['pymongo', 'python-decouple', 'joblib'],
)