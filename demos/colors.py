import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors
import numpy as np

def color_tiles(colors):
    """Create a figure with colored tiles based on the provided colors."""
    nb_colors = len(colors)
    fig, ax = plt.subplots(figsize=(nb_colors, 2))
    for i, color in enumerate(colors):
        rect = Rectangle((i, 0), 1, 1, color=color)
        ax.add_patch(rect)
        ax.text(i + 0.5, 0.5, color, va='center', ha='center', fontsize=12, color='white' if mcolors.rgb_to_hsv(mcolors.to_rgb(color))[2] < 0.5 else 'black')
    ax.set_xlim(0, nb_colors)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.show()




def color_lines(colors):
    """Create a figure with colored lines based on the provided colors."""
    th = np.linspace(0, 2*np.pi, 512)
    fig, ax = plt.subplots(figsize=(6, 2))

    for j, c in enumerate(colors):
        v_offset = -(j / len(colors))
        ax.plot(th, .1*np.sin(2*th) + v_offset, color=c)
        ax.annotate("'C{}'".format(j), (0, v_offset),
                    xytext=(-1.5, 0),
                    ha='right',
                    va='center',
                    color=c,
                    textcoords='offset points',
                    family='monospace')

        ax.annotate("{!r}".format(c), (2*np.pi, v_offset),
                    xytext=(1.5, 0),
                    ha='left',
                    va='center',
                    color=c,
                    textcoords='offset points',
                    family='monospace')
    ax.axis('off')
    plt.show()