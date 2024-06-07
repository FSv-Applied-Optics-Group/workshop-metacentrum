import sys
import os
import pysftp
from io import BytesIO, StringIO

# RUN: python meta_communication_workshop.py test.py

# Load env variables from .env
from dotenv import load_dotenv
load_dotenv()

# Fetch filename from cmd args
FILENAME = sys.argv[1]

# Fetch env variables
SFTP_META_HOST = os.environ.get("SFTP_META_HOST")
SFTP_META_USER = os.environ.get("SFTP_META_USER")
SFTP_META_PWD = os.environ.get("SFTP_META_PWD")

# Project folder on the SFTP server
AO_PROJECT_FOLDER = "/storage/projects/CVUT_Fsv_AO/workshop/"
PROJECT_USER_FOLDER = f"{AO_PROJECT_FOLDER}/workshop_test"

# Create connection
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

# Run file (powershell)
run_file = "run_workshop.sh"

with pysftp.Connection(host=SFTP_META_HOST, username=SFTP_META_USER, password=SFTP_META_PWD, cnopts=cnopts) as sftp:

    # Change directory to the group folder
    sftp.chdir(AO_PROJECT_FOLDER)
    #print(sftp.listdir(AO_PROJECT_FOLDER))

    # Create project folder if it does not exist
    if not sftp.isdir(PROJECT_USER_FOLDER):
        sftp.mkdir(PROJECT_USER_FOLDER)

    # Change to project folder
    sftp.chdir(PROJECT_USER_FOLDER)
    #print(sftp.pwd)

    runsh = BytesIO()
    with open(run_file, "r") as f:
        [
            runsh.write(
                str.encode(line.replace("<FILE_NAME>", FILENAME))
            )
            for line in f.readlines()
        ]

    with open(run_file, "wb") as f:
        f.write(runsh.getbuffer())

    # Upload file to meta
    sftp.put(run_file)
    sftp.put(f"{FILENAME}")
    #sftp.put(f"tests/train_config.yaml")
    #sftp.put(f"tests/2402071244.keras")
    #print(sftp.listdir())

    #os.remove("run.sh")

    print(sftp.execute(f"qsub {PROJECT_USER_FOLDER}/" + run_file))

    # end
