---
name: non-root-charms
description: Assess whether a charm complies with non-root user requirements, and if not, mitigate by changing the code to run as a non-root user.
argument-hint: path-to-charm-repo
user-invocable: true
---

# Non-root Charms

## Requirements

To use this skill, you need to have the following:
- A charm repository that you want to assess and modify to comply with non-root user requirements.
- Docker installed on your system to build and test the image. Check that docker is installed, otherwise install docker by following the instructions in the [official Docker documentation](https://docs.docker.com/get-docker/) for Ubuntu. 

## Overview

The skill allows performing three main tasks:

* Assessment: Assess whether a charm complies with non-root user requirements, and identify relevant issues.
* Mitigation: Provide guidance on how to modify the charm to run as a non-root user.
* Verification: Ensure that the changes made to the charm successfully enforce non-root user execution.
* Contribution: Contribute to the charm repository with the necessary changes to comply with non-root user requirements, including code changes and tests.

## Assessment

To assess whether a charm complies with non-root user requirements, you can follow these steps:
1. Identify all the charms included in a given repository
2. For each charm, check the following:
  - Check non-root charm container: Check either `metadata.yaml` or `charmcraft.yaml` to see if it specifies a non-root user in its configuration (`charm-user` key must be set to `non-root`).
  - Check non-root workloads. For each workload container (each entry defined in the `containers` section of either `metadata.yaml` or `charmcraft.yaml`), check that:
    - `uid` and `gid` are set to `584792`.  
    - Identify the container image used by the charm by checking the `upstream-source` field in the `resources` section that has the same key as the `resource` field in the `containers` section.
    - Check in the charm code for any operation (through Pebble) that requires read/write commands
    - Pull the image from the network and verify that permissions in the docker image on the path required to be used by the charm are set correctly to allow non-root user access (`584792` has read and write permissions).
3. Provide a report of the assessment, in the form:
    - Charm name: <charm-name>
    - Non-root charm container: <compliant/non-compliant>
    - Workloads: 
        - <container-name>: <compliant/non-compliant>
        - Reason: <reason for non-compliance, if applicable>
  The reason for non-compliance for containers can be one of the following:
    - non-root user issue: `uid` and `gid` are not set to `584792`.
    - Permission issue: when the charm code includes operations that require read/write commands without proper permissions for non-root users.

## Mitigation

Depending on the issues identified during the assessment phase, the following mitigation can be taken:

1. If the charm does not specify a non-root user in its configuration, update the `metadata.yaml` or `charmcraft.yaml` file to include the `charm-user` key set to `non-root`.
2. If the charm's workload containers do not have `uid` and `gid` set to `584792`, update the `metadata.yaml` or `charmcraft.yaml` file to set these values for each container.
3. If there are permission issues identified in the charm code, a new image needs to be built with the correct permissions for non-root users. You MUST use `rockcraft` to build the image, although it is resource intensive. DO NOT use `Dockerfile`. To do this:
    - Identify the base image used by the charm by checking the `upstream-source` field in the `resources` section of the charm's configuration.
    - Find the repository in Github containing the source code for the base image name in public repositories. As a first step, try to find a repository that has a `rockcraft.yaml` file that has the key "name" with a value similar to the name of the container key. Try to also strip away general suffixes (like for instance `-image`) or prefixes. If you don't find any repository with a `rockcraft.yaml` file, you can try to find any repository that has a `Dockerfile` and uses the same base image as the one used by the charm. Before proceeding further, make sure that the repository you have found is trustworthy and reliable and ask confirmation to the user.
    - Once you find the repository, assess whether it is using `rockcraft` or `docker` to build the image:
        - If it is using `docker`, translate the `Dockerfile` into a `rockcraft.yaml` file that is stored in the repository of the charms under a folder named `image`. Use `rockcraft pack` to make sure you can build the image. Use the `rockcraft.yaml` file as reference for subsequent steps.
        - If it is using `rockcraft`, use the `rockcraft.yaml` in the image repository that has just been found in the previous step as reference for subsequent steps.
    - Check the `rockcraft.yaml` to make sure that:
        - `run_user: _daemon_` is set to ensure that the image runs as a non-root user.
        - The permissions for the path used by the charm are set correctly to allow non-root user. Please use a dedicated part of the yaml file to set the permissions for the path used by the charm and the `override-prime` section, for instance:
        ```yaml
        parts:
            user-setup:
                plugin: nil
                override-prime: |
                # Please refer to https://discourse.ubuntu.com/t/unifying-user-identity-across-snaps-and-rocks/36469
                # for more information about shared user.
                HUB_GID=584792
                HUB_UID=584792

                craftctl default

                chown -R ${HUB_GID}:${HUB_UID} opt/
                chmod -R 750 opt/

                chown -R ${HUB_GID}:${HUB_UID} etc/
                chmod -R 750 etc/...
        ```
        You can find a full example of a `rockcraft.yaml` file with the correct configuration for non-root user in the [references](./references/non-root-rock.yaml).
    - Add a test in the repository that runs the image using docker and verifies that the image is running as non-root user and that the permissions for the path used by the charm are set correctly to allow non-root user access. You can refer to the `test_non_root_image.py` file in the [references](./references/test_non_root_image.py) for an example of how to implement this test.


    - Build the new image and update the charm's `metadata.yaml` or `charmcraft.yaml` file to reference the new image.


## Verification

First check if the charm has an existing integration test that verifies that the charm deploys and goes into active/idle state, using either `juju.wait(jubilant.all_active, ...)`  or `await ops_test.model.wait_for_idle(status="active",...)`. If such a test exists, you can add the security context verification to that test. If not, you can create a new integration test that deploys the charm and verifies the security context.

To add the test

1. Add boiler plate functions. First provide the boilerplate for the integration test. If there is an `helpers.py` file in the integration test directory, you can add the functions defined in `asserts/non-root-check.py` in the helpers module. If not, you can create a new helper module for the security context verification.

2. Once the support functions are in place, you can add the test function that checks the security context of the containers. At the top of the integration test file, add the following imports and build the `CONTAINERS_SECURITY_CONTEXT_MAP` from `metadata.yaml`. This map is generated automatically from the `uid`/`gid` values in the `containers` section, plus a `charm` entry for the Juju agent container (UID/GID 170). Then 

```python
from <helper> import assert_security_context, generate_container_securitycontext_map, get_pod_names

METADATA = yaml.safe_load(Path("./metadata.yaml").read_text())
CONTAINERS_SECURITY_CONTEXT_MAP = generate_container_securitycontext_map(METADATA)
```

3. Add the test after the charm is deployed and active. The test **must be placed after** a test (or fixture) that deploys the charm and waits for it to be active — for example, right after `test_build_and_deploy_hub_charm` which ends with `juju.wait(jubilant.all_active, ...)`. Do **not** create a separate test file unless there is no test deploying the charm. 

```python
@pytest.mark.parametrize("container_name", list(CONTAINERS_SECURITY_CONTEXT_MAP.keys()))
def test_container_security_context(
    juju: jubilant.Juju,
    charm_name: str,
    container_name: str,
) -> None:
    """Test container security context is correctly set.

    Verify that container spec defines the security context with correct
    user ID and group ID.
    """
    lightkube_client = lightkube.Client()
    pod_name = get_pod_names(juju.model, charm_name)[0]
    assert_security_context(
        lightkube_client,
        pod_name,
        container_name,
        CONTAINERS_SECURITY_CONTEXT_MAP,
        juju.model,
    )
```

This test will check that the container's security context is correctly set to run as a non-root user, ensuring that the charm complies with non-root user requirements.

## Contribution

### Requirements

Make sure that `gh` was installed and configured on your system. If not, ask the user to configure it by following the instructions in the [official GitHub CLI documentation](https://cli.github.com/manual/installation). YOU DO NOT configure `gh` for the user or ask for API keys.

After making the necessary changes to the charm to comply with non-root user requirements, you can contribute these changes back to the charm repository. If the charm was already compliant, do not do anything in this phase. If you had to make changes, open a PR with these changes.
1. First, fork the charm repository and add the remote to the local git repository.
2. Create a new branch for your changes. Use a branch called "wip-non-root-compliance". If the branch already exists, add a suffix with a number. For example, if "wip-non-root-compliance" already exists, name the branch "wip-non-root-compliance-2".
3. Commit the changes to the new branch and push it to your forked repository.
4. Open a pull request from your forked repository to the original charm repository. The PR description should summarize the result of the assessment, the mitigation that was taken, and the tests that were added. 
5. Keep on checking the PR to make sure that the CI has correctly passed. If it does not pass it after 3 times you make changes, ask for help to troubleshoot the issue to the user, and stop do things automatically.  