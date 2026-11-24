# Reproduction

## Verify scores immediately

Use Python 3.10 or 3.11. The first script needs the standard library. The second uses NumPy.

```sh
python -m pip install -r requirements-audit.txt
python evidence/verify_results.py
python evidence/verify_core_counts.py
```

The first verifies the evidence checksums, 96 JVS cells and 84 JVS point contrasts using the archived trial cosines, and arithmetic from the measured-response summaries. The second enumerates eligible core trials from the crop manifests, checks all 200 core model-condition rows and recreates the ten harmonized bootstrap intervals. These checks require zero audio downloads. The paired room intervals and auxiliary methods are supplied at archived precision.

## Rerun from recordings

Follow [Dataset and checkpoint setup](DATA-AND-MODELS.md). Use separate Python 3.10 environments for CVSM, SSL, and the Torch audio render/baselines. The [frozen environment snapshots](../archive/environments/) document the original versions. Install FFmpeg with libmp3lame, libsndfile, and the relevant packages. On Linux with the historical package versions available, the archived requirements can be used to reconstruct each environment. The minimal setup for JVS/room rendering and scores is NumPy, SciPy, SoundFile and FFmpeg. TorchScript inference additionally needs PyTorch. CVSM uses TensorFlow 2.15.1 and NumPy 1.26.4. The Torch rendering profile adds TorchAudio, Demucs and EnCodec. ECAPA and MERT add SpeechBrain and Transformers respectively.

The commands below assume those environments are named .venv-cvsm, .venv-ssl and .venv-torch. Use the equivalent Python executables for your installation. The default output lives in runs/. To run multiple trials or compare toolchains, give every command the same alternative --runs directory. A completed render manifest prevents accidental replacement.

```sh
.venv-ssl/bin/python workflow/prepare.py jvs
.venv-cvsm/bin/python workflow/embed.py jvs cvsm_art
.venv-cvsm/bin/python workflow/embed.py jvs cvsm_a
.venv-ssl/bin/python workflow/embed.py jvs ssl
.venv-ssl/bin/python workflow/score.py jvs

.venv-ssl/bin/python workflow/prepare.py room
.venv-cvsm/bin/python workflow/embed.py room cvsm_art
.venv-ssl/bin/python workflow/embed.py room ssl
.venv-ssl/bin/python workflow/score.py room
```

JVS returns both the original orientation with descriptive EER and the two-orientation factorial. The room command returns all four response pairs, paired intervals and the secondary mixed-gallery comparisons. A score command can be limited to available encoders with repeated --model options. Use --datasets or --models to point at matching assets outside the clone.

For f2 and g1, replace jvs with f2 or g1 in the three stages. Render via .venv-torch, use all five encoders, run CVSM models via .venv-cvsm, SSL via .venv-ssl, and ECAPA and MERT via .venv-torch. Same workflow for t1-f2 and t1-g1, which reuse the original cohort inputs and need the already scored f2/g1 embeddings as a comparator. Use musdb for the recorded-mixture separation experiment, again with the Torch render environment and all five encoders.

The rerun writes fresh outputs only. Compare them to the [claim map](CLAIMS.md) and saved result files. FFmpeg versions can change codec renders. EnCodec and HTDemucs had small run-to-run differences in the documented source replay. Preserve the stored result snapshot and report meaningful drift.

## Build the revised Acta Acustica draft

Compile the self-contained LaTeX source with Tectonic or run `pdflatex` twice from the manuscript directory.

```sh
cd manuscript/acta-acustica
tectonic singer_or_studio_revised.tex
```

## Regenerate the earlier reading copy

Install Matplotlib, Markdown, Pillow, ReportLab and system DejaVu fonts if regeneration is useful. The PDF build retains line numbering.

```sh
python manuscript/make_figures.py --pilots archive/core --factorial archive/factorial/results.json --output runs/figures
python manuscript/build_pdf.py --source manuscript/when_production_changes_the_match.md --output runs/reading-copy.pdf
```

The source-controlled figures are in manuscript/figures/. The build command uses those figures. Compare any rerendered images before replacing them. The manuscript and professor PDF are context for coauthors writing the paper.
