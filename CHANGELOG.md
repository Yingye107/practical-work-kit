# Changelog

## 0.2.1 — 2026-10-05

- Make the public README, installation guide, quick start, worked examples, and plugin interface copy English-only.
- Translate all four skill labels, descriptions, and starter prompts; keep the shared skill instructions and behavior unchanged.
- Remove the Chinese README from the current source and release ZIP. Earlier releases and Git history remain available.

## 0.2.0 — 2026-10-05

- Add Claude plugin and marketplace manifests while keeping one shared set of four skills for Codex and Claude.
- Document Claude Code installation and skill commands, plus Claude chat/Cowork marketplace and ZIP entry points.
- Release one ZIP for both hosts; keep prior releases available.
- Validate Claude metadata, version parity, local source boundaries, and absence of runtime components with additional negative controls.

## 0.1.3 — Unreleased

- For features that depend on a trigger or schedule, check whether execution started as well as whether it failed, using an observable result from the actual entry point.
- Keep this check conditional on the feature being reviewed. No background service, new account connection, or required form is added.

## 0.1.2 — Unreleased

- Add a public privacy notice and its listing URL to resolve the OpenAI draft's privacy-policy check.
- Prepare a skills-only package for the OpenAI public plugin directory, with a square static icon and publisher website/support links.
- Use ordinary starter prompts in the listing; users can start without knowing skill command names.
- Validate required icon references and their reviewed bytes. Keep the four skills and upstream license files unchanged.
- Add a project banner and a one-minute budget example to both READMEs.
- Keep the reviewed PNG and editable SVG with the package; validation requires the PNG's reviewed fingerprint.

Version 0.1.1 was used for an initial draft. Version 0.1.2 addressed its privacy-policy finding and was submitted for review on 2026-10-03. Submission does not imply public-directory approval; current platform status must be checked separately.

## 0.1.0 — 2026-10-02

First public GitHub release.

- Four skills: check work, challenge plans, shape ideas, and carry context.
- Portable plugin manifest, one marketplace entry, and skill interface metadata.
- English and Traditional Chinese introductions, installation instructions, and worked examples.
- Publisher identity, source provenance, upstream license files, contribution guide, and security policy.
- Offline validation, meaningful negative controls, pinned read-only CI, and a deterministic skills-only ZIP builder.

The four skill instruction files retain the reviewed initial behavior. This release adds public documentation and publishing metadata. It is not a claim of OpenAI public-directory approval, independent expert consensus, or measured benefit for most users.
