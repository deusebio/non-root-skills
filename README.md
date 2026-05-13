# Non-root AI Skill

Create an AI Skill to automate the enablement of unprivileged charms across the ecosystem. The AI Skill should allow to:
1. Assess the charm: read an existing charm, analyze it to assess whether it satisfies the non-root requirements (both for charm containers and workload containers) and analyzing the requirement for the permissions. Checking for compliance to non-root requirements.
2. Implement mitigation: making required changes to make the charm comply with non-root requirement
3. Verify the changes. The skill should create a dedicated test for testing that the charm is indeed working as non-root.
4. (optional) Open a PR upstream to contribute finding the images used by the charm