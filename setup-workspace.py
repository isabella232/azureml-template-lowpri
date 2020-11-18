# imports
import argparse

from azureml.core import Workspace
from azureml.core.compute import ComputeTarget, AmlCompute, AksCompute

# setup argparse
parser = argparse.ArgumentParser()
parser.add_argument("--subscription-id", type=str, default=None)
parser.add_argument("--workspace-name", type=str, default="default")
parser.add_argument("--resource-group", type=str, default="azureml-template-lowpri")
parser.add_argument("--location", type=str, default="eastus")
args = parser.parse_args()

# define aml compute target(s) to create
amlcomputes = {
    "gpu-cluster": {
        "vm_size": "STANDARD_NC24S_V3",
        "min_nodes": 0,
        "max_nodes": 2,
        "idle_seconds_before_scaledown": 1200,
        "vm_priority": "lowpriority",
    }
}

# create workspace
ws = Workspace.create(
    args.workspace_name,
    subscription_id=args.subscription_id,
    resource_group=args.resource_group,
    location=args.location,
    create_resource_group=True,
    exist_ok=True,
    show_output=True,
)
ws.write_config()

# create aml compute targets
for ct_name in amlcomputes:
    if ct_name not in ws.compute_targets:
        compute_config = AmlCompute.provisioning_configuration(**amlcomputes[ct_name])
        ct = ComputeTarget.create(ws, ct_name, compute_config)
        ct.wait_for_completion(show_output=True)
