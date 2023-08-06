from setuptools import setup

authors = ["Dominik Bober", "Adam Klekowski", "Szymon Duda", "Przemysław Ziaja"]

description = """The project was implemented for the Theory of Compilation and Compilators class at AGH UST.
The main goal was to implement a language and compilator that allows generating UML sequence diagram based on friendly and human-readable source code."""

setup(
    name='daspuml_compiler',
    version='1.0',
    license='MIT',
    description=description,
    author=", ".join(authors),
    author_email='',
    url='https://gitlab.com/agh-dasp/daspuml-language',
    keywords=['UML'],
    install_requires=[
        "antlr4-python3-runtime>=4.9.2",
        "plantuml>=0.3.0"
    ],
    packages=['daspuml_compiler'],
    entry_points={
        'console_scripts': [
            'dasp=daspuml_compiler.main:main'
        ]
    },
)
