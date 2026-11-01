import Mathlib

/-!
# NFOT formal definitions

This module defines the mathematical event-time objects used by the first
formal-verification milestone. It deliberately does not identify recorded
event timestamps with neural processing time or physical display onset.
-/

namespace NFOT

/-- A protocol-recorded initiating-event timestamp, in seconds. -/
abbrev InitiatingTime := ℝ

/-- A protocol-recorded feedback-endpoint timestamp, in seconds. -/
abbrev FeedbackTime := ℝ

/-- A trial is temporally ordered when its feedback endpoint is not earlier
than its initiating event. This is a protocol validity condition, not a
consequence of the gap definition. -/
def EventsOrdered (t₀ : InitiatingTime) (tₙ : FeedbackTime) : Prop :=
  t₀ ≤ tₙ

end NFOT
