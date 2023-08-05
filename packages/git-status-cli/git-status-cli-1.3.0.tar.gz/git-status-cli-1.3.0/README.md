# gitstatus

Get the status of all your gits in one command!

# Installation

```
pipx install gitstatus
```
Installation with pipx (or pip but pipx is preferred) will make the gitstatus command available globally:
<p align="center">
    <img src="https://github.com/LivinParadoX/gitstatus/blob/main/screenshots/install_1.png">
</p>

# CLI Usage

```
Usage: gitstatus [OPTIONS]

  Get the status of all your gits in one command!

Options:
  --help  Show this message and exit.
```
Before use, gitstatus must be configured by editing the config.yaml file (it will automatically be created if it does not exist):
<p align="center">
    <img src="https://github.com/LivinParadoX/gitstatus/blob/main/screenshots/config_1.png">
</p>
The syntax is plain YAML:
<p align="center">
    <img src="https://github.com/LivinParadoX/gitstatus/blob/main/screenshots/config_2.png">
</p>
gitstatus will execute git status for each of your repositories and will repeatedly ask you to issue commands until all of your repositories are in a clean state:
<p align="center">
    <img src="https://github.com/LivinParadoX/gitstatus/blob/main/screenshots/usage_1.png">
    <img src="https://github.com/LivinParadoX/gitstatus/blob/main/screenshots/usage_2.png">
</p>

Any submodule is automatically handled

# Authors

* Alexandre Janvrin, penetration tester at Beijaflore (https://www.beijaflore.com/en/)

# License

AGPLv3+, see LICENSE.txt for more details.

# URLs

* https://pypi.org/project/git-status-cli/
* https://github.com/LivinParadoX/gitstatus/
