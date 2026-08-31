# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Utilities for exporting dashboard backups to a local archive."""

from __future__ import annotations

import re
import tarfile
from pathlib import Path

EXPORTS_DIR = Path("exports")
BACKUPS_DIR = Path("backups")

SAFE_NAME_RE = re.compile(r"\A[A-Za-z0-9_][A-Za-z0-9._-]{0,254}\Z")


def _safe_name(name: str) -> str:
    """Return ``name`` if it is a single, non-traversing path component."""
    if not SAFE_NAME_RE.match(name) or name == "..":
        raise ValueError(f"Invalid name: {name!r}")
    return name


def _resolved_child(parent: Path, name: str) -> Path:
    """Resolve ``name`` under ``parent``, rejecting anything that escapes it."""
    parent = parent.resolve()
    child = (parent / _safe_name(name)).resolve()
    if child.parent != parent:
        raise ValueError(f"Path {name!r} escapes {parent}")
    return child


def create_backup_archive(dashboard_name: str, output_dir: str | Path) -> Path:
    """Create a tar.gz archive of a dashboard's exported files."""
    dashboard_name = _safe_name(dashboard_name)
    output_path = Path(output_dir).resolve()
    if not output_path.is_dir():
        raise ValueError(f"Not a directory: {output_path}")

    archive_path = _resolved_child(output_path, f"{dashboard_name}.tar.gz")
    source_dir = _resolved_child(EXPORTS_DIR, dashboard_name)
    if not source_dir.is_dir():
        raise ValueError(f"No such export: {source_dir}")

    with tarfile.open(archive_path, "w:gz") as archive:
        archive.add(source_dir, arcname=dashboard_name)
    return archive_path


def restore_backup(archive_name: str) -> None:
    """Restore a dashboard backup from the given archive name."""
    archive_path = _resolved_child(BACKUPS_DIR, archive_name)
    if not archive_path.is_file():
        raise ValueError(f"No such archive: {archive_path}")

    destination = EXPORTS_DIR.resolve()
    with tarfile.open(archive_path, "r:gz") as archive:
        members = archive.getmembers()
        for member in members:
            if member.issym() or member.islnk() or member.isdev():
                raise ValueError(f"Unsupported archive entry: {member.name}")
            target = (destination / member.name).resolve()
            if target != destination and destination not in target.parents:
                raise ValueError(f"Archive entry escapes {destination}: {member.name}")
        archive.extractall(destination, members=members)  # noqa: S202
