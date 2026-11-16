# Runbook template

A runbook is opened under pressure, by someone who was not there when the
decision was made. This skeleton assumes that reader. Fill every bracket;
delete nothing; if a step cannot name its EXPECTED EVIDENCE, the step is
not done — write what you would see, or take the step out.

Structure rules (the doctor in CI enforces what it can):

1. Every command is a real path in this repository — `runbook-doctor`
   fails the build when a step names a script that no longer exists.
2. Every step says what success LOOKS LIKE (a log line, an output, a
   state). "Run it" is not a step; "run it and expect X" is.
3. The rollback section is written with the same care as the forward
   path, or the runbook admits there is no rollback — in writing.
4. Variables used in commands are defined in the Variables section —
   the doctor flags a `$VAR` that appears exactly once and nowhere else.

Copy this file per runbook; do not link to it from fifty runbooks, because
a template nobody edits rots into a claim.
