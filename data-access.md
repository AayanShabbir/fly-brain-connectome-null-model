# FlyWire data access: formats, schemas, and local load paths

Scope: exactly what the dataset is, the file formats, the schemas, the official access tools, and one concrete local-load path (format, node/edge schema, storage and memory footprint).

Working assumptions: brain-only release = FAFB (full adult female brain, v783); full-CNS = BANC (Brain And Nerve Cord); the "June 2026 update" is the full-CNS connectome paper (Nature 2026, Bates/Phelps/... Murthy/Jefferis). One synapse-theory note up front: the cell-type companion paper describes the graph as 139,255 nodes and ~15.1M weighted edges, which is the canonical graph figure; the Zenodo synapse point-table is roughly 130M raw rows.

## TL;DR for a load engineer

- The graph you want to load is the weighted directed edge list (`proofread_connections_783.feather`, one row per neuron-pair per neuropil) plus the neuron id array (`proofread_root_ids_783.npy`). That is ~15M edges and ~140K nodes, and it loads in RAM on a laptop.
- The raw synapse-level table (`flywire_synapses_783.feather`, ~130M rows) is 9.5 GB on disk and expands to tens of GB in RAM. Do not load it if you only need the graph; reach for it only when you need per-synapse coordinates or transmitters.
- Gzip CSV mirrors of the same products are served by Codex's static download API (`/api/download_resource?data_product=...&dataset=...&api_token=...`).
- Volumetric and segmentation data (EM chunks) are not gracefully downloadable. They live in a live CloudVolume proprietary store and are pulled for regions, never in bulk.
- Formats: Apache Arrow (Feather) and NumPy .npy for the graph; gzipped CSV from Codex; CloudVolume/CAVE for volumetric and live queries.

## Graph nodes and edges

- Nodes = proofread neurons (root IDs). FAF v783: 139,255 proofread neurons (Dorkenwald et al. 2024; Nature s41586-024-07558-y).
- Edges = directed, weighted synapses. Canonical graph figure: ~15.1M weighted edges (Schlegel et al. companion paper, s41586-024-07686-5).
- Total raw detected chemical synapses ~130M; of these, ~80M pass thresholds and are associated with proofread pairs (paper Methods). The released `flywire_synapses_783.feather` holds all synapses passing the thresholds (~130M rows).
- Neurons are intrinsic/central vs optic lobes; the resource adds cell-class/type (8,453 types), hemilineages, nerves, and neurotransmitter predictions (see Schlegel et al.).

## File formats & schemas (Zenodo doi:10.5281/zenodo.10676866, v783.0, total 10.6 GB)

1. `flywire_synapses_783.feather`, ~130M-row synapse table (9.5 GB). Schema (per Zenodo):
   - `id` synapse id
   - `pre_pt_root_id` / `post_pt_root_id`, presynaptic/postsynaptic neuron ids
   - `connection_score` (Buhmann et al. 2021), `cleft_score` (Heinrich et al. 2018; threshold 50)
   - transmitter probabilities: `gaba, ach, glut, oct, ser, da`
   - spatial: `pre_pt_position_{x,y,z}`, `post_pt_position_{x,y,z}` (nm)
2. `proofread_connections_783.feather`, the neuron-pair-per-neuropil edge list (the graph). One row per (pre,post,neuropil) if there is >= 1 synapse. Columns: pre_pt_root_id, post_pt_root_id, neuropil, syn_count, plus per-synapse avg transmitter probabilities.
3. `per_neuron_neuropil_count_pre_783.feather` / `_post_783.feather`, summarized postsynapse counts per neuron per neuropil (233.8 MB / 16.9 MB).
4. `proofread_connections_783.npy`, padded NumPy array of all proofread root ids (the node list).

## Official retrieval route

| Route | Tool/library | Use case | Auth |
|---|---|---|---|
| Zenodo doi 10.5281/zenodo.10676866 | any HTTP | Static bulk download of the connectivity graphs (Feather+npy) | none |
| Codex data-download API | `https://codex.flywire.ai/api/download_resource?data_product=...&dataset=...&api_token=...` | Gzipped CSV mirrors; products such as `consolidated_cell_types`, `connections_princeton` | free Codex API token |
| CloudVolume (`cloudvolume` py) + CAVE | python `cloudvolume`, `caveclient` | Volumetric segmentation + live synapse/annotation queries in source project | CAVE/FlyWire token required for live mapping |
| 3D/browser | Codex UI (codex.flywire.ai) | interactive, non-bulk | Google sign-in |
| Runinterop toolchains | `fafbseg` (py) & `flywire.cloudvolume` (R) | programmatic access on top of CAVE | token |

Codex's FAQ is explicit: "Codex intentionally does not provide a general programmatic live-query API for bulk access; use the static downloads." For non-FlyWire datasets (MANC/MCNS/MAOL) you use the Janelia homepages, not Codex bulk.

## A concrete local-load path

Recommended approach (no distinct VM needed; it works on a laptop if you skip the synapse table):

1. `pip install pandas pyarrow fafbseg` (navis optional, for morphology).
2. Pull `proofread_connections_783.feather` and `proofread_root_ids_783.npy` from Zenodo (a few GB).
3. Load with `pandas.read_feather()` (or stream with `pyarrow.feather.read_table()`, which supports chunked reads via `table.num_rows`, `table.slice()`).
4. Build the graph in `networkx.DiGraph()` from `sources.zip(pre_pt_root_id, post_pt_root_id, syn_count)`. For 15.1M edges × 2 ids (~16 B) that is about 460 MB plus dict overhead (~2 GB) of main memory, which is fine on a 16 GB laptop.
5. For synapse-level analyses, keep the data on-disk in Arrow (memory-mapped) and read per-neuron or per-flight windows rather than loading all 9.5 GB.

### Storage + RAM footprint (working estimate)

| Object | Disk (zenodo) | RAM if loaded whole |
|---|---|---|
| `flywire_synapses_783.feather` | 9.5 GB | ~20-40 GB (float64-heavy), avoid on laptop |
| `proofread_connections_783.feather` | ~1.5-4 GB (est) | ~0.5-2 GB in RAM as DataFrame; ~0.5-1 GB as nx graph |
| neuron count table | 233.8 MB | ~1 - 3 GB |
| Full graph in networkx | (edges ~15.1M) | ~0.5-1.5 GB |

Volumetric segmentation (EM, EMU) is terabytes and is not downloadable; use CloudVolume region reads (single neurons/meshes only), or email the Seung lab for a full copy if you need to train on EM.

Uncertainty: the exact byte size of the proofread_connections file was not captured (the Zenodo listing truncated); I'd put it in the 3-5 GB class. The neuron counts are validated directly against the Nature paper text.