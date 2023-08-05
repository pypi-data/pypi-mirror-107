import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="transcr-esiviero", # Replace with your own username
    version="0.0.9",
    author="Emily Siviero",
    author_email="esiviero@unibz.it",
    description="My first package to make the transcription process easier",
    long_description=long_description,
    license = 'MIT',
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
        'SpeechRecognition',
        'nltk',
        'gTTS',
        'googletrans==3.1.0a0'
    ],
)