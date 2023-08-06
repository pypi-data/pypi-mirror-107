import click
from dnastack.client.auth import login
from dnastack.client import *
from dnastack.cli.utils import assert_config, get_config, set_config
import dnastack.constants
import datetime as dt


@click.group()
@click.pass_context
def auth(ctx):
    pass


@auth.command("login")
@click.pass_context
def cli_login(ctx, refresh=False):
    personal_access_token = get_config(ctx, "personal_access_token")
    email = get_config(ctx, "email")
    auth_params = {
        "client_id": get_config(ctx, "client-id"),
        "client_secret": get_config(ctx, "client-secret"),
        "redirect_uri": get_config(ctx, "client-redirect-uri"),
        "wallet_uri": get_config(ctx, "wallet-url"),
    }

    try:
        access_token = login(
            email,
            personal_access_token,
            auth_params=auth_params,
            search_url=get_config(ctx, "search-url"),
            drs_url=re.search(
                r"(?<=https://)([^/])+(?=/.*)", get_config(ctx, "drs-url")
            ).group(0),
        )
    except:
        # click.secho(f"There was an error generating an access token", fg="red")
        sys.exit(1)

    # convert the expiry from a relative time to an actual timestamp

    set_config(ctx, "oauth_token", {get_config(ctx, "drs-url"): access_token})
