import json
import os
import os.path as op
import logging
import pandas as pd
import unidecode
import glob
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


logger = logging.getLogger(__name__)


def load_conf_from_path(path):
    conf = dict()

    for name in glob.glob(f"{path}/*"):

        # Load YAML files
        if name.endswith(".yml"):
            logger.info(f"Loading data from file {name}")
            with open(name, "r") as f:
                conf.update(yaml.load(f, Loader=Loader))

        # Load JSON files
        elif name.endswith(".json"):
            logger.info(f"Loading data from file {name}")
            with open(file=name, mode="r", encoding="utf-8") as f:
                conf.update(json.load(f))

    return conf


def load_melusine_conf():
    conf = dict()

    # Load default Melusine conf
    default_config_directory = op.dirname(op.abspath(__file__))
    conf.update(load_conf_from_path(default_config_directory))

    # Load custom Melusine conf
    custom_config_directory = os.getenv("MELUSINE_CONFIG_DIR")
    if custom_config_directory:
        conf.update(load_conf_from_path(custom_config_directory))

    name_list = load_name_file(custom_config_directory, default_config_directory)

    conf["words_list"]["names"] = name_list

    return conf


def load_name_file(custom_config_directory, default_config_directory):
    # Load Name file
    if custom_config_directory and op.exists(
        os.path.join(custom_config_directory, "names.csv")
    ):
        name_file = op.join(custom_config_directory, "names.csv")
    else:
        name_file = op.join(default_config_directory, "names.csv")
    logger.info(f"Reading names from file {name_file}")
    try:
        df_names = pd.read_csv(name_file, encoding="utf-8", sep=";")
        name_list = df_names["Name"].values
        name_list = [unidecode.unidecode(p).lower() for p in name_list]
    except FileNotFoundError:
        name_list = []
    return name_list


config = load_melusine_conf()
