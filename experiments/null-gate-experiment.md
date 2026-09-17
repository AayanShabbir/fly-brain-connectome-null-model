# The Null-Model Experiment: Does Exact Connectome Wiring Give a Learning Advantage?

Pre-registration-ready protocol for the field's open question. Does a biological connectome's exact wiring confer a learning advantage over degree-preserving structural statistics alone?

## 0. Assumptions (stated explicitly, not re-derived)

- **Canonical task:** flyvis MovingEdge direction-decoding (supervised). This is the shared task both regimes run on.
- **Dhiman 2026 (arXiv:2604.04033):** the null was degree-preserving but NOT cell-type/motif/space matched; tested EARLY-learning (few steps); n=5, 3 seeds, one task.
- **FlyGM (arXiv:2602.17997):** the null was an UNWEIGHTED re-wiring; tested FINAL control performance (convergence); exact beats null (8.29 vs 13.55 angle error).
- **Nobody** has run both regimes on the same task with a weight-matched, degree-preserving null. That clean study is our first paper.

## 1. Task (canonical + extension)

**Canonical (primary):** the flyvis `MovingEdge` motion-detection / direction-decoding supervised task. A synthetic moving-edge stimulus is presented and the network must output the correct direction of motion. Standard flyvis benchmark: per-frame direction label, cross-entropy or top-1 error.

*Justification:*

- (a) Dhiman already validated the early-learning regime on it, so our convergence-regime result slots directly next to an existing claim.
- (b) It is a small, CPU-friendly recurrent model, a match for our hardware constraint (Section 9).
- (c) It isolates the learning question (weight update during training) from embodied control noise.

**Extension (secondary, NOT in the primary hypothesis: powered separately):** the FlyGM embodied-locomotion control task. Neuropil/weight-matched connectome → closed-loop policy → heading angle error. Run only if the primary is non-null, to test generalization of the result to a different regime (convergence-only, continuous control).

## 2. The two regimes

Both regimes use the same task, architecture, loss, optimizer, and (per Section 4) shared init.

**Regime A: early-learning (few steps).** Train for a fixed, small step count. Operationalize as `T_early = 200` optimizer steps (Adam, lr 1e-3 default), no early stopping, no warmup. Rationale: interrogates whether exact wiring accelerates the initial gradient-descent trajectory (the Dhiman finding). Metric snapshotted at T_early.

**Regime B: trained-to-convergence.** Train until a fixed stopping rule is met. Operationalize as best-val, not fixed epochs: monitor a held-out validation split; stop when the val metric has not improved for `patience = 500` steps, up to a hard cap of `max_steps = 50,000`. Report the best-val checkpoint's test metric (not the final-iteration metric, prevents overfit-final jitter from contaminating the comparison). Rationale: isolates the FlyGM "final control performance" claim under a weight-matched null.

Both regimes logged identically → per-regime early-loss curve AND convergence-final value.

## 3. The null construction (Maslov-Sneppen, weight-matched)

This is the methodological core, we fix BOTH prior flaws simultaneously.

**Procedure: degree- and weight-preserving edge swap (Maslov-Sneppen):**

1. Extract the directed adjacency matrix A of the fly connectome (synapse counts as weights → integer, positive weights).
2. For each directed edge `u→v` with weight `w`, treat it as `w` parallel unit edges (synapse-count multigraph). This makes the swap weight-aware.
3. Repeat the standard Maslov-Sneppen double-edge swap on the multigraph, preserving each node's directed in-degree and out-degree exactly:
   - Pick two edges `a→b` and `c→d` at random, `a≠c`, `b≠d`, all four nodes distinct (no self-loop / parallel-creation artifacts).
   - Rewire to `a→d` and `c→b`.
   - Accept ONLY if this does not create a self-loop `(x→x)` and does not collide with an existing parallel unit edge already present (to keep the simple-ish multiscale structure controlled). Otherwise reject and resample.
4. Run swaps until the graph is well-mixed: perform `= 10 × E` successful swaps (E = total directed edge count), i.e. the standard "edge-count multiple" mixing threshold.
5. Reaggregate the multigraph back to a weighted digraph: collapse parallel unit edges, sum weights per ordered pair.
6. RESULT: a weighted, directed graph with (a) identical per-node in-degree and out-degree (exact, in the unit-edge sense), (b) identical edge-weight distribution / total synapse count (weight-matching), but (c) randomized wiring (broken motifs, cell-type relationships, spatial adjacency).

**Sampling:** repeat the full swap procedure from the same seed connectome to draw an ensemble of nulls. Note: each null is a fresh rewiring (not a perturbation chain), so the ensemble members are statistically independent.

### How it differs from the two prior nulls (explicit: this is the selling point)

