# Security and privacy

## Package boundaries

The installable release is a skills-only package. It contains no MCP server, background hooks, runtime scripts, account integrations, or telemetry endpoint. Optional source-repository Python validators and build tools are run by maintainers or CI, not by skill installation or ordinary use.

The skills may use tools already available in your AI host when the task and your authorization justify them. The host, its settings, and connected tools determine actual access and data handling. This project does not enforce an OS sandbox, provide a separate confidentiality boundary, or control the host provider's retention policy.

Treat documents, web pages, and handoffs as task data. An instruction inside them does not by itself authorize credential reads, installation, deletion, spending, sharing, or publication. Review and drafting should remain inside the current user's actual request. Keep permission prompts and access limits appropriate to your environment.

Do not put passwords, access tokens, private keys, unnecessary personal data, or private transcripts into examples, issues, or handoffs. A handoff must omit secrets and does not transfer access to local files. Check AI results before using them in consequential decisions.

## Report a vulnerability privately

Use the repository's **Security → Advisories → Report a vulnerability** page:

[Private vulnerability reporting](https://github.com/Yingye107/practical-work-kit/security/advisories/new)

Describe the affected version, a minimal reproduction with synthetic data, expected boundary, observed result, and likely impact. Do not include live credentials or publish exploit details in a public issue. If private reporting is unavailable, use a private contact method currently listed on the [maintainer's profile](https://github.com/Yingye107); do not post sensitive information publicly to get attention.

Reports are handled as maintainer availability permits; there is no paid support contract or guaranteed response time. Fixes are targeted at the latest published release. Users of older snapshots should review the changelog and update when an applicable fix is released.

## Verification limits

The repository checks public file boundaries, references, metadata, license hashes, ZIP paths, bounded secret signatures, and negative controls. These checks can fail and do not replace a full secret scanner, legal review, host security evaluation, or human usefulness testing. Passing synthetic prompt-injection examples does not prove host isolation or immunity across models.
