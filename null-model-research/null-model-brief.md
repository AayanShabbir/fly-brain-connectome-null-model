# Does exact wiring drive connectome learning advantages, or do degree-preserving statistics suffice?

Author: Aayan Shabbir. Date: 2026-09-14.

Scope: concise research brief based on primary sources. The findings below come from the live web, arXiv HTML/PDF, and GitHub as of the writing date, and all URLs were verified reachable (HTTP 200 or fetched) during this session. Preprints are flagged as such. The term "learning advantage" is read two ways in this literature, early-optimization efficiency (Dhiman) versus final-task performance or convergence (FlyGM), and the verdict differs between the two.

## Verdict

Not settled. The answer is regime- and task-dependent, and the two strongest primary studies directly contradict each other.

- For early-learning dynamics on a fixed motion-decoding task under shared random init plus a degree-preserving null, the connectome's apparent advantage vanishes (Dhiman 2026, arXiv:2604.04033). In that setup, degree-preserving statistics and a fair init explain the effect; exact wiring adds no measurable learning benefit.
- For final-task control performance in embodied locomotion, the exact connectome beats its own degree-preserving rewiring (FlyGM, arXiv:2602.17997: 8.29° vs 13.55° angle error at high yaw), which directly contradicts Dhiman.
- For dynamical structure at fixed, frozen dynamics, the field's cleanest decomposition (Therianos, arXiv:2606.17745) says gross response (gain, dimensionality, non-normality) is statistics-governed, while input routing and dominant-mode identity are exact-wiring-specific.
- For predicting real neural activity, a degree-preserving shuffled connectome performs far worse than the true connectome (Creamer/Leifer/Pillow, C. elegans), which supports exact-wiring importance.

Bottom line: exact wiring does not reliably beat a well-constructed degree-preserving null on learning-efficiency metrics in the flyvis setup, but it does beat it on final control performance and on routing/mode structure. The field's consensus is that degree-preserving nulls are the mandatory control, and that coarse statistics set the regime while exact wiring sets the geometry (routing plus modes). Whether exact wiring buys a learning advantage is contested and unresolved.

## Numbered findings (each with a verified working URL)

1. Dhiman 2026, "Topological Sensitivity in Connectome-Constrained Neural Networks" (the key paper).
   URL: https://arxiv.org/abs/2604.04033 (HTML: https://arxiv.org/html/2604.04033v1) | Code: https://github.com/nalin-dhiman/Connectome-Constrained-Neural-Networks
   Method (read in full): a flyvis-based Drosophila connectome compared against a naive self-loop-matched random graph and a degree-preserving rewired null, on the MovingEdge direction-decoding task. Uses a three-stage "control ladder":
   - Stage A (weak): both models recovered from a connectome-trained checkpoint; the null matches only node/edge/self-loop counts. The connectome looks better: loss 0.514 vs 0.698, mean activity 0.656 vs 1.861, runtime 252s vs 309s (5 steps); 0.499 vs 0.557 loss, 0.740 vs 1.379 activity (10 steps).
   - Stage B (init control): shared from-scratch random init → the loss advantage vanishes (loss diff −0.0020 at both 5 and 10 steps, vs +0.1841 under checkpoint init).
   - Stage C (degree-preserving null): rewired graph matching directed in/out-degree plus self-loops → the activity advantage vanishes or reverses (loss diff +0.0003, activity diff −0.0106 at 5 steps).
   - Robustness: a 5-sample degree-preserving ensemble across 3 seeds → connectome loss 0.5155±0.0067 vs null 0.5172±0.0061; activity 0.5453 vs 0.5346. No advantage recovered.
   Claim: "Apparent topology advantages in connectome-constrained neural networks are highly sensitive to initialization and null-model design, and do not robustly persist under degree-preserving controls."
   Honest caveats, stated by the author: a single task family (MovingEdge); a short horizon (5/10 steps, not convergence); only 3 seeds; the degree-preserving null does not match higher-order structure (clustering, motifs, spatial layout); spectral properties uncontrolled; parameter-sharing is implementation-bound (rewiring preserves the flyvis metadata tables).

2. Therianos 2026, "A frozen rate operator from the complete larval connectome: degree and weight govern the gross response, exact wiring governs input routing and mushroom-body modes."
   URL: https://arxiv.org/abs/2606.17745 (HTML v2: https://arxiv.org/html/2606.17745v2)
   Exact wording (abstract/conclusion): "a connectome's gross operator behavior is largely a property of its degree and weight statistics, while the routing of input and the identity of the dominant driving modes are written into its exact wiring." Earlier v1 phrasing: "Coarse statistics set the regime; the precise pattern of connections sets the geometry." Method: runs the complete larval Drosophila connectome (2,825 neurons in its strongly connected core) as a frozen leaky-tanh rate operator with no fitted single-neuron parameters, against a degree-and-weight-matched rewiring ensemble plus cell-class-preserving, size-matched, singular-subspace, and family-wise controls. Results: gain, effective dimensionality, non-normality, and near-linearity all sit within a few percent of the matched ensemble (statistics-governed); sparse-input routing confined to about 1/5 of the core (vs ~2/3 for the ensemble) and mushroom-body concentration of the leading driving modes are exact-wiring-specific and survive the extra controls. Two candidate localizations were retracted. This is the strongest support for the "exact wiring sets routing/modes" side.

