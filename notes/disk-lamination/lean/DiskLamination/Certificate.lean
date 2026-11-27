import Init.Grind.Ordered.Ring

set_option linter.unusedSectionVars false

namespace DiskLamination

open Lean.Grind

variable {R : Type} [CommRing R] [LE R] [LT R] [Std.LawfulOrderLT R]
  [Std.IsLinearOrder R] [OrderedRing R]

/-- Gaussian-integer-style pairs representing complex numbers over an ordered
commutative ring.  No division or argument function is needed in the certificate. -/
structure C (R : Type) where
  re : R
  im : R

namespace C

def zero : C R := ⟨0, 0⟩
def ofReal (r : R) : C R := ⟨r, 0⟩
def add (u v : C R) : C R := ⟨u.re + v.re, u.im + v.im⟩
def neg (u : C R) : C R := ⟨-u.re, -u.im⟩
def mul (u v : C R) : C R :=
  ⟨u.re * v.re - u.im * v.im, u.re * v.im + u.im * v.re⟩
def conj (u : C R) : C R := ⟨u.re, -u.im⟩
def n2 (u : C R) : R := u.re ^ 2 + u.im ^ 2

/-- `F A B = Im(B * conj A)`. -/
def F (A B : C R) : R := (mul B (conj A)).im

/-- `G z A B = Im(z * A * conj B)`. -/
def G (z A B : C R) : R := (mul (mul z A) (conj B)).im

theorem red_F (z A B : C R) : F (add A B) B = F A B := by
  cases A; cases B; cases z
  simp [F, add, mul, conj]
  grind

theorem red_G (z A B : C R) :
    G z (add A B) B = G z A B + z.im * n2 B := by
  cases A; cases B; cases z
  simp [G, n2, add, mul, conj]
  grind

theorem blue_F (z A B : C R) :
    F A (add B (mul z A)) = F A B + z.im * n2 A := by
  cases A; cases B; cases z
  simp [F, n2, add, mul, conj]
  grind

theorem blue_G (z A B : C R) :
    G z A (add B (mul z A)) = G z A B := by
  cases A; cases B; cases z
  simp [G, add, mul, conj]
  grind

theorem ordinary_F (z A B : C R) : F A (add A B) = F A B := by
  cases A; cases B; cases z
  simp [F, add, mul, conj]
  grind

theorem ordinary_G (z A B : C R) :
    G z A (add A B) = G z A B + z.im * n2 A := by
  cases A; cases B; cases z
  simp [G, n2, add, mul, conj]
  grind

theorem rotated_F (z A B : C R) :
    F B (add B (mul z A)) = G z A B := by
  cases A; cases B; cases z
  simp [F, G, add, mul, conj]
  grind

theorem rotated_G (z A B : C R) :
    G z B (add B (mul z A)) = n2 z * F A B + z.im * n2 B := by
  cases A; cases B; cases z
  simp [F, G, n2, add, mul, conj]
  grind

theorem red_cancellation_substitution (z A : C R) :
    G z A (neg A) = -z.im * n2 A := by
  cases A; cases z
  simp [G, n2, neg, mul, conj]
  grind

theorem blue_cancellation_substitution (z A : C R) :
    F A (neg (mul z A)) = -z.im * n2 A := by
  cases A; cases z
  simp [F, n2, neg, mul, conj]
  grind

theorem eq_neg_of_add_eq_zero {A B : C R} (h : add A B = zero) :
    B = neg A := by
  cases A; cases B
  simp [add, zero, neg] at h ⊢
  grind

theorem first_eq_neg_of_add_eq_zero {A B : C R} (h : add A B = zero) :
    A = neg B := by
  cases A; cases B
  simp [add, zero, neg] at h ⊢
  grind

theorem nonzero_component {A : C R} (h : A ≠ zero) :
    A.re ≠ 0 ∨ A.im ≠ 0 := by
  cases A with
  | mk ar ai =>
    by_cases har : ar = 0
    · right
      intro hai
      change ai = 0 at hai
      apply h
      simp [zero, har, hai]
    · left
      exact har

theorem sqsum_nonneg (a b : R) : 0 ≤ a ^ 2 + b ^ 2 := by
  have ha : 0 ≤ a ^ 2 := OrderedRing.sq_nonneg
  have hb : 0 ≤ b ^ 2 := OrderedRing.sq_nonneg
  have h := OrderedAdd.add_le_add ha hb
  simpa [Semiring.add_zero] using h

