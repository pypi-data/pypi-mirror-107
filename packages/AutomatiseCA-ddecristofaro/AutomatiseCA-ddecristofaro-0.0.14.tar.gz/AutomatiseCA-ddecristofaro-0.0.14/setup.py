import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AutomatiseCA-ddecristofaro", 
    version="0.0.14",
    author="Domenico De Cristofaro",
    author_email="ddecristofar@unibz.it",
    description="An automatic trascription system for Conversational Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
      'requests',
      'ibm_watson',
      'noisereduce',
      'scipy',
      'pydub',
      'praat-parselmouth'
      ],
)