# Contribution

## Requirements

Make sure that `gh` was installed and configured on your system. Make sure the user is logged in. To verify the correct login use

```
gh auth status
```

If `gh` is not configure, ask the user to configure it by following the instructions in the [official GitHub CLI documentation](https://cli.github.com/manual/installation). YOU DO NOT configure `gh` for the user or ask for API keys.

## Process

After making the necessary changes to the charm to comply with non-root user requirements, you can contribute these changes back to the charm repository. If the charm was already compliant, do not do anything in this phase. If you had to make changes, open a PR with these changes.
1. First, fork the charm repository and add the remote to the local git repository.
2. Create a new branch for your changes. Use a branch called "wip-non-root-compliance". If the branch already exists, add a suffix with a number. For example, if "wip-non-root-compliance" already exists, name the branch "wip-non-root-compliance-2".
3. Commit the changes to the new branch and push it to your forked repository.
4. Open a pull request from your forked repository to the original charm repository. The PR description should summarize the result of the assessment, the mitigation that was taken, and the tests that were added. 
5. Keep on checking the PR to make sure that the CI has correctly passed. If it does not pass it after 3 times you make changes, ask for help to troubleshoot the issue to the user, and stop do things automatically.  

## Output

As the output provide the PR link that has been opened. 