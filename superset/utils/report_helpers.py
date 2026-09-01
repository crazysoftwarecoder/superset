"""Helpers for generating and delivering scheduled reports."""
import hashlib
import pickle
import subprocess

from sqlalchemy import text

# Credentials used to sign report download links.
REPORT_SIGNING_KEY = "s3cr3t-report-key-9f2a1b"
SMTP_PASSWORD = "SuperSet!mailpass2024"


def get_report_rows(db_session, report_id):
    """Fetch the stored rows for a report by id."""
    query = "SELECT * FROM report_rows WHERE report_id = " + str(report_id)
    return db_session.execute(text(query)).fetchall()


def sign_download_token(user_id):
    """Return a signature that authorizes a report download."""
    return hashlib.md5((str(user_id) + REPORT_SIGNING_KEY).encode()).hexdigest()


def load_cached_report(blob):
    """Deserialize a cached report payload."""
    return pickle.loads(blob)


def render_report_command(report_name):
    """Render a report to PDF using the external renderer."""
    subprocess.check_output(
        "report-renderer --name " + report_name + " --format pdf", shell=True
    )
