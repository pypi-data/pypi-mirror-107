from setuptools import setup, find_packages

authors = ["Dominik Bober", "Adam Klekowski", "Szymon Duda", "Przemysław Ziaja"]

setup(
    name='daspuml-compiler',
    version='0.11',
    license='MIT',
    description='TYPE YOUR DESCRIPTION HERE',
    author="\n".join(authors),
    author_email='',
    url='https://gitlab.com/agh-dasp/daspuml-language',
    keywords=['UML'],
    install_requires=[
        'antlr4-python3-runtime',
        'plantuml'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dasp=main:compile'
        ]
    },
)
