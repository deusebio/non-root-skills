# TESTING

The following guidance is to provide reference implementations of non-root charms to be used to evaluate the performance and quality of the current skills. The "Reference table" below provides the detail about the reference implementations to be compared changes with.

## How to test

When evaluating the performance, first checkout the charm repository at the pinned commit linked in the `Reference Charm Repository` column, then run the AI skill in `dry-mode` with minimal input using

```bash
/non-root-charms <charm-repository> in dry-mode
```

The AI skill should make code changes autonomously and report back only once it has finished, providing as output the local branches with the changes for each repository (charm and rock).

Evaluate that the changes implemented are consistent with the reference implementation provided by the PR and provide a summary when they are not, splitting misalignment into major differences and minor/nitpick changes (e.g. variable naming) that do not affect functionalities.

### Evaluation rubric

| Severity | Examples |
| -------- | -------- |
| **Major** | Wrong UID/GID value; missing `run_user` in `rockcraft.yaml`; security-context test not added; non-root permissions not set on required paths |
| **Minor** | Variable naming differences; comment wording; cosmetic ordering of YAML keys |

## Reference table

For charm rows, the `Reference Charm Repository` links to the pinned starting commit to check out before running the skill. The `Repository` columns represent the base-reference of the reference PR that is linked in the "PR Link" column that can be used to compare the skill's output against.

| Test Case | Reference Charm Repository | Artifact   | Repository | PR Link |
| --------- | -------------------------- | ---------- | ---------- | ------- |
| spark-integration-hub | [canonical/spark-integration-hub-k8s-operator](https://github.com/canonical/spark-integration-hub-k8s-operator/tree/2d8cf5316ab1ace1847895776d8687591b63f7cf) | charm  | [canonical/spark-integration-hub-k8s-operator](https://github.com/canonical/spark-integration-hub-k8s-operator) | https://github.com/canonical/spark-integration-hub-k8s-operator/pull/212 |
| alertmanager | [canonical/alertmanager-k8s-operator](https://github.com/canonical/alertmanager-k8s-operator/tree/9bc06c3d0eefc9e182825e2ec019ef5bce84cf84) | charm  | [canonical/alertmanager-k8s-operator](https://github.com/canonical/alertmanager-k8s-operator) | https://github.com/canonical/alertmanager-k8s-operator/pull/434 |
| alertmanager | [canonical/alertmanager-k8s-operator](https://github.com/canonical/alertmanager-k8s-operator/tree/9bc06c3d0eefc9e182825e2ec019ef5bce84cf84) | rock  | [canonical/alertmanager-rock](https://github.com/canonical/alertmanager-rock/tree/8f6dc795246ab8c623e290706fcf62f55fcf8dfc) | https://github.com/canonical/alertmanager-rock/pull/64 |

## Run testing

When asked to run the full scale testing, apply the testing framework to each "Test case" applied to the "Reference Charm Repository" listed in the "Reference table" above, and evaluate the changes with respect to the provided reference implementations, providing a summary for each "Test case" as summarized in "Evaluation rubric".