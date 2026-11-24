# Singer or Studio?

This repository contains the manuscript and experimental record for a controlled benchmark of production mismatch in singer retrieval. Each trial compares one same-singer candidate with one different-singer candidate. On JVS-MuSiC, with a dry query and a synthetically reverberated same-singer candidate held fixed, applying the same reverb recipe to the different-singer candidate reduced CVSM-ART ranking error from **46.24% to 17.52%**. The paired reduction was **28.72 percentage points** (95% interval **22.76–35.17**). The measured-room-filter follow-up is reported separately.

## Start here

1. Read the [revised Acta Acustica draft PDF](manuscript/acta-acustica/singer_or_studio_revised.pdf) or edit the [LaTeX source](manuscript/acta-acustica/singer_or_studio_revised.tex).
2. Use the [technical supplement](evidence/supplement.md) and [claim-to-evidence map](docs/CLAIMS.md) to trace the reported results to the saved evidence.
3. Follow the [reproduction guide](docs/REPRODUCTION.md) to check saved results, then see [dataset and model setup](docs/DATA-AND-MODELS.md) for a waveform-to-score rerun.

The [earlier reading copy](manuscript/Singer%20or%20Studio%20-%20When%20Production%20Changes%20the%20Match.pdf) and [professor copy](manuscript/Singer%20or%20Studio%20-%20The%20Thesis.pdf) remain available for background.

```sh
python -m pip install -r requirements-audit.txt
python evidence/verify_results.py
python evidence/verify_core_counts.py
```

The first check recalculates JVS rankings and point contrasts from preserved trial-level cosine scores. The second reconstructs all 200 core model-condition trial masks and rates from the crop manifests and saved singer error counts. It also reproduces all ten shared-condition intervals. Both checks work without audio or model downloads.

| Directory | Contents |
| --- | --- |
| [manuscript](manuscript/) | Reading copies, editable text, figures and build scripts |
| [evidence](evidence/) | Exact result tables, score-level evidence, input manifests, protocols and verification scripts |
| [workflow](workflow/) | Portable model fetch, crop rendering, embedding and scoring commands |
| [archive](archive/) | Source analysis scripts, original outputs, selected-inference recheck, auxiliary method and artist-level records |
| [docs](docs/) | Claim map, setup, literature notes, model hashes, validation and [import history](docs/HISTORY.md) |

Audio, embeddings, private training assets and large checkpoint files belong in ignored local directories. The released encoders are fetched from their upstream sources and verified by hash. The optional Yakura and fine-tuning baseline weights are author-local, with archived results available here. This paper's evidence is machine-only. Participant responses and listening-study material are outside its scope.


## Contributors
Desu Nayanika Sri Sai Jhansi [https://github.com/desunayani-ssj] \
Shivani Kona [https://github.com/shivani11-glitch] \
Venkata Sathvik Chittipaka [https://github.com/sathvikchitti] \
Umanth Reddy [https://github.com/Umanth-Reddy] \
Ruthvik Marri [https://github.com/hawkeye007-dev]
