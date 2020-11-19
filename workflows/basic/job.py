# imports
from pathlib import Path
from azureml.core import Workspace
from azureml.core import ScriptRunConfig, Experiment, Environment
from azureml.core.runconfig import MpiConfiguration

# settings
experiment_name = "azureml-template-lowpri-pl"
compute_name = "gpu-cluster"
environment_name = "pt-lightning"
environment_file = "environment.yml"
source_dir = "src"
entry_script = "train-multi-node.py"
num_nodes = 2

# get root of git repo
prefix = Path(__file__).parent

# get relative paths
source_dir = str(prefix.joinpath(source_dir))
environment_file = str(prefix.joinpath(environment_file))

# create environment
env = Environment.from_conda_specification(environment_name, environment_file)

# specify a GPU base image
env.docker.enabled = True
env.docker.base_image = (
    "mcr.microsoft.com/azureml/openmpi3.1.2-cuda10.2-cudnn8-ubuntu18.04"
)

# script arguments
arguments = [
    "--max_epochs",
    100,
    "--gpus",
    4,
    "--accelerator",
    "ddp",
    "--num_nodes",
    num_nodes,
]

# create job config
mpi_config = MpiConfiguration(node_count=2, process_count_per_node=4)

src = ScriptRunConfig(
    source_directory=source_dir,
    script=entry_script,
    arguments=arguments,
    environment=env,
    compute_target=compute_name,
    distributed_job_config=mpi_config,
)

# get workspace
ws = Workspace.from_config()

# submit job
run = Experiment(ws, experiment_name).submit(src)
run.wait_for_completion(show_output=True)
