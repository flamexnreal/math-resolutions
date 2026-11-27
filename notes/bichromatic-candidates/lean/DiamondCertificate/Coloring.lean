import DiamondCertificate.Data

namespace DiamondCertificate

private theorem sameRemaining (a b d x y : Color)
    (hab : a ≠ b) (had : a ≠ d) (hbd : b ≠ d)
    (hxa : x ≠ a) (hxb : x ≠ b) (hxd : x ≠ d)
    (hya : y ≠ a) (hyb : y ≠ b) (hyd : y ≠ d) : x = y := by
  simp only [Ne, ← Fin.val_inj] at *
  omega

theorem bichromatic_forbidden (c : Vertex → Color) (proper : Proper c) :
    ¬ (c 0 = c 2 ∧ c 1 = c 3) := by
  rintro ⟨h02, h13⟩
  have h01 := proper 0 1 (by decide)
  have h120 := proper 12 0 (by decide)
  have h121 := proper 12 1 (by decide)
  have h141 := proper 14 1 (by decide)
  have h140 : c 14 ≠ c 0 := h02 ▸ proper 14 2 (by decide)
  have h1412 := proper 14 12 (by decide)
  have h200 := proper 20 0 (by decide)
  have h201 : c 20 ≠ c 1 := h13 ▸ proper 20 3 (by decide)
  have h2012 := proper 20 12 (by decide)
  have h1420 : c 14 = c 20 :=
    sameRemaining _ _ _ _ _ h01 h120.symm h121.symm h140 h141 h1412 h200 h201 h2012
  have h160 : c 16 ≠ c 0 := h02 ▸ proper 16 2 (by decide)
  have h161 : c 16 ≠ c 1 := h13 ▸ proper 16 3 (by decide)
  have h1620 := proper 16 20 (by decide)
  have h1612 : c 16 = c 12 :=
    sameRemaining _ _ _ _ _ h01 h200.symm h201.symm h160 h161 h1620 h120 h121 h2012.symm
  have h150 : c 15 ≠ c 0 := h02 ▸ proper 15 2 (by decide)
  have h1512 : c 15 ≠ c 12 := h1612 ▸ proper 15 16 (by decide)
  have h1520 : c 15 ≠ c 20 := h1420 ▸ proper 15 14 (by decide)
  have h151 : c 15 = c 1 :=
    sameRemaining _ _ _ _ _ h120.symm h200.symm h2012.symm h150 h1512 h1520
      h01.symm h121.symm h201.symm
  have h1712 := proper 17 12 (by decide)
  have h1720 : c 17 ≠ c 20 := h1420 ▸ proper 17 14 (by decide)
  have h171 : c 17 ≠ c 1 := h151 ▸ proper 17 15 (by decide)
  have h170 : c 17 = c 0 :=
    sameRemaining _ _ _ _ _ h2012.symm h121 h201 h1712 h1720 h171
      h120.symm h200.symm h01
  have h191 : c 19 ≠ c 1 := h151 ▸ proper 19 15 (by decide)
  have h1912 : c 19 ≠ c 12 := h1612 ▸ proper 19 16 (by decide)
  have h1920 := proper 19 20 (by decide)
  have h190 : c 19 ≠ c 0 := h170 ▸ proper 19 17 (by decide)
  exact h190
    (sameRemaining _ _ _ _ _ h2012.symm h121 h201 h1912 h1920 h191
      h120.symm h200.symm h01)

end DiamondCertificate
