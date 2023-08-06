import setuptools


setuptools.setup(
    name='VisPathways',
    version='0.1.1.9',
    description='A python and command line package to summarize and visualize pathway (gene set) hierarchies and enrichments.',
    long_description='Please check out our README file at this link for documentations: https://github.com/tommyfuu/FancyTaxonomies/blob/main/stableUsage/README.md',
    url='https://github.com/tommyfuu/FancyTaxonomies/blob/main/stableUsage',
    author='Chenlian (Tom) Fu',
    author_email='tfu@g.hmc.edu',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pandas',
                      'numpy',
                      'scipy',
                      'ete3',
                      'PyQt5',
                      'matplotlib',
                      ],
    py_modules=['enrichment', 'InferGoKeggToGOBP', 'InferGoReactomeToGOBP', 'InferGoSlimToGOBP',
                'mergeDatabases', 'simpleTime', 'summarizePathwayHierarchy', 'treeGO', 'VisPathways'],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
