"""Entry-point used by hosting platforms (App Service / Container) to start the MCP server.

Assumes your MCP implementation lives in app.py and exposes a FastMCP instance named `mcp`.
If your file/module name differs, update the import accordingly.
"""

import os

# Optional: allow overriding the module path via env var (useful across environments)
MCP_APP_MODULE = os.getenv("MCP_APP_MODULE", "app")  # default: app.py
MCP_APP_OBJECT = os.getenv("MCP_APP_OBJECT", "mcp")  # default: mcp instance in app.py
TRANSPORT = os.getenv("MCP_TRANSPORT", "streamable-http")

def main():
    module = __import__(MCP_APP_MODULE)
    mcp = getattr(module, MCP_APP_OBJECT)

    # FastMCP exposes .run(); keep transport HTTP for APIM compatibility.
    # Host/port are passed via common env vars when available.
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", os.getenv("WEBSITES_PORT", "8000")))

    # Many runtimes inject PORT/WEBSITES_PORT; FastMCP reads host/port in newer versions.
    # Pass defensively if supported.
    try:
        mcp.run(transport=TRANSPORT, host=host, port=port)
    except TypeError:
        # Fallback for SDK versions where host/port args aren't accepted
        mcp.run(transport=TRANSPORT)


if __name__ == "__main__":
    main()
