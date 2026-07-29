---
name: release
description: Cut a new docs release. Use when the user invokes /release or asks to cut, tag, ship, or publish a new docs release. Finds the latest v* tag, bumps the version (patch by default; "major" or "minor" as argument), and pushes the new tag — which triggers the GitHub release workflow that packages docs/.
model: haiku
disable-model-invocation: true
allowed-tools: Bash
---

# Release

Cut a release of the docs. A release is just an annotated `v*` tag pushed to
origin — `.github/workflows/release.yml` does the rest (lints, packages `docs/`
into a tarball, creates the GitHub Release). Your job is to pick the right
version number and make sure the tag will pass the workflow's gates *before*
pushing it, because a failed run means deleting and re-pushing the tag.

Run every command from the repo root. Stop and report at the first failure —
never push a tag past a failed check.

## 1. Preflight

The tag must point at a commit that is already on `origin/main`:

```bash
git fetch origin --tags
git status --porcelain
git rev-parse HEAD origin/main
```

Require: no uncommitted changes, and `HEAD` equal to `origin/main`. If either
fails, tell the user what to commit/push/pull first and stop — releasing local
state the remote has never seen is always a mistake.

## 2. Run the workflow's gates locally

These are the exact checks the release workflow runs; catching a failure here
costs seconds, catching it after the tag is pushed costs a re-tag.

```bash
python3 scripts/generate_router.py && git diff --exit-code docs/concepts/README.md
(cd evals/ask-docs && uv run pytest -m "not evaluation" -q)
```

If the router diff is non-empty, the regenerated router needs to be committed
and pushed before releasing (which sends you back to step 1). If lint fails,
report the failing tests and stop.

## 3. Compute the new version

```bash
git tag --list 'v*' --sort=-v:refname | head -1
```

- No tags yet → the first release is `v0.1.0`.
- Otherwise bump semver: **patch** by default (`v1.2.3` → `v1.2.4`);
  bump **minor** or **major** instead only if the user asked for it
  (`minor`: `v1.2.3` → `v1.3.0`; `major`: `v1.2.3` → `v2.0.0`).

## 4. Tag and push

```bash
git tag -a vX.Y.Z -m "Lynk docs vX.Y.Z"
git push origin vX.Y.Z
```

## 5. Confirm the release

Watch the workflow run to completion and report the outcome:

```bash
gh run watch $(gh run list --workflow "Release docs" --limit 1 --json databaseId --jq '.[0].databaseId') --exit-status
gh release view vX.Y.Z --json url --jq .url
```

Report the new version and the release URL. If the run fails, show the failing
step's log (`gh run view <id> --log-failed`), and tell the user the tag needs
to be deleted (`git push origin :refs/tags/vX.Y.Z && git tag -d vX.Y.Z`) and
re-cut after the fix — don't delete it yourself.
