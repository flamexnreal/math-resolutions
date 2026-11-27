import DiamondCertificate.Data

namespace DiamondCertificate

def rimEdges : List Edge := [(0, 1), (1, 2), (2, 3), (0, 3)]

def degree (v : Vertex) : Nat :=
  (vertices.filter (hasEdge v)).length

def Triangle (a b c : Vertex) : Prop := Adj a b ∧ Adj b c ∧ Adj c a

def ListedFace (a b c : Vertex) : Prop :=
  ∃ f ∈ faces, List.Perm [f.1, f.2.1, f.2.2] [a, b, c]

instance (a b c : Vertex) : Decidable (Triangle a b c) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _))

theorem edges_simple : edges.Nodup ∧ ∀ e ∈ edges, e.1 < e.2 := by decide

theorem rim_induced (u v : Vertex) (hu : u ∈ rim) (hv : v ∈ rim) :
    Adj u v ↔ edgeKey u v ∈ rimEdges :=
  (by decide : ∀ u ∈ rim, ∀ v ∈ rim, Adj u v ↔ edgeKey u v ∈ rimEdges) u hu v hv

theorem interior_min_degree (v : Vertex) (hv : v ∉ rim) : 5 ≤ degree v :=
  (by decide : ∀ v ∈ vertices, v ∉ rim → 5 ≤ degree v) v (mem_vertices v) hv

private def faceKey (a b c : Vertex) : List Vertex :=
  if a ≤ b then
    if b ≤ c then [a, b, c] else if a ≤ c then [a, c, b] else [c, a, b]
  else
    if a ≤ c then [b, a, c] else if b ≤ c then [b, c, a] else [c, b, a]

private theorem faceKey_spec (a b c : Vertex) :
    List.Perm (faceKey a b c) [a, b, c] ∧ (faceKey a b c).Pairwise (· ≤ ·) := by
  unfold faceKey
  split <;> split <;> (try split) <;> constructor
  · exact List.Perm.refl _
  · simp [Fin.le_def] at * <;> omega
  · exact List.Perm.cons a (List.Perm.swap b c [])
  · simp [Fin.le_def] at * <;> omega
  · exact (List.perm_middle (a := c) (l₁ := [a, b]) (l₂ := [])).symm
  · simp [Fin.le_def] at * <;> omega
  · exact List.Perm.swap a b [c]
  · simp [Fin.le_def] at * <;> omega
  · exact List.perm_middle (a := a) (l₁ := [b, c]) (l₂ := [])
  · simp [Fin.le_def] at * <;> omega
  · exact (List.Perm.swap b c [a]).trans
      (List.perm_middle (a := a) (l₁ := [b, c]) (l₂ := []))
  · simp [Fin.le_def] at * <;> omega

private def faceKeys : List (List Vertex) :=
  faces.map fun f => faceKey f.1 f.2.1 f.2.2

private def triangleKeys : List (List Vertex) :=
  vertices.flatMap fun a =>
    (vertices.filter fun b => decide (a < b ∧ Adj a b)).flatMap fun b =>
      (vertices.filter fun c => decide (b < c ∧ Adj b c ∧ Adj c a)).map fun c => [a, b, c]

private theorem mem_triangleKeys {a b c : Vertex} (hab : a < b) (hbc : b < c) :
    [a, b, c] ∈ triangleKeys ↔ Triangle a b c := by
  simp only [triangleKeys, List.mem_flatMap, List.mem_filter, List.mem_map, mem_vertices,
    true_and, decide_eq_true_eq]
  constructor
  · rintro ⟨x, y, hy, z, hz, key⟩
    simp only [List.cons.injEq, and_true] at key
    rcases key with ⟨rfl, rfl, rfl⟩
    exact ⟨hy.2, hz.2.1, hz.2.2⟩
  · rintro ⟨ab, bc, ca⟩
    exact ⟨a, b, ⟨hab, ab⟩, c, ⟨hbc, bc, ca⟩, rfl⟩

private theorem faceKey_eq_iff (f : Face) {a b c : Vertex} (hab : a < b) (hbc : b < c) :
    faceKey f.1 f.2.1 f.2.2 = [a, b, c] ↔ List.Perm [f.1, f.2.1, f.2.2] [a, b, c] := by
  obtain ⟨hp, hs⟩ := faceKey_spec f.1 f.2.1 f.2.2
  constructor
  · intro h
    simpa only [h] using hp.symm
  · intro h
    apply List.Perm.eq_of_pairwise (fun _ _ _ _ => Fin.le_antisymm) hs _ (hp.trans h)
    simpa using And.intro ⟨Fin.le_of_lt hab, Fin.le_of_lt (Fin.lt_trans hab hbc)⟩
      (Fin.le_of_lt hbc)

private theorem triangle_keys_agree : List.Perm triangleKeys faceKeys := by
  decide +kernel

theorem triangles_exact (a b c : Vertex) (hab : a < b) (hbc : b < c) :
    Triangle a b c ↔ ListedFace a b c := by
  rw [← mem_triangleKeys hab hbc, triangle_keys_agree.mem_iff, faceKeys, List.mem_map]
  simp only [ListedFace, faceKey_eq_iff _ hab hbc]

