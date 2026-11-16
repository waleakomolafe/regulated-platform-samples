## DR-0003 — OIDC federation over stored cloud secrets

- Status: accepted
- Context: pipelines authenticate to the cloud somehow. The traditional
  answer is a client secret stored as a CI secret: a long-lived
  credential whose entire security model is that nobody ever prints it.
  In a regulated environment that model fails three ways — the secret
  exists (so it can leak), it expires on a schedule nobody owns (so it
  breaks silently), and audit has to take "only the pipeline uses it" on
  trust.
- Decision: the deploy template federates. `permissions: id-token: write`
  plus `azure/login` with client/tenant/subscription IDs from environment
  VARIABLES (public values, not secrets). GitHub mints a short-lived
  token per run; Azure trusts the declared workflow. No cloud credential
  is ever stored, on any side.
- Alternative: a service principal with a stored client secret, rotated
  quarterly. Rejected: rotation is a system with three quiet failure
  modes (rotation job dies, new secret misses one repo, old secret
  lingers), and a leaked rotation window is a full-compromise window.
  Federation has none of these properties; its worst case is a declined
  token.
- Consequence: the GitHub environment must be configured (three vars, one
  federated credential on Azure) before the first deploy — five minutes
  of setup that removes a permanent class of incident. And any future
  pipeline that stores a cloud secret now has a decision record to argue
  against.
