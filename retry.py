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
run = next(exp.get_runs())
status = run.get_status()

if status in ["Failed", "Canceled", "CancelRequested", "NotResponding"]:
    print(f"Job status: {status}. Retrying job...")
    cmd = ["python", "workflows/basic/job.py"]
    res = subprocess.run(cmd, capture_output=True)
    print(res)
    break

print(f"Job status: {status}. Exiting...")