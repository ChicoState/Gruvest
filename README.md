# Contributions

[![Build Status](https://travis-ci.org/blueweaver/Gruvest.svg?branch=django)](https://travis-ci.org/blueweaver/Gruvest)
[![Coverage Status](https://coveralls.io/repos/github/blueweaver/Gruvest/badge.svg?branch=django)](https://coveralls.io/github/blueweaver/Gruvest?branch=django)

## Cloning the repo

```
$ git clone https://github.com/ChicoState/Gruvest.git
```
Clones the `main` development branch of the repository

If you want a specific branch other than `main`, use
```
$ git clone -b branch-name --single-branch https://github.com/ChicoState/Gruvest.git
```


## Development

DO NOT push to the `main` branch. Push to your feature branch. Submit a pull request to `main` from github.

### Creating your feature branch

```$ git branch IssueID-Feature-Name```
Creates a new branch named `IssueID-Feature-Name`


```$ git checkout IssueID-Feature-Name```
Switches to your development branch


```$ git push -u https://github.com/ChicoState/Gruvest.git IssueID-Feature-Name```
Sets the remote tracking / upstream repository branch

### Pulling ```main``` into your branch

```$ git pull https://github.com/ChicoState/Gruvest.git main```
Downloads changes in main branch and merges them with your branch.

If the changes in main should serve as the base in your feature branch, use the `--rebase` option

### Working with others on their feature branch

```
$ git fetch https://github.com/ChicoState/Gruvest.git TheirBranchName:YourCopyName
$ git checkout YourCopyName
```
Fetches their branch on the git server and makes a local clone of it
