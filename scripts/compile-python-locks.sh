#!/usr/bin/env bash

set -euo pipefail

readonly EXPECTED_UV_VERSION="0.12.5"
readonly TARGET_PLATFORM="linux"
readonly TARGET_PYTHON_VERSION="3.14"
readonly REPOSITORY_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly COMPILE_COMMAND="uv pip compile --python-version=$TARGET_PYTHON_VERSION --no-emit-package=setuptools --output-file=requirements.txt requirements.in"
readonly APPLICATIONS=(
  "flask-auth-dash-bootstrap"
  "flask-bootstrap"
  "flask-connextion-rest"
  "flask-dash-bootstrap"
  "flask-mongo-celery"
  "flask-sql-celery"
)

if [[ $# -gt 1 || ( $# -eq 1 && "$1" != "--check" ) ]]; then
  echo "usage: $0 [--check]" >&2
  exit 64
fi

actual_uv_version="$(uv --version | awk '{print $2}')"
if [[ "$actual_uv_version" != "$EXPECTED_UV_VERSION" ]]; then
  echo "uv $EXPECTED_UV_VERSION is required; found $actual_uv_version" >&2
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
    # Seed uv with the committed lock so --check verifies the reviewed solution
    # instead of upgrading unrelated transitive packages released afterward.
    cp "$lock_file" "$output_file"
  fi

  (
    cd "$REPOSITORY_ROOT/$application"
    uv pip compile \
      --quiet \
      --python-platform "$TARGET_PLATFORM" \
      --python-version="$TARGET_PYTHON_VERSION" \
      --no-emit-package=setuptools \
      --custom-compile-command "$COMPILE_COMMAND" \
      --output-file="$output_file" \
      requirements.in
  )

  if [[ -n "$temporary_directory" ]] && ! diff -u "$lock_file" "$output_file"; then
    check_failed=1
  fi
done

exit "$check_failed"
