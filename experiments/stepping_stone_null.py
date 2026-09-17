"""
Stepping-stone null experiment - tiny recurrent net, synthetic moving-edge task.
Compares two wiring variants: an "exact wiring" pattern vs a degree-preserving rewired null.
Real numbers only. Throwaway proof-of-execution, NOT the full connectome science.
"""
import math, random
import torch
import torch.nn as nn

torch.manual_seed(0)
random.seed(0)
DEV = "cpu"

N_IN, N_HID, N_OUT = 4, 32, 2
STEPS = 300
BATCH = 64
LR = 0.01

def make_task_batch(batch):
    """Synthetic moving-edge: a direction signal in 4 channels, label = direction."""
    xs, ys = [], []
    for _ in range(batch):
        d = random.randint(0, 1)
        x = torch.zeros(N_IN)
        x[d] = 1.0
        x[d + 2] = 0.8  # moving-edge-ish trailing signal
        xs.append(x)
        ys.append(d)
    return torch.stack(xs), torch.tensor(ys, dtype=torch.long)

class TinyRNet(nn.Module):
    def __init__(self, exact=True):
        super().__init__()
        self.inp = nn.Linear(N_IN, N_HID)
        self.rnn = nn.GRUCell(N_IN, N_HID)
        self.out = nn.Linear(N_HID, N_OUT)
        # Two wiring variants via the RECURRENT weight weight_hh (shape 3*HID x HID).
        # weight_hh is the "wiring": row = gate-unit output, col = which hidden unit it reads.
        with torch.no_grad():
            Wh = self.rnn.weight_hh.clone()
            if exact:
                # Structured sparse: keep only a designed block-diagonal of column-reads,
                # zero out the rest (structured connectivity, like a designed circuit)
                colmask = torch.zeros(N_HID)
                block = N_HID // 2
                for u in range(N_HID):
                    # unit u reads the two units in its group (block-diagonal structure)
                    if u < block:
                        colmask[0:block] = 1.0
                    else:
                        colmask[block:2*block] = 0.6
                Wh = Wh * colmask.unsqueeze(0).expand(3*N_HID, N_HID)
            else:
                # Degree-preserving rewired null: permute columns. A column permutation
                # preserves every unit's in-degree exactly while shuffling WHICH inputs
                # each gate reads - the canonical wiring-null for a fixed-architecture net.
                perm = torch.randperm(N_HID)
                Wh = Wh[:, perm]
            self.rnn.weight_hh.data = Wh

    def forward(self, x):
        h = torch.zeros(x.size(0), N_HID)
        h = self.rnn(x, h)
        return self.out(h)

def run(tag, exact):
    net = TinyRNet(exact=exact)
    opt = torch.optim.Adam(net.parameters(), lr=LR)
    lossf = nn.CrossEntropyLoss()
    log = {}
    for s in range(1, STEPS + 1):
        x, y = make_task_batch(BATCH)
        logits = net(x)
        loss = lossf(logits, y)
        opt.zero_grad(); loss.backward(); opt.step()
        if s in (50, 150, 300):
            log[s] = round(float(loss.item()), 4)
    return log

if __name__ == "__main__":
    print("torch:", torch.__version__, "| device:", DEV)
    exact = run("exact", True)
    rewire = run("rewired-null", False)
    print("\nWIRING-VARIANT COMPARISON (cross-entropy loss, lower = better trained)")
    print(f"{'step':>6} {'exact-wiring':>14} {'rewired-null':>14}")
    for s in (50, 150, 300):
        print(f"{s:>6} {exact[s]:>14} {rewire[s]:>14}")
    print("\nVERDICT(stepping-stone): early-learning diff =",
          round(exact[50] - rewire[50], 4), "at step 50")
    print("Note: tiny synthetic proof-of-execution only; not the full connectome science.")