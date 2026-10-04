# Technical verification when relevant

Identify the tested version from available commit, diff, file, or artifact information. A commit ID is useful when supplied or accessible; do not demand Git for a small pasted function.

Prefer the original reproducer and the smallest test that distinguishes correct behavior from the reported failure. Check the actual behavior, not just build success, HTTP acceptance, green CI, or a reviewer saying "done." Check whether logs and results correspond to the stated version and environment. Preserve coverage already established; rerun affected checks when relevant content changes.

Read failed, skipped, and missing tests separately. Look for assertions that cannot fail, mocked-away behavior, ignored exit codes, or tests aimed at a different path. Their presence is a lead; demonstrate how they weaken the specific claim before declaring a defect.

When a claimed feature depends on a trigger or schedule, check both "ran and failed" and "never ran." Verify that the expected trigger reaches the entry point and leaves an observable result.

When authorized and safe, a controlled negative test can verify the checker: supply an invalid input or disable a fix in an isolated copy. Do not mutate production or the user's original artifact during a review. Restore any isolated experimental change and disclose it.

An inaccessible check is a named limitation, not a reason to fabricate an overall pass or to refuse every check that remains possible. Tool installation and broad security audits are separate tasks.
