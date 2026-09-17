# CONSTRAINTS: the walls of the maze (V2, verified and cited)

Formal specification of the fly brain's measured properties, the walls any successful synthetic reconstruction must satisfy. They narrow the brute-force search from "all possible brains" to "brains like the fly."

V2 changes: every constraint now traces to a primary source. The citation cross-check for C1 through C10 passed, and the two methodology-pending items, C7 and C8, were confirmed from the Lin et al. Methods. The null-model gate below folds in the most recent and most authoritative finding (null-model-brief, 2026-09-14): the connectome's learning advantage is contested, and generators must not over-claim it.

## Measured constraints (all cited, 2026-09-15)

| # | Constraint | Value | Source (primary) | Confidence |
|:--|:---|:---|:---|:---|
| C1 | Node count | 139,255 neurons (127,978 high-confidence, ≥5-synapse graph) | Lin et al. Nature 2024; Dorkenwald et al. Nature 2024 | High |
| C2 | Connection density | ≈ 0.000161 (~0.016%) directed conn. prob. | Lin et al. (0.000870 / 5.4×); adjacency check 0.0001595 | High |
| C3 | Weighted synapses | 15.1M directed weighted / ~54.5M raw chemical (~32M at ≥5) | Lin et al. 2024 | High |
| C4 | Rich club | ~30% of neurons (40,218; cutoff total degree 37), 5.4× internal density (0.000870) | Lin et al. 2024 | High |
| C5 | Reciprocity | ≈ 0.138 connection reciprocity probability | Lin et al. 2024 | High |
| C6 | Recurrence | recurrent motifs (7-13) over-represented; feedforward motifs (1-3) under-represented | Lin et al. 2024 | High |
| C7 | Small-worldness S | S^Δ ≈ 141 (clustering 0.0463 vs ER 0.0003) | Lin et al. 2024 (Methods eqn. 1), previously PENDING, now confirmed | Med-High |
| C8 | Avg directed path | ≈ 4.42 hops (max 13) within giant SCC | Lin et al. 2024 (Main), previously PENDING, now confirmed | Med-High |
| C9 | Robustness | survives ~60% neuron removal; no command neurons | Lin et al. 2024 | High |
| C10 | Strongly-connected component | ~93.3% of neurons in single SCC (98.8% WCC) | Lin et al. 2024 | Med |

### Source map

- The C1–C10 structural values all trace to Lin, A., Yang, R., Dorkenwald, S., et al. "Network statistics of the whole-brain connectome of Drosophila." Nature 634, 153-165 (2024). DOI 10.1038/s41586-024-07968-y (Open Access, CC BY-NC-ND). Node counts are cross-checked against the companion wiring-diagram paper, Dorkenwald et al., 10.1038/s41586-024-07558-y (139,255 neurons / ~54.5M chemical synapses).
- Confidence note: all numbers refer to the October 2024 whole-brain connectome, not the June 2026 full-CNS extension (~166k neurons). The global metrics differ on that larger graph and must not be conflated.

## Null-model gate (new in V2, do not skip)

Status: contested. The most recent corpus reading (null-model-research/null-model-brief.md, 2026-09-14) holds that whether exact wiring confers a learning advantage is unresolved and directly disputed:

- Against an exact-wiring learning advantage (early-learning efficiency): Dhiman 2026 (arXiv:2604.04033). On the flyvis MovingEdge task, under shared from-scratch init plus a degree-preserving rewired null, the connectome's loss/activity advantage vanishes (stage B/C: the loss difference collapses from +0.184 to ≈0). Methodologically, the consensus is that degree-preserving nulls and shared-init controls are mandatory; a naive sparse-random baseline is not acceptable.
- For an exact-wiring advantage (final-task control): FlyGM (arXiv:2602.17997, NeurIPS 2025). Under degree-preserving rewiring, the exact connectome beats the null on final control performance (8.29° vs 13.55° angle error at high yaw). This contradicts Dhiman directly.
- Regime framing (Therianos, arXiv:2606.17745): coarse degree/weight statistics set the gross dynamical regime (gain, dimensionality), while exact wiring fixes input routing and the identity of the dominant modes.
- Activity prediction (Creamer/Leifer/Pillow, C. elegans): a degree-preserving shuffled connectome predicts neural activity far worse than the true connectome.

Evaluation gates for downstream reconstruction work:

1. Do not over-claim a connectome learning advantage. Any connectome-constrained synthetic reconstruction inherits the contested status above.
2. Mandatory controls: every learning/performance claim must be evaluated against a degree-preserving null and a shared-initialization baseline. A naive random-graph control is insufficient.
3. State the regime: early-learning efficiency and convergence/final performance give opposite verdicts, so any claim must name which is being tested.
4. Weight-matching caveat: neither headline null is clean. Dhiman's degree-preserving null is not cell-type/motif/spatial-aware, and FlyGM's degree-preserving rewiring null is unweighted. Treat neither as the final word.

The structural walls, C1 through C10, are not contested: they are measured graph statistics and stand as-is. Only the learning-advantage claim is gated.

## Status (V2)

- [x] Cross-check every constraint against its primary source (C1–C10 to Lin et al. Nature 2024 and companion papers), pass
- [x] Confirm the C4/C7/C8 methodology from Lin et al. (rich-club 5.4×/cutoff 37; S^Δ = 141 via Methods eqn. 1; path 4.42 via Main), confirmed
- [x] Fold the null-model finding into a gate (contested learning-advantage), done
- [ ] Extend with behavioral constraints after sim work: escape latency (~10ms Giant Fiber), feeding, grooming
- [ ] If a June-2026 full-CNS graph is adopted, re-derive C1–C10 for ~166k nodes (the current numbers are brain-only)

## Notes

- These are the search-space walls. Brute force explores only within them.
- Machine-readable form: constraints.json (same directory, version 2.0, same sources).
- Null-model authority: null-model-research/null-model-brief.md.