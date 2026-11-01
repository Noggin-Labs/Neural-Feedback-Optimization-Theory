import NFOT.Definitions

/-!
# Write-Back Gap

The Write-Back Gap is the difference between two protocol-defined recorded
event timestamps. The theorems below establish algebraic properties only.
They do not validate event semantics, clock synchronisation, physical display
timing, or a biological interpretation.
-/

namespace NFOT

/-- Event-to-feedback interval, measured in seconds. -/
def writeBackGap (t₀ : InitiatingTime) (tₙ : FeedbackTime) : ℝ :=
  tₙ - t₀

/-- Ordered event timestamps imply a non-negative Write-Back Gap. -/
theorem gap_nonnegative
    (t₀ : InitiatingTime) (tₙ : FeedbackTime)
    (h : EventsOrdered t₀ tₙ) :
    0 ≤ writeBackGap t₀ tₙ := by
  unfold EventsOrdered writeBackGap at *
  linarith

/-- Coincident timestamps produce a zero gap. -/
theorem gap_zero (t : ℝ) :
    writeBackGap t t = 0 := by
  simp [writeBackGap]

/-- Shifting both timestamps by the same amount leaves the gap unchanged. -/
theorem gap_shift_invariant (t₀ tₙ shift : ℝ) :
    writeBackGap (t₀ + shift) (tₙ + shift) = writeBackGap t₀ tₙ := by
  simp [writeBackGap]
  ring

/-- With a fixed initiating event, a later feedback endpoint cannot
produce a smaller gap. -/
theorem gap_monotone_feedback
    (t₀ tₙ₁ tₙ₂ : ℝ) (h : tₙ₁ ≤ tₙ₂) :
    writeBackGap t₀ tₙ₁ ≤ writeBackGap t₀ tₙ₂ := by
  unfold writeBackGap
  linarith

/-- A gap across two consecutive intervals is the sum of the component gaps. -/
theorem gap_decomposition (t₀ tₘ tₙ : ℝ) :
    writeBackGap t₀ tₙ = writeBackGap t₀ tₘ + writeBackGap tₘ tₙ := by
  unfold writeBackGap
  ring

end NFOT
