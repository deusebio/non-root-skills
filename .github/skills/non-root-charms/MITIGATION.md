# Mitigation

## Requirements

* `lxd` is installed and initialized
* `charmcraft` is installed
* `rockcraft` installed
* `docker` CLI is installed and it is authenticated. Use `docker info | grep Username` to check which username is used. DO NOT try to read credential informations from the disk.
* `gh` is installed and configured on your system.
* (optional) Github MCP client

## Input

Consume the output of the Assessment phase, in the format of 

```
Charm name: <charm-name>
Non-root charm container: <compliant/non-compliant>
Workloads: 
    - container-name: <container-name>
      status: <compliant/non-compliant>
      reason: <reason for non-compliance, if applicable>
```

## Process

Depending on the issues identified during the assessment phase, implement the following mitigations:

1. If the charm container is non-compliant, update the `metadata.yaml` or `charmcraft.yaml` file to include the `charm-user` key set to `non-root`.
2. If the charm's workload containers are not compliant because they do not have `uid` and `gid` set to `584792`, update the `metadata.yaml` or `charmcraft.yaml` file to set these values for each container.
3. If the workload images are not compliant (either because the image does not run as `_daemon_` or the path used by the charm do not have the correct permission), a new image needs to be built with the correct permissions for non-root users. You MUST use `rockcraft` to build the image, even if it is resource intensive. DO NOT use `Dockerfile`. To do this:
    1. Identify the base image used by the charm by checking the `upstream-source` field in the `resources` section of the charm's configuration.
    2. Find the repository in Github containing the source code for the base image name in public repositories. As a first step, try to find a repository in Github that has a `rockcraft.yaml` file that has the key `name` with a value similar to the name of the container key. Try to also strip away general suffixes (like for instance `-image`) or prefixes. If you don't find any repository from this search, ask guidance to the user.  
    3. Once you find the repository, clone the repository in the parent folder of the charm repository being analyzed. For instance, if the repository is at `./my_path/my_repo` the new repository should be clone into `./my_path/new_repo`. Then, Amend the `rockcraft.yaml`in the image repository to make the image compliant. Apply minimal change to the `rockcraft.yaml` to:
        - Set a non-root default user to `_daemon_`, corresponding to `uid=584792` and `gid=584792`. For `rockcraft.yaml` use `run_user: _daemon_` to ensure that the image runs as a non-root user.
        - Set the permissions for the path used by the charm to allow operations from `_daemon_`. When using `rockcraft.yaml`, use a dedicated part of the yaml file to set the permissions for the path used by the charm and the `override-prime` section, for instance:
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
        - Build the new image, using either `rockcraft` for a `rockcraft.yaml` file.
        - Add a test in the repository that runs the image using docker and verifies that the image is running as non-root user and that the permissions for the path used by the charm are set correctly to allow non-root user access. The test should explicitly assert the runtime UID/GID (for example with `id -u` and `id -g`) and path access checks. You can refer to the [`test_non_root_image.py`](./references/test_non_root_image.py) file in the [references folder](./references) for an example of how to implement this test. If the repository is using [dgoss](https://github.com/goss-org/goss/blob/master/extras/dgoss/README.md) to run the image validation, please stick to use the framework. You can refer to [`test_non_root_dgoss.yaml`](./references/test_non_root_dgoss.yaml) in the [references folder](./references) to an example of how to implement this.
        - Publish the image to my personal docker hub and update the charm's `metadata.yaml` or `charmcraft.yaml` file to reference the new image.

## Output 

Provide an output of the mitigations with the list of actions that have been taken based on the assessment, e.g. 

```
<non-compliance>: 
    - <action_1>
    - <action_2>
repos:
    - <charms-repo-path>
    - <image-repo-path>
artifacts:
    - <new-image-published-to-dockerhub> 
```