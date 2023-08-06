from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

authors = ["Dominik Bober", "Adam Klekowski", "Szymon Duda", "Przemysław Ziaja"]

setup(
    name='daspuml-compiler',
    version='0.4',
    license='MIT',
    description='TYPE YOUR DESCRIPTION HERE',
    author=authors,
    author_email='',
    url='https://gitlab.com/agh-dasp/daspuml-language',
    keywords=['UML'],
    install_requires=requirements,
    packages = find_packages(),
    entry_points={
        'console_scripts': [
            'dasp=main:main'
        ]
    },
)
