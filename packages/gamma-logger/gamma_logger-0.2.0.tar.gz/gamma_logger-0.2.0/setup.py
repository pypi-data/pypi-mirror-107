import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gamma_logger", # Replace with your own username
    version="0.2.0",
    author="Gaurav Singh, Danish khajuria",
    author_email="gauravsingh0109@gmail.com, danishkhajuria@gmail.com",
    description="A small logger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={
                    'gamma_logger': ['logging.conf'],
                 },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