theorem sqsum_pos {a b : R} (h : a ≠ 0 ∨ b ≠ 0) : 0 < a ^ 2 + b ^ 2 := by
  cases h with
  | inl ha =>
      have hsqa : 0 < a ^ 2 := OrderedRing.sq_pos ha
      have hsqb : 0 ≤ b ^ 2 := OrderedRing.sq_nonneg
      have hle0 := OrderedAdd.add_le_right (a ^ 2) hsqb
      have hle : a ^ 2 ≤ a ^ 2 + b ^ 2 := by
        simpa [Semiring.add_zero] using hle0
      exact Std.lt_of_lt_of_le hsqa hle
  | inr hb =>
      have hsqa : 0 ≤ a ^ 2 := OrderedRing.sq_nonneg
      have hsqb : 0 < b ^ 2 := OrderedRing.sq_pos hb
      have hle0 := OrderedAdd.add_le_right (b ^ 2) hsqa
      have hle : b ^ 2 ≤ b ^ 2 + a ^ 2 := by
        simpa [Semiring.add_zero] using hle0
      have hlt : 0 < b ^ 2 + a ^ 2 := Std.lt_of_lt_of_le hsqb hle
      have heq : b ^ 2 + a ^ 2 = a ^ 2 + b ^ 2 := by grind
      rwa [heq] at hlt

theorem n2_nonneg (A : C R) : 0 ≤ n2 A := sqsum_nonneg A.re A.im

theorem n2_pos {A : C R} (h : A ≠ zero) : 0 < n2 A :=
  sqsum_pos (nonzero_component h)

theorem pos_mul_n2 {y : R} {A : C R} (hy : 0 < y) (hA : A ≠ zero) :
    0 < y * n2 A :=
  OrderedRing.mul_pos hy (n2_pos hA)

theorem add_nonneg {x y : R} (hx : 0 ≤ x) (hy : 0 ≤ y) : 0 ≤ x + y := by
  have h := OrderedAdd.add_le_add hx hy
  simpa [Semiring.add_zero] using h

theorem add_pos_of_nonneg_pos {x y : R} (hx : 0 ≤ x) (hy : 0 < y) :
    0 < x + y := by
  have hle0 := OrderedAdd.add_le_left hx y
  have hle : y ≤ x + y := by
    have hz : 0 + y = y := by grind
    rwa [hz] at hle0
  exact Std.lt_of_lt_of_le hy hle

theorem red_update_nonzero (z A B : C R)
    (hG : 0 ≤ G z A B) (hy : 0 < z.im) (hA : A ≠ zero) :
    add A B ≠ zero := by
  intro hzero
  have hB : B = neg A := eq_neg_of_add_eq_zero hzero
  have hp : 0 < z.im * n2 A := pos_mul_n2 hy hA
  have hsub : G z A B = -z.im * n2 A := by
    rw [hB]
    exact red_cancellation_substitution z A
  grind

theorem blue_update_nonzero (z A B : C R)
    (hF : 0 ≤ F A B) (hy : 0 < z.im) (hA : A ≠ zero) :
    add B (mul z A) ≠ zero := by
  intro hzero
  have hB : B = neg (mul z A) := first_eq_neg_of_add_eq_zero hzero
  have hp : 0 < z.im * n2 A := pos_mul_n2 hy hA
  have hsub : F A B = -z.im * n2 A := by
    rw [hB]
    exact blue_cancellation_substitution z A
  grind

end C

open C

/-- The algebraic sector state used in the update proof. -/
structure Invariant (z A B : C R) : Prop where
  left_ne : A ≠ zero
  right_ne : B ≠ zero
  F_nonneg : 0 ≤ F A B
  G_nonneg : 0 ≤ G z A B

structure Pair (R : Type) where
  A : C R
  B : C R

/-- All algebraic pair transitions occurring in the paper's update, exit, and
post-exit ordinary-addition steps.  Whether a particular geometric step has one
of these types is outside this algebraic certificate. -/
inductive Move where
  | redUpdate      -- (A, B) ↦ (A+B, B)
  | blueUpdate     -- (A, B) ↦ (A, B+zA)
  | ordinaryRight  -- (A, B) ↦ (A, A+B)
  | blueExit       -- (A, B) ↦ (B, B+zA)

def step (z : C R) (m : Move) (p : Pair R) : Pair R :=
  match m with
  | .redUpdate => ⟨add p.A p.B, p.B⟩
  | .blueUpdate => ⟨p.A, add p.B (mul z p.A)⟩
  | .ordinaryRight => ⟨p.A, add p.A p.B⟩
  | .blueExit => ⟨p.B, add p.B (mul z p.A)⟩

def run (z : C R) : List Move → Pair R → Pair R
  | [], p => p
  | m :: ms, p => run z ms (step z m p)

