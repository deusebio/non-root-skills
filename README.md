# Non-root AI Skill

Create an AI Skill to automate the enablement of unprivileged charms across the ecosystem. The AI Skill should allow to:
1. Assess the charm: read an existing charm, analyze it to assess whether it satisfies the non-root requirements (both for charm containers and workload containers) and analyzing the requirement for the permissions. Checking for compliance to non-root requirements.
2. Implement mitigation: making required changes to make the charm comply with non-root requirement
3. Verify the changes. The skill should create a dedicated test for testing that the charm is indeed working as non-root.
4. (optional) Open a PR upstream to contribute finding the images used by the charm


## How to use it

Import the skill in your harness and then just use

```
/non-root-charms <path-to-local-repository>
```

## Testing the skill against regressions

The skill also implements some testing to make sure its functionality are always in par with previous successful runs and non-root implementations. More information about the tests and the reference implementations can be found under the [TESTING.md](.github/skills/non-root-charms/TESTING.md) file.

To run regression tests, start a new session and use the following prompt:

```
First read the skill under .github/skills/non-root-charms. Once you have loaded its content and you understand its functionality, I would like to use the "testing" capabilities described in the TESTING.md file, to make sure that the skill has not regression with the previous reference implementations.
```

## License

The Integration Hub for Apache Spark K8s charm is free software, distributed under the Apache Software License, version 2.0.
See [LICENSE](https://github.com/deusebio/non-root-skills/blob/main/LICENSE) for more information.