# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

import pytest
import subprocess

from charmed_kubeflow_chisme.rock import CheckRock


@pytest.mark.abort_on_fail
def test_rock():
    """Test rock."""
    check_rock = CheckRock("rockcraft.yaml")
    rock_image = check_rock.get_name()
    rock_version = check_rock.get_version()
    LOCAL_ROCK_IMAGE = f"{rock_image}:{rock_version}"

    # Assert container runtime user/group matches the shared non-root identity.
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            LOCAL_ROCK_IMAGE,
            "sh",
            "-c",
            'test "$(id -u)" = "584792"',
        ],
        check=True,
    )

    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            LOCAL_ROCK_IMAGE,
            "sh",
            "-c",
            'test "$(id -g)" = "584792"',
        ],
        check=True,
    )

    # Assert the rock grants read access to expected files.
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            LOCAL_ROCK_IMAGE,
            "sh",
            "-c",
            'test -r "/kfp/metadata_writer/metadata_writer.py"',
        ],
        check=True,
    )

    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            LOCAL_ROCK_IMAGE,
            "sh",
            "-c",
            'test -r "/kfp/metadata_writer/metadata_helpers.py"',
        ],
        check=True,
    )