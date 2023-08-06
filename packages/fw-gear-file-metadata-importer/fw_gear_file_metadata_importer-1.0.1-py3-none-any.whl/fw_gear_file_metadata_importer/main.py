import logging
import sys
import typing as t
from pathlib import Path

import flywheel
from fw_meta import MetaData

from .files import dicom, nifti, siemens

AnyPath = t.Union[str, Path]

log = logging.getLogger(__name__)


def project_tag_update(project: flywheel.Project = None) -> None:
    """Helper function to update dicom allow/deny tag list"""
    if project:
        log.info("Updating allow/deny tag list from project.info.context.header.dicom.")
        # Updating allow/deny tag list from project.info.context.header.dicom
        dicom.update_array_tag(
            project.info.get("context", {}).get("header", {}).get("dicom", {})
        )


def run(
    file_type: str,
    file_path: AnyPath,
    project: flywheel.Project = None,
    siemens_csa: bool = False,
) -> t.Tuple[t.Dict, MetaData, t.Dict]:
    """Processes file at file_path.

    Args:
        file_type (str): String defining file type.
        file_path (AnyPath): A Path-like to file input.
        project (flywheel.Project): The flywheel project the file is originating
            (Default: None).
        siemens_csa (bool): If True parse Siemens CSA DICOM header (Default: False).

    Returns:
        dict: Dictionary of file attributes to update.
        dict: Dictionary containing the file meta.
        dict: Dictionary containing the qc metrics.

    """
    project_tag_update(project)
    log.info("Processing %s...", file_path)
    if file_type == "dicom":
        fe, meta, qc = dicom.process(file_path, siemens_csa=siemens_csa)
    elif file_type == "nifti":
        fe, meta, qc = nifti.process(file_path)
    elif file_type == "ptd":
        fe, meta, qc = siemens.process_ptd(file_path, siemens_csa)
    elif file_type is None:
        name = str(file_path)
        log.info(f"Could not find file type, trying to determine type by suffix")
        if name.endswith(".ptd"):
            fe, meta, qc = siemens.process_ptd(file_path, siemens_csa)
        elif (
            name.endswith(".dicom.zip")
            or name.endswith(".dcm.zip")
            or name.endswith(".dicom")
            or name.endswith(".dcm")
        ):
            fw, meta, qc = dicom.process(file_path, siemens_csa=siemens_csa)
        else:
            log.error(f"Could not determine file type from suffix.")
            sys.exit(1)
    else:
        log.error(f"File type {file_type} is not supported currently.")
        sys.exit(1)

    return fe, meta, qc
