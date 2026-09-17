# Where the fly-brain field stands: what each competitor has made public vs. hidden, and what we can legally build on

A web research pass (September 14, 2026) across the fly-brain emulation space. By "public" I mean a working URL proves the artifact exists and is downloadable or licensed; by "hidden" I mean no working URL surfaced for that artifact, which is only absence-of-evidence on the public web. Funding figures, accuracy claims, and founding dates are taken from cited press and reports, not independently checked against filings, and I flag that line by line. One baseline worth keeping in mind: the connectome itself (FlyWire, 139k neurons / ~15M synapses, Zenodo 10.5281/zenodo.10676866) is the free public substrate everyone in this field builds on. It is the shared, open base layer.

## The shared open substrate everyone floats on

| Artifact | URL | License | Status |
|---|---|---|---|
| FlyWire adult Drosophila connectome (Zenodo) | https://doi.org/10.5281/zenodo.10676866 | Free/open (Zenodo) | Public |
| FlyWire v783 connectome, Nature 2024 (Dorkenwald et al.) | https://doi.org/10.1038/s41586-024-07558-y | Open-access data | Public |
| Shiu et al. LIF brain model code | https://github.com/philshiu/Drosophila_brain_model | MIT | public (263★) |
| NeuroMechFly v2 / FlyGym body sim | https://github.com/NeLy-EPFL/flygym | Apache-2.0 | public (320★) |
| NeuroMechFly v1 | https://github.com/NeLy-EPFL/NeuroMechFly | Apache-2.0 | public |
| flybody body model (Vaxenburg et al., Nature 2025) | https://github.com/TuragaLab/flybody | Apache-2.0 | public (858★) |
| snedea/flybrain interactive browser sim | https://github.com/snedea/flybrain | MIT | public (91★) |

The practical takeaway: the stack of connectome plus LIF brain model plus biomechanical fly body in MuJoCo is fully open and permissively licensed (MIT/Apache-2.0). Nothing in the open substrate blocks us.

## EON Systems (Andregg): the one real commercial competitor

A San Francisco startup, founder/CEO Michael Andregg (alongside Alex Wissner-Gross), funded with $3.5M seed. Their pitch is embodied whole-brain emulation of Drosophila: the Shiu et al. 2024 LIF model running on the NeuroMechFly v2 body in MuJoCo. Multiple independent technical writeups confirm it is real, not vaporware.

### Code public?
Partially. EON has a public GitHub org, `eonsystemspbc`, with three repos:

- `fly-brain`, the LIF whole-brain model, with Brian2/Brian2CUDA/PyTorch/NEST GPU/neuromorphic backends. License GPL-2.0. 722★. https://github.com/eonsystemspbc/fly-brain (created 2026-03-05, last pushed 2026-08-29; the data bundle is pinned to a Google Drive folder, https://drive.google.com/drive/folders/1jiSfb5lNfm9gwP0YyyRz5ATIrDpBAcjs, verified in the README).
- `pathintegrationBPU`, Jupyter, 2★, public, no license field. https://github.com/eonsystemspbc/pathintegrationBPU
- `NEURD-sandbox`, proofreading tooling, 1★, public. https://github.com/eonsystemspbc/NEURD-sandbox

What is not released: the actual embodied closed loop, the coupling of the brain model to NeuroMechFly v2, the trained controller weights, and the MuJoCo integration that produces the walk-forward / turn / groom behavior. The public `fly-brain` repo is a headless brain emulation and backend benchmark, not the embodied fly. The flybody/NeuroMechFly integration layer is proprietary.

### Data public?
- Connectome: yes, but it is the shared FlyWire public data, not an EON release of their own.
- EON's simulation outputs: the `fly-brain` repo ships a results bundle on Google Drive per the README, but the embodied dataset, what the fly actually does in the body, is not published.
- Trained emulation weights: hidden, no download found.

### Papers public?
No peer-reviewed EON paper. The public record is:

- Their demo and X thread (Andregg, "we've uploaded a fruit fly"): reported at https://eternalsearch.net/news/260428315 and https://mindplex.ai (magazine URL, https://magazine.mindplex.ai/post/so-has-a-fruit-fly-been-uploaded-or-not-yet).
- The underlying science is public: Shiu et al. Nature 2024, https://www.nature.com/articles/s41586-024-07763-9, which predicts motor output at roughly 95% accuracy in a headless LIF model. That 95% is Shiu's number; it has nothing to do with EON's embodied claim.
- A note on the "~95% motor accuracy" figure the briefs cite: that is the Shiu paper's motor-prediction number, and press coverage frequently conflates it with EON's embodied demo. EON has released no method paper proving its embodied figure.

