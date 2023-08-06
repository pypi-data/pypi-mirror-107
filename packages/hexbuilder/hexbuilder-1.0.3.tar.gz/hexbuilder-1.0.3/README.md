# HexBuilder

![GitHub Release](https://img.shields.io/github/v/release/davidmaamoaix/HexBuilder) ![PyPI](https://img.shields.io/pypi/v/hexbuilder) ![PyPI - License](https://img.shields.io/pypi/l/hexbuilder)

Command line tool that converts a text file to its representing hex code.

HexBuilder is a command line tool that makes bytecode writing easier for the eye. It converts a commented text file:

```java
// header
ABCD DCBA 0000 0000
0000 0000 0000 0000

/*
    This is a multi-line comment.
*/
1239 9129

// oh and caps don't matter
AbCd cAfe
```

to a binary file whose hex dump is:

```java
ABCD DCBA 0000 0000
0000 0000 0000 0000
1239 9129 ABCD CAFE
```

So it basically strips all comments and whitespaces and converts a text file to a binary file.

## Installation

Install with pip:

```sh
pip install hexbuilder
```

## Usage

Enter in command line:

```sh
hexbuilder my_text_file
```

This will create a `.hex` file (same name as input) as output in the same directory.

Alternatively, the output file can be specified with `-o`:

```sh
hexbuilder my_text_file -o output.hex
```