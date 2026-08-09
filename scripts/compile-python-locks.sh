#!/usr/bin/env bash

set -euo pipefail

readonly EXPECTED_PIP_VERSION="26.0.1"
readonly EXPECTED_PIP_TOOLS_VERSION="7.6.0"
readonly EXPECTED_PYTHON_VERSION="3.14"
readonly REPOSITORY_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly APPLICATIONS=(
  "flask-auth-dash-bootstrap"
  "flask-bootstrap"
  "flask-connextion-rest"
  "flask-mongo-celery"
  "flask-sql-celery"
)

if [[ $# -gt 1 || ( $# -eq 1 && "$1" != "--check" ) ]]; then
  echo "usage: $0 [--check]" >&2
  exit 64
fi

actual_python_version="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
if [[ "$actual_python_version" != "$EXPECTED_PYTHON_VERSION" ]]; then
  echo "Python $EXPECTED_PYTHON_VERSION is required; found $actual_python_version" >&2
  exit 1
fi

actual_pip_version="$(python -m pip --version | awk '{print $2}')"

if [[ "$actual_pip_version" != "$EXPECTED_PIP_VERSION" ]]; then
  echo "pip $EXPECTED_PIP_VERSION is required; found $actual_pip_version" >&2
  exit 1
fi

if ! pip_tools_version_output="$(python -m piptools compile --version 2>&1)"; then
  echo "pip-tools could not run with pip $actual_pip_version:" >&2
  echo "$pip_tools_version_output" >&2
  exit 1
fi

actual_pip_tools_version="$(awk '{print $NF}' <<<"$pip_tools_version_output")"

if [[ "$actual_pip_tools_version" != "$EXPECTED_PIP_TOOLS_VERSION" ]]; then
  echo "pip-tools $EXPECTED_PIP_TOOLS_VERSION is required; found $actual_pip_tools_version" >&2
  exit 1
fi

check_failed=0
temporary_directory=""
if [[ "${1:-}" == "--check" ]]; then
  temporary_directory="$(mktemp -d)"
  trap 'rm -rf -- "$temporary_directory"' EXIT
fi

for application in "${APPLICATIONS[@]}"; do
  lock_file="$REPOSITORY_ROOT/$application/requirements.txt"
  output_file="requirements.txt"
  if [[ -n "$temporary_directory" ]]; then
    output_file="$temporary_directory/$application-requirements.txt"
  fi

  (
    cd "$REPOSITORY_ROOT/$application"
    CUSTOM_COMPILE_COMMAND="./scripts/compile-python-locks.sh" \
      python -m piptools compile \
      --quiet \
      --output-file="$output_file" \
      --strip-extras \
      requirements.in
  )

  if [[ -n "$temporary_directory" ]] && ! diff -u "$lock_file" "$output_file"; then
    check_failed=1
  fi
done

exit "$check_failed"
