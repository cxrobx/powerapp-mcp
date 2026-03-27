"""C8_ checksum computation for .msapp file integrity."""

import base64
import hashlib


def compute_checksum(data: bytes) -> str:
    """Compute a Power Apps C8_ checksum: C8_ + base64(SHA-256(data))."""
    digest = hashlib.sha256(data).digest()
    b64 = base64.b64encode(digest).decode("ascii")
    return f"C8_{b64}"


def compute_file_checksums(files: dict[str, bytes]) -> dict:
    """Compute checksums for all files and a master checksum.

    Args:
        files: dict of {path_in_zip: file_bytes}

    Returns:
        dict with ServerStampedChecksum and ServerPerFileChecksums
    """
    per_file: dict[str, str] = {}
    for path in sorted(files.keys()):
        per_file[path] = compute_checksum(files[path])

    # Master checksum: hash of all per-file checksums concatenated
    all_checksums = "".join(per_file[k] for k in sorted(per_file.keys()))
    master = compute_checksum(all_checksums.encode("utf-8"))

    return {
        "ServerStampedChecksum": master,
        "ServerPerFileChecksums": per_file,
    }
