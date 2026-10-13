from .palettes import color_lines

class Previewer:
    def __init__(self, palettes):
        self.palettes = palettes

    def display_generated_palettes(self):
        for idx, palette in enumerate(self.palettes, start=1):
            print(f"Palette {idx}:")
            print(color_lines(palette))
            print("\n")

        palettes_count = len(self.palettes)
        
        
