from colors.generate import generate_color_palette
from colors.processing import saturation
from demos.colors import color_tiles, color_lines
import json

def main():
    palette = generate_color_palette(n_colors=8, contrast=0, bw_contrast=0, n_results = 30, temperature=1.2, mode='random')
    print(len(palette['results']))
    for result in palette['results']:
        sorted_palette = sorted(result['palette'][:], key=saturation, reverse=True)
        color_lines(sorted_palette)


if __name__ == "__main__":
    main()
