import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, RegularPolygon, Circle, FancyArrow


def draw_beam(length, thickness):
    beam = Rectangle((0, 0), length, thickness, edgecolor='black', facecolor='white')
    axes.add_patch(beam)
    return


def draw_support(x_position, y_position, height, type):
    if type == 'pin':
        support = RegularPolygon((x_position, y_position), 3, radius=0.5 * height, edgecolor='black', facecolor='white')
        axes.add_patch(support)
    elif type == 'roller':
        support = Circle((x_position, y_position), radius=0.4 * height, edgecolor='black', facecolor='white')
        axes.add_patch(support)
    return


def draw_load(load_range, load_maximum, type, thickness, slope_sign=1, label='', label_side='left'):
    beam_top = np.full(len(load_range), thickness)
    if type == 'uniform':
        load_values = np.full(len(load_range), load_maximum)

        plt.plot(load_range, thickness + load_values, color='tab:blue')
        plt.fill_between(load_range, thickness + load_values, beam_top, color='tab:blue', alpha=0.5)
    elif type == 'triangle':
        load_slope = slope_sign * load_maximum / (load_range[-1] - load_range[0])
        if slope_sign < 0:
            load_x_intercept = load_range[-1]
        else:
            load_x_intercept = load_range[0]
        plt.plot(load_range, load_slope * (load_range - load_x_intercept) + thickness, color='tab:blue')
        plt.fill_between(load_range, load_slope * (load_range - load_x_intercept) + thickness, beam_top,
                         color='tab:blue', alpha=0.5)

    if len(label) > 0:
        if label_side == 'right':
            axes.text(load_range[-1] + 0.05 * (load_range[-1] - load_range[0]), load_maximum + thickness, label,
                      color='tab:blue', ha='left', va='center', fontsize=14)
        else:
            axes.text(load_range[0] - 0.05 * (load_range[-1] - load_range[0]), load_maximum + thickness, label,
                      color='tab:blue', ha='right', va='center', fontsize=14)
    return


def draw_force(x_position, y_position, x_component, y_component, label=''):
    force_arrow = FancyArrow(x_position, y_position, x_component, y_component,
                             width=0.07, length_includes_head=True, color='red')
    axes.add_patch(force_arrow)
    if len(label) > 0:
        axes.text(x_position + 1.2 * x_component, y_position + 1.2 * y_component, label,
                  color='red', ha='center', va='center', fontsize=14)
    return


def draw_3d_arrow(start, direction, annotation, ax):
    arrow_length = np.linalg.norm(direction)
    arrow_head_length = 0.002 * arrow_length
    # Plot the arrow
    ax.quiver(start[0], start[1], start[2],
              direction[0], direction[1], direction[2],
              pivot='tail', arrow_length_ratio=arrow_head_length)
    # length=arrow_length,
    ax.text(1.1 * direction[0], 1.1 * direction[1], 1.1 * direction[2], annotation, ha='center', va='center')
    return


def calculate_unit_vector(start, end):
    unit_vector = (end - start) / np.linalg.norm(end - start)
    return unit_vector


def calculate_force_components(start, end, magnitude):
    unit_vector = calculate_unit_vector(start, end)
    force_vector = magnitude * unit_vector
    return force_vector


if __name__ == '__main__':
    beam_length = 10
    beam_width = 1

    figure, axes = plt.subplots()
    figure.patch.set_visible(False)
    axes.axis('off')

    draw_beam(beam_length, beam_width)
    draw_support(0, -0.5 * beam_width, beam_width, type='pin')
    draw_support(beam_length, -0.4 * beam_width, beam_width, type='roller')

    maximum_load = 1.0
    load_x_values = np.linspace(0, 0.5 * beam_length)
    draw_load(load_x_values, maximum_load, 'triangle', beam_width)  # , label=r'$f_0$', label_side='right')

    maximum_load = 1.0
    load_x_values = np.linspace(0.5 * beam_length, beam_length)
    draw_load(load_x_values, maximum_load, 'uniform', beam_width, label=r'$f_0$', label_side='right')

    # plt.text(0.333*beam_length, beam_width + 1.1*maximum_load, r'$f_0$', ha='center', va='bottom', fontsize=14, color='tab:blue')

    applied_force = [0, -2]
    draw_force(0.5 * beam_length, beam_width, applied_force[0], applied_force[1], label=r'$\vec{F}$')

    plt.xlim([-beam_width, beam_length + beam_width])
    plt.ylim([-2 * beam_width, beam_width + 4 * maximum_load])

    axes.set_aspect('equal')
    plt.tight_layout()
    # plt.savefig('Beam.png')
    plt.show()
