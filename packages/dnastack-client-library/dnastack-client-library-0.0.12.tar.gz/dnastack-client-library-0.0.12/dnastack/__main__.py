import click
import yaml
import os
from dnastack.cli import *
import dnastack


def load_config_from_file(ctx):
    ctx.obj = {}

    # Create the config file if necessary
    if not os.path.exists(config_file_path):
        with open(config_file_path, "w+") as config_file:
            yaml.dump(ctx.obj, config_file)

    with open(config_file_path, "r+") as config_file:
        data = yaml.safe_load(config_file)
        if data:
            for key in data.keys():
                ctx.obj[key] = data[key]


@click.group()
def dnastack():
    load_config_from_file(click.get_current_context())


dnastack.add_command(search_commands.search)
dnastack.add_command(config_commands.config)
dnastack.add_command(file_commands.files)
dnastack.add_command(auth_commands.auth)

if __name__ == "__main__":
    dnastack()
