"""deploy modules helps for the deployement of application on deepchain"""
import configparser
import os
import shutil

import pkg_resources
import requests
from deepchain import log
from deepchain.cli import BaseCLICommand


def download_command_factory(args):
    return DownloadCommmand(args.app_name, args.app_dir)


class DownloadCommmand(BaseCLICommand):
    def __init__(self, app_name: str, app_dir: str):
        self.app_name = app_name
        self.app_dir = app_dir

    @staticmethod
    def register_subcommand(parser):
        download_parser = parser.add_parser(
            name="download", help="download public app from deepchain  hub"
        )

        download_parser.add_argument(
            "app_name",
            action="store",
            type=str,
            help="app name in the format creatorEmail:appName",
        )
        download_parser.add_argument(
            "app_dir",
            action="store",
            type=str,
            help="destination folder",
        )

        download_parser.set_defaults(func=download_command_factory)

    def run(self):
        """
        Download public app
        """
        config = configparser.ConfigParser()
        config.read(pkg_resources.resource_filename("deepchain", "cli/config.ini"))
        url = config["APP"]["DEEP_CHAIN_URL"]
        if os.path.exists(f"{self.app_dir}") and len(os.listdir((f"{self.app_dir}"))) > 0:
            log.warning("Destination folder is not empty, exiting.")
            return
        os.mkdir(f"{self.app_dir}")
        self.unpack(self.download_tar(url))
        [self.unpack(f"{self.app_dir}/{f}") for f in os.listdir(self.app_dir)]

    def download_tar(self, url) -> str:
        """Download app tar file on deepchain hub

        Args:
            url ([type]): [description]

        Returns:
            [str]: path of the registered tar file
        """
        req = requests.get(f"{url}/public-apps/{self.app_name}")
        if req.status_code != 200:
            log.warning(f"api returning {req.status_code}, exiting.")
            exit(1)
        with open(f"{self.app_dir}/tmp.tar", "wb") as file:
            file.write(req.content)
        return f"{self.app_dir}/tmp.tar"

    def unpack(self, file):
        shutil.unpack_archive(file, self.app_dir)
        os.remove(file)
