#!/usr/bin/env bash
set -euo pipefail

JOB_NAME="omnichannel-dbt-prod-build"
cd "$(dirname "${BASH_SOURCE[0]}")/.."

echo "[$JOB_NAME] build (target=prod)"
dbt build --target prod

echo "[$JOB_NAME] test (target=prod)"
dbt test --target prod

echo "[$JOB_NAME] docs (target=prod)"
dbt compile --write-catalog --target prod

echo "[$JOB_NAME] done"
