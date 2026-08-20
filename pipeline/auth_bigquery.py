"""
Run this first: python auth_bigquery.py
Opens a browser (your logged-in Chrome) for Google OAuth consent and writes
Application Default Credentials to ~/.config/gcloud/application_default_credentials.json.
The mysql_to_bq_pipeline script picks these up automatically via google-cloud-bigquery /
pandas-gbq -- no key file or hardcoded secret needed.
"""
import subprocess
import sys

import google.auth
from google.auth.exceptions import DefaultCredentialsError


def already_authenticated() -> bool:
    try:
        google.auth.default()
        return True
    except DefaultCredentialsError:
        return False


def main() -> None:
    if already_authenticated():
        print("Application Default Credentials already present.")
        return

    print("No Application Default Credentials found. Opening browser to authenticate...")
    result = subprocess.run(["gcloud", "auth", "application-default", "login"])
    if result.returncode != 0:
        print("gcloud auth failed.", file=sys.stderr)
        sys.exit(result.returncode)

    print("Authenticated.")


if __name__ == "__main__":
    main()
