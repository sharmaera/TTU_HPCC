"""Helpers for requesting DMTCP checkpoints from inside a Python process."""

import logging
import os
import subprocess

DMTCP_ENV_VARS = (
    "DMTCP_COORD_HOST",
    "DMTCP_COORD_PORT",
    "DMTCP_TMPDIR",
    "DMTCP_CHECKPOINT_DIR",
)


def is_running_under_dmtcp():
    """Return True when this process appears to be managed by DMTCP."""
    return any(os.environ.get(var) for var in DMTCP_ENV_VARS)


def request_dmtcp_checkpoint(reason):
    """Request a DMTCP checkpoint."""
    logging.info(f"DMTCP checkpoint requested: {reason}")

    if not is_running_under_dmtcp():
        logging.warning(
            "DMTCP checkpoint requested, but this process does not appear "
            "to be running under dmtcp_launch; skipping."
        )
        return

    try:
        result = subprocess.run(
            ["dmtcp_command", "--checkpoint"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300,
        )

        logging.info("DMTCP checkpoint completed")

        if result.stdout:
            logging.info(result.stdout.strip())

    except FileNotFoundError:
        logging.error(
            "dmtcp_command was not found. "
            "Make sure the DMTCP module is loaded."
        )

    except subprocess.TimeoutExpired:
        logging.error("DMTCP checkpoint command timed out")

    except subprocess.CalledProcessError as e:
        logging.error(
            f"DMTCP checkpoint command failed | "
            f"Return code: {e.returncode} | "
            f"stderr: {e.stderr.strip()}"
        )
