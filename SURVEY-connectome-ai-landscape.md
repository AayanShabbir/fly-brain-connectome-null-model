# Connectome-constrained AI and synthetic brain emulation: a five-domain research survey

A deep research survey run on September 14, 2026 across five parallel streams (academic, open-source, neuromorphic, industry, and scaling), plus a deep-research pass. All primary sources were fetched live, arXiv API, GitHub REST, web retrieval, and I graded each claim by maturity.

## Ground truth

- FlyWire whole adult brain, 139,255 neurons / ~54.5M synapses (Nature 2024, 10.1038/s41586-024-07558-y; companion 10.1038/s41586-024-07686-5). 100 TV EM volume.
- MaleCNS 166k neurons (v1.0 2026) · FANC (nerve cord) · BANC (full CNS). Zenodo 10.5281/zenodo.10676866.

## Academic papers & preprints

### Motif mining / subcircuits
- HiPerMotif (parallel subgraph isomorphism, connectomics-scale), arXiv:2507.04130. A preprint; the speed claims are unreplicated.
- Ring attractor connectome + motif enumeration (EB→PB→FB compass), eLife 10:e66039 (2021); E-PG heading bump, Science 10.1126/science.aal4835.
- Visual column / EMD, T4/T5, Nature 500:175 (10.1038/nature12450); hexagonal-lattice CNN from optic-lobe columns, arXiv:1806.04793.

### Connectome-grounded GNN / spiking SSM
- FlyGM / FlyGNN, whole FlyWire connectome as a recurrent MPNN, PPO-trained to control a physics fly (flight angular error 8.29° vs 125.36° for a random graph), arXiv:2602.17997 (+ NeurIPS 2025). Honest scope: wiring-constrained, no plasticity or memory.
- PHCSSM, Parallelized Hierarchical connectome spiking SSM; ALIF+STP+Dale+STDP, ~1-5k params, 6 UEA datasets, arXiv:2604.01295. Single-author preprint, with a caveat: the "connectome" here is an abstract hierarchy, not the FlyWire wiring.

### Mushroom body memory & forgetting
- MB associative logic (PPL-1/PAM DAN→KC→MBON coincidence), eLife 3:e04577 (2014); adult α-lobe eLife 6:e26975 (2017); larval eLife 6:e23454; reward octopamine→dopamine Nature 492:433.
- Catastrophic forgetting: sleep-replay joint repr (bioRxiv 10.1101/688622); sleep replay reduces forgetting incl SNN (Nat Comms 13:7742, 10.1038/s41467-022-34938-7); columnar local-rule SNNs (arXiv:2506.17169). I could not find a primary paper behind "generative replay eliminating forgetting in SNNs", that framing is hype.

## Open-source code, datasets & emulation engines

- NeLy-EPFL/flygym = NeuroMechFly v2 (MuJoCo, `mujoco>=3.9`, Apache-2.0, 315★), the flagship runnable embodied fly. v1 is archived.
- MuJoCo bodies: erojasoficial-byte/fly-brain (138k-neuron, MIT), seven-monarchs/NeuroFly, abgnydn/webgpu-fly (browser).
- Connectome data/code: murthylab/codex (codex.flywire.ai source, Apache-2.0), seung-lab/FlyConnectome, CAVEconnectome/, htem/BANC-project, flyconnectome/fancr, navis-org/navis + fafbseg-py, TuragaLab/flyvis (MIT, 155★).
- The "flywire-ai" GitHub org does not exist (404). Index: cobanov/awesome-fly (CC0, 243★). MaleCNS R: natverse/malecns (GPL-3.0, 290★).
- Browser: CATMAID (GPL, 201★), neuPrint (BSD-3), Codex; spiking brains in browser snedea/flybrain (MIT, 88★).
- Caveat: no repo does whole-brain emulation. flygym is a biomechanical body; the brains run model-assumed LIF over the static FlyWire v783 graph.

## Neuromorphic hardware & edge AI

