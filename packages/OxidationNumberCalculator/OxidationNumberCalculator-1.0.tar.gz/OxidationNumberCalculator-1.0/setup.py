from setuptools import setup
import pathlib
here = pathlib.Path('README.md').parent.resolve()

setup(
    name = 'OxidationNumberCalculator',
    packages = ['OxidationNumberCalculator'],
    description='An alpha version of an oxidation number calculator that can be used on compounds/Elements or Chemical Equations.',
    long_description=(here / 'README.md').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    version = '1.00',
    license='MIT',
    author = 'Harold J. Iwen',
    author_email = 'inventorsniche349@gmail.com',
    url = 'https://www.inventorsniche.com',
    download_url = 'https://github.com/Hiwen-STEM/OxidationNumberCalculator',
    keywords = ['Oxidation','Number','Oxidation_Number','oxidation_number','stoichiometry','chemical','equation','chemical_equation'],
    install_requires=[
        'mendeleev'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',     
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
