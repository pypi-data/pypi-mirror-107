import setuptools

setuptools.setup(
    name="dstree",
    version="1.0",
    license='MIT',
    author="datadriven42",
    author_email="datadriven42@gmail.com",
    description="A module for visualization of a nested python data structure",
    long_description=open('README.md', encoding = 'utf-8').read(),
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "numpy",
        "torch",
        "treelib",
        "pandas",
        "graphviz"
    ],
    python_requires='>=3.8',
)