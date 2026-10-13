# Color Generation

## 25/12/2025: API Calls

I am using the Huemint API to generate color palettes!
I started by trying to tweak parameters to get better results.

For now, I am using a stategy where I include all colors, even black and white, in the initial palette sent to the API. I try to constrain everything, including the generated colors to black and white. 

This is not working very well: sometimes the colors are not very distinct from black and white, or from each other. I think this is because the contrast constraints are not being fully respected — the adjacency matrix being overconstrained is an issue stated in the api source.

### Next Steps
Next strategy is to not include black and white in the api call, and then filter after it to ensure the colors match our constraints.
- have n_colors = n_colors - 2, and always add black and white as first two colors
- post-process to ensure contrast thresholds are met
  - luminance contrast check filter
  - chroma check filter

## 27/12/2025: API Calls v2

I modified the api call to:
- not include black and white
- not have a contrast constraint
- use the random generation mode instead of transformer/diffusion

It's now looking alright! I ended up not implementing the post-processing filters for now, as the results are looking good enough.
I sorted the colors by saturation, for the cycler to look better (and the default more basic plots, with colors C0, C1 and little else, to look nicer).

I do recognise that we might need to revisit this in the future, as some colors are still quite close to black or white, and we should probably tweak them when they are paired with either black or white backgrounds.