theorem invariant_move (z : C R) (m : Move) (p : Pair R)
    (hy : 0 < z.im) (h : Invariant z p.A p.B) :
    Invariant z (step z m p).A (step z m p).B := by
  cases p with
  | mk A B =>
    cases m with
    | redUpdate =>
        constructor
        · exact red_update_nonzero z A B h.G_nonneg hy h.left_ne
        · exact h.right_ne
        · change 0 ≤ C.F (C.add A B) B
          rw [C.red_F z A B]
          exact h.F_nonneg
        · change 0 ≤ C.G z (C.add A B) B
          rw [C.red_G z A B]
          exact add_nonneg h.G_nonneg (Std.le_of_lt (pos_mul_n2 hy h.right_ne))
    | blueUpdate =>
        constructor
        · exact h.left_ne
        · exact blue_update_nonzero z A B h.F_nonneg hy h.left_ne
        · change 0 ≤ C.F A (C.add B (C.mul z A))
          rw [C.blue_F z A B]
          exact add_nonneg h.F_nonneg (Std.le_of_lt (pos_mul_n2 hy h.left_ne))
        · change 0 ≤ C.G z A (C.add B (C.mul z A))
          rw [C.blue_G z A B]
          exact h.G_nonneg
    | ordinaryRight =>
        constructor
        · exact h.left_ne
        · exact red_update_nonzero z A B h.G_nonneg hy h.left_ne
        · change 0 ≤ C.F A (C.add A B)
          rw [C.ordinary_F z A B]
          exact h.F_nonneg
        · change 0 ≤ C.G z A (C.add A B)
          rw [C.ordinary_G z A B]
          exact add_nonneg h.G_nonneg (Std.le_of_lt (pos_mul_n2 hy h.left_ne))
    | blueExit =>
        constructor
        · exact h.right_ne
        · exact blue_update_nonzero z A B h.F_nonneg hy h.left_ne
        · change 0 ≤ C.F B (C.add B (C.mul z A))
          rw [C.rotated_F z A B]
          exact h.G_nonneg
        · change 0 ≤ C.G z B (C.add B (C.mul z A))
          rw [C.rotated_G z A B]
          have hzF : 0 ≤ n2 z * F A B :=
            OrderedRing.mul_nonneg (n2_nonneg z) h.F_nonneg
          have hyB : 0 ≤ z.im * n2 B :=
            Std.le_of_lt (pos_mul_n2 hy h.right_ne)
          exact add_nonneg hzF hyB

theorem invariant_run (z : C R) (ms : List Move) (p : Pair R)
    (hy : 0 < z.im) (h : Invariant z p.A p.B) :
    Invariant z (run z ms p).A (run z ms p).B := by
  induction ms generalizing p with
  | nil => exact h
  | cons m ms ih =>
      exact ih (step z m p) (invariant_move z m p hy h)

/-- Headline algebraic certificate: after every finite sequence of the four
update transitions, both carried values are still nonzero and the two sector
forms are still nonnegative. -/
theorem update_noncancellation_certificate (z : C R) (ms : List Move) (p : Pair R)
    (hy : 0 < z.im) (h0 : Invariant z p.A p.B) :
    (run z ms p).A ≠ zero ∧ (run z ms p).B ≠ zero ∧
    0 ≤ F (run z ms p).A (run z ms p).B ∧
    0 ≤ G z (run z ms p).A (run z ms p).B := by
  have h := invariant_run z ms p hy h0
  exact ⟨h.left_ne, h.right_ne, h.F_nonneg, h.G_nonneg⟩

theorem ofReal_ne_zero {r : R} (hr : 0 < r) : ofReal r ≠ zero := by
  intro h
  simp [ofReal, zero] at h
  grind

theorem ofReal_F (a b : R) : F (ofReal a) (ofReal b) = 0 := by
  simp [F, ofReal, mul, conj]
  grind

theorem ofReal_G (z : C R) (a b : R) :
    G z (ofReal a) (ofReal b) = z.im * a * b := by
  cases z
  simp [G, ofReal, mul, conj]
  grind

/-- Positive real initial carried values satisfy the invariant.  In the paper
these are the initial unit cluster values before the mixed color run. -/
theorem positive_real_initial_invariant (z : C R) {a b : R}
    (hy : 0 < z.im) (ha : 0 < a) (hb : 0 < b) :
    Invariant z (ofReal a) (ofReal b) := by
  constructor
  · exact ofReal_ne_zero ha
  · exact ofReal_ne_zero hb
  · simp [ofReal_F]
  · rw [ofReal_G]
    have hab : 0 < a * b := OrderedRing.mul_pos ha hb
    have hp : 0 < (z.im * a) * b := by
      have hya : 0 < z.im * a := OrderedRing.mul_pos hy ha
      exact OrderedRing.mul_pos hya hb
    have hrewrite : z.im * a * b = (z.im * a) * b := by grind
    rw [hrewrite]
    exact Std.le_of_lt hp

#print axioms red_F
#print axioms red_G
#print axioms blue_F
#print axioms blue_G
#print axioms ordinary_F
#print axioms ordinary_G
#print axioms rotated_F
#print axioms rotated_G
#print axioms red_cancellation_substitution
#print axioms blue_cancellation_substitution
#print axioms invariant_move
#print axioms invariant_run
#print axioms update_noncancellation_certificate
#print axioms positive_real_initial_invariant

end DiskLamination
