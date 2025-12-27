# Color Generation

## API Calls

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