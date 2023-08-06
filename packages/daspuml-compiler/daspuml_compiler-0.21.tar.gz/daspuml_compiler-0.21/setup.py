from setuptools import setup, find_packages

authors = ["Dominik Bober", "Adam Klekowski", "Szymon Duda", "Przemysław Ziaja"]

setup(
    name='daspuml_compiler',
    version='0.21',
    license='MIT',
    description='TYPE YOUR DESCRIPTION HERE',
    author=", ".join(authors),
    author_email='',
    url='https://gitlab.com/agh-dasp/daspuml-language',
    keywords=['UML'],
    install_requires=[
        'antlr4-python3-runtime',
        'plantuml'
    ],
    packages=['src'],
    entry_points={
        'console_scripts': [
            'dasp=src.main:main'
        ]
    },
)
