# Contributions

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