### What they have not published
- No replication-grade writeup of the brain-to-body interface: how they select descending neurons, how they translate them into NeuroMechFly commands, or what "accuracy" the 95%/91% figures actually refer to. An independent analysis (greaterwrong.com/posts/ybwcxBRrsKavJB9Wz) makes the case that the behavior leans heavily on NeuroMechFly's pre-trained motor controllers, which are prebuilt rather than brain-trained; per the Shiu-model framing, the fly does not really fly, it flaps on the ground.
- No plasticity or learning. LIF has none, and EON's own posts and press acknowledge this.
- No released embodied control policy, so the interpretability claim that "5 motor neurons fired because 12,000 sensory neurons detected this pattern" (nexi.fund/whole-brain-emulation-eon-2026) is a claim, not an artifact.

This is exactly where honest independent work lands harder: a re-implementation that publishes a clear, replicable brain-to-body coupling plus a defined accuracy metric beats a video plus an X thread.

### License: safe for us to build on?
Differential. There are two distinct layers. Their shared-open architecture (Shiu model [MIT], NeuroMechFly v2 [Apache-2.0], flybody [Apache-2.0]) is fully safe to use. Their `fly-brain` repo is GPL-2.0: you may read and fork it, but any modified or derived distribution must also be GPL-2.0 under copyleft. Do not copy their code into a proprietary or closed core. Treat it as reference-only and re-implement rather than copy if we want a permissive license. The embodied coupling is closed-source and unpublished, so there is nothing to build on there at all; you would be reverse-engineering their demo, and no license grants anything in that direction.

## Memazing (Seung): the credible "not-yet" player

A startup founded by Princeton connectome pioneer Sebastian Seung, who co-leads FlyWire. It was announced around December 2025, with the goal of emulating the fly brain in software and a roadmap toward larger brains. Pre-product. Funding is not public. The founding is real, confirmed by press coverage and by Harvard's disclosure of Seung's financial interest.

- Code public? No. No GitHub org or repo exists for Memazing, as far as GitHub and public-web searches show.
- Data public? No. No model, weights, or dataset has been released under the Memazing name yet.
- Papers public? No standalone work. Seung's pre-startup connectome work is public (FlyWire, https://doi.org/10.1038/s41586-024-07558-y), but Memazing itself has released nothing.
- The gap: everything about the actual emulation is hidden, no code, no data, no paper, no demo. Pre-product. Seung is the most credible-scientist competitor, with deep connectomics credentials, but with zero public artifacts it is currently a team plus a thesis, not a stack.
- License: safe to build on by default. Nothing published means nothing to conflict with, and we have no dependency on them.

Sources: corememory.com/p/exclusive-connectome-pioneer-sebastian-seuing-memazing ; hms.harvard.edu news (Harvard Medical School, "Seung declares financial interest in Memazing"); ascii.co.uk news 2025-12-18 "Seung Launches Memazing"; X @mindthrust/2001397369598890091.

## FlyGM / FlyGNN (academic group): the open, citable baseline

A university group rather than a startup, with two related works, both presented at NeurIPS'25:

- Fly-connectomic Graph Model (FlyGM), arXiv:2602.17997 (an LREC-style journal paper).
- flyGNN, the NeurIPS 2025 conference version: https://neurips.cc/virtual/2025/131402 ; OpenReview: https://openreview.net/forum?id=WELrlKB4be (and KFmIRruzvL).

The work builds the Drosophila connectome as a graph neural network controller plus RL (IL to PPO) for a physics fly body, using the flybody (Vaxenburg) simulator.

