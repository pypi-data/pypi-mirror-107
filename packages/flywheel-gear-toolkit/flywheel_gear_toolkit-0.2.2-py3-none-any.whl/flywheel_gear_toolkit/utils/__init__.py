"""Gear toolkit utilities module."""
import json
import logging
import subprocess
import sys
import typing as t

log = logging.getLogger(__name__)


def install_requirements(req_file):
    """Install requirements from a file programatically

    Args:
        req_file (str): Path to requirements file

    Raises:
        SystemExit: If there was an error from pip
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
    except subprocess.CalledProcessError as e:
        log.error(f"Could not install requirements, pip exit code {e.returncode}")
        sys.exit(1)


class BytesEncoder(json.JSONEncoder):
    # Overwrite default handler for bytes objects
    def default(self, obj: t.Any) -> str:
        """Default json encoder when not handled.

        Handle bytes objects and pass everything else to the default JSONEncoder.

        For bytes, convert to hex and return the first 10 characters, or truncate.

        Args:
            obj (Any): Object to be encoded, can be anything, this only handles bytes.

        Returns:
            str: encoded obj.
        """
        if isinstance(obj, bytes):
            return (
                obj.hex()
                if len(obj) < 10
                else f"{obj.hex()[:10]} ... truncated byte value."
            )
        return json.JSONEncoder.default(self, obj)
