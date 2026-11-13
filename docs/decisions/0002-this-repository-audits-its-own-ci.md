## DR-0002 — This repository audits its own CI

- Status: accepted
- Context: a repository that teaches pipeline hygiene while its own
  workflows carry tag-pinned third-party actions would be describing
  controls it does not run. The supply-chain failure mode for sample
  repositories is silent: upstream action compromised, sample repo auto-runs
  it on the next push.
- Decision: CI audits this repository's workflows with pipeline-sentinel on
  every push, and every third-party action is pinned to a full commit SHA
  with the version in a comment. The auditor runs before any job is
  trusted to have run correctly.
- Alternative: pin by major version tag (`actions/checkout@v4`) and rely
  on GitHub's ecosystem. Rejected: a tag is a movable pointer controlled
  by the upstream repo; the SHA is not. The whole value of the pin is that
  upstream cannot change what we run.
- Consequence: dependency updates are manual — read the diff, move the
  SHA. That is the honest price of a supply chain you can explain.
