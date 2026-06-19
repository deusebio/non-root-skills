# Verification

## Input 

Consume the output from the assessment phase to implement the verification steps. The verification steps can be implemented straight after the assessment phase, but the final verification to make sure the changes/tests align can also be done after the mitigation phase has been completed. Should there be any issue coming from the mitigation step, a feedback look between the Verification and Mitigation phases needs to be established. 

## Process

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

4. Make sure that the changes align with the repository standards and it complies with the linting and static typing rules. Check if the repository defines contributing guidelines and make sure you are running the checks. If there are issues due to changes done in the Mitigation phase, notify this to the agent that has done the Mitigation. If you have done those changes, fix them yourself. 

## Output

Commit changes and provide as output the list of commits. 