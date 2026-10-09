# Color science for ClaroScuro palettes

> **Authored by Claude (Anthropic)**, drafted 2026-10-09 at Marta's request, for the ClaroScuro logbook. Not written by Marta. Provenance: statements tagged **[checked]** were verified against a source while drafting (library source code or a web page). Everything else comes from my background knowledge: treat it as a well-informed starting point and verify before citing.

## 0. What we are designing

Three artifacts, in increasing difficulty:

1. A **categorical palette**: a short list of colors for lines, bars and points (matplotlib's `axes.prop_cycle`).
2. **Continuous colormaps**: sequential and diverging, for heatmaps and images.
3. **Light and dark variants** of both.

The goal is that they work for as many viewers and media as possible: viewers with color vision deficiency (CVD), thin lines, white versus black backgrounds, and print.

## 1. How we see color (just enough)

- The retina has three cone types (long-, medium-, short-wavelength: L, M, S). Because there are three, any color sensation can be matched by three numbers. That is why every color space is 3-D.
- Downstream, the signals are recombined into opponent channels: **luminance** (roughly L+M), **red-green** (L-M) and **blue-yellow** (S-(L+M)).
- The luminance channel resolves fine detail much better than the chromatic channels do. Consequence for plots: thin lines and small marks are told apart mostly by **lightness**, and only secondarily by hue. This is the single most useful fact for line-plot palettes, and it is also what rescues viewers with CVD (their luminance channel is intact).

## 2. Color spaces: from a hex code to "how different do these look?"

- **sRGB (hex)** is device-oriented and *gamma-encoded*: the numbers are not proportional to emitted light. Blending, averaging and CVD matrices must be done in **linear-light** RGB. **[checked]** `colorspacious` converts to linear sRGB before applying CVD matrices.
- **CIE XYZ** is device-independent; its Y is luminance. WCAG's "relative luminance" is Y.
- **CIELAB** (1976) gives L* (lightness) and a*, b* (opponent axes); the Euclidean distance is called deltaE76. Much better than RGB, still not uniform: equal numbers can look quite different, notably in saturated blues. **CIEDE2000** adds correction terms to fix this, but it is a formula, not a Euclidean space, so you cannot interpolate in it or do geometry with it.
- **CIECAM02 / CAM02-UCS** (Luo, Cui & Li, 2006): a color *appearance* model (it models viewing conditions), plus a remapping into a Euclidean space with coordinates J' (lightness), a', b'. Distance there approximates perceived difference, and because it is Euclidean we can interpolate colormaps and run farthest-point searches. Three variants exist: **UCS** (compromise), **LCD** (tuned for large differences) and **SCD** (small differences). **[checked]** `colorspacious` provides all three. Viridis was designed in CAM02-UCS. A categorical palette is a *large*-difference problem, so LCD is arguably the better fit for palette distances; we use UCS by default and should compare.
- **OKLab** (Ottosson, 2020): a newer, simpler space with good uniformity and hue linearity (used by CSS Color 4). Not in `colorspacious`, but about ten lines to implement. A possible alternative; not needed now.
- **Caveat on every distance above:** they are models fitted to experiments on large patches in controlled conditions. **[checked]** Szafir (2018) measured color difference for points, bars and lines on crowd-sourced displays and found that smaller marks weaken perceived difference, while elongated marks (lines) are more discriminable than points. A 1 pt matplotlib line is thin but long, so we add a safety margin to thresholds rather than trust them blindly, and calibrate by eye and on paper.

## 3. Color vision deficiency (CVD)

- **[checked]** From the `colorspacious` source comments: about 5% of men have deuteranomaly, about 1% are deuteranopic or on the protanomaly spectrum, and tritanomaly is under 0.01%. (Other sources quote roughly 8% of men and 0.5% of women of Northern European ancestry for any red-green deficiency.)
- Types: **protan** (L cones anomalous or absent), **deutan** (M), **tritan** (S). The suffix *-anomaly* means shifted sensitivity (partial deficiency, a continuum of severity); *-opia* means the cone class is absent (dichromacy).
- Effect: the red-green axis collapses, so colors that differ mostly along red-green look alike. The **blue vs orange/yellow** axis and **lightness** survive.
- Simulation models: Brettel, Viénot & Mollon (1997) and Viénot et al. (1999) for dichromats; **Machado, Oliveira & Fernandes (2009)** for anomalous trichromacy with adjustable severity. The Machado model is a 3x3 matrix per type and severity (0 to 100 in steps of 10). **[checked]** `colorspacious` embeds the authors' matrices (doi 10.1109/TVCG.2009.113) and applies them to linear-light sRGB (`sRGB1+CVD`, `_CVD_forward` in `conversion.py`). The authors' page does not state which RGB space the matrices assume; linear light is the physically sensible reading.
- We simulate at **severity 100** for protan, deutan and tritan: the worst case. A palette that survives severity 100 also survives milder severities (not guaranteed in theory, but expected).
- Limits: simulation approximates an average observer on an idealized display; real people and screens vary. We claim "worst-case aware", never "colorblind-proof". **[checked]** The `glasbey` package docs make the same disclaimer about their CVD option.
- Practical rules (Okabe & Ito 2008; Wong 2011; Tol): vary lightness as well as hue; lean on blue vs orange/yellow; avoid red/green/brown/orange at equal lightness; never rely on hue alone; add redundant encodings (direct labels, line styles, markers) when there are many series.

## 4. Categorical palettes

### 4.1 From requirements to numbers

| Requirement | Metric | Parameter |
|---|---|---|
| Distinguishable (normal vision) | min pairwise deltaE' in CAM02-UCS | `min_delta_e` |
| Distinguishable under CVD | min over {protan, deutan, tritan} of min pairwise deltaE' after simulation | `min_delta_e_cvd` (lower than the above; CVD inevitably compresses) |
| Visible on the background | WCAG contrast ratio against white (light mode) / black (dark mode) | `min_contrast` (3.0) |
| Not garish, inside sRGB | J' and C' bounds, in-gamut | `lightness_bounds`, `chroma_bounds` |
| Useful at every length | greedy order (prefix property) | - |
| (later) Easy to name | color-name distance (Heer & Stone 2012) | - |

### 4.2 The maximin formulation

Pick n colors from a candidate set so that the *smallest* distance between any two is as large as possible, where the distance between two colors is the **minimum over viewing conditions** (normal, protan, deutan, tritan) of their deltaE' after simulation. This is the "max-min dispersion" problem.

Greedy farthest-first heuristic: start from a seed color, then repeatedly add the candidate whose distance to its nearest already-chosen color is largest.
- **Prefix property:** the first 2, 3, 4... colors are each good on their own. This matters because most plots show only C0, C1, C2.
- For a true metric, farthest-first is a known 2-approximation of the optimum. Our min-over-conditions distance is a minimum of metrics, which need not obey the triangle inequality, so we treat the result as a *good heuristic*, not a guarantee.
- **Candidate set:** a grid in (J', C', h), converted to sRGB, with out-of-gamut points discarded (not clipped). Grid resolution trades quality for speed.
- **Multiple hypotheses** for the picker come from different seeds / random restarts; **pinned colors** (v2) are just extra seeds.
- Same family as Glasbey et al. (2007) and tools such as `glasbey`, `distinctipy` and iwanthue. **[checked, partly]** I could not confirm which distance metric the `glasbey` package uses; one third-party source says CIE76. We therefore implement our own on `colorspacious` and use `glasbey` only as a cross-check.
- Report, for each palette, the largest prefix length k that still meets the thresholds. If the default n = 8 fails the CVD threshold past color 6, the honest output is "this palette is good for 6, use line styles beyond that".

### 4.3 Contrast with the background, and why light and dark palettes differ

WCAG contrast ratio = (L1 + 0.05) / (L2 + 0.05), with L the relative luminance (Y). WCAG 2.1 SC 1.4.11 asks for at least 3:1 for graphical objects.
- Against white (L = 1): need Y <= 0.30.
- Against black (L = 0): need Y >= 0.10.
- A color that works on both therefore has Y in [0.10, 0.30], a narrow band. But categorical palettes need *lightness variety* to survive CVD (section 3). So light and dark modes get **separate palettes**, and `derive` builds one from the other.
- Caveat: the WCAG 2 ratio is a crude model and is known to be inaccurate on dark backgrounds; APCA (proposed for WCAG 3) is the usual critique-driven alternative. We use WCAG as a floor, not as the whole story. Pure black and white are the extremes; slides on dark gray need less.

### 4.4 Deriving the dark variant (heuristic)

Keep each color's hue h, move J' to meet the contrast floor on the new background, reduce chroma if needed to stay in gamut (and slightly, since saturated colors glare on black), then **re-run every check**. CVD distances can shrink because the lightness range changed. A candidate whose derived twin fails is dropped. The size of the chroma reduction is a judgment call to settle by eye.

### 4.5 How many colors?

Around 7 to 8 is the common practical ceiling for telling lines apart and mapping them to a legend; there is no sharp number. Default n = 8 sits at the edge, and under CVD fewer are reliably separable (see the prefix report above).

## 5. Continuous colormaps

- **Kinds:** sequential (ordered magnitude), diverging (deviation from a meaningful midpoint), cyclic (phase). Qualitative maps are just categorical palettes.
- **Why uniformity matters:** equal data steps should give equal perceived steps. Otherwise the colormap invents structure: rainbow/jet have non-monotone lightness, which creates false edges and bands (Borland & Taylor 2007; Crameri et al. 2020).
- **Recipe** (viridis; Kovesi 2015): a path through a perceptually uniform space such that (i) J' is strictly monotone and about linear in position; (ii) hue and chroma vary smoothly to add discriminability (multi-hue) while staying in sRGB gamut; (iii) the path is traversed at constant speed (arclength-parameterized in CAM02-UCS). Because lightness carries the ordering, such maps stay readable under CVD and in grayscale print.
- **Our construction (proposed):** anchor hues come from the chosen palette; prescribe J'(t); fit a smooth (a', b') path; reduce chroma where it leaves the gamut; resample 256 steps by arclength.
- **Diverging:** two sequential arms sharing a neutral midpoint, symmetric in J' about it; midpoint light in light mode, dark in dark mode; arms along blue vs orange, not red vs green.
- **Background interaction:** the end of a sequential map near the background lightness vanishes for scatter points or lines; keep the J' range away from the background, or accept it for heatmaps only.
- **Metrics we compute:** minimum derivative of J' > 0; coefficient of variation of per-step deltaE'; J' monotone after CVD simulation; J' range; fraction of the path that needed gamut clipping.
- **Fallbacks and references:** viridis and cividis (cividis was optimized for CVD, Nuñez, Anderton & Renslow 2018), Crameri's scientific colour maps.
- Matplotlib detail: an `.mplstyle` can only *name* `image.cmap`, not define a colormap, so `mpl/cmaps.py` registers the theme's colormaps before the style is loaded.

## 6. Mapping to ClaroScuro modules

| Concept | Module |
|---|---|
| sRGB <-> CAM02-UCS, CVD simulation | `authoring/color/spaces.py` |
| deltaE', WCAG contrast, worst-case CVD distance | `authoring/color/metrics.py` |
| Thresholds and bounds | `authoring/color/constraints.py` |
| Report card per candidate | `authoring/color/evaluate.py` |
| Okabe-Ito / Tol, maximin generator, Huemint | `authoring/color/sources/` |
| Light -> dark derivation | `authoring/color/derive.py` |
| Sequential / diverging maps | `authoring/color/colormaps.py` |

## 7. Decisions to calibrate (not yet made)

- Default thresholds: compute Okabe-Ito's and Tol's worst-case deltaE' in our metric and set defaults at or above them, so the numbers are defensible rather than invented.
- UCS versus LCD for palette distances (section 2).
- How much to lower chroma in dark mode; whether to add color-name distance (Colorgorical).
- Pure black versus dark gray as the dark background.
- All of the above get a by-eye pass and a printed test.

## 8. Reading list

- Okabe, M. & Ito, K. (2008). *Color Universal Design (CUD): How to make figures and presentations that are friendly to colorblind people.*
- Wong, B. (2011). Points of view: Color blindness. *Nature Methods* 8, 441.
- Tol, P. *Colour schemes* (SRON technical note).
- Machado, G. M., Oliveira, M. M. & Fernandes, L. A. F. (2009). A physiologically-based model for simulation of color vision deficiency. *IEEE TVCG* 15(6). doi 10.1109/TVCG.2009.113.
- Luo, M. R., Cui, G. & Li, C. (2006). Uniform colour spaces based on CIECAM02. *Color Research & Application* 31(4).
- Smith, N. & van der Walt, S. (2015). *A better default colormap for matplotlib* (the viridis talk).
- Kovesi, P. (2015). Good colour maps: how to design them. arXiv:1509.03700.
- Crameri, F., Shephard, G. E. & Heron, P. J. (2020). The misuse of colour in science communication. *Nature Communications* 11.
- Nuñez, J. R., Anderton, C. R. & Renslow, R. S. (2018). Optimizing colormaps with consideration for color vision deficiency. *PLOS ONE* (arXiv:1712.01662).
- Borland, D. & Taylor, R. M. (2007). Rainbow color map (still) considered harmful. *IEEE CG&A* 27(2).
- Glasbey, C., van der Heijden, G., Toh, V. & Gray, A. (2007). Colour displays for categorical images. *Color Research & Application* 32(4).
- Gramazio, C. C., Laidlaw, D. H. & Schloss, K. B. (2017). Colorgorical. *IEEE TVCG* 23(1).
- Heer, J. & Stone, M. (2012). Color naming models for color selection, image editing and palette design. *CHI*.
- Szafir, D. A. (2018). Modeling color difference for visualization design. *IEEE TVCG* 24(1).
- Harrower, M. & Brewer, C. A. (2003). ColorBrewer.org. *The Cartographic Journal* 40(1).
- W3C. *WCAG 2.1*, SC 1.4.11 Non-text Contrast.
- Ottosson, B. (2020). *A perceptual color space for image processing* (OKLab).
