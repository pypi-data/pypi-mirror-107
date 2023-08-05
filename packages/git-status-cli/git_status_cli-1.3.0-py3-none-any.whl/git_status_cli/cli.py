import os
import shlex
import shutil
import subprocess as sp
from configparser import ConfigParser
from importlib import resources
from pathlib import Path

import click
import yaml
from tabulate import tabulate


def load_user_config():
    app_dir = Path(click.get_app_dir("gitstatus"))

    try:
        with open(app_dir / "config.yaml") as config_file:
            return yaml.safe_load(config_file)

    except FileNotFoundError:
        os.makedirs(app_dir, mode=0o755, exist_ok=True)

        with resources.path("git_status_cli", "config.yaml") as config_path:
            shutil.copy(config_path, app_dir)

        return load_user_config()


USER_CONFIG = load_user_config()


def get_alias(command):
    try:
        return USER_CONFIG["aliases"][command]
    except KeyError:
        return command


def run_command(command, cwd):
    command = get_alias(command)
    try:
        click.echo(f"Running command: {command}")
        sp.run(shlex.split(command), cwd=cwd)
    except FileNotFoundError:
        click.echo(f"COMMAND NOT FOUND: {command}")


def clean(git):
    for action in USER_CONFIG.get("default_cleaning_actions", []):
        run_command(action, cwd=git)

    if not USER_CONFIG.get("default_is_enough", False):
        click.secho(str(git), fg="blue")
        sp.run(
            "git status".split(),
            cwd=git,
        )
        run_command(click.prompt(click.style(f"{git}$ ", fg="blue")), cwd=git)
    return get_status(git)


def get_status(git):

    status_lines = (
        sp.run(
            "git status --short --branch".split(),
            cwd=git,
            stdout=sp.PIPE,
            stderr=sp.DEVNULL,
        )
        .stdout.decode()
        .splitlines()
    )

    if (
        "ahead" in status_lines[0]
        or "behind" in status_lines[0]
        or len(status_lines) > 1
    ):
        return clean(git)

    return [
        click.style(str(git), fg="blue"),
        click.style("OK", fg="green"),
        status_lines[0][3:],
    ]


def gather_submodules(gits):
    sub_gits = set()
    for git in gits:
        try:
            with open(git / ".gitmodules") as gitmodules_file:
                gitmodules = ConfigParser()
                gitmodules.read_file(gitmodules_file)
                sub_gits |= gather_submodules(
                    {
                        git / gitmodules[section]["path"]
                        for section in gitmodules.sections()
                    }
                )
        except FileNotFoundError:
            pass
    return gits | sub_gits


@click.command()
def main():
    """Get the status of all your gits in one command!"""
    try:
        assert USER_CONFIG is not None

        gits = set()
        try:
            gits = {
                dir
                for dir in Path(USER_CONFIG.get("gits_folder")).iterdir()
                if dir.is_dir()
            }
        except TypeError:
            pass

        gits |= {Path(dir) for dir in USER_CONFIG.get("individual_gits", [])}

        gits = gather_submodules(gits)

        assert gits != set()

        click.echo(
            tabulate(
                [get_status(git) for git in gits],
                headers=["Git", "Status", "Branch"],
            )
        )

    except AssertionError as error:
        click.echo(
            "Please edit your config file to include at least one git: "
            f"{Path(click.get_app_dir('gitstatus')) / 'config.yaml'}",
        )
