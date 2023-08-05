import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aitestflow",
    version="0.0.1",
    author="Vinaykumar Puppala",
    author_email="vinaykumar.puppala@outlook.com",
    description="aitestflow is a Python package used for creating automated test scripts for all types of applications. ",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    # python setup.py sdist bdist_wheel
    install_requires=['pytest-parallel', 'pytest-xdist',
                      'pandas', 'azure-devops==5.0.0b9',
                      'selenium==3.141.0', 'requests',
                      'cx_oracle', 'pymssql',
                      'mysql-connector==2.2.9', 'jsonpath',
                      'pytest', 'xlrd', 'XlsxWriter',
                      'cryptography', 'tabulate',
                      'pysftp', 'jaydebeapi==1.2.3',
                      'elasticsearch==7.6.0', 'chardet', 'msedge-selenium-tools', 'datacompy',
                      'Appium-Python-Client','webdriver-manager','junit_xml'],

    url="https://github.com/WIINAI-KKUMAR/aitestflow",
    packages=setuptools.find_packages(exclude=["tests", "reports"]),
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