- Code public? Ambiguous and weak. The paper is public (arXiv 2602.17997, HTML at https://arxiv.org/html/2602.17997) and spells out the full method, algorithm, IL+PPO pipeline, baselines, ablations, making it highly replicable from text alone. A repo `Lunamos/flygnn` exists under MIT (https://github.com/Lunamos/flygnn) at 2★ with a single push on 2025-09-30, created by an anonymous individual account rather than the paper authors' org. It is almost certainly an unaffiliated reproduction or echo, not canonical. No official `flygm` or `flygnn` code repo from the authors surfaced in GitHub search.
- Data public? Nothing released. No trained weights, no official checkpoint, no official repo data.
- Papers public? Yes, fully. arXiv:2602.17997 (v1 + v2), the NeurIPS 2025 page, and the OpenReview forum.
- The gap: code and weights are withheld, so the exact trained policies and the tuned node/edge composition are not out there, and reproducing their exact numbers requires re-running the described pipeline. They explicitly show the connectome as a GNN with RL beating random/MLP baselines, which is the key evidence that the wiring itself is a strong inductive bias. Independent replication is well served because the paper is method-complete, but the official-implementation gap is real.
- License: safe. The paper is open-access (arXiv/OpenReview), the MIT `Lunamos/flygnn` echo is permissive, and building a connectome-GNN is not encumbered by any patent or restriction I found. We can re-implement freely.

## Sandia Loihi 2 (neuromorphic): the hardware-frontier player

Sandia National Laboratories / Intel. They ran the full FlyWire connectome (140K neurons, 50M synapses) on 12 Intel Loihi 2 chips, claiming roughly 113× latency and ~6,600× energy wins versus conventional hardware. Paper: arXiv:2508.16792 (cs.DC, 22 Aug 2025).

- Code public? No. No public GitHub repo or repository for the Loihi 2 mapping/simulation was found.
- Data public? No. The input is the public FlyWire connectome, but Sandia's mapping config, constraints, and validation harness are not released.
- Papers public? Yes. arXiv:2508.16792 (abstract plus full PDF/HTML): https://arxiv.org/abs/2508.16792
- The gap: the paper is a performance and feasibility demonstration, not a control or behavior result. The Loihi 2 runs the LIF connectome fast and cheap, but the authors publish no embodied behavior and no reusable software; it is a benchmark on proprietary research hardware most groups cannot access. Nobody but Sandia has the silicon, and their win is speed and energy, not something our software stack needs to compete with, we run on commodity GPU/CPU, and the connectome is trivially within reach.
- License: safe. The paper is open-access with no published software or data to conflict with. The Loihi 2 configs are hardware-specific and irrelevant to a software path.

## Other real players and foundations observed

- FlyBrainLab (Lazar, Columbia), open-source platform for executable Drosophila circuit models. eLife 2021, https://elifesciences.org/articles/62362. Focus is circuit logic, not whole-body RL.
- NeuroMechFly / FlyGym v2 (EPFL, Ramdya), the dominant open body plus RL sim; Apache-2.0. A foundation layer.
- flybody (DeepMind + Janelia, Vaxenburg 2025, Nature 643:1312), Apache-2.0, 858★. A foundation layer.
- snedea/flybrain, MIT interactive browser sim (139K LIF in WebWorker/WebGL). Hobby-scale, MIT.
- Worm and C. elegans precedents (heyseth/worm-sim, snedea fork), open, MIT.
- Beyond EON and Memazing, no other funded commercial startups surfaced in this pass.

## Who is real and who has nothing released

| Player | Type | Code released | Data/weights | Paper | Real artifact? | How we respond |
|---|---|---|---|---|---|---|
| EON Systems | Startup (funded $3.5M) | Partial (GPL-2.0 headless brain only) | Embodied: no | No (only X/demo + Shiu underlying) | Embodied demo (video) but coupling closed | Out-publish the coupling + metric |
| Memazing (Seung) | Startup (pre-product) | None | None | None (only pre-startup connectomics) | Nothing | Act and release first, they have no artifact to defend |
| FlyGM/FlyGNN | Academic | Weak (unofficial MIT echo only) | No | arXiv + NeurIPS (method-complete) | Paper (citable) | Replicate; cite; extend the GNN |
| Sandia Loihi 2 | National-lab research | No | No | arXiv | Hardware benchmark | Ignore for software stack |
| Open substrate (Shiu, NeuroMechFly, flybody, FlyWire) | Open source | MIT/Apache-2.0 | Release | Release | Release | Build directly on it |

Reading the table: only EON has shipped a real embodied artifact, and its reusable core, the brain-to-body interface plus trained policies, is hidden. Memazing has the strongest scientific founding and the least to show. FlyGM is the only fully citable science but ships no official code or weights. Sandia is a hardware demo with no reusable software. The field's actual open stack is the substrate itself, which is Apache-2.0/MIT and unencumbered.

## Licensing recommendation: what we may build on

1. Safe to build on (permissive):
   - FlyWire connectome (Zenodo, free)
   - Shiu LIF model, MIT (philshiu/Drosophila_brain_model)
   - NeuroMechFly v1/v2 / FlyGym, Apache-2.0 (NeLy-EPFL)
   - flybody, Apache-2.0 (TuragaLab)
   - snedea/flybrain, MIT; Lunamos/flygnn, MIT
   - FlyGM/FlyGNN papers (open-access), citable, re-implementable
2. Reference only (copyleft; do not copy into our core):
   - EON `fly-brain`, GPL-2.0. Read it and understand it, but if we ship a derived or modified copy it must be GPL-2.0. Better to re-implement the ideas under our own permissive license.
3. Not available (closed or unpublished; cannot build on at all):
   - EON embodied coupling + trained policies (proprietary, hidden)
   - Memazing (nothing released)
   - Sandia Loihi 2 mapping/config (unreleased, hardware-specific)
4. Net: there is no legal blocker for an honest, permissively licensed independent implementation built directly on the MIT/Apache-2.0 open substrate. The defensible differentiator is releasing the brain-to-body coupling plus a defined accuracy metric, something neither EON (hidden) nor Memazing (nothing) nor FlyGM (weights hidden) makes public.

## Source index (working URLs, all retrieved 2026-09-14)

Connectome / substrate:
- https://doi.org/10.5281/zenodo.10676866 · https://doi.org/10.1038/s41586-024-07558-y
- https://github.com/philshiu/Drosophila_brain_model (MIT) · https://www.nature.com/articles/s41586-024-07763-9

EON:
- https://github.com/eonsystemspbc/fly-brain · https://github.com/eonsystemspbc/pathintegrationBPU · https://github.com/eonsystemspbc/NEURD-sandbox
- https://eternalsearch.net/news/260428315 · https://robohorizon.eu/en-us/magazine/2026/03/eon-uploaded-a-fruit-flys-brain-and-it-actually-works
- https://magazine.mindplex.ai/post/so-has-a-fruit-fly-been-uploaded-or-not-yet · https://greaterwrong.com/posts/ybwcxBRrsKavJB9Wz
- https://nexi.fund/whole-brain-emulation-eon-2026

Memazing:
- https://www.corememory.com/p/exclusive-connectome-pioneer-sebastian-seuing-memazing
- https://hms.harvard.edu/news/researchers-publish-first-complete-connectome-fruit-fly-brain-spinal-cord
- https://ascii.co.uk/news/article/news-20251218-6b517055/seung-launches-memazing-to-emulate-fruit-fly-brain-in-software
- https://x.com/mindthrust/status/2001397369598890091

FlyGM / FlyGNN:
- https://arxiv.org/abs/2602.17997 · https://arxiv.org/html/2602.17997 · https://github.com/Lunamos/flygnn (MIT)
- https://neurips.cc/virtual/2025/131402 · https://openreview.net/forum?id=WELrlKB4be

Sandia:
- https://arxiv.org/abs/2508.16792 · https://www.sandia.gov/news/publications/hpc-annual-reports/article/advancing-neuromorphic-computing-at-the-neural-exploration-and-research-lab/

Body sims / other:
- https://github.com/NeLy-EPFL/flygym (Apache-2.0) · https://github.com/TuragaLab/flybody (Apache-2.0)
- https://pypi.org/project/flygym-gymnasium · https://www.nature.com/articles/s41586-025-09029-4 (flybody Nature)
- https://elifesciences.org/articles/62362 (FlyBrainLab) · https://github.com/snedea/flybrain (MIT)

## Uncertainty and gaps in this analysis

- EON's exact embodied accuracy figure (91% vs 95%) is press-conflated; no primary EON method document was found.
- Memazing funding is not public; the founding date (~Dec 2025) comes from press, not filings.
- The official FlyGM/FlyGNN author repo could not be located; only an anonymous MIT echo was found, so this is being treated as "no official code release," but it should be re-checked on the authors' current pages.
- The Zenodo DOI for the connectome is quoted from the project's earlier data-access note and was not re-fetched here.
- This is a draft web pass, and lecture- or paper-indexed code (for instance, author-hosted mirrors) may exist beyond what GitHub search surfaced.