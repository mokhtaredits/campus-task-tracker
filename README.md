# Campus Task Tracker

Campus Task Tracker is a small web app for organizing coursework. Add tasks,
mark them complete, reopen them, or delete them. SQLite stores task state.

## Tech stack

- Python 3.13 with Flask and Waitress
- SQLite for persistence
- Docker and Docker Compose
- GitHub Actions for container build and smoke testing

## Run with Docker Compose

Requirements are Docker Engine with Compose v2, or Docker Desktop. Run the
commands below from the cloned repository's root.

```sh
docker compose build
docker compose up -d --wait
docker compose ps
```

Open [the tracker](http://127.0.0.1:8000/) and
[the health endpoint](http://127.0.0.1:8000/health). The health endpoint returns
HTTP 200 and `{"status":"ok"}` when the task database is readable.

### Verify the application

1. Add a task named **Review Docker lab notes**. It should appear as **Pending**.
2. Click **Complete** and verify the state is **Completed**.
3. Run `docker compose down` followed by `docker compose up -d --wait`.
   Reload the page and verify that the task still exists.
4. Use **Reopen** to return it to **Pending**, then click **Delete**.

### Stop and clean up

```sh
docker compose down
```

To remove the Compose volume and permanently clear its tasks, run
`docker compose down -v`. To remove the built image after the container is
removed, run `docker image rm campus-task-tracker:1.0`.

### Configuration

| Name | Default | Purpose |
| --- | --- | --- |
| Host address and port | `127.0.0.1:8000` | Browser access from the Docker host |
| Container port | `8000` | Waitress HTTP server |
| `TASK_DB` | `/app/data/tasks.db` in Docker, `data/tasks.db` locally | SQLite database location |
| Compose volume | `task-data` | Stores the database across container replacement |

No environment values or credentials are required. If port 8000 is already
in use, change the host side of the Compose mapping to
`127.0.0.1:8001:8000` and use port 8001 in the browser.

### Run with Docker CLI

Stop Compose before using the same host port. This example uses its own
named volume.

```sh
docker build --progress=plain -t campus-task-tracker:1.0 .
docker run -d --name campus-task-tracker -p 127.0.0.1:8000:8000 --mount source=campus-task-data,target=/app/data campus-task-tracker:1.0
docker ps --filter name=campus-task-tracker
docker stop campus-task-tracker
docker rm campus-task-tracker
```

To delete the CLI example's data, run `docker volume rm campus-task-data`
after removing the container.

### Make shortcuts

If GNU Make is installed, use `make build`, `make run`, and `make stop`.
Each target calls Docker Compose.

## Run locally on Windows

Install Python 3.14, then run these commands in PowerShell from the project
root. Use Ctrl+C to stop the server before starting Docker on the same port.

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\waitress-serve.exe --listen=127.0.0.1:8000 src.app:app
```

## Assignment documentation

- [Technical notes](docs/notes.md)
- [Demonstration screenshots](docs/screenshots/)

## Attribution

This starter was created for this assignment without using an existing
open-source application as its base. It uses
[Flask](https://flask.palletsprojects.com/),
[Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/),
and the [official Python container image](https://hub.docker.com/_/python).

