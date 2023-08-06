import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SQython",
    version="0.0.5",
    author="Max Paul",
    author_email="maxkpaul21@gmail.com",
    description="A SQL wrapper for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        'psycopg2',
        'numpy',
        'pandas',
        'psycopg2-binary'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)