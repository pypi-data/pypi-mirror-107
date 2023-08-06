import setuptools
import scraper

with open('readme.md') as fr:
    long_description = fr.read()

setuptools.setup(
    name='scraperlib',
    version=scraper.__version__,
    author='Luferov V.S.',
    author_email='lyferov@yandex.ru',
    description='Fuzzy logic tool box as matlab',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Luferov/FuzzyLogicToolBox',
    packages=setuptools.find_packages(),
    install_requires=[
        'aiohttp>=3.7.4',
        'bs4==0.0.1',
        'requests>=2.25.1'
    ],
    test_suite='tests',
    python_requires='>=3.8',
    platforms=["any"]
)