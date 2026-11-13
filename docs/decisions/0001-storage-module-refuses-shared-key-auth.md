## DR-0001 — The storage module refuses shared-key authentication

- Status: accepted
- Context: Storage accounts default to shared-key auth — a 512-bit key that
  grants full control, lives for as long as nobody rotates it, and appears
  in connection strings, which appear in code, tickets, and CI logs. In a
  regulated environment the key is simultaneously a credential leak risk
  and an audit finding waiting for its quarter.
- Decision: the module sets `shared_access_key_enabled = false` as a
  constant. Access is Entra identities with RBAC only. The key does not
  exist.
- Alternative: keep shared keys enabled and rotate them on a schedule.
  Rotation requires a rotation system, a break-glass path, and someone to
  notice when it stops running — three dependencies, all of which fail
  quietly. Deleting the key needs none of them.
- Consequence: any tooling that speaks shared-key (some legacy backup
  agents, ancient SDK patterns) must move to Entra auth first. That cost
  is paid once per tool, at adoption, in code review — where it is
  visible — instead of continuously, at audit time, where it is not.
