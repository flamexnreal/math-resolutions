import Std

namespace DiamondCertificate

abbrev Vertex := Fin 21
abbrev Color := Fin 4
abbrev Edge := Vertex × Vertex
abbrev Face := Vertex × Vertex × Vertex

def vertices : List Vertex := List.finRange 21

def rim : List Vertex := [0, 1, 2, 3]

def edges : List Edge := [
  (0, 1), (0, 3), (0, 12), (0, 20), (1, 2), (1, 12), (1, 14),
  (2, 3), (2, 14), (2, 15), (2, 16), (3, 16), (3, 20), (4, 5),
  (4, 6), (4, 8), (4, 13), (4, 18), (5, 6), (5, 9), (5, 12),
  (5, 18), (5, 20), (6, 7), (6, 8), (6, 9), (7, 8), (7, 9),
  (7, 10), (7, 11), (8, 10), (8, 13), (9, 11), (9, 20), (10, 11),
  (10, 13), (10, 17), (10, 19), (11, 19), (11, 20), (12, 14), (12, 17),
  (12, 18), (12, 20), (13, 17), (13, 18), (14, 15), (14, 17), (15, 16),
  (15, 17), (15, 19), (16, 19), (16, 20), (17, 18), (17, 19), (19, 20)]

def faces : List Face := [
  (0, 1, 12), (0, 12, 20), (0, 20, 3), (1, 2, 14), (1, 14, 12), (2, 3, 16),
  (2, 15, 14), (2, 16, 15), (3, 20, 16), (4, 5, 18), (4, 6, 5), (4, 8, 6),
  (4, 13, 8), (4, 18, 13), (5, 6, 9), (5, 9, 20), (5, 12, 18), (5, 20, 12),
  (6, 7, 9), (6, 8, 7), (7, 8, 10), (7, 10, 11), (7, 11, 9), (8, 13, 10),
  (9, 11, 20), (10, 13, 17), (10, 17, 19), (10, 19, 11), (11, 19, 20), (12, 14, 17),
  (12, 17, 18), (13, 18, 17), (14, 15, 17), (15, 16, 19), (15, 19, 17), (16, 20, 19)]

def graph6 : String := "Tl?GWCJ@oB?Jp?AIK?P?@K?C?JoWEG?WySUH"

private def g6Digits (record : String) : List Nat :=
  record.toList.map fun ch => ch.toNat - 63

/-- Short graph6 orders the pairs by increasing upper endpoint, then lower endpoint. -/
def decodeShortGraph6 (record : String) : List Edge :=
  let digits := (g6Digits record).tail.toArray
  vertices.flatMap fun v => vertices.filterMap fun u =>
    let i := v.val * (v.val - 1) / 2 + u.val
    if u < v ∧ Nat.testBit digits[i / 6]! (5 - i % 6) then some (u, v) else none

theorem census_exact :
    graph6.toList.head? = some 'T' ∧ graph6.toList.length = 36 ∧
    (∀ ch ∈ graph6.toList, 63 ≤ ch.toNat ∧ ch.toNat < 127) ∧
    List.Perm (decodeShortGraph6 graph6) edges := by decide +kernel

def edgeKey (u v : Vertex) : Edge := if u < v then (u, v) else (v, u)

def hasEdge (u v : Vertex) : Bool := edges.contains (edgeKey u v)
def Adj (u v : Vertex) : Prop := hasEdge u v = true

instance (u v : Vertex) : Decidable (Adj u v) :=
  inferInstanceAs (Decidable (hasEdge u v = true))

theorem adj_iff_edge (u v : Vertex) : Adj u v ↔ edgeKey u v ∈ edges := by
  simp [Adj, hasEdge]

theorem adj_symmetric (u v : Vertex) : Adj u v ↔ Adj v u := by
  simp only [adj_iff_edge]
  by_cases heq : u = v
  · subst v
    rfl
  · have hlt : u < v ∨ v < u := by
      simp only [Fin.lt_def, ← Fin.val_inj] at *
      omega
    rcases hlt with h | h <;> simp [edgeKey, h, Fin.lt_asymm h]

def Proper (c : Vertex → Color) : Prop :=
  ∀ u v, Adj u v → c u ≠ c v

theorem mem_vertices (v : Vertex) : v ∈ vertices := List.mem_finRange v

theorem census_order : vertices.Nodup ∧ vertices.length = 21 := by decide

end DiamondCertificate
