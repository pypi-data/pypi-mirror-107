import os

auth_params = {
    "wallet_uri": "https://wallet.prod.dnastack.com/",
    "redirect_uri": "https://wallet.prod.dnastack.com/",
    "client_id": "dnastack-cli",
    "client_secret": "4FnZEngqOGYDCjUYDjkacVkdNXFunDExfIVeBOexkZPOUVbolVOpyZLsnxj6DTi2",
}


config_file_path = f"{os.path.expanduser('~')}/.dnastack/config.yaml"
cli_directory = f"{os.path.expanduser('~')}/.dnastack"
downloads_directory = f"{os.path.expanduser('~')}/.dnastack/downloads"

ACCEPTED_CONFIG_KEYS = [
    "search-url",
    "drs-url",
    "personal_access_token",
    "email",
    "oauth_token",
    "wallet-url",
    "client-id",
    "client-secret",
    "client-redirect-uri",
]

auth_scopes = (
    "openid drs-object:write drs-object:access search:info search:data search:query"
)
