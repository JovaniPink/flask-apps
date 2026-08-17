# Application maintenance model

- **Status:** Current repository contract
- **Last verified:** 2026-08-17

Flask Apps is a collection, not one deployable service. Every directory must be
classified before its code, dependency graph, or documentation is described as
supported.

## Classifications

| State | Meaning | Required evidence |
| --- | --- | --- |
| Maintained | Included in the root support matrix and current CI | Exact lock, install/check/audit, exercised tests, and required container/Compose gates |
| Experimental | Owned code with a bounded learning purpose but no complete support contract | Clear status and limitations; never included in release-wide claims |
| Historical | Preserved example outside the current CI and dependency-maintenance boundary | Status and successor or reactivation requirements |
| Vendored runtime asset | Third-party source or compiled asset retained for runtime/attribution | Upstream license and provenance; no dormant package-manager graph |

The current maintained list lives in the root [`README.md`](../README.md). This
document defines the classification rules rather than duplicating that list.

## Promotion to maintained

An experimental or historical application becomes maintained only when one
focused change provides:

1. a supported Python/runtime boundary;
2. reviewed direct pins and a complete reproducible installation lock;
3. dependency conflict and vulnerability checks;
4. tests that exercise its real application boundary;
5. container or Compose build, health, and non-root checks when applicable;
6. an application README with exact run and validation commands; and
7. a CI lane that runs those gates on the default branch.

A successful import, a passing unit test borrowed from another sample, or a
README alone is insufficient.

## Retirement or demotion

Demote a maintained application when its runtime is unsupported, lock cannot be
reproduced, security findings cannot be bounded, or its exercised CI contract is
removed. Preserve useful history, state the limitation, and identify the
replacement or the evidence needed for reactivation.

Vendored build manifests and obsolete toolchains should not be restored merely
to rebuild assets already retained and attributed. Reintroducing a toolchain is
a new supply-chain decision requiring its own review and validation.
