# pyATS Server

## Overview

This project provides a FastAPI server interface for AI agents and systems to interact with network devices via pyATS. Interactions are carried out over HTTP.

> [!NOTE]
> This project is a _proof-of-concept_, so I won't be adding new features on request. If you need more functionality, feel free to fork the repo.

## Features

- Retrieve device health data (memory, CPU, logging).
- Obtain interface details and configuration.
- Currently supports only IOS-XE functions.

## Setup

Add your network devices by placing your `pyats_testbed.yaml` file in the [config](config/) directory. A default testbed is available. Update the [TESTBED_FILE](config/global_settings.py#L11) variable if you use a different filename.

The env var `PYATS_SERVER_PORT` set the port the pyATS server will listen to. [Defaults](.env.example#L1) to `57000`.

## Run

You can run directly on your shell or using a container.

### Option 1. Container Based

Start the container

```bash
make container-run
```

Stop the container

```bash
make stop-container
```

### Option 2. Shell based

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server using one of the following commands:

```bash
make run
```

## API Endpoints

See the endpoints in the OAD client at `http://<IP_SERVER>:<PYATS_SERVER_PORT>/docs` or the docstrings in the source code under the [pyats_connector/api](pyats_connector/api/) directory.

Endpoints:

- `GET /health/memory`
- `GET /health/cpu`
- `GET /health/logging`
- `GET /interface/running-config`
- `GET /interfaces/status-and-description`
- `GET /interfaces/status`
- `GET /interface/detailed-status`
- `GET /interface/information`
- `GET /interface/admin-status`
- `GET /interface/verify-state-up`
- `GET /interface/events`
- `GET /devices/list`
- `GET /isis/neighbors`
- `GET /isis/interface-events`
- `GET /isis/interface-information`
- `GET /vrf/present`
- `GET /interface/interfaces-under-vrf`
- `GET /routing/routes`
- `PATCH /interface/shut`
- `PATCH /interface/unshut`

## Additional Information

- Use the provided `pyats_server.json` for client code generation.
- For testing pyATS functions independently of the API layer, see the comments in [tests/README.md](tests/README.md).
