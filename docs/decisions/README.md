# Decision records

The format every decision record in this folder follows. The value of a
decision record is not the decision — it is the CONSTRAINTS and the
ALTERNATIVE, written down while they are still fresh, so the next engineer
does not re-litigate the choice from zero, and an auditor can see the
decision had a reason.

Format (keep it to five fields, one page):

    ## DR-NNNN — <title>
    - Status: accepted | superseded by DR-MMMM
    - Context: the constraint that forced the decision (facts, not narrative)
    - Decision: what we do
    - Alternative: the strongest option we did NOT take, and why it lost
    - Consequence: what this commits us to going forward

Rules:

1. One decision per record. A record that decides three things decides
   nothing.
2. The Alternative field is mandatory. A record without an alternative is
   a memo, not a decision.
3. Superseding is normal. Status changes to "superseded by DR-MMMM" and
   the file stays — the history IS the evidence.
