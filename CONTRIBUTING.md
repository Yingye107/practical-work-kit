# Contributing

Thanks for helping make these skills useful. Start with a small, real task that the current instructions handle badly. Clearer language, useful examples, focused references, and demonstrated fixes are welcome.

## Propose a change

Open an issue for a bug or idea with the relevant skill, the input, expected behavior, actual behavior, and host/version when relevant. Remove credentials, private conversations, and identifying data. For security issues, use [private reporting](SECURITY.md) instead of a public issue.

Before a large rewrite or a new service, discuss the intended benefit. Small wording and example fixes can go directly to a pull request. No contribution agreement or new account connection is required by this project.

## Make the change

1. Fork the repository and create a branch.
2. Change only the relevant instructions or files. Preserve existing licenses and source acknowledgements; record a new upstream source and its license if you incorporate it.
3. For behavior changes, include a representative input and actual response, plus an input that should not trigger the workflow. Distinguish synthetic examples from host runs or human feedback. Avoid unrelated mandatory forms, invented finding quotas, and automatic external actions.
4. Run the checks below and describe what you checked in the pull request. For a small prose correction, do not invent a new test that merely repeats the edited wording.

```sh
python tools/validate.py
python -m unittest discover -s tests -v
python tools/build_release.py --output dist
```

Python 3.11+ and Git are needed; no third-party Python packages are required. Build outputs are written to the ignored `dist/` folder. The validator uses an explicit public file set; when adding a necessary public resource, update that set and relevant references together. Do not weaken a security check just to make a new file pass.

## Release maintenance

Keep `plugin.json`, installation examples, and `CHANGELOG.md` consistent with the release version. Recheck changed skills with representative tasks, validate the staged files, and publish a tag from the intended commit. Attach the generated ZIP and `SHA256SUMS.txt` to a GitHub release. Verify the published source and assets match the checked bytes.

The source repository includes optional validation tools and CI; the installable ZIP intentionally excludes those executables. Private QA logs, personal skill copies, local paths, credentials, and development snapshots must never enter the repository or release archive.

By submitting a contribution, you agree to license it under the project's Apache-2.0 license, while retaining applicable third-party license requirements. Follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Maintainer availability may vary; no response-time guarantee is offered.
