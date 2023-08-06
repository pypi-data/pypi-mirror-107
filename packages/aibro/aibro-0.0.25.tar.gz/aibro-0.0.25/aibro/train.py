import datetime
import os
import shutil
from time import sleep
from typing import Any
from typing import Dict
from typing import Optional

import numpy as np
import requests
import tensorflow as tf
from dotenv import load_dotenv

from aibro.sio import connect_to_server_socket
from aibro.sio import sio_disconnect
from aibro.utils import datetime_to_timestamp_ms
from aibro.utils import pickle_and_base64_decode
from aibro.utils import timestamp_ms_to_datetime_str
from aibro.utils import unpack_base64_encoded_pickle

load_dotenv(".env")

IS_LOCAL = os.environ.get("IS_LOCAL", "false") == "true"
SERVER_HOST = (
    os.environ.get("SERVER_HOST", "3.236.105.55") if IS_LOCAL else "3.236.105.55"
)
AUTHENTICATED_USER_ID = None


def fit(
    model: Any,
    train_X: np.ndarray,
    train_Y: np.ndarray,
    machine_id: str,
    batch_size: int = 1,
    epochs: int = 1,
    validation_X: np.array = None,
    validation_Y: np.array = None,
    description="",
    fit_kwargs: Dict[str, Any] = {},
):
    assert model.__class__.__module__.startswith("tensorflow")
    train(
        model=model,
        train_X=train_X,
        train_Y=train_Y,
        machine_id=machine_id,
        batch_size=batch_size,
        epochs=epochs,
        validation_X=validation_X,
        validation_Y=validation_Y,
        description=description,
        fit_kwargs=fit_kwargs,
    )


def train(
    batch_size: int,
    epochs: int,
    machine_id: str,
    model: Any = None,
    train_X=None,
    train_Y=None,
    validation_X=None,
    validation_Y=None,
    previous_job_id=None,
    description="",
    fit_kwargs: Dict[str, Any] = {},
) -> Optional[str]:
    job_id = None
    try:
        # job_id = "456e7d3e-cab8-4111-aa01-b9fcf2aaee6a"
        # _connect_to_server(job_id, SERVER_HOST, resume=False)
        # return
        user_id = _check_authentication()

        # TODO: currently assume model is TF, pidata is numpy
        if model:
            print("Serializing model")
            serialized_model = model.to_json()
            loss = pickle_and_base64_decode(model.loss)
            metrics = pickle_and_base64_decode(model.compiled_metrics)
            # Optimizer cannot pickle directly due to local
            optimizer = pickle_and_base64_decode(model.optimizer._name)

        print("Serializing dataset")
        encoded_train_X = (
            pickle_and_base64_decode(train_X) if train_X is not None else None
        )
        encoded_train_Y = (
            pickle_and_base64_decode(train_Y) if train_Y is not None else None
        )
        encoded_validation_X = (
            pickle_and_base64_decode(validation_X) if validation_X is not None else None
        )
        encoded_validation_Y = (
            pickle_and_base64_decode(validation_Y) if validation_Y is not None else None
        )

        connect_to_server_socket(SERVER_HOST, "8000")
        data = {
            "model_json": serialized_model if model else None,
            "encoded_train_X": encoded_train_X,
            "encoded_train_Y": encoded_train_Y,
            "encoded_validation_X": encoded_validation_X,
            "encoded_validation_Y": encoded_validation_Y,
            "user_id": user_id,
            "batch_size": batch_size,
            "epochs": epochs,
            "machine_id": machine_id,
            "fit_kwargs": fit_kwargs,
            "metrics": metrics if model else None,
            "loss": loss if model else None,
            "optimizer": optimizer if model else None,
            "job_id": previous_job_id,
            "description": description,
        }
        resp = _post_json(data, "v1/model_and_dataset")

        if resp.status_code != 200:
            _handle_error(resp)

        job_id = resp.json()["job_id"]
        server_public_ip = resp.json()["server_public_ip"]
        _connect_to_server(job_id, server_public_ip)

        return job_id

    except Exception as e:
        error_msg = str(e)
        print(f"{str(e)}")
        if "Connection aborted" in error_msg and job_id:
            _handle_server_interruption(job_id, machine_id, batch_size, epochs)
        return job_id


def get_model(job_id: str, epoch: int, directory="."):
    _check_authentication()

    data = {"job_id": job_id, "epoch": epoch}
    resp = _post_json(data, "v1/get_model")
    if resp.status_code == 200:
        content = resp.json()["model_ckpt_content"]
        unpacked_model_content = unpack_base64_encoded_pickle(content)
        file_name = f"{directory}/model_{epoch:04d}.h5"
        f = open(file_name, "wb")
        f.write(unpacked_model_content)
        f.close()
        print(f"Saved model to {file_name}")
    else:
        _handle_error(resp)


def get_tensorboard_logs(job_id: str, directory="."):
    _check_authentication()

    data = {"job_id": job_id}
    resp = _post_json(data, "v1/get_tensorboard_logs")
    if resp.status_code == 200:
        content = resp.json()["log_zip"]
        log_zip = unpack_base64_encoded_pickle(content)
        file_name = f"{directory}/logs.zip"
        f = open(file_name, "wb")
        f.write(log_zip)
        f.close()
        log_dir = f"{directory}/logs/{job_id}/"
        shutil.unpack_archive(file_name, log_dir, "zip")
        os.remove(file_name)
        print(f"Saved logs to {log_dir}")
    else:
        _handle_error(resp)


