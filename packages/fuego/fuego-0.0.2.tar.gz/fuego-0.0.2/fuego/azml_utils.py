from pathlib import Path

from azureml.core import (
    Dataset,
    Environment,
    Experiment,
    ScriptRunConfig,
    Workspace,
)
from azureml.core.compute import AmlCompute, ComputeTarget
from azureml.core.runconfig import MpiConfiguration
from azureml.tensorboard import Tensorboard
from tabulate import tabulate


available_instances = {
    "1xK80": "Standard_NC6",
    "2xK80": "Standard_NC12",
    "4xK80": "Standard_NC24",
    "1xM60": "Standard_NV6",
    "2xM60": "Standard_NV12",
    "4xM60": "Standard_NV24",
    "1xV100": "Standard_NC6s_v3",
    "2xV100": "Standard_NC12s_v3",
    "4xV100": "Standard_NC24s_v3",
    "8xV100": "Standard_ND40rs_v2",
    "CPU": "Standard_D8_v3",
}


def get_environment(requirements_file: Path, docker_image: str):
    if not requirements_file.exists():
        raise RuntimeError(f"Given requirements file '{requirements_file}' does not exist at the provided path")
    elif requirements_file.name.endswith(".txt"):
        env = Environment.from_pip_requirements("my-pip-env", requirements_file)
    elif requirements_file.name.endswith(".yml"):
        env = Environment.from_conda_specification("my-env", requirements_file)
    else:
        print("Couldn't resolve env from requirements file")

    env.docker.enabled = True
    env.docker.base_image = docker_image
    return env


def get_inferred_instance(gpu_type: str, num_gpus: int):
    if gpu_type is None:
        return available_instances.get("CPU")
    instance = available_instances.get(f"{num_gpus}x{gpu_type}")
    assert instance is not None, f"Could not look up inferred instance w/ Num GPUs: {num_gpus} and GPU Type: {gpu_type}"
    return instance


def find_or_create_compute_target(
    workspace,
    name,
    vm_size="STANDARD_NC6",
    min_nodes=0,
    max_nodes=1,
    idle_seconds_before_scaledown=1200,
    vm_priority="lowpriority",
):

    if name in workspace.compute_targets:
        return ComputeTarget(workspace=workspace, name=name)
    else:
        config = AmlCompute.provisioning_configuration(
            vm_size=vm_size,
            min_nodes=min_nodes,
            max_nodes=max_nodes,
            vm_priority=vm_priority,
            idle_seconds_before_scaledown=idle_seconds_before_scaledown,
        )
        target = ComputeTarget.create(workspace, name, config)
        target.wait_for_completion(show_output=True)
    return target


def submit_basic_run(
    script,
    script_args,
    workspace_config="./config.json",
    target_name="my-cluster",
    gpu_type="K80",
    num_gpus=1,
    min_nodes=0,
    max_nodes=10,
    num_nodes=1,
    dataset_name=None,
    dataset_mount_dir="/dataset",
    experiment_name="pycloud-dev",
    requirements_file="./environment.yml",
    docker_image="mcr.microsoft.com/azureml/openmpi3.1.2-cuda10.2-cudnn8-ubuntu18.04",
):
    ws = Workspace.from_config(workspace_config)
    compute_target = find_or_create_compute_target(
        ws, target_name, get_inferred_instance(gpu_type, num_gpus), min_nodes, max_nodes
    )
    env = get_environment(requirements_file, docker_image)
    run_config = ScriptRunConfig(
        source_directory=Path(script).parent,
        script=Path(script).name,
        arguments=script_args,
        compute_target=compute_target,
        environment=env,
        distributed_job_config=MpiConfiguration(process_count_per_node=1, node_count=num_nodes),
    )
    if dataset_name is not None:
        ds = ws.datasets.get(dataset_name)
        run_config.run_config.data = {ds.name: ds.as_mount(dataset_mount_dir)}

    run = Experiment(ws, experiment_name).submit(run_config)
    return run


def list_datasets(workspace_config: Path):
    ws = Workspace.from_config(workspace_config)
    names, versions, dates = [], [], []
    for ds_name in ws.datasets:
        names.append(ds_name)

    print(
        tabulate(
            {"Datasets": names},
            headers="keys",
            tablefmt="github",
        )
    )


def create_dataset(workspace_config, source_dir, name, description=None, overwrite=False):
    ws = Workspace.from_config(workspace_config)
    datastore = ws.get_default_datastore()
    datastore.upload(
        src_dir=source_dir,
        target_path=name,
        overwrite=overwrite,
        show_progress=True,
    )
    _ = Dataset.File.from_files(path=[(datastore, name)]).register(
        workspace=ws,
        name=name,
        description=description,
        create_new_version=True,
    )


def create_tensorboard(workspace_config, experiment_name):
    ws = Workspace.from_config(workspace_config)
    exp = Experiment(ws, experiment_name)
    tb = Tensorboard([*exp.get_runs()])
    tb.start()
    _ = input("press any key to stop tensorboard")
    tb.stop()
