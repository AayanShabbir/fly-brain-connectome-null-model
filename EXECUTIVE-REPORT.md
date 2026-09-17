# Fly brain connectome: executive summary

This synthesizes the deep-research corpus. Primary evidence is documented in `report.md`, `report-deep.md`, and `sources.md`.

## What the dataset is

- FlyWire is the first complete synaptic wiring diagram of an adult *Drosophila melanogaster* brain.
- The body of the data is 139,255 proofread neurons. Applying a threshold of at least 5 synapses per connection gives a high-confidence graph of 127,978 neurons and 2,613,129 directed weighted edges (the canonical connectome graph). The raw synapse point-table runs to roughly 130M rows.
- The 2026 extension covers the full CNS (brain plus ventral nerve cord, BANC v888 / Nature+Google Cell 2026): 166k+ neurons and about 125M synaptic connections, the largest brain map by neuron count to date. This one is a male fly.
- Download from Zenodo (`10.5281/zenodo.10676866`) as Feather + npy (10.6 GB). Codex bulk CSV is available via `/api/download_resource`. Live queries go through CAVE/CloudVolume with a token, scoped to a region.
- Locally, `proofread_connections_783.feather` plus `proofread_root_ids_783.npy` load into networkx at roughly 0.5-1.5 GB of RAM on a laptop. Avoid a full load of the 9.5 GB synapse table; memory-map it instead.
- Codex deliberately offers no general live-query bulk API, so static downloads are the practical route.

## Measured structural architecture

| Property | Value | Why it matters |
|---|---|---|
| Connection probability | 0.000161 (about 1 in 6,200 pairs) | Sparse; never plan a dense-mesh router |
| Avg connection strength | 12.6 synapses | Weights carry real signal |
| Single SCC / WCC | 93.3% / 98.8% of neurons | Whole graph reachable cheaply |
| Avg directed path | 4.42 hops (max 13) | A ~5-hop hub net reaches everything |
| Small-worldness Sᵈ | 141 (vs 3.21 worm, 98.1 internet) | Cheap global communication despite sparsity |
| Rich club | cutoff degree 37 → 40,218 neurons ≈ 30%; internal connection probability 5.4× the overall rate | Concentrate router compute in a ~30% core |
| Reciprocity | 0.138; about 2 in 3 neurons sit in at least one reciprocal pair | Recurrence is a feature, not a bug |
| Motifs | feedforward under-represented, recurrent over-represented | Allow feedback edges |
| Hubs | broadcasters (out ≥ 5× in, about 75% cholinergic) vs integrators (in ≥ 5× out, dopaminergic) | Two hub roles → two router types |
| Hub topology | no command neurons (unlike C. elegans); distributed rich club | Robust, alternative paths everywhere |
| Communities | 78 anatomically defined neuropils (the paper does not run unsupervised modularity) | Spatial/regional routing seams |

## What people build on it

- Embodied simulation: `erojasoficial-byte/fly-brain` runs 138,639 LIF neurons and 15M synapses on v783 inside a NeuroMechFly v2 + MuJoCo body (vision, olfaction, gustation, flight). It needs a CUDA GPU with at least 6 GB VRAM; the author used an RTX 5090 laptop. Identical connectomes diverge once embodied Hebbian plasticity is added (81% vs 47% escape rates). Local execution on consumer hardware (GTX 1660 6GB) meets the minimum specification for embodied simulation, whereas CPU-only hardware is restricted to topological and feedforward benchmarks.
- Neuromorphic: the whole connectome runs on 12 Intel Loihi 2 chips, over 100× faster than numerical simulation, with the advantage growing as sparsity increases (Sandia).
- Graph-DL/RL: a fly-connectomic graph model acts as a MuJoCo controller with better sample efficiency; connectome-constrained networks predict visual-system activity (nature 634:1132).
- The original LIF model is Shiu et al. 2024 (Nature 634:210).

## Implications for network architecture

The measured properties suggest concrete design patterns for routing-heavy networks, stated here as hypotheses the null-model experiment is built to test.

- Hub-spoke routing: rather than a dense mesh, concentrate throughput in a small rich club (about 30% of entities acting as routers) with the remaining ~70% attached as spokes through hubs. The fly shows a ~5-hop path reaches everything.
- Sparse, event-driven traffic: activate routes only when messages fire rather than polling or keeping every connection alive; a small always-hot core plus a large cold population that wakes on demand. The measured starting allocation is ~30% / ~70%.

Honest limits: a typical knowledge graph is far smaller and less sparse than the fly, so the transfer is of pattern (sparse hubs, feedback, event-driven traffic) rather than the literal 0.016% density. And a connectome is not enough on its own (Scheffer & Meinertzhagen): wiring is a prior, not function, and the fly simulations only worked once Hebbian plasticity and embodiment were added.

## Next-step candidates

1. Pull the actual graph (`proofread_connections_783.feather`, roughly 1-4 GB), compute rich-club plus hub/community stats on the real data, and produce a concrete analysis of which routing changes the topology actually supports.
2. Sparse routing pilot: evaluate an event-driven hub-spoke topology against a continuously-polled alternative.
3. Hardware feasibility probe for embodied simulation (GTX 1660 6GB baseline) prior to scaling experimental runs.
