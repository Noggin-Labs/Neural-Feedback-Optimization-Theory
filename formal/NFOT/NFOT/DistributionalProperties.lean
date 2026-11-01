import NFOT.WriteBackGap

/-!
# Finite-sample distributional examples

This module gives a deliberately small, exact example: two equally weighted
three-observation samples can have the same arithmetic mean and different
population variances. This proves mathematical possibility, not an NFOT
performance effect, a biological claim, or a result about the repository's
444-row derived table.
-/

namespace NFOT

/-- Arithmetic mean of an equally weighted three-value sample. -/
def mean3 (x : ℝ × ℝ × ℝ) : ℝ :=
  (x.1 + x.2.1 + x.2.2) / 3

/-- Population variance of an equally weighted three-value sample. -/
def variance3 (x : ℝ × ℝ × ℝ) : ℝ :=
  ((x.1 - mean3 x) ^ 2
    + (x.2.1 - mean3 x) ^ 2
    + (x.2.2 - mean3 x) ^ 2) / 3

/-- Equally weighted sample with values 0, 1, and 2. -/
def lowVarianceSample : ℝ × ℝ × ℝ := (0, 1, 2)

/-- Equally weighted sample with values 0, 0, and 3. -/
def highVarianceSample : ℝ × ℝ × ℝ := (0, 0, 3)

theorem example_samples_have_equal_means :
    mean3 lowVarianceSample = mean3 highVarianceSample := by
  norm_num [mean3, lowVarianceSample, highVarianceSample]

theorem low_variance_sample_variance :
    variance3 lowVarianceSample = (2 : ℝ) / 3 := by
  norm_num [variance3, mean3, lowVarianceSample]

theorem high_variance_sample_variance :
    variance3 highVarianceSample = 2 := by
  norm_num [variance3, mean3, highVarianceSample]

theorem example_samples_have_different_variances :
    variance3 lowVarianceSample ≠ variance3 highVarianceSample := by
  rw [low_variance_sample_variance, high_variance_sample_variance]
  norm_num

end NFOT
