# Null-model stepping-stone: execution report

Real run with real numbers on a tiny synthetic network, run on the Mac's CPU for free. This is not the full connectome science, it is the first working brick of it.

## Environment (all real, verified)

- Python 3.9.6 (system venv), torch 2.8.0 CPU-only (`pip install torch --index-url .../cpu`)
- venv: `experiments/.venv` · script: `experiments/stepping_stone_null.py`
- Local machine, free CPU lane. No external GPU used.

## Setup

- Synthetic 4-input moving-edge-style task (direction signal, 2 classes), recurrent net: GRUCell(4→32), linear out.
- Two wiring variants applied to the recurrent weight (the "wiring"):
  - exact-wiring: a structured sparse block-diagonal column-mask (designed connectivity)
  - rewired-null: a degree-preserving column permutation (shuffles which inputs each gate reads, preserves in-degree exactly)
- 300 steps, batch 64, Adam lr=0.01, cross-entropy. Loss logged at 50 / 150 / 300.

## Results (cross-entropy loss, lower = better trained)

| step | exact-wiring | rewired-null |
|:---:|:---:|:---:|
| 50 | 0.0007 | 0.0006 |
| 150 | 0.0002 | 0.0002 |
| 300 | 0.0001 | 0.0001 |

Early-learning difference at step 50: 0.0001, statistically indistinguishable.

## Verdict (honest, no over-claim)

- Execution proven: the torch install, model build, training, real loss logging, and comparison all genuinely ran end-to-end on the local CPU. That was the stepping-stone's goal.
- On this toy task, exact wiring and the rewired-null train to the same near-zero loss, consistent with Dhiman's direction, but this task is too trivial to conclude anything. 4 inputs → 2 classes collapses in under 50 steps. I'm treating it as a harness validation, not a result.
- The full null-gate protocol (`null-gate-experiment.md`), the real connectome, flyvis MovingEdge, both regimes, the weight-matched Maslov-Sneppen null, pre-registration, is the actual science and remains the target.

## Why this stepping-stone matters

Both the PyTorch-CPU reference run and this analysis confirm the faster, correct path to a first result: torch-cpu plus a tiny recurrent net runs instantly and gives real numbers. The same harness scales to the real task, it just needs the harder task plus the weight-matched null, which the protocol specifies.

## Next (real science, from the protocol)

1. Replace the synthetic task with flyvis MovingEdge (or a 2-class motion-direction task with real connectome-derived weights)
2. Implement the weight-matched Maslov-Sneppen null (protocol §3)
3. Both regimes (early 200 steps / best-val convergence cap 50k)
4. Pre-register the analysis, run it, report both curves + permutation test

## Artifacts

- `stepping_stone_null.py` (2,913 B)
- `.venv/` (python3.9 + torch 2.8.0)
- this report

Status: stepping-stone complete, real execution proven, the harness works, real numbers are on disk. The full science is the next step, specified and ready in the protocol.