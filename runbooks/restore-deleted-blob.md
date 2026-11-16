# Restore an accidentally deleted blob (secure-storage accounts)

Applies to: every storage account deployed by
`terraform/modules/secure-storage` (blob versioning + soft delete are
module constants, so this runbook works on all of them).

## Assumptions

- You have Entra access with the Storage Blob Data Contributor role on the
  account. If you do not, stop: shared keys are disabled by the module,
  and there is no key to fall back to — get the role.
- The deletion happened within the retention window (30 days by default,
  see the module's `retention_days`).

## Identify what was deleted

    az storage blob list --account-name <account> --container-name <container> --include-deleted --auth-mode login

Success looks like: the deleted blob appears with `isDeleted: true` and a
`DeletedOn` timestamp matching the incident window.

## Restore

    az storage blob restore --account-name <account> --container-name <container> --name <blob> --auth-mode login

Success looks like: the blob reappears in a normal (non-deleted) listing,
and the application confirms the content is the PRE-DELETION version —
restore returns the last versioned state, not the file as it was one
second before deletion.

## Verify with the application, not with storage

The restore is done when a real consumer reads the object successfully —
a health check, a download, a signed-URL fetch by the owning service.
Storage saying "the blob exists" is not evidence the incident is over.

## Rollback

None needed: restore is additive. If the WRONG version was restored,
restore again to the earlier version snapshot — versioning retains the
history the deletion tried to remove.

## Notes

- Do not disable versioning or soft delete to "make deletions cleaner."
  The recoverability floor is a module constant (30 days) and lowering it
  fails the plan.
- If the deletion is malicious rather than accidental, this runbook is
  step one. Step two is the incident process: preserve the evidence
  before restoring over it.