3. FlyGM / FlyGNN, "Whole-Brain Connectomic Graph Model Enables Whole-Body Locomotion Control in Fruit Fly" (Jin, Zhu, Zhang, Sui; NeurIPS 2025).
   URL: https://arxiv.org/abs/2602.17997 (HTML: https://arxiv.org/html/2602.17997)
   The whole-FlyWire connectome instantiated as a recurrent message-passing network, trained with IL+PPO to control a physics (MuJoCo) fly. Controls include a degree-preserving rewiring of the connectome ("DP Rewiring": shuffles edges while preserving each neuron's in/out-degree), an Erdős–Rényi graph with matched node/edge counts, and an MLP. Final angle error in degrees (full pipeline, high-yaw ψ=7): connectome weighted 8.29±0.21 vs DP Rewiring 13.55±0.69 vs Erdős–Rényi 125.36±8.96 vs MLP 13.90±0.45. The connectome also converges faster in imitation learning. This directly contradicts Dhiman's conclusion: under a degree-preserving null, exact wiring still wins on final control performance. Caveats: FlyGM's DP-rewiring baseline is unweighted (unit-strength edges) while the connectome is weighted, so it is not a fully weight-matched null, and it measures final convergence rather than early-learning efficiency.

4. Replications, critiques, and rebuttals of Dhiman 2026. I found no peer-reviewed replication or direct rebuttal. The closest public critique is a machine-generated review on pith.science with "3 major / 3 minor" objections:
   URL: https://pith.science/paper/2604.04033
   Major objections: (1) the degree-preserving null is not cell-type-aware, motif-preserving, or spatially constrained; if higher-order structure (cell-type blocks, motifs) drives the residual differences, Dhiman's result only shows that degree plus init explain the weak-control gap, not that topology is irrelevant. (2) The n=5 ensemble is small, with no dispersion/confidence intervals or permutation tests reported, so it is unclear whether the connectome sits outside or merely near the null distribution. (3) The construction and decision rule of the pre-training activity-scale diagnostic are unspecified. The review's desk verdict: a "useful control-ladder correction," though the degree-preserving foil may still leave cell-type and motif structure unmatched. No formal rebuttal exists yet.

5. Adjacent primary study: a C. elegans connectome-constrained model (Creamer, Leifer, Pillow).
   URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC12485687/ | bioRxiv: https://www.biorxiv.org/content/10.1101/2024.09.22.614271v3 (doi:10.1101/2024.09.22.614271)
   A latent linear dynamical system constrained to the C. elegans connectome predicts whole-brain causal interactions (relative correlation 0.92, about as good as the data predicts itself). A shuffled connectome (row/column permutation, which preserves the degree sequence) achieves much lower performance, and adding connections beyond the connectome does not help. This is a degree-preserving null that supports exact-wiring importance for predicting real activity, a direct counterpoint to Dhiman's flyvis result, though for a different organism and task (activity prediction vs learning-efficiency).

6. Adjacent primary study: flyvis / connectome-constrained DMN (Lappalainen et al., Nature 2024), the study Dhiman re-examines.
   URL: https://www.nature.com/articles/s41586-024-07939-3 (PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC11525180/)
   A connectome-constrained, task-optimized deep mechanistic network of the fly optic lobe (64 cell types, 45,669 neurons, 1.5M connections) predicts neural activity across 26 studies. The key point for this question: sparsity itself is what makes connectivity predictive, with a median Pearson correlation of 0.85 at 10% connectivity vs 0.38 at 80% (using only connectivity, no strengths). This supports the statistics/regime reading: the advantage is largely carried by sparse, degree-like structure rather than by the exact placement of every synapse.

7. Adjacent primary study: theory of connectome-constrained RNNs (Beiran & Litwin-Kumar, Nature Neuroscience 2025).
   URL: https://www.nature.com/articles/s41593-025-02080-4 (bioRxiv: https://www.biorxiv.org/content/10.1101/2024.02.22.581667v1)
   Teacher–student theory: a connectome alone is often insufficient to constrain recurrent dynamics (a degenerate solution space), but recordings from a small subset of neurons remove the degeneracy. The solution spaces of connectome-constrained and unconstrained models are qualitatively different. This cautions against over-interpreting connectome-constrained models when they are insufficiently constrained, and frames exact wiring as one constraint among several (weights, recordings), consistent with Dhiman's methodological point that connectivity alone is not sufficient.

8. Prior negative-control / null-model studies in graph and SNN learning, supporting the "statistics suffice" side.
   - Reservoir computing with real brain connectomes (Bio-ESNs): constraining reservoir connectivity with empirical connectomes of three primate species gave performance "as good as" random conditions on memory tasks. URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC9710781/, supports the view that coarse/statistical structure (density, degree) is enough for generic reservoir tasks.
   - Dhiman's own control ladder (finding 1) is the cleanest negative-control result in the connectome-constrained learning literature: under a fair init plus a degree-preserving null, the learning-efficiency advantage disappears.

9. Prior negative-control / null-model studies supporting the "exact wiring matters" side.
   - Creamer/Leifer/Pillow shuffled-connectome control (finding 5): degree-preserving shuffle degrades activity prediction.
   - Therianos routing/mode controls (finding 2): exact wiring fixes routing and mushroom-body modes beyond degree-and-weight-matched ensembles.
   - FlyGM degree-preserving rewiring control (finding 3): the exact connectome beats DP rewiring on final control performance.

10. What the field currently believes (consensus, strongest side first).
    The methodological consensus is strong and settled: degree-preserving nulls and shared-initialization controls are mandatory when claiming a connectome learning advantage, and naive sparse-random baselines are no longer acceptable (Dhiman; the pith review; the null-model literature Dhiman cites). The substantive consensus is that coarse statistics set the gross/global dynamical regime (gain, dimensionality, non-normality, near-linearity, Therianos; sparsity-driven predictivity in flyvis, Lappalainen), while exact wiring fixes routing and dominant-mode identity (Therianos; C. elegans activity prediction, Creamer). The contested piece is whether exact wiring confers a learning advantage: Dhiman (early-learning, flyvis) says no; FlyGM (final control, locomotion) says yes. The strongest, most-cited support for "exact wiring matters" is the routing/mode and activity-prediction evidence (Therianos, Creamer, Lappalainen); the strongest support for "statistics suffice for learning" is Dhiman plus the reservoir-computing result.

## Hard-caveat section: what is still unsettled

1. The two headline studies measure different things. Dhiman tests early-optimization efficiency (5/10 steps) on a motion-decoding task; FlyGM tests final-task control performance (trained to convergence) on embodied locomotion. These are not the same claim, and neither study controls the other's regime. No single study has run the same task under both early-learning and convergence evaluation with a fully weight-matched degree-preserving null.

2. Null-model adequacy is the crux, and it is not resolved. Dhiman's degree-preserving null matches in/out-degree and self-loops but not clustering, motifs, cell-type blocks, spatial layout, or spectral properties (an author-stated limitation). The pith review's major objection #1 is exactly this: if higher-order structure drives residual effects, Dhiman's "disappearance" only proves that degree plus init explain the weak-control gap, not that topology is irrelevant. FlyGM's DP-rewiring null is unweighted, so it is not a clean weight-matched control either.

3. Small samples and weak statistics. Dhiman uses 3 seeds and a 5-sample ensemble with no reported dispersion or permutation tests against the null distribution; FlyGM reports mean±std over limited runs. Neither establishes whether the connectome sits outside the null distribution with tight confidence.

4. No replication or rebuttal of Dhiman exists yet. The only public critique is a machine-generated review (pith.science, grok-4.5) with 3 major objections; no human peer-reviewed replication or rebuttal has been published. FlyGM, which contradicts Dhiman, does not cite it, so the contradiction is unaddressed in the literature.

5. Underdetermination of connectivity. Beiran & Litwin-Kumar show that a connectome often does not uniquely constrain dynamics; exact wiring is necessary but not sufficient, since weights, signs, and recorded activity matter. This makes "does exact wiring drive learning advantages" partly ill-posed without specifying the parameterization and the training control.

6. Scope of the verdict. Dhiman's negative result is confined to one task (flyvis MovingEdge) and one organism's visual circuit. The C. elegans activity-prediction result and the FlyGM locomotion result are different organisms and tasks, and both favor exact wiring. Generality across tasks and species is untested.

## Sources cited (all verified working at time of writing)

- https://arxiv.org/abs/2604.04033 (Dhiman; plus HTML and GitHub nalin-dhiman/Connectome-Constrained-Neural-Networks)
- https://arxiv.org/abs/2606.17745 (Therianos; plus HTML v2)
- https://arxiv.org/abs/2602.17997 (FlyGM; Jin, Zhu, Zhang, Sui; plus HTML)
- https://pith.science/paper/2604.04033 (machine critique of Dhiman)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12485687/ (Creamer/Leifer/Pillow, C. elegans; doi:10.1101/2024.09.22.614271)
- https://www.nature.com/articles/s41586-024-07939-3 (Lappalainen et al., flyvis DMN, Nature 2024)
- https://www.nature.com/articles/s41593-025-02080-4 (Beiran & Litwin-Kumar, Nat Neurosci 2025)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9710781/ (Bio-ESN reservoir computing with real connectomes)