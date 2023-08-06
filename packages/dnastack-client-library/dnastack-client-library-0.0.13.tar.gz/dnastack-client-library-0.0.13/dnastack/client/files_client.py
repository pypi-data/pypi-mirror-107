import click
import urllib3
import threading
import os
from typing import Optional
from dnastack.constants import *
from requests import Response
from requests.exceptions import HTTPError
from dnastack.client.utils import get_drs_client
from dnastack.client.auth import login
import gzip
import re
import sys
import io
import pandas as pd

# since our downloads are multi-threaded, we use a lock to avoid race conditions
output_lock = threading.Lock()


def get_host(url):
    return re.search(r"(?<=https://)([^/])+(?=/.*)", url).group(0)


def handle_file_response(download_file, data):
    # decode if fasta
    if re.search(r"\.fa", download_file):
        data = data.decode("utf-8")

    return data


def file_to_dataframe(download_file, data):
    # turn into dataframe for FASTA/FASTQ files, otherwise just return raw data
    if re.search(r"\.fa", download_file):
        data = data.split("\n", maxsplit=1)

        meta = data[0]
        sequence = data[1].replace("\n", "")  # remove newlines

        return pd.DataFrame({"meta": [meta], "sequence": [sequence]})

    return data


def is_drs_url(url):
    return url[:6] == "drs://"


def get_object_info_url_from_drs(url):
    drs_host = re.search(r"(?<=drs://)([^/])+(?=/.*)", url)
    if not drs_host:
        click.secho(f"Could not get drs object id from url {url}\n", fg="red")
        raise Exception(f"Could not get drs object id from url {url}")
    object_url = f"https://{drs_host.group(0)}/ga4gh/drs/v1/"
    return object_url, drs_host


def download_file(
    url,
    output_dir,
    oauth_token: Optional[dict] = None,
    email: Optional[str] = None,
    personal_access_token: Optional[str] = None,
    auth_params: Optional[dict] = None,
    out: Optional[list] = None,
):

    http = urllib3.PoolManager()
    chunk_size = 1024
    download_url = url
    download_file = ""
    signed_access_ids = ["az-blobstore-signed"]

    if is_drs_url(url):
        # parse the drs url to the resource url
        try:
            drs_server, drs_host = get_object_info_url_from_drs(url)
            drs_client = get_drs_client(drs_server)
            object_id = url.split("/")[-1]
            object_info = drs_client.get_object_info(object_id)
        except HTTPError as e:
            if e.response.status_code == 401:
                # if their PAT and email is set, try to log into the appropriate DRS server an retry getting the object
                if email and personal_access_token:
                    try:
                        if drs_host not in oauth_token.keys():
                            oauth_token[drs_host] = login(
                                email,
                                personal_access_token,
                                auth_params=auth_params,
                                drs_url=drs_server,
                            )
                        # create a new client with token and get object info with the new client
                        drs_client = get_drs_client(drs_server, oauth_token[drs_host])
                        object_info = drs_client.get_object_info(object_id)
                    except:
                        click.secho("Access Denied", fg="red")
                else:
                    click.secho(
                        f"Authorization required for {drs_server}. Please login or configure your email and personal access token",
                        fg="red",
                    )
                    sys.exit(1)
            elif e.response.status_code == 404:
                click.secho(f"DRS object with id {object_id} does not exist", fg="red")
                sys.exit(1)
            elif e.response.status_code == 403:
                click.secho("Access Denied", fg="red")
                sys.exit(1)
            else:
                click.secho(
                    "There was an error getting object info from the DRS Client",
                    fg="red",
                )
                sys.exit(1)
        except Exception as e:
            sys.exit(1)

        if "access_methods" in object_info.keys():
            for access_method in object_info["access_methods"][0]:
                if access_method.get("access_id", None):
                    if access_method["access_id"] in signed_access_ids:
                        click.echo("found signed access_id @ access_method level")
                        try:
                            object_access = drs_client.get_object_access(
                                object_id, access_method["access_id"]
                            )
                        except HTTPError as e:
                            click.echo(e)
                            sys.exit(1)
                        download_url = object_access["url"]
                        break

                # if we have an https, use that
                if access_method["type"] == "https":
                    download_url = access_method["access_url"]["url"]
                    download_file = download_url.split("/")[-1]
                    break
        else:
            return  # next page token, just return
    else:
        click.secho(f'"{url}" is not a valid DRS url', fg="red")
        return

    try:
        download_stream = http.request("GET", download_url, preload_content=False)
    except:
        click.secho("There was an error downloading " + download_url, fg="red")
        return

    if out is not None:
        data = handle_file_response(download_file, download_stream.read())
        output_lock.acquire()
        out = out.append(file_to_dataframe(download_file, data))
        output_lock.release()

    else:
        with open(f"{output_dir}/{download_file}", "wb+") as dest:
            stream_size = int(download_stream.headers["Content-Length"])
            click.echo(
                f"Downloading {url} into {output_dir}/{download_file} ", nl=False
            )
            file_stream = download_stream.stream(chunk_size)
            with click.progressbar(length=stream_size) as download_progress:
                for chunk in file_stream:
                    dest.write(chunk)
                    download_progress.update(chunk_size)


def download_files(
    urls,
    output_dir=downloads_directory,
    oauth_token: Optional[str] = None,
    email: Optional[str] = None,
    personal_access_token: Optional[str] = None,
    auth_params: Optional[dict] = None,
    out=None,
):
    download_threads = []

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for url in urls:
        download = threading.Thread(
            target=download_file(
                url,
                output_dir,
                oauth_token=oauth_token,
                email=email,
                personal_access_token=personal_access_token,
                auth_params=auth_params,
                out=out,
            ),
            name=url,
        )
        download.daemon = True
        download_threads.append(download)
        download.start()

    for thread in download_threads:
        thread.join()

    if out is None:
        click.secho("Download complete into " + output_dir, fg="green")
