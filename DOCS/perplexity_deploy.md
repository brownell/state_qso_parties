<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# I want to deploy an app to fly.io. The web app is in python and uses sqlite3 for data storage. The database should be in a separate volume so that the data persists across updates of the software volume. There are also static data (reference) files that can live in the same volume as the software. I have used VS Code for development and have the container extensions installed. Can I use VS Code to automate some of the work of building and deploying the app. And if so how?

Yes. Use VS Code’s **Tasks** feature to run Fly.io’s command-line tools. That gives you a repeatable “build and deploy” command inside VS Code, while a Fly Volume keeps your SQLite database separate from the application image. You do not need a special Fly.io extension—or even a local Docker daemon if you use Fly’s remote builder.[^1_1][^1_2]

The setup I would use is:

- Application code and read-only reference files: packaged in the Docker image under `/app`.
- SQLite database: stored on a persistent Fly Volume mounted at `/data`.
- Deployment configuration: committed to your project as `Dockerfile`, `fly.toml`, and `.vscode/tasks.json`.
- Routine deployment: choose a task in VS Code that runs `fly deploy --remote-only --ha=false`.[^1_2][^1_3][^1_4]


## 1. Separate the application files from persistent data

Strictly speaking, you do not need a separate “software volume.” Fly builds your application into an image; the Fly Volume is the separate persistent storage attached to the running Machine. Files on that volume survive normal deployments and restarts.[^1_3][^1_2]

A project layout could be:

```text
myapp/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── fly.toml
├── reference/
│   ├── lookup.csv
│   └── other-reference.json
├── templates/
├── static/
└── .vscode/
    └── tasks.json
```

The corresponding runtime layout would be:

```text
/app/                      # From the application image
    app.py
    reference/
    templates/
    static/

/data/                     # Mounted Fly Volume
    app.db
```

Keep the mount at `/data`, not `/app`, so the persistent mount does not obscure your application files.

In Python, make the database location configurable and resolve reference files relative to your code:

```python
import os
import sqlite3
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent

DB_PATH = Path(
    os.environ.get("DATABASE_PATH", str(APP_DIR / "local-data" / "app.db"))
)
REFERENCE_DIR = APP_DIR / "reference"


def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH), timeout=30)
    conn.row_factory = sqlite3.Row
    return conn
```

This example uses a local development database unless `DATABASE_PATH` is set. On Fly, you will set it to `/data/app.db` through `fly.toml`, which supports both environment variables and volume mounts. If your existing application already uses a variable such as `EVENTS_DB`, keep that name consistently instead.[^1_5]

## 2. Define how to build and start the application

Fly can build directly from your project’s Dockerfile. The container extensions you already have are useful for local inspection and testing, but the deployment task can simply invoke Fly’s CLI.[^1_2]

Since you did not specify the Python framework, the following is a Flask example, assuming `app.py` exports a Flask object named `app`. For another framework, substitute its production server command.

`Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "4", "app:app"]
```

For this Flask example, `requirements.txt` must include `Flask`, `gunicorn`, and your other application dependencies.

Use a `.dockerignore` to keep development databases, virtual environments, and secrets out of the image:

```text
.git/
.vscode/
.venv/
venv/
__pycache__/
*.py[cod]

.env
.env.*

local-data/
*.db
*.db-*
*.sqlite
*.sqlite-*
*.sqlite3
*.sqlite3-*
```

Do not exclude `reference/`: those files are intentionally included by `COPY . .`. If some reference files are themselves SQLite databases, narrow the ignore patterns so those particular read-only files are included.

## 3. Perform the one-time Fly setup

Run these commands in VS Code’s integrated terminal, in the project directory. Install Fly’s CLI in the same Linux environment where your VS Code tasks will execute, then authenticate.

```bash
fly auth login
fly launch --no-deploy --ha=false
```

Choose an application name and region. `--no-deploy` lets you review the generated configuration before the first deployment; Fly detects an existing Dockerfile.[^1_6][^1_2]

For a concrete example, the configuration below uses `dfw`. Use the same region when creating the volume.

