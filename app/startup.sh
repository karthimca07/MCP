#!/usr/bin/env bash
set -euo pipefail

# Startup command file for Azure App Service (Linux) or generic containers.
# App Service supports specifying a startup command file such as startup.sh.

# Ensure stdout/stderr are unbuffered for better container logs
export PYTHONUNBUFFERED=1

# Default port for local; App Service sets WEBSITES_PORT/PORT
export PORT="${PORT:-${WEBSITES_PORT:-8000}}"

# If you keep your code in /home/site/wwwroot (App Service), this will already be the CWD.
# Otherwise, uncomment and adjust:
# cd /home/site/wwwroot

# Install dependencies if you’re using Oryx build and requirements.txt is present.
# (No-op if already installed.)
if [ -f requirements.txt ]; then
  python -m pip install --upgrade pip >/dev/null
  python -m pip install -r requirements.txt >/dev/null
fi

# Start the MCP server
exec python startup.py
