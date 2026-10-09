# Style Generation

There are 3 key steps in generating a theme in our package:
1. Generate multiple hypotheses of color palettes
2. (Have the user) select one and refine it
3. Have a way to use the generated palette in different applications

## Generating multiple hypotheses
This is done in the `claroscuro.authoring.color.generate` module. I am not sure yet whether this should be a class or just functions. Essentially, we only need one function that, given some parameters, returns multiple color palettes. However, there are some extra things we want to do:
- Ensure the colors generated are accessible (i.e., have enough contrast between them)
- Allow the user to specify some colors they want to include in the palette (e.g., primary color)
- Create slight variants of the same color for light and dark modes

To achieve this, I am not sure yet how to structure the code. One idea is to have a `PaletteGenerator` class that takes in the parameters and has a method `generate_palettes()` that returns the palettes. For the sake of ensuring each piece of code has a single responsibility, I might create helper functions or classes for:
- Validating color contrast
- Adjusting colors for light/dark modes

Maybe the `PaletteGenerator` can use these helpers internally. This way, the main function remains clean and focused on generating palettes, while the helpers handle the specific tasks. And we can orchestrate everything in a clear way, inside the class.

**Concept**:
```python
class PaletteGenerator:
    def __init__(self, user_colors=None, n_colors=8, contrast=...):
        self.user_colors = user_colors
        self.n_colors = n_colors
        self.contrast = contrast
        ...

    def generate(self, n_palettes=10) -> List[Palette]:
        # Use Huemint API to generate palettes
        # Post-process palettes to ensure contrast
        return palettes

class Palette:
    def __init__(self, colors: List[str]):
        if not all(self._validate_hex(c) for c in colors):
            raise ValueError("Invalid color hex code")
        self.colors = colors

    def _adjust_for_mode(self, mode: str) -> List[str]:
        # Adjust colors for light/dark mode
        return adjusted_colors

    def light_mode(self) -> List[str]:
        return self._adjust_for_mode('light')

    def dark_mode(self) -> List[str]:
        return self._adjust_for_mode('dark')

    def _validate_hex(self, color: str) -> bool:
        # Validate if the color is a valid hex code
        return is_valid
```

## Selecting and refining palettes
Once we have multiple palette hypotheses, the user should be able to select one and refine it. This could be done via a simple CLI or GUI where the user can see the generated palettes and pick one. 
After selection, we can provide options to tweak individual colors (e.g., lighten/darken, change hue) and see the updated palette in real-time.
However, the key bit is about finalizing the palette for use. Generate colormaps, both continuous and discrete, for use in visualizations.

I am thinking of going for the CLI approach, as it is simpler to use and reduces distractions (the whole point). I want to implement this in `claroscuro.cli`, but I need to think about which components go into this and which of them have responsibilities that belong elsewhere (e.g., in `claroscuro.authoring.color`).

The experience requires:
1. Initialize palette generation by accepting user parameters
2. Displaying generated palettes
3. Allowing the user to select one
4. Triggering the building of style sheets and colormaps based on the selected palette

Now, we have to think about the best way to organize this. The display code should come from `claroscuro.authoring.preview`, as it is responsible for showing colors to the user. The palette generation comes from `claroscuro.authoring.color.generate`. The building of style sheets and colormaps should be in `claroscuro.authoring.build`, and, if there are processing specific steps, these should come from `claroscuro.authoring.color.process`. The CLI code should orchestrate all these components.

I think that, when calling this, the best interface would be something like `claroscuro init`.