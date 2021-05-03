#! /usr/bin/env python

import os
import json
import signal
import subprocess
import time
import shutil

import click


# Ensure an environment variable exists and has a value
def setenv(variable, default):
    os.environ[variable] = os.getenv(variable, default)
    # print(f"env: {variable}:{os.environ[variable]}")

setenv("APPLICATION_CONFIG", "development")

APPLICATION_CONFIG_PATH = "config"
DOCKER_PATH = "docker"


def app_config_file(config):
    return os.path.join(APPLICATION_CONFIG_PATH, f"{config}.json")

def docker_compose_file(config):
    return os.path.join(DOCKER_PATH, f"{config}.yml")

def configure_env(config):
    # Read configuration from the relative JSON file
    with open(app_config_file(config)) as f:
        config_data = json.load(f)

    # Convert the config into a usable Python dictionary
    config_data = dict((i["name"], i["value"]) for i in config_data)

    for key, value in config_data.items():
        try:
            if key == 'MONGODB_SETTINGS':
                setenv(key, json.dumps(value))
                # print(f"Set {key}:{value}")

            if key == 'DEBUG_TB_PANELS':
                setenv(key, json.dumps(value))

            if key in os.environ:
                # print(f"duplicate: {key}:{value}")
                pass

            if not key in os.environ:
                setenv(key, value)
                # print(f"Set {key}:{value}")

        except Exception as error:
            print(f"config variable: {key}:{value} : {error}")

@click.group()
def cli():
    pass

@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def flask(subcommand):
    configure_env(os.getenv("APPLICATION_CONFIG"))

    cmdline = ["flask"] + list(subcommand)

    try:
        p = subprocess.Popen(cmdline)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()


def docker_compose_cmdline(commands_string=None):
    config = os.getenv("APPLICATION_CONFIG")
    print(f"config: {config}") #, os_env: {os.environ}")

    configure_env(config)

    compose_file = docker_compose_file(config)
    print(f"compose_file: {compose_file}")

    if not os.path.isfile(compose_file):
        raise ValueError(f"The file {compose_file} does not exist")

    command_line = [
        "docker-compose",
        "-p",
        config,
        "-f",
        compose_file,
    ]

    if commands_string:
        command_line.extend(commands_string.split(" "))

    print(f"command_line: {command_line}")
    return command_line

@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def compose(subcommand):
    cmdline = docker_compose_cmdline() + list(subcommand)

    try:
        p = subprocess.Popen(cmdline)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()

@cli.command()
@click.argument("filenames", nargs=-1)
def test(filenames):
    """
    Initializes test environment, loads testing config and sets it to env variables, generates init script if applicable for mongo, spins mongo container, then executes pytest
    """
    os.environ["APPLICATION_CONFIG"] = "testing"
    configure_env(os.getenv("APPLICATION_CONFIG"))

    cmdline = docker_compose_cmdline("up -d")
    subprocess.call(cmdline)

    #cmdline = docker_compose_cmdline("logs db")
    #wait_for_logs(cmdline, "Waiting for connections")

    ##### Modify for mongo
    ##### Modify for mongo

    # run_mongo([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])

    ##### Modify for mongo
    ##### Modify for mongo

    cmdline = ["pytest", "-s", "--cov-branch", "--verbosity=4", "--cov-report=term-missing","--cov=hello.py"] 
    cmdline.extend(filenames)
    print(f"test command: {cmdline}")
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline("down")
    subprocess.call(cmdline)

if __name__ == '__main__':
    cli()
