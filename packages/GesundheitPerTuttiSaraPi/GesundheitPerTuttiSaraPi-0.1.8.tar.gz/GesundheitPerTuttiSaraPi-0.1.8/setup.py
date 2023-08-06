import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GesundheitPerTuttiSaraPi", # Replace with your own username
    version="0.1.8",
    author="Sara Picciau",
    author_email="spicciau@unibz.it",
    description="Gesundheit per tutti",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    
    entry_points = {
      'console_scripts': ['GesundheitPerTuttiSaraPi=GesundheitPerTuttiSaraPi.GesundheitPerTuttiSaraPi_module:main'],
      },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #package_dir={"": "src"},
    packages= setuptools.find_packages(),  #where="src"),
    python_requires=">=3.6",
    install_requires=[
      'gTTS',
     'Translator',
     'easyocr',
     ],

)