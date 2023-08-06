## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Usage](#usage)

---

## General info
The project was implemented for the Theory of Compilation and Compilators class at AGH UST.

The main goal was to implement a language and compilator that allows generating UML sequence diagram based on friendly and human-readable source code.

### Origin of the name <span style="color:yellow">daspUML</span>
- <span style="color:yellow"><b>D</b></span>ominik
- <span style="color:yellow"><b>A</b></span>dam
- <span style="color:yellow"><b>S</b></span>zymon
- <span style="color:yellow"><b>P</b></span>rzemysław
	
## Technologies
Project is created with:
* [ANTLR](https://www.antlr.org/)
* [PlantUML](https://plantuml.com/)
	
## Setup
To run this project, install it locally using [pip](https://pypi.org/project/daspuml-compiler/):
```shell
$ pip install daspuml_compiler 
```

## Usage
To check all available parameters, execute:
```bash
$ dasp --help                  
usage: dasp [-h] [-d OUTPUT_DIR] [-o OUTPUT] input_file

positional arguments:
  input_file            a name of file with source code with daspUML

optional arguments:
  -h, --help            show this help message and exit
  -d OUTPUT_DIR, --output_dir OUTPUT_DIR
                        a name of output directory
  -o OUTPUT, --output OUTPUT
                        a name of output png file
```

### Examples
Copy one of the example source code (e.g. [example_daspuml.dasp](https://gitlab.com/agh-dasp/daspuml-language/-/blob/master/examples/example_daspuml.dasp)).

Execute the daspuml_compiler:
```shell
$ dasp example_daspuml.dasp
```