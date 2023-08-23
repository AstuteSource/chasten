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
    - **Example Sentence**: "Her remarks are a gift to me even as they chasten
    and redirect my efforts to expand the arguments of this book into a larger
    one.", [Cambridge English
    Corpus](https://www.cambridge.org/gb/cambridgeenglish/better-learning-insights/corpus)

- **chasten** (uncountable or singular noun) "a tool that analyzes the abstract
syntax tree of a Python program to detect potential sources of programmer
mistakes so as to prevent program failure", [AstuteSource
Developers](https://github.com/AstuteSource).
    - **Student Sentence**: "I'm glad that `chasten` reminded me to add
    docstrings and type annotations to all of the functions in `main.py`. It was
    easy to see what to fix!"
    - **Instructor Sentence**: "`chasten` makes it easy for me to reliably
    confirm that student programs have the required coding constructs. It's much
    better than using regular expressions!"
    - **Developer Sentence**: "Since I was already familiar with XPATH
    expressions, `chasten` made it fun and easy for me to do an automate
    analysis of a Python codebase that I maintain."
    - **Researcher Sentence**: "In addition to helping me quickly scan the
    source code of Python projects, `chasten`'s analysis dashboard lets me
    effectively explore the data I collect."

## 🔋Features

- ✨ Easy-to-configure, automated analysis of a Python program's abstract syntax tree
- 📃 Flexible and easy-to-use YAML-based configuration file for describing analyses and checks
- 🪂 Automated generation and verification of the YAML configuration files for an analysis
- 🚀 Configurable saving of analysis results in the JSON, CSV, or SQLite formats
- 🚧 Automated integration of result files that arise from multiple runs of the tool
- 🌄 Interactive results analysis through the use of a locally running datasette server
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

Follow these steps to install the `chasten` program:

- Install Python 3.11 for your operating system
- Install [pipx](https://github.com/pypa/pipx) to support program installation in isolated environments
- Type `pipx install chasten` to install Chasten
- Type `pipx list` and confirm that Chasten is installed
- Type `chasten --help` to learn how to use the tool

## 🪂 Configuration

You can configure `chasten` with two YAML files, normally called `config.yml`
and `checks.yml`. Although `chasten` can generate a starting configuration, you
can check out the 📦
[AstuteSource/chasten-configuration](https://github.com/AstuteSource/chasten-configuration)
repository for example(s) of configuration files that setup the tool. Although
the `config.yml` file can reference multiple check configuration files, this
example shows how to specify a single `checks.yml` file:

```yml
# chasten configuration
chasten:
  # point to a single checks file
  checks-file:
    - checks.yml
```

The `checks.yml` file must contain one or more checks. What follows is an
example of a check configuration file with two checks that respectively find the
first executable line of non-test and test-case functions in a Python project.
Note that the `pattern` attribute specifies the XPATH version 2.0 expression
that `chasten` will use to detect the specified type of Python function. You can
type `chasten configure validate --config <path to chasten-configuration/
directory>` after filling in `<path to chasten-configuration>` with the
fully-qualified name of your configuration directory and the tool will confirm
that your configuration meets the tool's specification. You can also use the
command `chasten configure create` command to automatically generate a starting
configuration! Typing `chasten configure --help` will explain how to configure
the tool.

```yml
checks:
  - name: "all-non-test-function-definition"
    code: "FUNC"
    id: "FUNC001"
    description: "First executable line of a non-test function, skipping over docstrings and/or comments"
    pattern: '//FunctionDef[not(contains(@name, "test_"))]/body/Expr[value/Constant]/following-sibling::*[1] | //FunctionDef[not(contains(@name, "test_"))]/body[not(Expr/value/Constant)]/*[1]'
  - name: "all-test-function-definition"
    code: "FUNC"
    id: "FUNC002"
    description: "First executable line of a test function, skipping over docstrings and/or comments"
    pattern: '//FunctionDef[starts-with(@name, "test_")]/body/Expr[value/Constant]/following-sibling::*[1] | //AsyncFunctionDef[starts-with(@name, "test_")]/body/Expr[value/Constant]/following-sibling::*[1] | //FunctionDef[starts-with(@name, "test_")]/body[not(Expr/value/Constant)]/*[1] | //AsyncFunctionDef[starts-with(@name, "test_")]/body[not(Expr/value/Constant)]/*[1]'
    count:
      min: 1
      max: 10
```

## ✨ Analysis

Since `chasten` needs a project with Python source code as the input to its
`analysis` sub-command, you can clone the
📦 [AstuteSource/lazytracker](https://github.com/AstuteSource/lazytracker) and
📦 [AstuteSource/multicounter](https://github.com/AstuteSource/multicounter)
repositories that are forks of existing Python projects created for convenient
analysis. To incrementally analyze these two projects with `chasten`, you can
type the following commands:

- After creating a `subject-data` directory that contains a `lazytracker`
directory, run the `chasten analyze` command for the `lazytracker` program:

```shell
chasten analyze lazytracker \
        --config <path to the chasten-configuration/ directory> \
        --search-path <path to the lazytracker/ directory> \
        --save-directory < path to the subject-data/lazytracker/ directory> \
        --save
 ```

- Now you can scan the output to confirm that `chasten` finds `6` test functions
in the `lazytracker` project. If you look in the `subject-data/lazytracker`
directory you will find a JSON file with a name like
`chasten-results-lazytracker-20230823162341-4c23fc443a6b4c4aa09886f1ecb96e9f.json`.
Running `chasten` on this program more than once will produce a new results file
with a different timestamp (i.e., `20230823162341`) and unique identifier (i.e.,
`4c23fc443a6b4c4aa09886f1ecb96e9f`) in its name, thus ensuring that you do not
accidentally write over your prior results when you use the `--save` option.
