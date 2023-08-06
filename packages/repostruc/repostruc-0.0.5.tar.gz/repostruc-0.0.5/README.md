# REPOSTRUC

>`repostruc` is a cross-platform library that returns the directory structure in a formated form. The structure can be copied to your clipboard or a .md file can be made available.[`.md example`](PROJECTINFO.md)

## Ignored files

>`repostruc` ignores files from [`.gitinore`](.gitinore) file if present else ignores commonly ignored files and directories.

## Install the Requirements

```bash
 pip install repostruc
```

## Usage

### To clipboard

```bash
repostruc -c
```

### To file

```bash
repostruc -f filepath
```

### To [`PROJECTINFO.md`](PROJECTINFO.md)

```bash
repostruc -r -f
```

## Example

 View [`PROJECTINFO.md`](PROJECTINFO.md) which was made using `repostruc`

## Built With

* [`pathlib`](https://pypi.org/project/pathlib/) - pathlib offers a set of classes to handle filesystem paths.
* [`pyperclip`](https://pypi.org/project/pyperclip3/) - Cross-platform clipboard utilities supporting both binary and text data.
* [`gitignore_parser`](https://pypi.org/project/gitignore-parser/) - A spec-compliant gitignore parser for Python 3.5+
* [`docopt`](https://pypi.org/project/docopt/) - creates beautiful command-line interfaces

## Contributing

Please read [CONTRIBUTING.md](https://github.com/) for details on our code of conduct, and the process for submitting pull requests.

## Authors

* **Atharva Gundawar** - *Initial work* - [Github handle](https://github.com/Atharva-Gundawar)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Generator function from [*Aaron Hall's*](https://stackoverflow.com/users/541136/aaron-hall) answer [here](https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python)
