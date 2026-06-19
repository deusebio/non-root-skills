# Assessment

Doing the assessment of the charms and the image. 

## Requirements

1. Docker is installed and it is functional. Pull an example image `hello-world` and check the permission for some path in the image. 

## Process

To assess whether a charm complies with non-root user requirements, you can follow these steps:
1. Identify all the charms included in a given repository
2. For each charm, check the following:
  - Check non-root charm container: Check either `metadata.yaml` or `charmcraft.yaml` to see if it specifies a non-root user in its configuration (`charm-user` key must be set to `non-root`).
  - Check non-root workloads. For each workload container (each entry defined in the `containers` section of either `metadata.yaml` or `charmcraft.yaml`), check that:
    - `uid` and `gid` are set to `584792`.  
    - Identify the container image used by the charm by checking the `upstream-source` field in the `resources` section that has the same key as the `resource` field in the `containers` section.
    - Check in the charm code for any operation (through Pebble) that requires read/write commands
    - Pull the image and verify using docker commands that permissions for the paths required by the charm are set correctly to allow non-root user access (`584792` has read and write permissions). For the assessment DO NOT check the upstream `rockcraft.yaml` file. This will be done in the mitigation phase if needed.
3. Provide a report of the assessment, in the form:
    - Charm name: <charm-name>
    - Non-root charm container: <compliant/non-compliant>
    - Workloads: 
        - <container-name>: <compliant/non-compliant>
        - Reason: <reason for non-compliance, if applicable>
  The reason for non-compliance for containers can be one of the following:
    - non-root user issue: `uid` and `gid` are not set to `584792`.
    - Permission issue: when the charm code includes operations that require read/write commands without proper permissions for non-root users.

## Output

Create a yaml with the following format:

```
Charm name: <charm-name>
Non-root charm container: <compliant/non-compliant>
Workloads: 
    - <container-name>: <compliant/non-compliant>
    - Reason: <reason for non-compliance, if applicable>
```

Also output a Markdown table. See an example of the table below:

| Component | Status | Details |
|-----------|--------|---------|
| **Charm container** | ❌ Non-compliant | `charm-user` was not set in `metadata.yaml` |
| **Workload container (integration-hub)** | ❌ Non-compliant | `uid` and `gid` were not set to `584792` |
| **Upstream image permissions** | ✅ Compliant | The upstream image (`ghcr.io/canonical/spark-integration-hub`) already has correct permissions — `/etc/hub/` and `/etc/hub/conf/` are owned by `_daemon_` (uid=584792, gid=584792) with `rwxr-x---` permissions |
| **Pebble operations** | ✅ Compliant | All read/write/exec operations in the charm code operate on paths already owned by `_daemon_` |
