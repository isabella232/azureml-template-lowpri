# imports
import argparse
import subprocess
from azureml.core import Workspace

# experiment name
experiment_name = "azureml-template-lowpri"

# setup argparse
parser = argparse.ArgumentParser()
args = parser.parse_args()

# get workspace
ws = Workspace.from_config()

# do stuff
exp = ws.experiments[experiment_name]

for run in exp.get_runs():
    print(run.status)
    if run.status in [
        "Completed",
        "Running",
        "Queued",
        "Starting",
        "Preparing",
        "Finalizing",
        "NotStarted",
    ]:
        break
    elif run.status in ["Failed", "Canceled", "CancelRequested", "NotResponding"]:
        cmd = ["python", "workflows/basic/job.py"]
        res = subprocess.run(cmd, capture_output=True)
        print(res)
