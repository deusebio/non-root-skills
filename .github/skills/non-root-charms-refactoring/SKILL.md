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

* Assessment: Assess whether a charm complies with non-root user requirements, and identify relevant issues. Refer to [Assessment section](./ASSESSMENT.md) for more information.
* Mitigation: Provide guidance on how to modify the charm to run as a non-root user. Refer to [Mitigation section](./MITIGATION.md) for more information.
* Verification: Ensure that the changes made to the charm successfully enforce non-root user execution. Refer to [Verification section](./VERIFICATION.md) for more information.
* Contribution: Contribute to the charm repository with the necessary changes to comply with non-root user requirements, including code changes and tests. Refer to [Contribution section](./CONTRIBUTION.md) for more information.


## How to use the skill

To use the skill, you can invoke it with the path to the charm repository as an argument. For example:

```bash
/non-root-charms /path/to/charm/repo
```