Review and edit the generated `fly.toml`:

```toml
app = "your-unique-app-name"
primary_region = "dfw"

[build]
  dockerfile = "Dockerfile"

[env]
  DATABASE_PATH = "/data/app.db"

[[mounts]]
  source = "app_data"
  destination = "/data"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory = "512mb"
```

The important relationships are:

- `DATABASE_PATH` points inside the mounted volume.
- `source = "app_data"` matches the volume name.
- `internal_port = 8080` matches the server’s listening port.
- The volume and application Machine must be in the same region.[^1_7][^1_5]

Create the volume explicitly:

```bash
fly volumes create app_data --region dfw --size 1
```

Then deploy:

```bash
fly deploy --remote-only --ha=false
```

Fly builds the image remotely and deploys it. The `--ha=false` option prevents automatically provisioning spare Machines; this configuration deliberately starts with a single application Machine and its SQLite volume.[^1_4][^1_8]

If this is an existing Fly app rather than a new one, inspect its current Machines and volumes before creating more:

```bash
fly status
fly volumes list
```

`--ha=false` does not scale an existing multi-Machine app down to one; scaling an existing app is a separate operation.[^1_8]

## 4. Add the VS Code deployment tasks

Create `.vscode/tasks.json` with the following content. VS Code supports process tasks with explicit arguments and a working directory, so the commands run from the project root.[^1_9][^1_1]

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Fly: Deploy",
      "type": "process",
      "command": "fly",
      "args": [
        "deploy",
        "--remote-only",
        "--ha=false"
      ],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "dedicated"
      }
    },
    {
      "label": "Fly: Status",
      "type": "process",
      "command": "fly",
      "args": ["status"],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "problemMatcher": []
    },
    {
      "label": "Fly: Logs",
      "type": "process",
      "command": "fly",
      "args": ["logs"],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "dedicated"
      }
    },
    {
      "label": "Fly: SSH console",
      "type": "process",
      "command": "fly",
      "args": ["ssh", "console"],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "problemMatcher": []
    }
  ]
}
```

Now use:

1. Save your changes.
2. Select Terminal → Run Task.
3. Choose `Fly: Deploy`.
4. Watch the build and deployment output in VS Code’s terminal.[^1_10]

That one task handles the build and deployment; you do not need separate local image-building and registry-pushing steps. Fly’s remote build is particularly convenient when working from your Chromebook’s Linux environment.[^1_2]

If VS Code reports that `fly` cannot be found, ensure its executable is on the environment’s `PATH`, or replace `"command": "fly"` with its absolute executable path.

## 5. Handle database initialization and migrations correctly

There is one important Fly-specific trap: do not initialize or migrate this SQLite database using a Dockerfile `RUN` command or Fly’s `release_command`. The persistent volume is unavailable during image builds, and Fly does not mount it in the temporary Machine used for `release_command`.[^1_3]

Instead, run an idempotent initialization/migration script when the actual application Machine starts, before starting the web server. For example:

`start.sh`:

```sh
#!/bin/sh
set -eu

python migrate.py

exec gunicorn \
    --bind 0.0.0.0:8080 \
    --workers 1 \
    --threads 4 \
    app:app
