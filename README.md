# Fly brain connectome: null model benchmark

Does the exact wiring of a fruit-fly brain confer a genuine learning advantage in artificial networks, or does that advantage disappear under rigorous null controls?

This is a research project on the **FlyWire Drosophila connectome**, the complete map of the
139,000 neurons and 15 million connections in an adult fruit fly's brain. It is the largest
complete brain map reconstructed to date and is open-access.

## Why build this

The field is divided on a foundational question. Two 2026 papers point in opposite directions.
One (Dhiman, arXiv:2604.04033) finds that the connectome's apparent sample-efficiency advantage disappears once
compared against degree-preserving randomized wiring. Another (FlyGM/FlyGNN, arXiv:2602.17997) finds that
exact wiring yields superior task performance at convergence.

Nobody has run the test both groups imply: the same task, evaluated during early-learning *and*
after full training, against a rigorous null that preserves both degree distribution and synaptic weights.
That is the experiment this repository establishes. Either outcome is publishable, which is the value of
framing a clean empirical benchmark rather than relying on speculation.

## Repository contents

The repository contains the complete research pipeline: measured graph properties of the fly's
wiring, formal constraint specifications, project roadmap, comprehensive research briefs (70+ cited sources),
and runnable benchmarks.

The `experiments/` directory houses the core benchmark: a pre-registration-ready
protocol and a lightweight PyTorch CPU benchmark comparing exact versus rewired connectivity
with verified numerical outputs.

## Quick start

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
python experiments/stepping_stone_null.py
```

Runs on a standard CPU in seconds.

## Scope and methodology

The initial benchmark runs locally on standard CPU hardware without requiring GPU compute.
All claims are grounded strictly in logged empirical data. This project investigates network
topology and learning dynamics, without speculative claims regarding biological cognition.

## Author

Aayan Shabbir, Biochemistry major (pre-med track) at Binghamton University, self-taught builder.

MIT licensed.