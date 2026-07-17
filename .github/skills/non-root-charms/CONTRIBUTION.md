# Contribution

## Requirements

Make sure that `gh` was installed and configured on your system. Make sure the user is logged in. To verify the correct login use

```
gh auth status
```

If `gh` is not configured, ask the user to configure it by following the instructions in the [official GitHub CLI documentation](https://cli.github.com/manual/installation). YOU DO NOT configure `gh` for the user or ask for API keys.

## Process

After making the necessary changes to comply with non-root user requirements, you can contribute these changes back to the relevant repositories. If everything was already compliant, do not do anything in this phase. If you had to make changes, open PRs as described below. When running in `dry-mode`, do not push changes to the repository and only create the local branches with the changes to be evaluated.

### Charm repository PR

1. Fork the charm repository and add the remote to the local git repository.
2. Create a new branch for your changes. Use a branch called "wip-non-root-compliance". If the branch already exists, add a suffix with a number. For example, if "wip-non-root-compliance" already exists, name the branch "wip-non-root-compliance-2".
3. Commit the changes to the new branch and push it to your forked repository.
4. Open a pull request from your forked repository to the original charm repository. The PR description should summarize the result of the assessment, the mitigation that was taken, and the tests that were added. If a rock image PR was also opened (see below), include a "Related" section in the PR body referencing it (e.g. `canonical/<rock-repo>#<number>`).
5. Keep on checking the PR to make sure that the CI has correctly passed. If it does not pass it after 3 times you make changes, ask for help to troubleshoot the issue to the user, and stop doing things automatically.

### Rock image repository PR (only if image was rebuilt)

If the mitigation phase required rebuilding the rock image, you must also open a PR in the image repository:

1. Fork the rock image repository and add the remote to the local git repository.
2. Create a new branch using the same name as the charm branch ("wip-non-root-compliance", with a numeric suffix if needed).
3. Commit the amended `rockcraft.yaml` and the tests (either using python code or dgoss) to the new branch and push it to your forked repository.
4. Open a pull request from your forked repository to the original rock image repository. The PR description should include:
   - A summary of why the image needed to be rebuilt (which paths required permission fixes)
   - The specific changes made to `rockcraft.yaml` (`run_user` and `user-setup` part)
   - The test results (from `test_non_root_image.py` or the dgoss file, as appropriate for the repository)
   - A "Related" section referencing the charm PR (e.g. `canonical/<charm-repo>#<number>`)
5. Update the charm PR body to add a "Related" section referencing the rock image PR (e.g. `canonical/<rock-repo>#<number>`).
6. Keep on checking the PR to make sure that the CI has correctly passed. If it does not pass it after 3 times you make changes, ask for help to troubleshoot the issue to the user, and stop doing things automatically.

## Output

As output provide the list of branches and PR links that have been opened (when not running in `dry-mode`). If verification produced commits, include the commit list alongside the PR links. The output of this step shall be provided in the following format:

| Repository        | Branch        | PR Link                                              |
|-------------------|---------------|------------------------------------------------------|
| <charm-repo-path> | <branch-name> | <pr-link>. Use `dry-mode` when running in `dry-mode` |
| <rock-repo-path>  | <branch-name> | <pr-link>. Use `dry-mode` when running in `dry-mode` |
