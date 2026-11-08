Scripts for "Metaplectic Jacquet-Langlands, companion paper (rank two, wild place)", Draft 2.
Pure Python 3 (fractions, pickle, numpy for step4-6 linear algebra only). Run from this directory
after editing the sys.path lines (they point to the scripts directory) or by placing the files there.
Recommended order to verify the cocycle/symbol layer independently:
  python3 step7_symbols.py            # solves the cubic Hilbert symbols of F and E_0 -> symbols.pkl
  python3 step12_H1_proof_check.py    # referee's example, closed form of kappa, symbol facts, (H1) identity
Finite design layer: step1_G3.py, step2_finite.py, step3_actions.py, step4_design.py, step6_orbit.py.
Corroboration: step5_H1.py, step8_H1test.py, step8b.py, step9_H1_stratified.py, step10_defects.py,
               step11_endtoend.py, step11b.py.
Level two (Draft 5): step13_level2.py (needs finite.pkl from step2_finite.py, included), then
  step14_level2_restriction.py and step15_level2_clifford.py (needs design_0011020002.pkl from step6, included);
  zsolve.py is the exact integer solver used by step13. Total about ten minutes.
