import DiamondCertificate.Coloring
import DiamondCertificate.Disk
import DiamondCertificate.Generation

namespace DiamondCertificate

/-- Exact finite conditions for the straight-line realization. The conversion
to a plane disk and the projection of the paper's moves are in the handoff. -/
structure CandidateData : Prop where
  simple : edges.Nodup ∧ ∀ e ∈ edges, e.1 < e.2
  induced : ∀ u v, u ∈ rim → v ∈ rim → (Adj u v ↔ edgeKey u v ∈ rimEdges)
  minDegree : ∀ v, v ∉ rim → 5 ≤ degree v
  triangles : ∀ a b c : Vertex, a < b → b < c → (Triangle a b c ↔ ListedFace a b c)
  noDuplicateFaces :
    faces.Pairwise (fun f g => ¬ List.Perm [f.1, f.2.1, f.2.2] [g.1, g.2.1, g.2.2])
  square : rim = [0, 1, 2, 3] ∧ rimEdges = [(0, 1), (1, 2), (2, 3), (0, 3)] ∧
    0 < width ∧ rim.map point = [(0, 0), (width, 0), (width, width), (0, width)]
  distinctPoints : ∀ u v, u ≠ v → point u ≠ point v
  interior : ∀ v, v ∉ rim → InsideSquare (point v)
  noVertexOnEdgeLine : ∀ e ∈ edges, ∀ v, v ≠ e.1 → v ≠ e.2 → det e.1 e.2 v ≠ 0
  separatedEdges :
    ∀ e ∈ edges, ∀ f ∈ edges, DisjointEnds e f → SameSide e f ∨ SameSide f e
  positiveFaces : ∀ f ∈ faces, 0 < doubleArea f
  faceEdges : ∀ f ∈ faces, Triangle f.1 f.2.1 f.2.2
  emptyFaces : ∀ f ∈ faces, ∀ v, v ≠ f.1 → v ≠ f.2.1 → v ≠ f.2.2 → OutsideFace f v
  fullArea : (faces.map doubleArea).sum = 2 * width * width

theorem candidate_data : CandidateData :=
  ⟨edges_simple, rim_induced, interior_min_degree, triangles_exact, faces_distinct,
    square_boundary, points_injective, interior_in_square, edge_line_free,
    nonincident_separation, faces_positive, faces_on_edges, faces_empty, faces_fill_area⟩

theorem census_counterexample_certificate :
    CandidateData ∧
    (∀ c : Vertex → Color, Proper c → ¬ (c 0 = c 2 ∧ c 1 = c 3)) ∧
    (∀ ms : List Move, ¬ OrderTrace ms vertices.length) :=
  ⟨candidate_data, bichromatic_forbidden, by simpa only [census_order.2] using order21_unreachable⟩

#print axioms census_counterexample_certificate
#print axioms candidate_data
#print axioms census_exact
#print axioms census_order
#print axioms adj_iff_edge
#print axioms adj_symmetric
#print axioms mem_vertices
#print axioms bichromatic_forbidden
#print axioms orderInvariant
#print axioms order21_unreachable
#print axioms edges_simple
#print axioms rim_induced
#print axioms interior_min_degree
#print axioms triangles_exact
#print axioms faces_distinct
#print axioms square_boundary
#print axioms points_injective
#print axioms interior_in_square
#print axioms edge_line_free
#print axioms nonincident_separation
#print axioms faces_positive
#print axioms faces_on_edges
#print axioms faces_empty
#print axioms faces_fill_area

end DiamondCertificate
