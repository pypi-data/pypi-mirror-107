# flake8: noqa
import time
import os
from azurebatchload.upload import Upload
from azurebatchload.download import Download
from azurebatchload.utils import Utils
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv(override=True, verbose=True)

os.chdir("/Users/erfannariman/Workspace/staffing/module_demos")

# Download(
#     destination=".",
#     source="test",
#     folder="data",
#     method="batch",
#     list_files=["2009 car efficiency.csv", "2010 car efficiency.csv"]
# ).download()

Upload(
    destination="test",
    source="data/azurebatchload",
    method="single",
    extension=".csv",
    overwrite=True,
    # list_files=["2009 car efficiency.csv", "2010 car efficiency.csv"]
).upload()

# files = Utils(
#     container="test", name_starts_with="data", dataframe=True, extended_info=True
# ).list_blobs()
#
# print(files)
