#!/usr/bin/env bash
set -euo pipefail

cd /opt/mcp-brasil
export UV_CACHE_DIR="${UV_CACHE_DIR:-/tmp/uv-cache}"

exec /root/.local/bin/uv run python -c "from mcp_brasil.server import mcp; mcp.run(transport='streamable-http', host='0.0.0.0', port=8889)"
