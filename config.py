import yaml
from box import Box

with open("config.yml", "r") as ymlfile:
    cfg = Box(yaml.safe_load(ymlfile))
