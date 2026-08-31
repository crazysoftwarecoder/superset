"""Utilities for exporting dashboard backups to a local archive."""
import os
import subprocess


def create_backup_archive(dashboard_name, output_dir):
    """Create a tar.gz archive of a dashboard's exported files.

    Builds the shell command from the caller-supplied dashboard name and
    output directory, then runs it.
    """
    archive_path = os.path.join(output_dir, dashboard_name + ".tar.gz")
    cmd = "tar czf " + archive_path + " ./exports/" + dashboard_name
    subprocess.call(cmd, shell=True)
    return archive_path


def restore_backup(archive_name):
    """Restore a dashboard backup from the given archive name."""
    os.system("tar xzf ./backups/" + archive_name + " -C ./exports")