theorem faces_distinct :
    faces.Pairwise (fun f g => ¬ List.Perm [f.1, f.2.1, f.2.2] [g.1, g.2.1, g.2.2]) :=
  by decide +kernel

abbrev Point := Int × Int

def width : Int := 250

def coords : Vector Point 21 := #v[
  (0, 0), (250, 0), (250, 250), (0, 250), (125, 124), (119, 120), (121, 126),
  (121, 130), (125, 128), (114, 129), (128, 133), (117, 134), (132, 90), (130, 127),
  (189, 128), (168, 169), (128, 190), (144, 130), (130, 118), (129, 148), (92, 133)]

def point (v : Vertex) : Point := coords[v]

def det (a b c : Vertex) : Int :=
  let (x, y) := point a
  let (u, v) := point b
  let (s, t) := point c
  (u - x) * (t - y) - (v - y) * (s - x)

abbrev InsideSquare (p : Point) : Prop :=
  0 < p.1 ∧ p.1 < width ∧ 0 < p.2 ∧ p.2 < width

/-- Both endpoints of `f` lie in the same open half-plane of the line through `e`. -/
abbrev SameSide (e f : Edge) : Prop :=
  (0 < det e.1 e.2 f.1 ∧ 0 < det e.1 e.2 f.2) ∨
  (det e.1 e.2 f.1 < 0 ∧ det e.1 e.2 f.2 < 0)

abbrev DisjointEnds (e f : Edge) : Prop :=
  e.1 ≠ f.1 ∧ e.1 ≠ f.2 ∧ e.2 ≠ f.1 ∧ e.2 ≠ f.2

abbrev OutsideFace (f : Face) (v : Vertex) : Prop :=
  det f.1 f.2.1 v < 0 ∨ det f.2.1 f.2.2 v < 0 ∨ det f.2.2 f.1 v < 0

def doubleArea (f : Face) : Int := det f.1 f.2.1 f.2.2

theorem square_boundary :
    rim = [0, 1, 2, 3] ∧ rimEdges = [(0, 1), (1, 2), (2, 3), (0, 3)] ∧
    0 < width ∧ rim.map point = [(0, 0), (width, 0), (width, width), (0, width)] :=
  by decide

theorem points_injective (u v : Vertex) (h : u ≠ v) : point u ≠ point v :=
  (by decide : ∀ u ∈ vertices, ∀ v ∈ vertices, u ≠ v → point u ≠ point v)
    u (mem_vertices u) v (mem_vertices v) h

theorem interior_in_square (v : Vertex) (hv : v ∉ rim) : InsideSquare (point v) :=
  (by decide : ∀ v ∈ vertices, v ∉ rim → InsideSquare (point v)) v (mem_vertices v) hv

set_option maxRecDepth 4096 in
set_option maxHeartbeats 2000000 in
theorem edge_line_free (e : Edge) (he : e ∈ edges) (v : Vertex)
    (h₁ : v ≠ e.1) (h₂ : v ≠ e.2) : det e.1 e.2 v ≠ 0 := by
  have check : (edges.all fun e => vertices.all fun v =>
      decide (v ≠ e.1 → v ≠ e.2 → det e.1 e.2 v ≠ 0)) = true := by decide +kernel
  exact of_decide_eq_true (List.all_eq_true.mp (List.all_eq_true.mp check e he)
    v (mem_vertices v)) h₁ h₂

set_option maxRecDepth 4096 in
set_option maxHeartbeats 2000000 in
theorem nonincident_separation (e : Edge) (he : e ∈ edges) (f : Edge) (hf : f ∈ edges)
    (h : DisjointEnds e f) : SameSide e f ∨ SameSide f e := by
  have check : (edges.all fun e => edges.all fun f =>
      decide (DisjointEnds e f → SameSide e f ∨ SameSide f e)) = true := by decide +kernel
  exact of_decide_eq_true (List.all_eq_true.mp (List.all_eq_true.mp check e he) f hf) h

theorem faces_positive (f : Face) (hf : f ∈ faces) : 0 < doubleArea f :=
  (by decide : ∀ f ∈ faces, 0 < doubleArea f) f hf

theorem faces_on_edges (f : Face) (hf : f ∈ faces) : Triangle f.1 f.2.1 f.2.2 :=
  (by decide : ∀ f ∈ faces, Triangle f.1 f.2.1 f.2.2) f hf

set_option maxRecDepth 4096 in
set_option maxHeartbeats 2000000 in
theorem faces_empty (f : Face) (hf : f ∈ faces) (v : Vertex)
    (h₁ : v ≠ f.1) (h₂ : v ≠ f.2.1) (h₃ : v ≠ f.2.2) : OutsideFace f v := by
  have check : (faces.all fun f => vertices.all fun v =>
      decide (v ≠ f.1 → v ≠ f.2.1 → v ≠ f.2.2 → OutsideFace f v)) = true := by decide +kernel
  exact of_decide_eq_true (List.all_eq_true.mp (List.all_eq_true.mp check f hf)
    v (mem_vertices v)) h₁ h₂ h₃

theorem faces_fill_area : (faces.map doubleArea).sum = 2 * width * width := by decide

end DiamondCertificate
