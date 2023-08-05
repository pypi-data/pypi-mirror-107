import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atomvision", # Replace with your own username
    version="0.0.1",
    author="Kamal Choudhary",
    author_email="kamal.choudhary@nist.gov",
    description="atomvision",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JARVIS-Materials-Design/atomvision",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
