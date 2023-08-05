import setuptools
import pp_pripel

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=pp_pripel.__name__,
    version=pp_pripel.__version__,
    author=pp_pripel.__author__,
    author_email=pp_pripel.__author_email__,
    description="Privacy-preserving Event Log Publishing with contextual Information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samadeusfp/PRIPEL",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pm4py==1.2.10',
        'diffprivlib==0.3.0',
        'numpy>=1.18.2',
        'scipy>=1.5.2',
        'python_dateutil>=2.8.1'
    ],
    project_urls={
        'Source': 'https://github.com/samadeusfp/PRIPEL'
    }
)

