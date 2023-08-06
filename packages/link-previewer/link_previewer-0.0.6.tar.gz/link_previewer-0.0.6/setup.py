from setuptools import setup 

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name='link_previewer',
        version='0.0.6',
        description='Gives the link preview based on Open Graph Protocol',
        py_modules=["previewer"],
        package_dir={'':'src'},
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        long_description=long_description, 
        long_description_content_type="text/markdown",
        install_requires = [
            "beautifulsoup4==4.9.3",
            "certifi==2020.12.5",
            "chardet==4.0.0",
            "filelock==3.0.12",
            "idna==2.10",
            "lxml==4.6.3",
            "requests==2.25.1",
            "requests-file==1.5.1",
            "six==1.16.0",
            "soupsieve==2.2.1",
            "tldextract==3.1.0",
            "urllib3==1.26.4",
            ],
        extras_require = {
            "dev": [
                "pytest>=5",
                "check-manifest==0.46",
                "twine==3.4.1",
                ]
            },
        url="https://github.com/amiaynara/link_previewer.git",
        author="Amiay Narayan",
        author_email="amiayn@iitbhilai.ac.in",

)
