# Project Structure

## 27/12/2025: Initial Thoughts

I want to document the project structure of ClaroScuro to help new contributors understand how everything is organized. This will include directories, key files, and their purposes.


## Directory Overview
- `src/`: Contains the source code for the application.
    - `claroscuro/`: Main application package.
        - `authoring/`: Modules related to the theme design process.
        - `cli/`: Command-line interface components.
        - `mpl/`: Matplotlib integration and utilities.
        - `styles/`: Static style assets.
- `docs/`: Documentation files, including this logbook.
- `tests/`: Unit and integration tests for the application.

ChatGPT's suggestion:

```
claroescuro/
├── pyproject.toml
├── README.md
├── uv.lock
├── .gitignore
│
├── src/
│   └── claroescuro/
│       ├── __init__.py
│       ├── __main__.py          # python -m claroescuro
│
│       ├── setup.py             # user-facing presets (notebook, paper, slides)
│       ├── context.py           # style contexts & decorators
│
│       ├── styles/              # STATIC STYLE ASSETS (committed)
│       │   ├── base.mplstyle
│       │   ├── bg_light.mplstyle
│       │   ├── bg_dark.mplstyle
│       │   ├── colors_light.mplstyle
│       │   ├── colors_dark.mplstyle
│       │   ├── scale_notebook.mplstyle
│       │   ├── scale_paper.mplstyle
│       │   ├── scale_slides.mplstyle
│       │   └── tufte.mplstyle
│
│       ├── mpl/                 # Matplotlib glue (thin, boring, stable)
│       │   ├── __init__.py
│       │   ├── cyclers.py
│       │   ├── cmaps.py
│       │   └── mplstyle.py
│
│       ├── authoring/            # INTERNAL: design & generation
│       │   ├── __init__.py
│       │   ├── build.py          # palette → mplstyle pipeline
│       │   │
│       │   ├── color/            # color science & palette generation
│       │   │   ├── __init__.py
│       │   │   ├── spaces.py
│       │   │   ├── metrics.py
│       │   │   ├── constraints.py
│       │   │   ├── search.py
│       │   │   ├── palettes.py
│       │   │   ├── colormaps.py
│       │   │   └── filters.py
│       │   │
│       │   └── preview/          # visualization for authoring decisions
│       │       ├── __init__.py
│       │       ├── palettes.py
│       │       ├── colormaps.py
│       │       ├── styles.py
│       │       └── compare.py
│
│       └── cli/                 # CLICK LIVES HERE (and ONLY here)
│           ├── __init__.py
│           ├── main.py           # click.Group
│           ├── build.py          # `claroescuro build`
│           ├── preview.py        # `claroescuro preview ...`
│           └── styles.py         # optional helpers
│
│
├── docs/
│   └── logbook/                 # handwritten design logs (versioned)
│
├── logs/                        # runtime logs (gitignored)
│
└── tests/
    ├── __init__.py
    └── authoring/
        ├── test_metrics.py
        ├── test_constraints.py
        └── test_spaces.py
```

## Designing for Interaction

I am starting to think about how to best structure the code to facilitate user interaction: not the CLI, but the user facing modules. These are the first ones I will be focusing on.

Essentially, there are 2 knobs to turn: scale and dark/light mode.
Maybe the best way is just to start with a function that takes these 2 parameters and sets up the theme accordingly.


## 09/10/2026: Architecture plan (authored by Claude)

*Written by Claude at Marta's request, after reviewing the repo. Supersedes the ChatGPT tree above where they differ. The full approved plan is the source of truth for build order; this is the summary.*

### Layers

```
cli  ->  authoring  ->  theme (data)  <-  runtime (use)
                           ^
                         locate (project | global | default)
```

- **Runtime** (`style.py`, `locate.py`, `theme.py`, `mpl/`) depends only on stdlib, matplotlib and `platformdirs`. `import claroscuro; claroscuro.use()` never pulls in `requests`, `colorspacious` or `click`.
- **Authoring** (`authoring/`): color science, candidate generation, preview, build.
- **CLI** (`cli/`): the only place `click` appears; orchestrates, no color math.

### Target layout

```
src/claroscuro/
  __init__.py, style.py, theme.py, locate.py
  mpl/        cmaps.py, fonts.py
  styles/     base, scale_*, mode_{light,dark}, typeface_{serif,sans}, frame_{open,box,grid}, default/
  fonts/
  authoring/
    color/    spaces, metrics, constraints, evaluate, derive, colormaps, sources/{curated,maximin,huemint}
    preview/  palettes, cvd, colormaps, gallery, printtest
    build.py
  cli/        main, init, preview
```

### Public API: one function, five optional knobs

```python
claroscuro.use(scale="paper", mode="light", theme=None, typeface="serif", frame="open")
```

- `scale`: paper | notebook | slides. Owns canvas size and text size together; there is deliberately no font-size knob. If a figure doesn't fit, change `figsize`, or set `plt.rcParams["font.size"]` (the style sheets only ever set `font.size` numerically, so everything else follows).
- `mode`: light | dark. (Was called "theme" in the old code; "theme" now means the saved palette bundle.)
- `theme`: name of a saved palette + colormaps.
- `typeface`: serif | sans. `frame`: open | box | grid.

### Where generated themes live

`<scope-dir>/themes/<name>/{theme.json, colors_light.mplstyle, colors_dark.mplstyle}`, in one of two scopes chosen at `claroscuro init`: project (`./.claroscuro/`, found by walking up from the cwd) or global (`platformdirs` user config dir). Lookup at runtime: project, then global, then the packaged default. `theme.json` is the source of truth; the `.mplstyle` files are derived from it.

### Authoring flow

`Constraints -> Propose -> Check & rank -> Choose -> Finish -> Theme -> files`. Candidate sources (curated Okabe-Ito/Tol, our own maximin generator, Huemint) each produce light palettes; every candidate gets a derived dark twin and is scored (distinguishability, color-vision-deficiency robustness, contrast with the background) before you see it. See [color-theory.md](color-theory.md) for the reasoning.