def available_machines():
    _check_authentication()
    resp = requests.get(
        f"http://{SERVER_HOST}:8000/v1/marketplace_machines",
    )
    if resp.status_code != 200:
        _handle_error(resp)
    else:
        print("Available Resources:")
        for name, spec in resp.json().items():
            available_counts = spec["AVAILABLE"]
            if available_counts <= 0:
                continue

            GPU_type = spec["GPU"]
            num_vCPU = spec["CPU CORES"]
            pricing = spec["PRICING"]
            print(
                f"{f'Machine Id: {name}' : <26} {f'GPU Type: {GPU_type}' : <18} {f'num_vCPU: {num_vCPU}' : <15} {f'cost: {pricing}' : <20}"  # noqa
            )


def retrain(
    job_id: str,
    machine_id: str,
    batch_size: int,
    epochs: int,
    resume: bool = False,
):
    user_id = _check_authentication()
    data = {
        "job_id": job_id,
        "user_id": user_id,
        "machine_id": machine_id,
        "batch_size": batch_size,
        "epochs": epochs,
        "resume": resume,
    }

    try:
        connect_to_server_socket(SERVER_HOST, "8000")
        resp = _post_json(data, "v1/retrain")

        if resp.status_code == 500:
            _handle_error(resp)

        job_id = resp.json()["job_id"]
        server_public_ip = resp.json()["server_public_ip"]
        _connect_to_server(job_id, server_public_ip)

    except Exception as e:
        print(f"{str(e)}")


def retrain_with_new_model(
    model: Any,
    job_id: str,
    machine_id: str,
    batch_size: int,
    epochs: int,
    description="",
):
    train(
        machine_id=machine_id,
        batch_size=batch_size,
        epochs=epochs,
        previous_job_id=job_id,
        model=model,
        description=description,
    )


def retrain_with_new_data(
    job_id: str,
    machine_id: str,
    batch_size: int,
    epochs: int,
    train_X,
    train_Y,
    validation_X=None,
    validation_Y=None,
    description="",
):
    train(
        machine_id=machine_id,
        batch_size=batch_size,
        epochs=epochs,
        train_X=train_X,
        train_Y=train_Y,
        validation_X=validation_X,
        validation_Y=validation_Y,
        previous_job_id=job_id,
        description=description,
    )


def list_trials(last_days=1):
    user_id = _check_authentication()
    last_day_ts = datetime_to_timestamp_ms(
        datetime.datetime.now() - datetime.timedelta(days=last_days)
    )
    data = {"user_id": user_id, "last_day_ts": last_day_ts}
    resp = _post_json(data, "v1/list_trials")
    if resp.status_code == 200:
        _format_trial_history(resp.json()["user_jobs"])
    else:
        _handle_error(resp)


def _format_trial_history(trials):
    print(
        f"{'Date' : <20} {'Job id' : <40} {'Status' : <10} {'Current epoch' : <20} Description"
    )
    for trial in trials:
        formatted_date = timestamp_ms_to_datetime_str(
            trial["job_created_ms"] // 1000, "%m/%d/%Y %H:%M:%S"
        )
        is_completed = trial["is_completed"]
        current_epoch = trial["current_epoch"]
        is_training = trial["is_training"]
        if is_training:
            status = "training"
        elif is_completed:
            status = "completed"
        else:
            status = "not started"
        job_id = trial["job_id"]
        description = trial["description"]
        print(
            f"{f'{formatted_date}' : <20} {f'{job_id}' : <40} {f'{status}' : <10} {f'{current_epoch}' : <20} {description}"  # noqa
        )


def _handle_server_interruption(job_id, machine_id, batch_size, epochs):
    print("Server interrupted, starting a new server to resume")
    retrain(job_id, machine_id, batch_size, epochs, resume=True)


def _check_authentication() -> Optional[str]:
    global AUTHENTICATED_USER_ID
    if not AUTHENTICATED_USER_ID:
        email = input("Enter your email: ")
        data = {"email": email}
        resp = _post_json(data, "v1/authenticate")

        if resp.status_code == 200:
            AUTHENTICATED_USER_ID = resp.json()["user_id"]
            print("Successfully authenticated!")
        else:
            _handle_error(resp)
    else:
        print("Already authenticated!")

    return AUTHENTICATED_USER_ID


def _connect_to_server(
    job_id: str, server_public_ip: str, port: str = "12345", resume: bool = False
):
    connect_to_server_socket(server_public_ip, port)

    data = {"tensorflow_version": tf.__version__, "resume": resume}
    resp = _post_json(data, job_id, host=server_public_ip, port="12345")
    if resp.status_code == 200:
        print("Done")
        sleep(1)
        sio_disconnect()

        # Stop spot after it's done
        data = {"job_id": job_id}
        resp = _post_json(data, "v1/stop_spot")
        if resp.status_code != 200:
            _handle_error(resp)
    else:
        _handle_error(resp)


def _post_json(
    data: Dict[str, Any], endpoint: str, host: str = SERVER_HOST, port: str = "8000"
):
    headers = {"Content-Type": "application/json"}
    return requests.post(
        f"http://{host}:{port}/{endpoint}",
        json=data,
        headers=headers,
    )


def _handle_error(resp):
    content = resp.content.decode("utf-8")
    sio_disconnect()
    raise Exception(content)