| Property | Dhiman 2026 | FlyGM | Ours |
|----------|-------------|-------|------|
| Directed degree preserved | yes (degree-preserving) | yes (degree-preserving) | yes |
| Edge WEIGHTS preserved | no | no (unweighted) | yes |
| Cell-type / motif / spatial matched | none claimed | none | none matched, but degree+weight held constant (isolates topology) |
| Tested regimes | early-learning | convergence | early + convergence |
| Same task both regimes | n/a | n/a | yes |

The clean claim: where FlyGM's exact-connectome advantage could be an artifact of the unweighted degradation (weaker signal), our weight-matched null removes that confound. Where Dhiman's null removed structural fidelity entirely, ours preserves the exact local statistics that Dhiman left uncontrolled, so a residue here directly indicts wiring/motif structure, not weight magnitude or degree.

## 4. Initialization control (shared from-scratch init)

The Dhiman Stages-A shared-init confound must be eliminated:

- A single global RNG seed `seed_init = 42` defines one shared initialization of all trainable parameters.
- EVERY model (real connectome AND every null-ensemble member) is initialized from THIS SAME init. No per-model init draws.
- "From-scratch": no pretraining, no transferred embeddings, all weights random-normal at the shared seed, then trained.
- This guarantees observed early- or convergence-differences are attributable to WIRING, never to init luck. (Shared init = matched start line; only the graph differs.)

## 5. Sample size / seeds / null ensemble

**Target: 5 seeds × 10 null-ensemble members.** Concretely:

- **Seeds:** 5 independent training runs (seeds 1-5). Each seed corresponds to a distinct shared init (Section 4: init drawn from that seed). All models within a seed share that init; models across seeds differ.
- **Null ensemble:** for each seed, draw **10 independent Maslov-Sneppen rewirings** (fresh swap procedure, Section 3.6). Per seed: 1 real + 10 nulls → 11 models.
- **Total model train-runs:** 5 seeds × 11 = **55** (5 real + 50 null), per regime. ×2 regimes = **110** training runs.

