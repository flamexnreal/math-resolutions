import Std

namespace DiamondCertificate

inductive Move where
  | lemma27 | lemma28 | lemma29

/-- Necessary order projection, not a model of the full moves.
The list records moves in reverse chronological order. -/
inductive OrderTrace : List Move → Nat → Prop where
  | diamond : OrderTrace [] 4
  | extend27 : OrderTrace ms n → OrderTrace (.lemma27 :: ms) (n + 12)
  | extend28 : OrderTrace (m :: ms) n → OrderTrace (.lemma28 :: m :: ms) (n + 4)
  | extend29 : OrderTrace (m :: ms) n → OrderTrace (.lemma29 :: m :: ms) (n + 3)

theorem orderInvariant {ms n} (h : OrderTrace ms n) :
    match ms with
    | [] => n = 4
    | _ :: _ => n = 16 ∨ n = 19 ∨ n = 20 ∨ 22 ≤ n := by
  induction h with
  | diamond => rfl
  | @extend27 ms n _ ih =>
      cases ms with
      | nil =>
          change n = 4 at ih
          left
          omega
      | cons _ _ =>
          change n = 16 ∨ n = 19 ∨ n = 20 ∨ 22 ≤ n at ih
          right; right; right
          omega
  | @extend28 m ms n _ ih =>
      change n = 16 ∨ n = 19 ∨ n = 20 ∨ 22 ≤ n at ih
      change n + 4 = 16 ∨ n + 4 = 19 ∨ n + 4 = 20 ∨ 22 ≤ n + 4
      omega
  | @extend29 m ms n _ ih =>
      change n = 16 ∨ n = 19 ∨ n = 20 ∨ 22 ≤ n at ih
      change n + 3 = 16 ∨ n + 3 = 19 ∨ n + 3 = 20 ∨ 22 ≤ n + 3
      omega

theorem order21_unreachable (ms : List Move) : ¬ OrderTrace ms 21 := by
  intro h
  have hi := orderInvariant h
  cases ms with
  | nil => cases hi
  | cons m ms =>
      change 21 = 16 ∨ 21 = 19 ∨ 21 = 20 ∨ 22 ≤ 21 at hi
      omega

end DiamondCertificate