```

Then replace the Dockerfile’s `CMD` with:

```dockerfile
CMD ["sh", "/app/start.sh"]
```

Here, `migrate.py` is your application-specific migration script, not a built-in Fly utility. It should:

- Use the same `DATABASE_PATH` as the application.
- Create the initial schema only when needed.
- Apply only migrations that have not already run.
- Never delete or overwrite the existing database merely because the app restarted.

The script is invoked on each startup, but a correctly versioned migration script performs no schema changes when the database is already current. This places the work on the Machine where the volume is available, rather than in Fly’s separate release Machine.[^1_11][^1_3]

## 6. Know the limits of the single-volume arrangement

This design satisfies your persistence requirement, but persistence is not the same as replication or backup:

- A Fly Volume is local to one server and attaches to one Machine at a time.
- Multiple volumes do not automatically share SQLite changes.
- A single-Machine application can have downtime during deployments or host failures.
- Fly’s volume snapshots should not be your only backup strategy for important data.[^1_3]

For a modest application that can tolerate brief downtime, a single Machine plus a persistent SQLite volume is a straightforward starting point. Keep independent database backups, and do not scale it horizontally without first designing SQLite replication or moving to a shared database service. Fly explicitly identifies replication and backups as application responsibilities for volume-backed deployments.[^1_8][^1_3]

<span style="display:none">[^1_12][^1_13][^1_14][^1_15][^1_16][^1_17][^1_18][^1_19][^1_20][^1_21][^1_22][^1_23][^1_24][^1_25][^1_26][^1_27][^1_28][^1_29][^1_30][^1_31][^1_32][^1_33][^1_34][^1_35]</span>

<div align="center">⁂</div>

[^1_1]: https://code.visualstudio.com/docs/debugtest/tasks

[^1_2]: https://docs.fly.io/languages-and-frameworks/dockerfile

[^1_3]: https://docs.fly.io/volumes/overview

[^1_4]: https://docs.fly.io/flyctl/cmd/fly_deploy

[^1_5]: https://docs.fly.io/reference/configuration

[^1_6]: https://docs.fly.io/flyctl/cmd/fly_launch

[^1_7]: https://docs.fly.io/launch/volume-storage

[^1_8]: https://docs.fly.io/apps/app-availability

[^1_9]: https://code.visualstudio.com/docs/reference/tasks-appendix

[^1_10]: https://code.visualstudio.com/docs/editing/getting-started/tips-and-tricks

[^1_11]: https://docs.fly.io/blueprints/seamless-deployments

[^1_12]: https://docs.fly.io/languages-and-frameworks/dockerfile.md

[^1_13]: https://docs.fly.io/reference/fly-launch/

[^1_14]: https://docs.fly.io/launch/deploy

[^1_15]: https://docs.fly.io/launch/create

[^1_16]: https://docs.fly.io/blueprints/working-with-docker

[^1_17]: https://docs.fly.io/getting-started/troubleshooting

[^1_18]: https://docs.fly.io/model-context-protocol/deploy-on/fly-machine

[^1_19]: https://fly.io/learn/docker-hosting.md

[^1_20]: https://community.fly.io/t/some-issues-with-volumes-on-apps-v2/11994

[^1_21]: https://docs.fly.io/blueprints/hermes-agent-on-fly-io

[^1_22]: https://docs.fly.io/launch/autoscale-by-metric

[^1_23]: https://fly.io/docs/blueprints/using-base-images-for-faster-deployments/

[^1_24]: https://community.fly.io/t/volume-not-available-in-release-command/6566

[^1_25]: https://community.fly.io/t/release-command-questions/2962

[^1_26]: https://community.fly.io/t/volume-not-yet-available-mounted-while-executing-entrypoint-sh/15324

[^1_27]: https://community.fly.io/t/where-is-our-data-postgres-database-volume-0mb/16247

[^1_28]: https://community.fly.io/t/error-release-command-failed-aborting-deployment-error-release-command-machine-5683623ae3708e-exited-with-non-zero-status-of-1/17446

[^1_29]: https://www.perplexity.ai/search/21f7d0b4-f446-4dca-9adc-3614b01e7a40

[^1_30]: https://www.perplexity.ai/search/b39456b4-4150-44e5-8635-5e5d8233523d

[^1_31]: https://www.perplexity.ai/search/cf815b4f-22ce-4fe2-900b-821fe80de637

[^1_32]: https://www.perplexity.ai/search/01c324af-066e-4679-bd75-e0378e0e47bb

[^1_33]: https://www.perplexity.ai/search/e897e8d6-70fd-4784-8d8a-a3fe7f451b94

[^1_34]: https://www.perplexity.ai/search/a7d91e03-394b-47e6-b144-442782d68d02

[^1_35]: https://www.perplexity.ai/search/eb6b3fab-6c84-4cb6-9009-9e954611da97


---

# Will Docker access my .env file, or do I need to put my secrets in fly.toml or directly in the cli or ui of fly.io

Docker will not automatically load your local `.env` file into the deployed application. For your Fly.io deployment, put sensitive values in Fly **secrets**, and keep non-sensitive configuration in `fly.toml`. Fly injects the secrets into your running Python process as environment variables.[^2_1][^2_2]

In the configuration I gave you, `.env` is explicitly excluded by `.dockerignore`, so it will not be included in the image—which is intentional. Without that exclusion, `COPY . .` could copy it into the image, but copying a file does not automatically load its contents into the environment. Do not bake your secrets into the image.[^2_3]

## Import your existing secrets from a file

You can import your existing `.env` from VS Code’s integrated terminal:

```bash
fly secrets import --app your-unique-app-name < .env
```

Fly documents importing dotenv-style files this way, so you do not have to enter every value individually. Only import values appropriate for production; a development `.env` may contain local paths, development credentials, or debug settings you do not want on Fly.[^2_4]

For example, you could maintain an untracked `.env.production` containing just production secrets:

```text
SECRET_KEY=your-production-secret
API_KEY=your-production-api-key
SMTP_PASSWORD=your-production-smtp-password
```

Then import it:

```bash
fly secrets import --app your-unique-app-name < .env.production
```

This keeps secret values out of the command itself and out of your VS Code task definitions. Fly stores the imported values encrypted and supplies them at runtime.[^2_1][^2_4]

## Alternatively, set individual secrets

For one or two values:

```bash
fly secrets set \
  SECRET_KEY='your-production-secret' \
  API_KEY='your-production-api-key' \
  --app your-unique-app-name
