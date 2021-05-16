import logging
import os
import sys
from logging.handlers import RotatingFileHandler

import yaml
from google_drive_downloader import GoogleDriveDownloader as gdd

from file_manager.path_utilities import ROOT_DIR

logger = logging.getLogger(os.path.basename(__file__))


def init_logger():
    log_name = os.path.join(ROOT_DIR, "app.log")
    handler = RotatingFileHandler(log_name, mode="w", maxBytes=100000, backupCount=1)
    handler.suffix = "%Y%m%d"
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=logging.INFO)
    if os.path.isfile(log_name):  # log already exists, roll over!
        handler.doRollover()
    # logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().addHandler(handler)


def load_yaml(file):
    try:
        return yaml.safe_load(open(file))
    except yaml.YAMLError as e:
        print(e), sys.exit(1)


def dump_yaml(data, file):
    yaml.dump(data, open(file, 'w'), default_flow_style=False)


def download_models(file_id: str, file_name: str):
    output = os.path.join(ROOT_DIR, 'models', file_name)
    gdd.download_file_from_google_drive(file_id=file_id,
                                        dest_path=output)