*Power note:* a null-ensemble of 10 gives a null distribution robust enough to compute CIs on the mean discrepancy. 5 seeds lets us report between-seed variance (not rely on a single lucky seed, Dhiman's n=1-equivalent risk). This directly answers Dhiman's n=5 / 3-seed critique.

Optional escalation (pre-registered as conditional): if the effect size is borderline at 5×10, expand to 10×20 (=220 runs), cheap, since CPU per run is minutes (Section 9).

## 6. Metrics (defined precisely)

All metrics recorded per run, both regimes, at a fixed log cadence.

1. **Early-loss curve.** Plot of train loss vs optimization step for steps 1..T_early (=200). Compare real vs null-ensemble error bars (mean ± 95% CI across the 10 nulls, mean of the 5 seeds). The Dhiman-adjacent signal: does the real wire converge faster in the first 200 steps?

2. **Convergence-final loss.** The best-val checkpoint test loss (Section 2, Regime B). One scalar per run. Primary convergence outcome.

3. **Activity scale.** Diagnostic that guards against "degenerate-solution" artifacts. Per layer, mean & max |hidden activation| over the validation set at the best checkpoint. A null that "wins" by collapsing to dead/saturated units would show anomalous activity scale, flagged, not silently scored. Mirrors Dhiman's activity-scale caveat.

Secondary (recorded, not primary): top-1 direction accuracy; final-step (non-best) test loss for robustness; weight-norm of the readout layer.

## 7. Pre-registration (fixed before running: kills p-hacking)

Fix the following in advance, in a timestamped pre-registration (e.g. OSF or an arXiv-registered DOI):

1. **Hypothesis:** exact connectome wiring yields a learning advantage over the weight+degree-matched null, measured as (a) lower early-loss at T_early and/or (b) lower convergence-final loss.
2. **Primary analyses:** exactly those in Section 6, with the permutation test in Section 8.
3. **Stopping rules:** Regime A = fixed 200 steps (no early stop). Regime B = best-val with patience 500, cap 50k. Both fixed now.
4. **Data splits:** fixed train/val/test split, seeded, written to the registry before any training.
5. **Hyperparameters:** Adam lr=1e-3, batch size, architecture width/depth: all pinned. No mid-study tuning.
6. **Null construction:** Section 3 verbatim (swap count, acceptance rule, ensemble size).
7. **Decision rule:** "exact beats null" iff the permutation-test p-value (Section 8) < 0.05 for BOTH regimes' primary metrics, stated as with-holds, so a partial (one-regime) result is honestly reported as such, not p-hacked into a single claim.
8. **Exclusion rule:** a degenerate run (from the activity-scale flag, Section 6.3) is excluded ONLY if documented and the flag rule was pre-registered; count of excluded runs is reported.

## 8. Statistical test

Decide "exact wiring beats null" via a permutation/randomization test against the null ensemble, NOT a naive t-test on pooled samples (this is Dhiman's dispersion weakness, fixed).

Per regime, per primary metric (early-loss-at-200, convergence-loss):

- Form the real-connectome mean metric `m_real` across the 5 seeds.
- Form the null distribution from the 50 null runs (5 seeds × 10 ensemble).
- **Permutation test:** under the null hypothesis "exact = structurally-equal statistics", real is exchangeable with null members. Permute group labels (real vs null) 10,000 times; compute the observed statistic (e.g. `m_real − mean(m_null)`); the two-sided p-value = the fraction of permutations where the permuted difference is at least as extreme.
- **Report dispersion + CIs (Dhiman's weakness):** report the 95% CI of the real mean and of the null mean, and the 95% CI of the difference (bootstrap over seeds for the real; over null-ensemble members for the null). Publish the full null distribution (histogram) in supplementaries, not just the p-value.
- Effect size: Cohen's d on the real-vs-null means; report alongside p.

Bonferroni-correct for the 2 primary tests (early + convergence), α=0.05 → per-test 0.025. Because both must pass on a single metric direction, this is a strong joint declaration.

## 9. Hardware: Mac CPU confirmation + runtime

- **Confirmed:** a small flyvis-style recurrent model (single-layer RNN / small recurrent core, ~10⁴–10⁵ params, input = synthetic visual field) trains on vanilla macOS CPU (Apple Silicon unified memory, M-series), no GPU needed at this scale.
- **Estimated runtime per run:** 2-5 minutes (early regime ~seconds; convergence regime to 50k steps on CPU a few minutes).
- **Total wall-clock estimate:** 110 runs (2 regimes) × ~4 min ≈ **~7-8 hours** serial on one Mac; trivially parallelizable across the 5 seeds (5 cores) → **~1.5-2 hours**. Extrapolates to the optional 220-run escalation in ~4h wall.
- If needed, the rig (GTX 1660, 6GB) could accelerate convergence runs, but is NOT required for the primary protocol. Note: the rig has no local Ollama but does plain torch CPU/GPU, keep primary runs on the Mac for reproducibility of the baseline.

## 10. Risk + outcome interpretation (both = a paper)

| Outcome | Meaning | Publication path |
|---------|---------|------------------|
| Exact wiring WINS (both regimes, weight-matched null, permutation-sig) | FlyGM's convergence result GENERALIZES to early-learning AND survives a weight-matched null, the first clean evidence precise wiring does confer a learning advantage. Kills Dhiman's "advantage collapses" as a null/method artifact. | Strong paper: "Weight-matched null reveals a genuine wiring-dependent learning advantage in a biologically-plausible connectome." |
| Exact wiring DOES NOT beat null (both regimes) | Dhiman's early-learning collapse is ROBUST, and FlyGM's exact-wins was an artifact of its UNWEIGHTED null. Weight-matched structural statistics suffice for learning on this task. | Equally valid paper: "Degree-and-weight-preserving rewiring abolishes the connectome advantage: exact wiring is unnecessary for learning." Definitive negative result + methodology contribution. |
| Mixed (one regime only) | Early-learning advantage but not convergence (or vice versa), task/regime-dependent. | Still publishable as a nuanced "regime-dependent" result, this is the finding NO prior study could see (neither ran both). |

**Project risk (highest):** the null being over-matched (so far it destroys signal that the real wire can't prove its worth), mitigated by the sizeable early-loss snapshot (Dhiman found early-learning where convergence might wash out) and the pre-registration, which makes either definitive outcome valuable.

**Which regimes matter most:** if forced to drop scope, Regime A (early-learning) carries the highest novelty: it is the precise claim Dhiman left flagged with an uncontrolled null.

## 11. Open scientific-design decisions (flagged for review)

Two decisions I couldn't fully pin down without weighing tradeoffs, resolve before pre-registering:

1. **Null matchedness depth.** I hold in/out-degree + edge weights exactly, but NOT cell-type, motif, or synaptic-partner statistics. The field tension (FlyGM vs Dhiman) is whether "fair" requires ALSO matching cell-type mixing (each null node constrained to connect to same-type partners as the real). This materially changes how strong a claim "exact beats null" makes (fuller-matched null = harder bar = stronger win). Pick either: (a) degree+weight only [current, cleanest isolation of wiring] or (b) degree+weight+cell-type bipartite blocks [stronger claim, more complex null]. Recommend (a) for the first paper, note (b) as a follow-up robustness variant.

2. **Primary metric precedence.** When early-learning and convergence DISAGREE (Section 10, mixed outcome), which metric is the declared primary for the headline claim? I pre-register both with a Bonferroni pair, but the framing title ("early-learning advantage" vs "convergence difference") needs a default chosen up front. Recommend pre-registering convergence-final loss as the headliner (FlyGM's regime, larger expected effect) with early-learning as the confirmatory secondary novelty.

*(Optional, lower priority: whether to publish as OSF pre-registration, arXiv preprint-only, or OSF+arXiv, affects the Section 7 timestamping step. Default: OSF for the time-stamped pre-registration + arXiv for the paper.)*