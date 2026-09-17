# Fly-brain connectome project: full roadmap

North star: total knowledge capture, then constraint-guided brute-force reconstruction of the Drosophila connectome. The goal is to learn how the fly brain's wiring works well enough to rebuild and predict it, not to claim we fully understand it.

Two ground rules worth stating up front:

- Order is non-negotiable: all research and knowledge capture comes first. Brute-force only runs once every fact is gathered, cited, and encoded as constraints. No rig compute before Phase 3 is fed.
- Real numbers or nothing. Every claim must withstand rigorous peer scrutiny, strictly avoiding ungrounded speculation.

## Master principle: the "walls of the maze"

The connectome is a map we already hold, not a live fly we can probe directly. We can't experiment on the biology, so the strategy is:

1. Capture everything that is known (the research-first phase, which is also the guaranteed-value phase)
2. Encode what is known as constraints, the walls of the maze
3. Brute-force only inside those walls, searching the plausible space rather than all brains

Raw brute-force over every possible network is effectively impossible. Constraint-guided brute-force over networks that satisfy the fly's measured properties is tractable. That is why research leads: the walls are what make the search cheap.

## Phase 0: Foundation

Done. Project scaffolding and the first research pass are complete: the corpus briefs and concept notes are written, CONSTRAINTS is drafted, and the experiments/ folder is standing. The first research operation (data access, structural architecture, capabilities, plus deep research) is complete.

## Phase 1: Total knowledge capture

Goal: assemble the complete fly-brain corpus, every fact cited and every number sourced. Research runs as dedicated study sessions, and results land in structured notes in this repository.

Corpus to capture:

1. The Nature 2024 bundle of four papers: the neuronal wiring diagram of an adult brain (Dorkenwald et al.), the network statistics of the whole-brain connectome (Lin, Yang, Murthy, Seung), the effectome (causal perturbation) paper, and the Shiu et al. LIF behavior model
2. The 2026 full-CNS release: BANC v888, roughly 166k neurons, brain plus ventral nerve cord
3. Neuromorphic: Sandia Loihi 2, 140k neurons / 50M synapses on 12 chips, reported more than 100x faster
4. Sims: erojasoficial-byte/fly-brain embodied LIF; eonsystemspbc/fly-brain multi-backend
5. Behavioral literature: escape (Giant Fiber, ~10ms), feeding, grooming, navigation
6. Network tooling: rich-club algorithms, hub detection (integrator/broadcaster), community detection

Phase 1 exit criteria:

- Every CONSTRAINTS.md value (C1 through C10) traced to its primary source with a working URL
- No number in the corpus that lacks a citation; anything unknown is flagged, not guessed
- Every cited fact in the corpus links back to a named source with a working URL

## Phase 2: Encode known facts as constraints

Goal: turn the research into a formal, machine-readable spec the generator must satisfy.

- Cross-check and finalize every constraint value against its cited source
- Convert CONSTRAINTS.md to constraints.json (the machine-readable walls)
- Define the search space formally: node count, density, rich-club, reciprocity, and the rest
- Add behavioral constraints (escape latency and so on) once the sims validate

Phase 2 exit: a spec strict enough that a generated network knows it is a fly.

## Phase 3: Connectome load and topology verification (CPU-only, cheap)

Goal: prove we can load the real data and reproduce the published numbers before any ML. This runs on the Mac's free CPU, not the rig.

- Download the real Zenodo graph (10.6GB), memory-map it, about 1.5GB in networkx
- Reproduce density, degree distribution, reciprocity, small-world S, and the rich-club cut-off
- Gate: if our tools cannot reproduce the published numbers, fix the tooling first. No ML is built on numbers we have not verified.

## Phase 4: Brute-force constraint-guided search (the rig, the cost)

Goal: generate candidate sparse-rule networks that satisfy the walls and keep the ones that match the fly's real behavior. This is the first rig spend and it is gated on Phases 1 through 3 all passing.

- Build the generator: emit candidate nets constrained by constraints.json
- Fitness: distance to the real topology (degree distribution, rich-club, reciprocity, small-world)
- Test survivors on tasks: does a fly-constrained net train better or resist damage more?
- First deliverable: "we searched N candidates, and these M actually reconstruct the fly's connectivity," backed by real rig logs

Honest rig reality: the GTX 1660 with 6GB is at the edge of what is workable. SNN training will be slow but usable; brain-scale GNN is feasible precisely because the fly is 0.016% dense, and sparsity is speed. If a run is impractical we ticket it and pivot rather than burn rig-hours.

Null-model experiment, deliverable #1, runs before Phases 3 and 4 on the Mac CPU for $0 (from the 2026-09-14 verdict). The field's open question is whether exact wiring gives a learning advantage at all. Dhiman tested early-learning and FlyGM tested convergence, and no one has run both on the same task against a weight-matched degree-preserving null. That clean study is our first paper and it costs nothing to run. The design is fixed from the start:

- Same task, both regimes (early-learning and convergence)
- Degree-preserving rewired null (Maslov-Sneppen) that preserves directed in/out-degree and weights, since FlyGM's null was unweighted and that is the gap we fix, plus shared from-scratch initialization
- The protocol and analysis are pre-registered before execution, eliminating researcher degrees of freedom and p-hacking

Either outcome is a publication. If exact wiring wins, the connectome-AI thesis is validated. If not, we are the ones who settled it rigorously. This is our cheapest competitive opening.

## Phase 5: Cross-connectome learning (parallel to Phases 3 and 4)

- C. elegans (302 neurons, the only fully-mapped connectome): why the fly's rules generalize
- Mouse cortex and human brain structural networks: public data, methods borrow
- Answer why evolution chose these walls, and what those walls are

## Phase 6: Writeup and deliverable

- Real numbers only; honest methodology
- Thesis-ready framing: "total knowledge capture + constraint-guided brute-force reconstruction of the Drosophila connectome"
- Public framing that survives an interviewer's hardest question

## Cost and resource guardrails

| Item | Lane | Cost posture |
|:---|:---|:---|
| Phase 1 research | deep-research sessions | cheap, $0.20-ish/day ceiling |
| Phase 3 verify | Mac CPU | $0 (free compute) |
| Phase 4 brute-force | rig GPU | Real, gated and budget-capped |
| All writing | structured notes | durable, version-controlled |

Compute policy: prioritize local verification and efficient batch research. High-tier model reasoning is reserved for complex structural analysis, with token usage monitored against budget.

## Open questions

1. Exactly where does the queued research session write its output? Ingestion will line up with that path once the file lands.
2. Phase 4 scope: full 139k-neuron graph or a reduced proxy first? My lean is a reduced proxy first to validate the pipeline cheaply, then the full graph.
3. Timeline: is this a slow weekly side-project (small batches, always durable) or bursts? My lean is weekly, a side project that gets touched each week.

A few decisions are already fixed: research-first is non-negotiable and brute-force is the payoff phase rather than the starting point. Every deliverable is written to this repository before it counts as done. And I will not invent a number or claim a run succeeded without the logs; unverified means not done.

Phase 0 is complete. Phase 1 is next, and the first research session's output gets ingested the moment it is available, cited, one logical unit at a time.