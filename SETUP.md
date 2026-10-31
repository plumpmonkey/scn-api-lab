# Setup and Troubleshooting

This lab runs on the **UWEcyber VM** and starts with **one command**. Read this only if you hit a
problem. All commands are bash commands to run in a terminal on the VM.

## Starting the service

**Requirements:** Docker running on the VM. Confirm:

```bash
docker --version
docker compose version
```

**Start the service** from inside the `vulnerable-api/` folder:

```bash
docker compose up --build
```

That builds the image (first run only, about a minute) and starts the API on
<http://localhost:5000>. Leave this terminal (terminal 1) open for logs; use a second terminal
(terminal 2) for `curl`, `gitleaks` and everything else. Stop with `Ctrl+C`, or from terminal 2:

```bash
docker compose down
```

The API is published on the VM's loopback address only (`docker port scn-notes-api` shows
`5000/tcp -> 127.0.0.1:5000`), so use Firefox **on the VM**. It is deliberately unreachable from
other machines.

**Your work persists.** The lab folder is bind-mounted into the container, so everything you edit or
commit is written to the VM's disk, not the container. Stop Docker, reboot the VM, come back next
session — open the same folder and continue. The container is disposable; the folder is not.

## Running gitleaks (no install needed)

gitleaks runs from its Docker image. From inside `vulnerable-api/`:

```bash
# Scan the files on disk:
docker run --rm -v "$PWD:/repo:ro" zricethezav/gitleaks:v8.30.1 dir /repo -v

# Scan the full git history:
docker run --rm -v "$PWD:/repo:ro" zricethezav/gitleaks:v8.30.1 git /repo -v
```

gitleaks exits with code 1 when it finds secrets — but also when the scan itself fails. Read the last
line (`leaks found: N`) rather than relying on the exit code.

## Common problems

| Symptom | Cause / fix |
|--------|-------------|
| `Cannot connect to the Docker daemon` | Docker is not running. Run `sudo systemctl start docker`, then try again. |
| `curl: (7) Failed to connect to localhost port 5000` | The container is not running. Check terminal 1 for an error, or run `docker compose ps`. Start it again with `docker compose up` in terminal 1. |
| Terminal 1 shows a Python error such as `NameError: name 'require_api_key' is not defined` and returns to the prompt | The app crashed on a mistake in `app.py` (here, the function was pasted below the routes that use it). Fix and save the file, then run `docker compose up` again in terminal 1. |
| `app.py` will not run and you cannot find the mistake | Copy the checkpoint for the task you are on, from inside `vulnerable-api/`: `cp ../checkpoints/app-after-task2.py app.py` (or `app-after-task3.py`, `app-after-task4-step5.py`). The Task 4 checkpoint needs your `.env` from Task 4, Steps 2–3. If the app had crashed, run `docker compose up` in terminal 1. |
| `curl: (56) Recv failure: Connection reset by peer` | The app was still starting. Wait until terminal 1 shows `Debugger is active!`, then run the command again. |
| `port is already allocated` on 5000 | Something else uses port 5000. Stop it, or change `127.0.0.1:5000:5000` to `127.0.0.1:5001:5000` in `docker-compose.yml` and use `localhost:5001`. |
| Code edits don't take effect | Check you saved the file, then run `docker compose restart` in terminal 2. Your code is bind-mounted, so a restart always loads the latest. |
| Changed `.env` but the old secret still works | Flask's reloader keeps the old environment. Run `docker compose restart` after **every** change to `.env`. |
| `KeyError: 'JWT_SECRET'` or `JWT_SECRET must be at least 32 characters; refusing to start` | Expected if `.env` is missing, or `JWT_SECRET` is empty or too short — the app fails safe rather than running insecurely. Fix `.env`, then run `docker compose up` in terminal 1. |
| `$TOKEN` is empty, or `curl` gets `missing bearer token` | Shell variables belong to one terminal. If you opened a new terminal, run the mint command again. |
| The mint command prints a long Python error instead of a token | The mint command imports your `app.py`, so a mistake in `app.py` shows up here. Check terminal 1 for the same error and fix the file. |
| gitleaks finds **0** secrets in history | You are probably scanning a folder with no `.git`. Confirm `git log --oneline` shows three commits. If it does not, run `cd ~/scn-api-lab/vulnerable-api` and check again. |
| gitleaks mount looks wrong / empty | Make sure you run the command **from inside `vulnerable-api/`** so `$PWD` points at the repo. |
| `Permission denied` deleting `__pycache__` files | Python inside the container creates them as root. Remove them with `docker run --rm -v "$PWD:/app" scn-notes-api rm -rf /app/__pycache__`. |
| Extension 1, Step 2 reports `unknown` instead of `unverified` | TruffleHog could not reach Stripe to check the key. Check the VM has internet access. |
