<img src="https://github.com/AstuteSource/chasten/blob/master/.github/images/chasten-logo.svg" alt="Chasten Logo"
    title="Chasten Logo" />
# 💫 chasten

[![build](https://github.com/gkapfham/chasten/actions/workflows/build.yml/badge.svg)](https://github.com/gkapfham/chasten/actions/workflows/build.yml)
![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/gkapfham/5300aa276fa9261b2b21b96c3141b3ad/raw/covbadge.json)
[![Language:
Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://github.com/gkapfham/chasten/search?l=python)
[![Code Style: black](https://img.shields.io/badge/Code%20Style-Black-blue.svg)](https://github.com/psf/black)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-blue.svg)](https://github.com/gkapfham/chasten/graphs/commit-activity)
[![License LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

## 🎉 Introduction

- **Chasten** is a Python program that uses
[XPATH](https://www.w3schools.com/xml/xpath_syntax.asp) expressions to find
patterns in the [abstract syntax
tree](https://docs.python.org/3/library/ast.html) (AST) of a Python program. You
can use Chasten to quickly implement your own configurable linting rules,
without having to use a complex AST analysis framework or resorting to imprecise
regular expressions.

- Do you want to ensure that a Python program has does not have any
triple-nested `for` loops inside of `async` functions? Or, do you want to
confirm that every function inside your Python program has type annotations and
a docstring comment? **Chasten can help**! It allows you to express these checks
&mdash; and many other types of analyses as well &mdash; in simple YAML files
that contain XPATH expressions.

## 😂 Definitions

- **chasten** (transitive verb) "to make someone aware of failure or of having
done something wrong", [Cambridge
Dictionary](https://dictionary.cambridge.org/us/dictionary/english/chasten).
    - **Sentence**: "Her remarks are a gift to me even as they chasten and
    redirect my efforts to expand the arguments of this book into a larger one."
    [Cambridge English
    Corpus](https://www.cambridge.org/gb/cambridgeenglish/better-learning-insights/corpus)

- **chasten** (uncountable or singular noun) "a tool that analyzes the abstract
syntax tree of a Python program to detect potential sources of programmer
mistakes so as to prevent program failure", [AstuteSource
Developers](https://github.com/AstuteSource).
    - **Student Sentence**: "I'm glad that `chasten` reminded me to add
    docstrings and type annotations to all of the functions in `main.py`. It was
    easy to see what to fix!"
    - **Instructor Sentence**: "`chasten` makes it easy for me to automatically
    and reliably confirm that student programs have the required coding
    constructs. It's so much better than regular expressions!"
    - **Developer Sentence**: "Since I was already familiar with XPATH
    expressions, `chasten` made it fun for me to do an automate analysis of
    a Python codebase that I maintain."
    - **Researcher Sentence**: "In addition to helping me quickly scan the
    source code of Python projects, `chasten`'s analysis dashboard lets me
    understand the data."

## 🔋Features

- ✨ Easy-to-configure, automated analysis of a Python program's abstract syntax tree
- 📃 Flexible and easy-to-use YAML-based configuration file for describing analyses and checks
- 🪂 Automated generation and verification of the YAML configuration files for an analysis
- 🚀 Configurable saving of analysis results in the JSON, CSV, or SQLite formats
- 🚧 Automated integration of result files that arise from multiple runs of the tool
- 📦 Interactive results analysis through the use of a locally running datasette server
- 🌎 Automated deployment of a datasette server on platforms like Fly or Vercel
- 🦚 Detailed console and syslog logging to furnish insights into the tool's behavior
- 💠 Rich command-line interface with robust verification of arguments and options
- 🤯 Interactive command-line generation through an easy-to-use terminal user interface

## ⚡️ Requirements

- Python 3.11
- Chasten leverages numerous Python packages, including notable ones such as:
    - [datasette](https://github.com/simonw/datasette): Interactive data analysis dashboards
    - [pyastgrep](https://github.com/spookylukey/pyastgrep): XPATH-based analysis of a Python program's AST
    - [pydantic](https://github.com/pydantic/pydantic): Automated generation and validation of configuration files
    - [rich](https://github.com/Textualize/rich): Full-featured formatting of text in the terminal
    - [trogon](https://github.com/Textualize/trogon): Automated generation of terminal user interfaces for a command-line tool
    - [typer](https://github.com/tiangolo/typer): Easy-to-implement and fun-to-use command-line interfaces

## 🔽 Installation

- Install Python 3.11 for your operating system
- Install [pipx](https://github.com/pypa/pipx) to support program installation in isolated environments
- Type `pipx install chasten` to install Chasten
- Type `pipx list` and confirm that Chasten is installed
- Type `chasten --help` to learn how to use the tool