```

Be aware that entering literal secrets this way can leave them in your shell history. File import avoids putting the values directly on the command line. You can list the configured secret names without displaying their values:

```bash
fly secrets list --app your-unique-app-name
```

Setting secrets normally updates and restarts the app’s Machines. To stage changes for your next deployment instead, use `--stage`:[^2_1]

```bash
fly secrets import --stage --app your-unique-app-name < .env.production
fly deploy --remote-only --ha=false
```


## Keep ordinary configuration in `fly.toml`

Your database path is not a secret, so it belongs here:

```toml
[env]
  DATABASE_PATH = "/data/app.db"
```

Passwords, API tokens, and session-signing keys should not be placed in this section—or in Dockerfile `ENV` instructions or `.vscode/tasks.json`. Fly’s documented separation is non-sensitive configuration in `fly.toml` and sensitive values in its secrets store.[^2_2]

## Read the values in Python

Your Python code reads Fly secrets just like any other environment variable:

```python
import os

SECRET_KEY = os.environ["SECRET_KEY"]
API_KEY = os.environ["API_KEY"]

DATABASE_PATH = os.environ.get("DATABASE_PATH", "/data/app.db")
```

No `.env` file needs to exist in the deployed container: Fly has already populated the process environment. These are runtime secrets, not values automatically available during the Docker image build.[^2_1]

For your workflow, keep `.env` for local development, import the production secrets into Fly once, and then use your normal VS Code deployment task. You do not need to re-import unchanged secrets on every deployment; they are stored with the Fly app, independently of your image.[^2_1]

<span style="display:none">[^2_10][^2_5][^2_6][^2_7][^2_8][^2_9]</span>

<div align="center">⁂</div>

[^2_1]: https://docs.fly.io/apps/secrets

[^2_2]: https://docs.fly.io/rails/the-basics/configuration

[^2_3]: https://community.fly.io/t/clarification-on-environment-variables/6309

[^2_4]: https://docs.fly.io/js/the-basics/secrets

[^2_5]: https://docs.fly.io/machines/runtime-environment

[^2_6]: https://community.fly.io/t/environment-variables-set-by-flyctl-secrets/12266

[^2_7]: https://community.fly.io/t/environment-variables/6601

[^2_8]: https://community.fly.io/t/accessing-autoset-env-variables/10190

[^2_9]: https://community.fly.io/t/support-fetching-variables-from-the-env-file/15523

[^2_10]: https://community.fly.io/t/access-fly-secrets-in-react-runtime/9284