- EventProp (exact grads, recurrent SNNs), Sci Rep 11:12829 (10.1038/s41598-021-91786-z); GeNN impl arXiv:2212.01232 + 2503.04341. mlGeNN learnable delays up to 26× faster, <½ memory (Nat Comms 10.1038/s41467-025-65394-8).
- Surrogate gradient: SuperSpike (1705.11146), SLAYER (99.4% MNIST, 1803.08930), Norse (819★).
- Loihi 2 full pipeline: EventProp + mlGeNN → NetX → NxKernel; delays ≤62 steps; SHD 67.9→88.0% on Loihi (arXiv:2510.13757); Lava (740★) + lava-dl.
- Measured vs GPU: CLP-SNN continuous learning 0.33 ms / 0.05 mJ = 113× lower latency, 6,600× lower energy vs a Jetson-class GPU (37.3 ms/333 mJ) arXiv:2511.01553; LCA sparse coding "orders of magnitude" vs A100/Jetson/M1 (2307.13762); full 140k-neuron connectome on 12 Loihi 2 chips, 3-350× faster than Brian 2 CPU (2508.16792, and note this compares against CPU, not GPU).
- Canonical energy: Loihi KWS 270 µJ/inf incl host → 37 µJ no-host (Yan 2021) vs 7.1 µJ SpiNNaker2.
- Honesty note: these energy wins are against edge GPUs at batch size 1; a GPU amortizes roughly 20×. The "EEDM"/"CAPE" acronyms do not appear in the primary sources (what I verified was 62-step delays plus dendritic compartments).

## Startups, commercial & labs

- Memazing (Seung): real, founded Dec 2025, fly-brain-in-silico; launch page only, funding not public. A funded startup, pre-product.
- Eon Systems PBC (eon.systems, Andregg): $3.5M seed led by Protocol Labs (+ Larry Page family office, Dec 2025); built on Shiu et al. Nature 2024 fly-brain model (10.1038/s41586-024-07763-9, ~95% motor-behavior accuracy); the "embodied fly" of Mar 2026 is an honest integration of published components. A funded startup working on real biology.
- Labs (real substance): HHMI Janelia FlyEM (EM pipeline), Princeton Seung/Murthy (FlyWire+Codex), Google Research Connectomics (tooling + MoGen ICLR 2026; no consumer AI runs on connectomes), NIH BRAIN (~$3B, BRAIN CONNECTS), Allen/Baylor/Princeton MICrONS, EPFL Blue Brain → Open Brain Institute (concluded Dec 2024; a statistical sim, not connectome emulation).
- Neighbors (NOT connectome-emulation): Numenta (principles), Cortical Labs (wetware). Connectomes.net is one-person, unfunded vaporware.

## Scaling roadmaps & insect→mammal transfer

- MICrONS mouse cortex: ~1 mm³ V1, >200k cells / 120k neurons / ~523M synapses, 75k+ with calcium imaging (Nat 2025, 10.1038/s41586-025-08790-w; microns-explorer.org/cortical-mm3; ~1.6 PB). Still mid-proofreading.
- Transfers I'm confident about: sparsity/wiring economy (Nature 2024, 10.1038/s41586-024-07939-3), sparse-expansion codes (MB≈cerebellum, eLife 10.7554/eLife.62576), rich-club as principle (10.1038/s41586-024-07968-y), brain/VNC hierarchy ≈ brain/spinal.
- The critical negative control: Dhiman 2026 (arXiv:2604.04033), connectome "learning advantages" vanish under degree-preserving nulls and shared init. Exact wiring sets routing; coarse stats set the regime (arXiv:2606.17745).
- Hybrid: Spike-driven Transformer V2 (2404.03663), motif→NAS (Johnson/JHU, 2305.17300), HexLattice init (1806.04793); fMRI-connectome Transformers are data fusion rather than architecture (limits: 2503.15902).
- Embodied connectome agent: a lateralized MB circuit doing real outdoor visual homing on a Raspberry Pi 4 at 8 Hz, under 9 kB (arXiv:2507.09725), the only verified connectome-constrained decision agent. Whole-brain emulation for autonomy remains speculative.

## Bottom line

1. The graph substrate is ready and public: FlyWire 139k / MICrONS 120k; tools (HiPerMotif, FlyGM, CAVEclient, flygym) run today.
2. Neuromorphic is the strongest hardware story: the connectome fits on 12 Loihi 2 chips, and the measured wins are real in the sparse/event/batch-1 regime, but against an edge GPU, not a datacenter.
3. There are only 2 real startups (Memazing and Eon); reproducible substance lives in the labs.
4. The honest brake: the connectome advantage in learning is largely an initialization / null-model artifact (arXiv:2604.04033). Exact wiring ≠ dynamics, and fly(200k)→mouse(70M)→human(80B) is not a numbers game. Transfer the principles, not the parameters.
5. Vaporware to ignore: "generative replay eliminates forgetting in SNNs", the "EEDM/CAPE" silicon specs, the "flywire-ai" org, "Connectomes.net", and "NeuroMechFly.jl". "Digital consciousness" is press framing.

## Cross-links

- [[FlyWire Connectome, Capabilities & Applications]] 
- [[ROADMAP]], this survey feeds Phase 1 total-knowledge capture (constraints before brute-force)