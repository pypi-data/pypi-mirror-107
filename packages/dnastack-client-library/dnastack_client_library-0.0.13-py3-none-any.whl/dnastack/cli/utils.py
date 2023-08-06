import sys
import click
import yaml
from dnastack.constants import config_file_path


def get_config(ctx, var_name, default=None, do_assert=False):
    # assert that the config is there
    if do_assert:
        assert_config(ctx, var_name)

    if has_config(ctx, var_name):
        return ctx.obj[var_name]
    return default


def set_config(ctx, var_name: str, value):
    if type(value) == dict:
        ctx.obj[var_name] = {}
        for key, val in zip(value.keys(), value.values()):
            ctx.obj[var_name][key] = val

    set_configs(ctx, [var_name], [value])


def set_configs(ctx, var_names: list, values: list):
    for key, val in zip(var_names, values):
        ctx.obj[key] = val

    with open(config_file_path, "w") as config_file:
        yaml.dump(ctx.obj, config_file)


def has_config(ctx, var_name):
    return var_name in ctx.obj.keys() and ctx.obj[var_name]


def assert_config(ctx, var_name):
    if not has_config(ctx, var_name):
        click.secho(
            f"The {var_name} configuration variable is not set. Run dnastack config {var_name} [{var_name.upper()}] to configure it",
            fg="red",
        )
        sys.exit()
