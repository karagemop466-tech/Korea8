#!/usr/bin/env bash
# Autonomous public-mirror restore for the E1 lane. This does not bypass DrivenData login.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python}"
if [[ -x "${ROOT}/.venv/bin/python" ]]; then PYTHON_BIN="${ROOT}/.venv/bin/python"; fi
exec "${PYTHON_BIN}" "${ROOT}/scripts/fetch_inputs.py"
