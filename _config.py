from _logger import logger
from dotenv import dotenv_values
import os
import shutil
import json

path_to_read = ".env"
if os.path.exists(path_to_read):
    config = dotenv_values(path_to_read)
else:
    shutil.copyfile("config.env",".env")
    logger.error(".env doesn't exists and created from templated. Edit .env and try again")

if __name__ == "__main__":
    logger.info("[Loaded Config]\n{}".format(json.dumps(config, indent=4, sort_keys=True, separators=(",",": "))))
    logger.error("Run python main.py, instead")
