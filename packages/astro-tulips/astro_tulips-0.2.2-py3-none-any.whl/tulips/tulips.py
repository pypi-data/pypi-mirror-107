
# Copyright (c) 2021, Eva Laplace e.c.laplace@uva.nl

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import matplotlib.pyplot as plt
import mesaPlot as mp
import numpy as np
from os import makedirs, path
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import ListedColormap
from matplotlib.patches import Wedge, Patch
from matplotlib.colors import Normalize, LogNorm
from matplotlib.animation import FuncAnimation
from tqdm import tqdm
import astropy.units as u

from . import colormodels
from . import blackbody

# Define global constants
ELEM_BASE = ['h1', 'he3', 'he4', 'c12', 'n14', 'o16', 'ne20', 'mg24', 'si28', 's32', 'ar36', 'ca40', 'fe56']
ELEM_HEAVY = ['s33', 's34', 'cl35', 'cl36', 'cl37', 'ar35', 'ar36', 'ar37', 'ar38', 'k39', 'k40', 'k41',
               'k42', 'k43', 'ca39', 'ca40', 'ca41','ca42', 'ca43', 'ca44', 'sc43', 'sc44', 'sc45', 'sc46',
               'ti44', 'ti45', 'ti46', 'ti47', 'ti48', 'v47', 'v48', 'v49', 'v50', 'v51', 'cr48', 'cr49',
               'cr50', 'cr51', 'cr52', 'cr53', 'cr54', 'cr55', 'cr56', 'cr57', 'mn51', 'mn52', 'mn53', 'mn54',
               'mn55', 'mn56', 'fe52', 'fe53', 'fe54', 'fe55', 'fe56', 'fe57', 'fe58', 'co55', 'co56', 'co57',
               'co58', 'co59', 'co60', 'ni55', 'ni56', 'ni57', 'ni58', 'ni59', 'ni60', 'ni61', 'cu59', 'cu60',
               'cu61', 'cu62', 'zn60', 'zn61', 'zn62', 'zn63', 'zn64']
# Custom colormap
CMAP_BASE = ListedColormap([ "#40C4FF",     # dark blue - h1
                             "#2979FF",     # lighter dark blue - he3
                             "#2962FF",     # light blue - he4
                             "#C6FF00",     # lime - c12
                             "#18FFFF",     # cyan - n14
                             "#00C853",     # dark green - o16
                             "#69F0AE",     # light green - ne20
                             "#8D6E63",     # light brown - mg24
                             "#5D4037",     # brown - si28
                             "#BDBDBD",     # pinkish purple - s32
                            ])
CMAP_HEAVY = plt.get_cmap("plasma", len(ELEM_HEAVY))
# Default values for percentages and fraction annotations
PERCENTAGE_LIST = [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
FRACTION_LIST = [0.25, 0.5, 0.75, 1.0]
# Mixing types
MIX_TYPES = ["No mixing", "Convection", "Softened convection", "Overshooting", "Semi-convection", "Thermohaline mixing",
             "Rotational mixing", "Rayleigh-Taylor mixing", "Minimum", "Anonymous"]
MIX_HATCHES = ['',      # no mixing
               'o',     # convective
               '.',     # softened convective
               'x',     # overshoot
               'O',     # semi-convective
               '\\',    # thermohaline
               '/',     # rotation
               '+',      # Rayleigh-Taylor
               '',      # minimum
               ''       # anonymous
               ]


def perceived_color(m, time_ind=-1, raxis="log_R", fps=10, fig=None, ax=None, show_time_label=True, time_label_loc=(),
                    time_unit="Myr", fig_size=(5.5, 4), axis_lim=-99, axis_label="", theta1=0, theta2=360, hrd_inset=True,
                    show_total_mass=True, show_surface=True, output_fname="perceived_color", anim_fmt=".mp4",
                    time_scale_type="model_number"):

    """
    Represent the model of a stellar object as circle with radius raxis. The color of the circle corresponds to its
    color as perceived by the human eye by assuming black body radiation at a certain effective temperature.
    Requires a MESA history file.
    :param m: mesaPlot object, already loaded a history file
    :param time_ind: int or tuple (start_index, end_index, step=1) or (start_index, end_index, step);
    if int: create the plot at the index time_ind. If tuple: create an animation from start index to end index with
    intervals of step.
    :param raxis: str, default axis to use as radius of the circle.
    :param fps: int, number of frames per second for the animation
    :param fig: Figure object. If set, plot on existing figure
    :param ax: Axes object. If set, plot on provided axis
    :param show_time_label: boolean, if set, insert a label that gives the age of the stellar object (in Myr)
    :param time_label_loc: tuple, location of the time label on the plot as fraction of the maximal size
    :param time_unit: str, valid astropy time unit
    :param fig_size: tuple, size of the figure in inches
    :param axis_lim: float, value to set for the maximum limit of the x and y axis.
    :param axis_label: str, label of the x and y labels
    :param theta1: int or float: Start angle for the wedge
    :param theta2: int or float: End angle for the wedge
    :param hrd_inset: boolean, if set, add an inset HRD where the location of the current model is indicated with a
    circle.
    :param show_total_mass: boolean, if set, display the value of the total mass of the model in the bottom
    right corner
    :param show_surface: boolean, default True, if set, show the outer boundary of the stellar object
    :param output_fname: str, name of the output file
    :param anim_fmt: str, format to use for saving an animation
    :param time_scale_type: str, one of "model_number", "linear", or "log_to_end"
    For model_number, the time follows the moment when a new MESA model was saved.
    For linear, the time follows linear steps in star_age.
    For log_time_to_end, the time axis is tau = log10(t_final - t), where t_final is the final star_age of the model
    :return: fig, ax
    """
    if fig is None:
        fig = plt.figure()
        fig.set_size_inches(fig_size)
    if ax is None:
        ax = plt.gca()

    start_ind, end_ind, ind_step = check_time_indeces(time_ind, m.hist.star_age)

    r = m.hist.data[raxis]

    # Set axis limits
    if axis_lim == -99:
        axis_lim = 1.1 * r.max()
    elif raxis[:3] == "log":
        axis_lim = np.log10(axis_lim)

    # replace smallest values with constant ratio
    smallest_radius_ratio = 0.01
    too_small = (r / axis_lim < smallest_radius_ratio)
    if np.any(too_small):
        r[too_small] = axis_lim * smallest_radius_ratio

    # Plot star as circle with color derived from Teff
    color = teff2rgb([10 ** m.hist.log_Teff[start_ind]])[0]

    lw = 0
    if show_surface:
        lw = 1.1
    circle = Wedge((0, 0), r[start_ind], theta1=theta1, theta2=theta2, facecolor=color, edgecolor='k',
                   lw=lw)
    ax.add_artist(circle)

    # Add time label
    if show_time_label:
        time = m.hist.star_age[start_ind]
        text = add_time_label(time, ax, time_label_loc=time_label_loc, time_unit=time_unit)

    # Set axis for plotting correctly sized circles
    ax.set_xlim([-axis_lim, axis_lim])
    ax.set_ylim([-axis_lim, axis_lim])
    ax.set_aspect('equal', adjustable='box')

    set_axis_ticks_and_labels(ax, raxis=raxis, axis_label=axis_label)

    if hrd_inset:
        axins, point = add_inset_hrd(m, ax=ax, time_index=start_ind)

    # Add mass label
    if show_total_mass:
        mass_text = ax.text(0.75 * axis_lim, -0.95 * axis_lim, "{}".format(round(m.hist.star_mass[start_ind], 1)) +
                            "$\,\\rm{M}_{\odot}$")

    # Create animation
    if end_ind != start_ind:
        # Create animation
        indices = range(start_ind, end_ind, ind_step)
        indices = rescale_time(indices, m, time_scale_type=time_scale_type)
        r = r[indices]
        t = m.hist.star_age[indices]
        log_teff = m.hist.log_Teff[indices]
        log_l = m.hist.log_L[indices]
        star_mass = m.hist.star_mass[indices]
        colors_ary = teff2rgb(10 ** log_teff)

        frames = len(indices)
        fps = fps
        bar = tqdm(total=frames)

        def init():
            circle.radius = r[0]
            circle.set_facecolor(colors_ary[0])
            ax.add_patch(circle)
            time = (t[0] * u.yr).to(time_unit)
            text.set_text("t = " + time.round(3).to_string())
            return circle, point

        def animate(ind):
            bar.update()
            time = (t[ind] * u.yr).to(time_unit)
            r_cur = r[ind]
            color = colors_ary[ind]
            circle.set_radius(r_cur)
            circle.set_facecolor(color)

            # Add time location
            if show_time_label:
                text.set_text("t = " + time.round(3).to_string())

            if hrd_inset:
                point.set_data(log_teff[ind], log_l[ind])

            if show_total_mass:
                mass_text.set_text("{}".format(round(star_mass[ind], 1)) + "$\,\\rm{M}_{\odot}$")

            return circle, point

        print("Creating animation")

        ani = FuncAnimation(fig, animate, init_func=init, frames=frames, interval=1000 / fps, blit=False, repeat=False)
        plt.subplots_adjust(top=0.99, left=0.12, right=0.89, hspace=0, wspace=0, bottom=0.1)

        # Save animation
        ani.save(output_fname + anim_fmt, writer="ffmpeg", extra_args=['-vcodec', 'libx264'])

    return fig, ax


def energy_and_mixing(m, time_ind=-1, show_mix=False, show_mix_legend=True, raxis="star_mass", fps=10, fig=None, ax=None,
                      show_time_label=True, time_label_loc=(), time_unit="Myr", fig_size=(5.5, 4), axis_lim=-99,
                      axis_label="", axis_units="", show_colorbar=True, cmin=-10,
                      cmax=10, cbar_label="", theta1=0, theta2=360, hrd_inset=True, show_total_mass=False,
                      show_surface=True, show_grid=False, output_fname="energy_and_mixing", anim_fmt=".mp4",
                      time_scale_type="model_number"):
    """
    Represent the model of a stellar object as circle with radius raxis. The circle is divided into rings whose color
    reflect how much energy is generated or lost from the star. Optionally, hashed areas representing mixing regions
    can be added. This corresponds to a "2D Kippenhahn plot".
    Requires MESA history files that contain burning_regions and optionally mixing_regions
    :param m: mesaPlot object, already loaded a history file
    :param time_ind: int or tuple (start_index, end_index, step=1) or (start_index, end_index, step);
    if int: create the plot at the index time_ind. If tuple: create an animation from start index to end index with
    intervals of step.
    :param show_mix: boolean. If set, add hatches for convection and overshooting zones in the star
    :param show_mix_legend: boolean, if set, show a legend for the mixing types
    :param raxis: str, default axis to use as radius of the circle.
    :param fps: int, number of frames per second for the animation
    :param fig: Figure object. If set, plot on existing figure
    :param ax: Axes object. If set, plot on provided axis
    :param show_time_label: boolean, if set, insert a label that gives the age of the stellar object
    :param time_label_loc: tuple, location of the time label on the plot as fraction of the maximal size
    :param time_unit: str, valid astropy time unit, default Myr
    :param fig_size: tuple, size of the figure in inches
    :param axis_lim: float, value to set for the maximum limit of the x and y axis.
    :param axis_label: str, label of the x and y labels
    :param axis_units: str, astropy unit for the x and y axis
    :param show_colorbar: boolean, if set, add a colorbar corresponding to the property shown
    :param cmin: float, minimum value to set for the colorbar
    :param cmax: float, maximum value to set for the colorbar, if smaller or equal to cmin, use the minimum and
    maximum values of property_name instead
    :param cbar_label: str, label to set for the colorbar
    :param theta1: int or float: Start angle for the wedge
    :param theta2: int or float: End angle for the wedge
    :param hrd_inset: boolean, if set, add an inset HRD where the location of the current model is indicated with a
    circle.
    :param show_total_mass: boolean, default False, display the value of the total mass of the model below the circle
    :param show_surface: boolean, default True, if set, show the outer boundary of the stellar object
    :param show_grid: boolean, default False, if set, add additional axes in crosshair form
    :param output_fname: str, name of the output file
    :param anim_fmt: str, format to use for saving an animation
    time_scale_type: str, one of "model_number", "linear", or "log_to_end"
    For model_number, the time follows the moment when a new MESA model was saved.
    For linear, the time follows linear steps in star_age.
    For log_time_to_end, the time axis is tau = log10(t_final - t), where t_final is the final star_age of the model
    :return: fig, ax
    """
    if fig is None:
        fig = plt.figure()
        fig.set_size_inches(fig_size)
    if ax is None:
        ax = plt.gca()

    start_ind, end_ind, ind_step = check_time_indeces(time_ind, m.hist.star_age)

    r = m.hist.data[raxis]

    # Set axis limits
    if axis_lim == -99:
        axis_lim = 1.1 * r.max()

    # replace smallest values with constant ratio
    smallest_radius_ratio = 0.01
    too_small = (r / axis_lim < smallest_radius_ratio)
    if np.any(too_small):
        r[too_small] = axis_lim * smallest_radius_ratio

    # Show energy and mixing regions
    burn_wedges_list = []
    mix_wedges_list = []
    p = mp.plot(rcparams_fixed=False)
    cmap = p.mergeCmaps([plt.cm.Purples_r, plt.cm.hot_r], [[0.0, 0.5], [0.5, 1.0]])
    qtop = "burn_qtop_"
    qtype = "burn_type_"
    try:
        m.hist.data[qtop + "1"]
    except ValueError:
        raise KeyError(
            "No field " + qtop + "* found, add mixing_regions 40 and burning_regions 40 to your history_columns.list")

    # Automatic colorbar limits
    if cmin == cmax:
        cmin = m.hist.data[qtop + "1"].min()
        cmax = m.hist.data[qtop + "1"].max()

    # Plot energy production / loss zones
    num_burn_zones = int([xx.split('_')[2] for xx in m.hist.data.dtype.names if qtop in xx][-1])
    width = 0
    sm = m.hist.star_mass
    norm = Normalize(vmin=cmin, vmax=cmax)
    for region in range(1, num_burn_zones + 1):
        # Plot burning regions
        radius = np.abs(m.hist.data[qtop + str(region)][start_ind] * sm[start_ind])
        burn = m.hist.data[qtype + str(region)][start_ind]
        # Width = current radius - previous radius
        width += radius
        color = cmap(norm(burn))
        # Center zone should be a circle, not a ring
        if region == 1:
            width = None
        wedge = Wedge((0, 0), radius, width=width, zorder=-region, color=color, theta1=theta1,
                      theta2=theta2)
        ax.add_artist(wedge)
        burn_wedges_list.append(wedge)
        width = -1 * radius

    # Plot mixing
    if show_mix:
        mix_qtop = "mix_qtop_"
        mix_qtype = "mix_type_"
        try:
            m.hist.data[qtop + "1"]
        except ValueError:
            raise KeyError(
                "No field " + qtop + "* found, add mixing_regions 40 and burning_regions 40 to your history_columns.list")

        num_mix_zones = int([xx.split('_')[2] for xx in m.hist.data.dtype.names if mix_qtop in xx][-1])
        width = 0
        sm = m.hist.star_mass
        norm = Normalize(vmin=cmin, vmax=cmax)

        legend_elements = []
        legend_names = []
        for region in range(1, num_mix_zones + 1):
            # Plot mixing regions
            radius = np.abs(m.hist.data[mix_qtop + str(region)][start_ind] * sm[start_ind])
            mix = m.hist.data[mix_qtype + str(region)][start_ind]
            # Width = current radius - previous radius
            width += radius
            hatch = MIX_HATCHES[int(mix)]
            # Center zone should be a circle, not a ring
            if region == 1:
                width = None
            wedge = Wedge((0, 0), radius, width=width, zorder=-region, hatch=hatch,
                          color="grey", alpha=0.8, lw=1, fill=False, theta1=theta1, theta2=theta2)
            ax.add_artist(wedge)
            mix_wedges_list.append(wedge)
            width = -1 * radius
            # Show legend
            if show_mix_legend:
                if mix > 0 and MIX_TYPES[int(mix)] not in legend_names:
                    legend_elements.append(
                        Patch(facecolor=None, hatch=hatch, edgecolor="grey", alpha=0.8, fill=False))
                    legend_names.append(MIX_TYPES[int(mix)])
        if show_mix_legend:
            ax.legend(legend_elements, legend_names, loc="upper right")

    # Add time label
    if show_time_label:
        time = m.hist.star_age[start_ind]
        text = add_time_label(time, ax, time_label_loc=time_label_loc, time_unit=time_unit)

    # Add crosshair
    if show_grid:
        #TODO: add grid
        pass

    if hrd_inset:
        axins, point = add_inset_hrd(m, ax=ax, time_index=start_ind)

    # Add mass label in lower right corner
    if show_total_mass:
        mass_text = ax.text(0.75 * axis_lim, -0.95 * axis_lim, "{}".format(round(m.hist.star_mass[start_ind], 1)) +
                            "$\,\\rm{M}_{\odot}$")

    # Add color-bar
    if show_colorbar:
        sm_colorbar = plt.cm.ScalarMappable(cmap=cmap, norm=Normalize(vmin=cmin, vmax=cmax))
        # fake up the array of the scalar mappable
        sm_colorbar.set_array(m.hist.data[qtype + '1'])
        cb = colorbar(sm_colorbar, ax=ax)
        cb.set_label(cbar_label)
        if cbar_label == "":
            cb.set_label('$\\log_{10}$ "energy generation/loss rate"')

    if show_surface:
        surface = Wedge((0, 0), r[start_ind], theta1=theta1, theta2=theta2, fill=False, facecolor="#FFFDE7",
                        edgecolor='k', lw=1.1)
        ax.add_artist(surface)

    # Set axis for plotting correctly sized circles
    ax.set_xlim([-axis_lim, axis_lim])
    ax.set_ylim([-axis_lim, axis_lim])
    ax.set_aspect('equal', adjustable='box')

    # Set axis and tick labels
    set_axis_ticks_and_labels(ax, raxis="star_mass", axis_label=axis_label)

    # Create animation
    if end_ind != start_ind:
        # Create animation
        indices = range(start_ind, end_ind, ind_step)
        indices = rescale_time(indices, m, time_scale_type=time_scale_type)
        r = r[indices]
        t = m.hist.star_age[indices]

        frames = len(indices)
        fps = fps
        bar = tqdm(total=frames)

        def init():
            wedge.radius = r[0]
            time = (t[0] * u.yr).to(time_unit)
            text.set_text("t = " + time.round(3).to_string())
            for artist in burn_wedges_list:
                ax.add_patch(artist)
            if show_mix:
                for artist in mix_wedges_list:
                    ax.add_patch(artist)
            return wedge, point, burn_wedges_list, mix_wedges_list

        def animate(ind):
            bar.update()
            time = (t[ind] * u.yr).to(time_unit)
            r_cur = r[ind]
            wedge.radius = r_cur
            log_teff = m.hist.log_Teff[indices]
            log_l = m.hist.log_L[indices]
            star_mass = m.hist.star_mass[indices]

            # Add burning
            width = 0
            for artist, region in zip(burn_wedges_list, range(1, num_burn_zones + 1)):
                # Plot burning regions
                radius = np.abs(m.hist.data[qtop + str(region)][indices][ind] * r_cur)
                burn = m.hist.data[qtype + str(region)][indices][ind]
                # Width = current radius - previous radius
                width += radius
                # Center zone should be a circle, not a ring
                if region == 1:
                    width = None
                color = cmap(norm(burn))

                # Change current artist
                artist.set_radius(radius)
                artist.set_color(color)
                artist.set_width(width)

                # Width = current radius - previous radius
                width = -1 * radius

            # Add mixing
            if show_mix:
                for mix_artist, region in zip(mix_wedges_list, range(1, num_mix_zones + 1)):
                    # Plot mixing regions
                    radius = np.abs(m.hist.data[mix_qtop + str(region)][ind] * r_cur)
                    mix = m.hist.data[mix_qtype + str(region)][indices][ind]
                    # Width = current radius - previous radius
                    width += radius
                    hatch = MIX_HATCHES[int(mix)]
                    # Center zone should be a circle, not a ring
                    if region == 1:
                        width = None

                    # Change current artist
                    mix_artist.set_radius(radius)
                    mix_artist.set_hatch(hatch)
                    mix_artist.set_width(width)
                    width = -1 * radius

            # Add time location
            text.set_text("t = " + time.round(3).to_string())

            if hrd_inset:
                point.set_data(log_teff[ind], log_l[ind])

            if show_total_mass:
                mass_text.set_text("{}".format(round(star_mass[ind], 1)) + "$\,\\rm{M}_{\odot}$")

            if show_surface:
                surface.set_radius(r_cur)

            return wedge, point, burn_wedges_list, mix_wedges_list

        print("Creating movie...")
        ani = FuncAnimation(fig, animate, init_func=init, frames=frames, interval=1000 / fps, blit=False, repeat=False)
        # Save animation
        ani.save(output_fname + anim_fmt, writer="ffmpeg", extra_args=['-vcodec', 'libx264'])
    return fig, ax


def property_profile(m, time_ind=-1, property_name="logRho", num_rings=-1, raxis="mass", log=False, log_low_lim=-2.1,
                     fps=10, fig=None, ax=None, show_time_label=True, time_label_loc=(), time_unit="Myr",
                     fig_size=(5.5, 4), axis_lim=-99, axis_label="", show_colorbar=True,
                     cmin=0, cmax=0, cbar_label="", theta1=0, theta2=360, hrd_inset=True, show_total_mass=True,
                     show_surface=True, show_grid=False, output_fname="property_profile", anim_fmt=".mp4"):

    """
    Represent the model of a stellar object as circle with radius raxis. The circle is divided into rings whose color
    reflect the values of a physical property of the model.
    Requires MESA profile files that contain this property and the corresponding MESA history file.
    :param m: mesaPlot object, already loaded a history file
    :param time_ind: int or tuple (start_index, end_index, step=1) or (start_index, end_index, step);
    if int: create the plot at the index time_ind. If tuple: create an animation from start index to end index with
    intervals of step.
    :param property_name: string, property of a MESA profile to be shown as colors
    :param num_rings: int, default -1, if greater than -1, limit the number of rings to this number
    :param raxis: str, default axis to use as radius of the circle.
    :param log: boolean, if set, show the natural logarithm of the property
    :param fps: int, number of frames per second for the animation
    :param fig: Figure object. If set, plot on existing figure
    :param ax: Axes object. If set, plot on provided axis
    :param show_time_label: boolean, if set, insert a label that gives the age of the stellar object (in Myr)
    :param time_label_loc: tuple, location of the time label on the plot as fraction of the maximal size
    :param time_unit: str, valid astropy time unit, default Myr
    :param fig_size: tuple, size of the figure in inches
    :param axis_lim: float, value to set for the maximum limit of the x and y axis.
    :param axis_label: str, label of the x and y labels
    :param show_colorbar: boolean, if set, add a colorbar corresponding to the property shown
    :param cmin: float, minimum value to set for the colorbar
    :param cmax: float, maximum value to set for the colorbar, if smaller or equal to cmin, use the minimum and
    maximum values of property_name instead
    :param cbar_label: str, label to set for the colorbar
    :param theta1: int or float: Start angle for the wedge
    :param theta2: int or float: End angle for the wedge
    :param hrd_inset: boolean, if set, add an inset HRD where the location of the current model is indicated with a
    circle.
    :param show_total_mass: boolean, default False, display the value of the total mass of the model below the circle
    :param show_surface: boolean, default True, if set, show the outer boundary of the stellar object
    :param show_grid: boolean, default False, if set, add additional axes in crosshair form
    :param output_fname: str, name of the output file
    :param anim_fmt: str, format to use for saving an animation
    :return: fig, ax
    """
    if fig is None:
        fig = plt.figure()
        fig.set_size_inches(fig_size)
    if ax is None:
        ax = plt.gca()

    start_ind, end_ind, ind_step = check_time_indeces(time_ind, m.hist.star_age)
    prof = find_profile(m, time_ind=start_ind)
    r = prof.data[raxis]
    prop = prof.data[property_name][:]

    automatic_limits = False
    # Set axis limits
    if axis_lim == -99:
        axis_lim = 1.1 * r.max()
        automatic_limits = True

    # Automatic colorbar limits
    if cmin == cmax:
        if log:
            # Replace zero and negative values with fill value
            prop[prop <= 0] = 1e-5
            cmin = np.log10(prop.min())
            cmax = np.log10(prop.max())
        else:
            cmin = prop.min()
            cmax = prop.max()

    # Plot a quantity as colored rings inside a stellar structure
    wedges_list = make_property_plot(ax, prof, property_name, raxis, log=log, cmin=cmin, cmax=cmax, num_rings=num_rings,
                                     theta1=theta1, theta2=theta2)

    # Add time label
    if show_time_label:
        time = prof.star_age
        text = add_time_label(time, ax, time_label_loc=time_label_loc, time_unit=time_unit)

    # Set axis for plotting correctly sized circles
    ax.set_xlim([-axis_lim, axis_lim])
    ax.set_ylim([-axis_lim, axis_lim])
    ax.set_aspect('equal', adjustable='box')

    # Add axis label
    set_axis_ticks_and_labels(ax, raxis=raxis, axis_label=axis_label)

    # Add annotations
    # add_ring_annotations(ax, rmax=prof.star_mass, show_percentage=True, show_fraction_labels=False)

    # Add crosshair
    if show_grid:
        #TODO: add grid
        pass

    if hrd_inset:
        axins, point = add_inset_hrd(m, ax=ax, time_index=start_ind)

    # Add mass label
    if show_total_mass:
        mass_text = ax.text(-0.25, -0.97 * axis_lim, "{}".format(round(prof.star_mass, 1)) + "$\,\\rm{M}_{\odot}$")

    # Add colorbar
    if show_colorbar:
        if num_rings > -1:
            selec = [int(i) for i in np.linspace(0, len(prof.mass) - 1, num_rings)]
            prop = prop[selec]
        cmap = plt.get_cmap("plasma", len(prop))
        norm = Normalize(vmin=cmin, vmax=cmax)
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=Normalize(vmin=cmin, vmax=cmax))
        # fake up the array of the scalar mappable
        sm.set_array(prof.data[property_name])
        bar = colorbar(sm, ax=ax)
        if cbar_label == "":
            cbar_label = property_name.replace("_", "")
            if log:
                cbar_label = "log " + cbar_label
        bar.set_label(cbar_label)

    if show_surface:
        surface = Wedge((0, 0), r.max(), theta1=theta1, theta2=theta2, fill=False, facecolor="#FFFDE7",
                        edgecolor='k', lw=1.1)
        ax.add_artist(surface)

    # Create animation
    if end_ind != start_ind:
        def init():
            for w in wedges_list:
                ax.add_patch(w)
            if show_time_label:
                time = (prof.star_age * u.yr).to(time_unit)
                text.set_text("t = " + time.round(3).to_string())
            if show_total_mass:
                mass_text.set_text("".format(round(prof.star_mass, 1)) + "$\,\\rm{M}_{\odot}$")
            if show_surface:
                surface.set_radius(r.max())
                ax.add_artist(surface)
            return wedges_list

        def animate(i):
            bar.update()
            prof = prof_list[i]
            r = prof.data[raxis][:]
            reversed = False
            if raxis != "mass" and raxis != "radius":
                if not reversed:
                    r = r[::-1]
                    reversed = True
            prop = prof.data[property_name][:]
            if num_rings > -1:
                selec = [int(i) for i in np.linspace(0, len(prof.mass) - 1, num_rings)]
                r = r[selec]
                prop = prop[selec]
            if log:
                prop = np.log10(prop)
            width = 0
            for ind, w in enumerate(wedges_list):
                radius = r[ind]
                w.set_radius(radius)
                # Plot rings
                value = prop[ind]
                # Width = current radius - previous radius
                width += radius
                # Center zone should be a circle, not a ring
                if ind == 0:
                    width = None
                w.set_width(width)
                w.set_color(cmap(norm(value)))
                width = -1 * radius
            # Update time label
            if show_time_label:
                time = (prof.star_age * u.yr).to(time_unit)
                text.set_text("t = " + time.round(3).to_string())

            if show_total_mass:
                mass_text.set_text("{}".format(round(prof.star_mass, 1)) + "$\,\\rm{M}_{\odot}$")

            if hrd_inset:
                point.set_data(np.log10(prof.Teff), np.log10(prof.luminosity[0]))
            if show_surface:
                surface.set_radius(r.max())
            if automatic_limits:
                # Update axis size to follow changes in radius
                axis_lim = 1.1 * r.max()
                ax.set_xlim([-axis_lim, axis_lim])
                ax.set_ylim([-axis_lim, axis_lim])
                ax.set_aspect('equal', adjustable='box')
        # Create animation
        ip = m.iterateProfiles(rng=[m.hist.model_number[start_ind], m.hist.model_number[end_ind]], step=ind_step)
        count = 0
        prof_list = []
        print("Loading profiles, this may take some time...")
        bar0 = tqdm()

        for i in ip:
            prof_list.append(m.prof)
            count += 1
            bar0.update()

        bar = tqdm()
        print("Creating movie...")
        ani = FuncAnimation(fig, animate, init_func=init, frames=count, interval=1000 / fps, blit=False, repeat=False)

        # Save animation
        # Fix issues with directory name
        ani.save(output_fname + anim_fmt, writer="ffmpeg", extra_args=['-vcodec', 'libx264'])

    return fig, ax


def chemical_profile(m, time_ind=-1, isotope_list=None, num_rings=-1, scale=-1, width=0.03, raxis="mass",
                     show_ring_annotations=True, fps=10, fig=None, ax=None, show_time_label=True, time_label_loc=(),
                     time_unit="Myr", fig_size=(5.5, 4), axis_lim=1.05, axis_label="", show_colorbar=True,
                     cbar_label="", show_legend=False, counterclock=True, startangle=90, hrd_inset=True,
                     show_total_mass=True, show_surface=False, output_fname="chemical_profile", anim_fmt=".mp4"):
    """
    Represent the model of a stellar object as a circle with radius raxis. The circle contains nested pie charts that
    show the composition of the star at a certain mass or radius coordinate.
    Requires MESA profile files that contain the profiles of certain isotopes, such as "h1" and the corresponding MESA
    history file.
    :param m: mesaPlot object, already loaded a history file
    :param time_ind: int or tuple (start_index, end_index, step=1) or (start_index, end_index, step);
    if int: create the plot at the index time_ind. If tuple: create an animation from start index to end index with
    intervals of step.
    :param isotope_list: None or list or np.array of str containing the names of isotopes to be included
    :param num_rings: int, default -1, if greater than -1, limit the number of nested pie charts to this number
    :param scale: float, value to scale the circle to. if negative, use the maximum value of the raxis
    :param width: minimum width of a nested pie chart ring
    :param raxis: str, default axis to use as radius of the circle.
    :param show_ring_annotations: boolean, if set add concentric rings on top of the nested pie charts
    :param fps: int, number of frames per second for the animation
    :param fig: Figure object. If set, plot on existing figure
    :param ax: Axes object. If set, plot on provided axis
    :param show_time_label: boolean, if set, insert a label that gives the age of the stellar object (in Myr)
    :param time_label_loc: tuple, location of the time label on the plot as fraction of the maximal size
    :param time_unit: str, valid astropy time unit, default Myr
    :param fig_size: tuple, size of the figure in inches
    :param axis_lim: float, value to set for the maximum limit of the x and y axis.
    :param axis_label: str, label of the x and y labels
    :param show_colorbar: boolean, if set, add a colorbar that gives the isotopes and corresponding colors.
    Note: cancels show_legend
    :param cbar_label: str, label to set for the colorbar
    :param show_legend: boolean, if set show legend for the isotopes and their corresponding color.
    Note: cancels show_colorbar
    :param counterclock: boolean, if set, plot the isotopes counterclockwise
    :param startangle: int or float: angle in degrees from the horizontal line at which to start plotting the isotopes.
    :param hrd_inset: boolean, if set, add an inset HRD where the location of the current model is indicated with a
    circle.
    :param show_total_mass: boolean, default False, display the value of the total mass of the model below the circle
    :param show_surface: boolean, default True, if set, show the outer boundary of the stellar object
    :param show_grid: boolean, default False, if set, add additional axes in crosshair form
    :param output_fname: str, name of the output file
    :param anim_fmt: str, format to use for saving an animation
    :return: fig, ax
    """
    if fig is None:
        fig = plt.figure()
        fig.set_size_inches(fig_size)
    if ax is None:
        ax = plt.gca()

    start_ind, end_ind, ind_step = check_time_indeces(time_ind, m.hist.star_age)
    prof = find_profile(m, time_ind=start_ind)
    r = prof.data[raxis]
    if scale < 0:
        # Set automatic value for the scale
        scale = r.max()

    # Create nested pie charts of isotopes
    isotope_list, artist_list = make_pie_composition_plot(ax, prof, startangle=startangle, raxis=raxis,
                                                          elem_list=isotope_list,
                                                          counterclock=counterclock, num_rings=num_rings,
                                                          scale=scale, width=width)
    # Add annotations
    rmax = np.sqrt(r.max()) / np.sqrt(scale)
    if show_ring_annotations:
        c_list, fll, r_list, pll = add_ring_annotations(ax, rmax=rmax, show_percentage=True, show_fraction_labels=False,
                                                        startangle=startangle)

    # Add time label
    if show_time_label:
        time = prof.star_age
        text = add_time_label(time, ax, time_label_loc=time_label_loc, time_unit=time_unit)

    # Set axis for plotting correctly sized circles
    ax.set_xlim([-axis_lim, axis_lim])
    ax.set_ylim([-axis_lim, axis_lim])
    ax.set_aspect('equal', adjustable='box')

    # Add axis label - no default values for axis label
    ax.set_xlabel(axis_label)
    ax.set_ylabel(axis_label)

    # Make sure to show the axis frame
    ax.set(frame_on=True)

    if hrd_inset:
        axins, point = add_inset_hrd(m, ax=ax, time_index=start_ind)

    # Add mass label
    if show_total_mass:
        mass_text = ax.text(0.65 * axis_lim, -0.97 * axis_lim, "{}".format(round(prof.star_mass, 1)) + "$\,\\rm{M}_{\odot}$")

    # Add color bar or legend for isotopes
    if show_colorbar or show_legend:
        # TODO: add colorbar or legend for chemical profile plots
        pass

    if show_surface:
        surface = Wedge((0, 0), rmax, theta1=0, theta2=360, fill=False, facecolor="#FFFDE7",
                        edgecolor='k', lw=1.1, zorder=600)
        ax.add_artist(surface)

    # Create animation
    if end_ind != start_ind:
        def init():
            if show_time_label:
                time = (prof.star_age * u.yr).to(time_unit)
                text.set_text("t = " + time.round(3).to_string())
            for pie in artist_list:
                for w in pie:
                    ax.add_patch(w)
            if show_total_mass:
                mass_text.set_text("".format(round(prof.star_mass, 1)) + "$\,\\rm{M}_{\odot}$")
            if show_surface:
                surface.set_radius(r.max())
            return artist_list

        def animate(i):
            bar.update()
            prof = prof_list[i]
            selec = [int(x) for x in np.linspace(0, len(prof.mass) - 1, num_rings)]
            data = prof.data[selec]
            masses = prof.data[raxis][selec]

            # Update pie charts
            radius = np.sqrt(masses) / np.sqrt(scale)
            if raxis[:3] == "log":
                shift = masses.min() + 1e-7
                radius = np.sqrt(np.abs(masses - shift)) / np.sqrt(np.abs(scale - shift))
            for ind, r_i in enumerate(radius):
                factor = 1
                if ind == len(masses) - 1:
                    factor *= -1
                theta1 = factor * startangle / 360.0

                for elem, w in zip(isotope_list, artist_list[ind]):
                    frac = data[elem][ind]
                    theta2 = (theta1 + frac) if counterclock else (theta1 - frac)
                    w.set_theta1(360. * min(theta1, theta2))
                    w.set_theta2(360. * max(theta1, theta2))
                    w.set_radius(r_i)
                    theta1 = theta2
            # Update time label
            if show_time_label:
                time = (prof.star_age * u.yr).to(time_unit)
                text.set_text("t = " + time.round(3).to_string())

            # Update annotations
            rmax = np.sqrt(masses.max()) / np.sqrt(scale)
            if show_ring_annotations:
                for ind, c in enumerate(c_list):
                    f = FRACTION_LIST[ind]
                    c.set_radius(f * rmax)
                for ind, rad in enumerate(r_list):
                    p = PERCENTAGE_LIST[ind]
                    x = rmax * np.sin(-p * 2 * np.pi)
                    y = rmax * np.cos(-p * 2 * np.pi)
                    rad.set_data([0, x], [0, y])

            if show_total_mass:
                mass_text.set_text("{}".format(round(prof.star_mass, 1)) + "$\,\\rm{M}_{\odot}$")

            if hrd_inset:
                point.set_data(np.log10(prof.Teff), np.log10(prof.luminosity[0]))

            if show_surface:
                surface.set_radius(rmax)

        # Create animation
        ip = m.iterateProfiles(rng=[m.hist.model_number[start_ind], m.hist.model_number[end_ind]], step=ind_step)
        count = 0
        prof_list = []
        print("Loading profiles, this may take some time...")
        bar0 = tqdm()

        for i in ip:
            prof_list.append(m.prof)
            count += 1
            bar0.update()

        bar = tqdm()
        print("Creating movie...")
        ani = FuncAnimation(fig, animate, init_func=init, frames=count, interval=1000 / fps, blit=False, repeat=False)

        # Save animation
        # Fix issues with directory name
        ani.save(output_fname + anim_fmt, writer="ffmpeg", extra_args=['-vcodec', 'libx264'])

    return fig, ax


def animated_hist_comp_test(m1, m2, fig=None, ax=None, raxis="log_R", label1="", label2="", time_index1=0,
                            time_index2=0, hrd_inset=True):
    """
    Plot two MESA models at the same time as half-circles with radius r over the same evolutionary time.
    :param label2:
    :param label1:
    :param time_index2:
    :param m1: mesaPlot object, already loaded a history file
    :param m2: second mesaPlot object, already loaded a history file
    :param fig: Figure object. If set, plot on existing figure
    :param ax: Axes object. If set, plot on provided axis
    :param raxis: str, valid column name for a MESA history file. This sets the outer radius of the star.
    :param time_label_loc: tuple, location of the time label on the plot as fraction of the maximal size
    :param time_index: int, contains time index of moment to plot
    :param hrd_inset: boolean, if set, add an inset HRD that indicates the current time index to each plot.
    :return: fig, ax
    :return: fig, ax
    """
    if fig is None:
        fig = plt.figure()
        fig.set_size_inches(11, 9)
    if ax is None:
        ax = plt.gca()

    # Normalize the radius from something small but still visible to something large
    # that still fits inside the plot
    r1 = m1.hist.data[raxis][:]   # Create a copy of the array to prevent changes to data
    t1 = m1.hist.star_age
    r2 = m2.hist.data[raxis][:]  # Create a copy of the array to prevent changes to data
    t2 = m2.hist.star_age
    lim = 1.1 * np.max([r1.max(), r2.max()])     # Adapt upper limit maximal radius
    # replace smallest values with constant ratio of 0.003
    smallest_radius_ratio = 0.01
    too_small1 = (r1/lim < smallest_radius_ratio)
    too_small2 = (r2 / lim < smallest_radius_ratio)
    if np.any(too_small2):
        r1[too_small1] = lim * smallest_radius_ratio
        r2[too_small2] = lim * smallest_radius_ratio

    # Add center circle, color is given by T_eff
    colors_ary1 = teff2rgb(10 ** m1.hist.log_Teff)
    colors_ary2 = teff2rgb(10 ** m2.hist.log_Teff)
    color1 = colors_ary1[time_index1]
    color2 = colors_ary2[time_index2]
    wedge1 = Wedge((0, 0), r1[time_index1], 90, 270, width=None, facecolor=color1,
                   edgecolor="k")
    ax.add_artist(wedge1)
    wedge2 = Wedge((0, 0), r2[time_index2], 270, 90, width=None, facecolor=color2,
                   edgecolor="k")
    ax.add_artist(wedge2)

    # Add dashed line to separate both models
    ax.plot([0, 0], [-lim, lim], ls='-', color='grey')

    # Add labels for both models
    ax.text(-lim / 2., 0.88 * lim, label1)
    ax.text(lim / 2., 0.88 * lim, label2)

    # Set axis for plotting correctly sized circles
    ax.set_xlim([-lim, lim])
    ax.set_ylim([-lim, lim])
    ax.set_aspect('equal', adjustable='box')

    set_axis_ticks_and_labels(ax, raxis=raxis)

    if hrd_inset:
        add_inset_hrd(m1, ax=ax, time_index=time_index1)
        add_inset_hrd(m2, ax=ax, time_index=time_index1, loc=4)
    return fig, ax


def animated_hist_comp(m1, m2, raxis="log_R", label1="", label2="", time_index_start1=0, time_index_start2=0,
                       time_index_end1=-1, time_index_end2=-1, time_indices=None, frames=200, fps=10,
                       plot_name_base="mesarings_comp_", plot_dir=".", hrd_inset=True,
                       fig_size=(11, 9)):
    # TODO: find out how to compute same indices. Make sure they have the same size
    # Idea: Scale model number from 0 to 1 and use same fractional time
    # TODO: Accept negative indices
    indices1 = np.linspace(time_index_start1, time_index_end1, frames, dtype=int)
    indices2 = np.linspace(time_index_start2, time_index_end2, frames, dtype=int)

    # Normalize the radius from something small but still visible to something large
    # that still fits inside the plot
    r1 = m1.hist.data[raxis][indices1]   # Create a copy of the array to prevent changes to data
    log_teff1 = m1.hist.log_Teff[indices1]
    log_l1 = m1.hist.log_L[indices1]
    # Second half
    r2 = m2.hist.data[raxis][indices2]  # Create a copy of the array to prevent changes to data
    log_teff2 = m2.hist.log_Teff[indices2]
    log_l2 = m2.hist.log_L[indices2]
    lim = 1.1 * np.max([r1.max(), r2.max()])     # Adapt upper limit maximal radius
    colors_ary1 = teff2rgb(10 ** log_teff1)
    colors_ary2 = teff2rgb(10 ** log_teff2)
    # replace smallest values with constant ratio of 0.003
    # TODO: Fix smallest radius
    smallest_radius_ratio = 0.08
    too_small1 = (r1 / lim < smallest_radius_ratio)
    too_small2 = (r2 / lim < smallest_radius_ratio)
    if np.any(too_small2):
        r1[too_small1] = lim * smallest_radius_ratio
        r2[too_small2] = lim * smallest_radius_ratio

    # Check if directory exists already, otherwise create a new one
    if not path.exists(plot_dir):
        makedirs(plot_dir)

    # Create initial figure
    fig = plt.figure(figsize=fig_size)
    ax = plt.gca()

    # Set axis for plotting correctly sized circles
    ax.set_xlim([-lim, lim])
    ax.set_ylim([-lim, lim])
    ax.set_aspect('equal', adjustable='box')

    set_axis_ticks_and_labels(ax, raxis=raxis)

    # Initial half-stars
    wedge1 = Wedge((0, 0), r1[0], 90, 270, width=None, facecolor=colors_ary1[0],
                   edgecolor="k")
    wedge2 = Wedge((0, 0), r2[0], 270, 90, width=None, facecolor=colors_ary2[0],
                   edgecolor="k")
    # Add inset
    axins1, axins2, point1, point2 = None, None, None, None  # intialize
    if hrd_inset:
        axins1, point1 = add_inset_hrd(m1, ax=ax, time_index=0, indices=indices1)
        axins2, point2 = add_inset_hrd(m2, ax=ax, time_index=0, indices=indices2, loc=4)

    # Add dashed line to separate both models
    ax.plot([0, 0], [-lim, lim], ls='-', color='grey')

    # Add labels for both models
    ax.text(-lim / 2., 0.88 * lim, label1)
    ax.text(lim / 2., 0.88 * lim, label2)

    def init():
        wedge1.set_radius(r1[0])
        wedge2.set_radius(r2[0])
        wedge1.set_facecolor(colors_ary1[0])
        wedge2.set_facecolor(colors_ary2[0])
        ax.add_patch(wedge1)
        ax.add_patch(wedge2)
        return wedge1, wedge2, point1, point2

    def animate(ind):
        bar.update()
        wedge1.set_radius(r1[ind])
        wedge2.set_radius(r2[ind])
        wedge1.set_facecolor(colors_ary1[ind])
        wedge2.set_facecolor(colors_ary2[ind])

        if hrd_inset:
            point1.set_data(log_teff1[ind], log_l1[ind])
            point2.set_data(log_teff2[ind], log_l2[ind])

        return wedge1, wedge2, point1, point2

    # Create animation
    bar = tqdm(total=frames)

    # TODO: Fix frames to match length of arrays
    ani = FuncAnimation(fig, animate, init_func=init, frames=frames, interval=1000 / fps, blit=False, repeat=False)
    # Save animation
    # Fix issues with directory name
    if plot_dir[-1] != '/':
        plot_dir += '/'
    # Fix issue with plot name
    if plot_name_base[-1] != '_':
        plot_name_base += '_'
    ani.save(plot_dir + plot_name_base + "movie.mp4", writer="ffmpeg", extra_args=['-vcodec', 'libx264'])

# ----------- Helper functions ----------------------


def find_profile(m, time_ind=0):
    """
    m : mesaPlot object
    time_ind: int, index of mesaPlot history
    Load the MESA profile closest to the time_ind given
    """
    model_number = m.hist.model_number[time_ind]
    m.loadProfile(num=model_number)
    return m.prof

def find_closest(ary, value):
    return np.abs(ary - value).argmin()

def set_axis_ticks_and_labels(ax, raxis="star_mass", axis_label=""):
    """
    Format the axis ticks such that no negative values are shown and
    :param ax: matplotlib axis object
    :param raxis: str, valid column name for a MESA history file. This sets the value used for the outer radius of the
     star.
    :param axis_label: str, user defined axis label
    :return:
    """
    # Set axis properties
    label = axis_label

    if label == "":
        label = raxis
        if raxis == "log_R" or raxis == "radius":
            label = "Radius" + "$ \,[\\rm{R}_\odot]$"
        elif raxis == "star_mass" or raxis == "mass":
            label = "Mass" + "$\,[\\rm{M}_\odot]$"
        elif "_" in label:
            label = label.replace("_", " ")
    ax.set_xlabel(label)
    ax.set_ylabel(label)

    # Change y tick labels
    if raxis[:3] == "log":
        ticks = ax.get_yticks()
        new_ticks = ['{:.0f}'.format(abs(np.sign(t)) * 10 ** abs(t)) for t in ticks]
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        ax.set_yticklabels(new_ticks)
        ax.set_xticklabels(new_ticks)
    else:
        ticks = ax.get_yticks()
        new_ticks = ['{:.1f}'.format(abs(t)) for t in ticks]
        ax.set_yticklabels(new_ticks)
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        ax.set_xticklabels(new_ticks)


def add_inset_hrd(m, time_index=100, ax=None, axins=None, fraction="20%", indices=None,
                  loc="lower left", bbox_to_anchor=None):
    """
    Add an inset HRD to a plot that highlights the current time-step
    :param m: mesaPlot object
    :param ax: axis object
    :param indices: None, list or ndarray, selected indices for plotting
    :param fraction: string, fraction of the parent axis used for setting the size of the inset
    :param axins: None or Axes, if provided, inset axis to use
    :param time_index: int, time index to highlight on inset plot
    :param loc: str or int, matpltolib location to put the inset axis on the parent axis
    :param bbox_to_anchor: tuple x, y, width height
    :return: (axins, point) Axes, created inset axis, and the point moving on the plot
    """
    # TODO: adapt to only show chosen range of time_ind
    if ax is None:
        ax = plt.gca()
    if indices is None:
        indices = np.arange(len(m.hist.log_Teff))

    if axins is None:
        axins = inset_axes(ax,
                           width=fraction,  # width = % of parent_bbox
                           height=fraction,  # height : 1 inch
                           loc=loc,
                           bbox_to_anchor=bbox_to_anchor
                           )
        axins.invert_xaxis()
        # move axis ticks
        axins.tick_params(axis='y', which='both', labelright=True, labelleft=False, direction='in')
        axins.tick_params(axis='x', which='both', labeltop=True, labelbottom=False, direction='in')
        axins.yaxis.set_ticks_position('right')
        axins.xaxis.set_ticks_position('top')
        axins.xaxis.set_ticks([])
        axins.yaxis.set_ticks([])
        # fix the number of ticks on the inset axes
        axins.yaxis.get_major_locator().set_params(nbins=3)
        axins.xaxis.get_major_locator().set_params(nbins=3)
        # Add labels
        # axins.set_xlabel("$\log_{10}T_{\\rm{eff}}$")
        # axins.set_ylabel("$\log_{10}L$", rotation=-90, labelpad=20)
        # axins.yaxis.set_label_position('right')
        # axins.xaxis.set_label_position('top')
        # For better output, use all the models within the range selected for the background evolution on the HRD
        axins.plot(m.hist.log_Teff[indices[0]:indices[-1] + 1], m.hist.log_L[indices[0]:indices[-1] + 1], "b", lw=1.25)

    # Add marker for current location
    point, = axins.plot([m.hist.log_Teff[indices][time_index]], [m.hist.log_L[indices][time_index]], ls=None,
                        marker="o", color="yellow", mec="k", mew=1, alpha=0.6)
    return axins, point


def teff2rgb(t_ary):
    """
    Convert effective temperature to rgb colors using colorpy
    :param t_ary: temperature array in K
    :return:
    """
    rgb_list = []
    for t in t_ary:
        rgb_list.append(colormodels.irgb_string_from_xyz(blackbody.blackbody_color(t)))
    return rgb_list


def colorbar(mappable, ax=None, **kwargs):
    # Trick from Joseph Long
    if ax is None:
        ax = mappable.axes
    fig = ax.figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    return fig.colorbar(mappable, cax=cax, **kwargs)


def make_pie_composition_plot(ax, prof, num_rings=0, scale=11.0, width=0.01, startangle=90,
                              elem_list=None, cmap=None, counterclock=True, raxis="mass", boundary=0, log_low_lim=-2.1):
    """
    Create a composition plot showing the percentage of composition for each element in each layer of the star
    :param ax: axis object
    :param prof: mesaPlot profile object
    :param num_rings: number of rings to plot on the
    :param scale: float, value to scale the plot to.
    :param width: float, width of each nested piechart
    :param startangle: float, value of the angle to start with for the piecharts
    :param elem_list: None or list list of isotopes to take into account
    :param counterclock : bool, optional, default: True, Specify fractions direction, clockwise or counterclockwise.
    :return:
    """
    if elem_list is None:
        p = mp.plot(rcparams_fixed=False)
        elem_list = p._listAbun(prof)
        if len(elem_list) == 22:
            elem_list = ELEM_BASE
        elif len(elem_list) == 129:
            elem_list = np.hstack([ELEM_BASE[:-3], ELEM_HEAVY])
    if cmap is None:
        if len(elem_list) == 13:
            inds_ar_ca_fe = np.array([6, 15, 54])
            cmap_list = np.vstack((CMAP_BASE(np.linspace(0, 1, 11)),
                                   CMAP_HEAVY(np.linspace(0, 1, len(ELEM_HEAVY)))[inds_ar_ca_fe]))
        elif len(elem_list) == 89:
            cmap_list = np.vstack((CMAP_BASE(np.linspace(0, 1, 11)),
                                   CMAP_HEAVY(np.linspace(0, 1, len(ELEM_HEAVY)))))
        else:
            cmap = plt.get_cmap("plasma", len(elem_list))
            cmap_list = cmap(np.linspace(0, 1, len(elem_list)))
    elif type(cmap) == str:
        cmap = plt.get_cmap(cmap, len(elem_list))
        cmap_list = cmap(np.linspace(0, 1, len(elem_list)))
    else:
        if len(elem_list) == 13:
            inds_ar_ca_fe = np.array([6, 15, 54])
            cmap_base = cmap
            cmap_list = np.vstack((cmap_base(np.linspace(0, 1, 11)),
                                   CMAP_HEAVY(np.linspace(0, 1, len(ELEM_HEAVY)))[inds_ar_ca_fe]))
    masses = prof.data[raxis]

    # Set limits of radial axis
    lim = 0
    if boundary > 0:
        lim = np.where(masses <= boundary)[0][0]
    low_lim = len(masses)
    if raxis[:3] == "log":
        low_lim = np.where(masses <= log_low_lim)[0][0]

    if num_rings > 0:
        selec = [int(i) for i in np.linspace(lim, low_lim - 1, num_rings)]
        data = prof.data[selec]
        masses = masses[selec]
    else:
        data = prof.data[lim:low_lim]
        masses = masses[lim:low_lim]
    artists = []
    radius = np.sqrt(np.abs(masses)) / np.sqrt(np.abs(scale))
    if raxis[:3] == "log":
        shift = masses.min() + 1e-7
        radius = np.sqrt(np.abs(masses - shift)) / np.sqrt(np.abs(scale - shift))
    for ind, r in enumerate(radius):
        vals = []
        for elem in elem_list:
            vals.append(data[elem][ind])
        # Fix problem with center zone
        if ind == len(masses) - 1:
            startangle *= -1
        pie = ax.pie(vals, radius=r, colors=cmap_list, startangle=startangle,
                     wedgeprops=dict(width=width, antialiased=True, linestyle="None"),
                     counterclock=counterclock)
        artists.append(pie[0])    # return Wedges only
    ax.set(aspect="equal")

    return elem_list, artists


def make_property_plot(ax, prof, property="logRho", raxis="mass", num_rings=-1, cmin=-5, cmax=10, log=False,
                       cmap_str="plasma", theta1=0, theta2=360):
    """
    Plot a circle containing concentric rings with a color that corresponds to the evolution of a property
    :param : axis object
    :param prof: mesaPlot profile object
    :param property: string, default logRho, existing quantity in the MESA profile
    :param raxis: string, dafault axis to use as radius representation. Any linear property can be used instead
     (for example radius)
    :param num_rings: int, default -1, if greater than -1, limit the number of rings to this number
    :param theta1: int or float: Start angle for the wedge (in degrees)
    :param theta2: int or float: End angle for the wedge (in degrees)
    :return: List of artists created in the plot
    """
    r = prof.data[raxis][:]
    if raxis != "mass" and raxis != "radius":
        r = r[::-1]

    prop = prof.data[property][:]
    if num_rings > -1:
        selec = [int(i) for i in np.linspace(0, len(prof.mass) - 1, num_rings)]
        r = r[selec]
        prop = prop[selec]
    if log:
        prop = np.log10(prop)

    cmap = plt.get_cmap(cmap_str, len(prop))
    norm = Normalize(vmin=cmin, vmax=cmax)
    artist_list = []
    width = 0
    for ind, r_ind in enumerate(r):
        # Plot burning regions
        radius = r_ind
        value = prop[ind]
        # Width = current radius - previous radius
        width += radius
        color = cmap(norm(value))
        # Center zone should be a circle, not a ring
        if ind == 0:
            width = None
        wedge = Wedge((0, 0), radius, theta1=theta1, theta2=theta2, width=width, color=color)
        ax.add_artist(wedge)
        artist_list.append(wedge)
        width = -1 * radius

    return artist_list


def add_ring_annotations(ax, rmax, fraction_list=None, show_fraction=True, show_fraction_labels=True,
                         use_actual_mass_fraction=True, percentage_list=None, show_percentage=False,
                         show_percentage_labels=False,
                         startangle=90, counterclock=True, loc=1.25, **kwargs):
    """
    Add concentric circles on an axis that indicate the fraction of the maximum radius given. Optionally,
    indications of percentages can also be given.
    :param ax: matplotlib axis object
    :param rmax: float, value of the maximum radius of the circle to compare to as a reference
    :param fraction_list: list, default None, list of floats giving the fractions of the total mass
    :param show_fraction: boolean, default True, whether or not to plot circles that have radii of a fraction
    of the reference circle radius
    :param show_fraction_labels: boolean, default True, whether or not to add labels indication the fractions
    :param use_actual_mass_fraction: boolean, default True, whether or not to locate the fraction circles at the
    location where a circle contains this mass or at a fraction of rmax
    :param percentage_list: list, default None, list of floats giving the percentages to add
    :param show_percentage: boolean, default False, whether to plot radial lines indicating a certain percentage
    :param show_percentage_labels: boolean, default False, whether or not to add labels indicating percentages
    :param startangle: float, value of the angle to start with for the percentages
    :param counterclock: bool, optional, default: True, Specify percentage direction, clockwise or counterclockwise.
    :param loc: float, default 1.25, location of percentage labels in units of fraction of rmax
    :return: list of matplotlib artists created
    """
    circle_list = []
    fraction_label_list = []
    rays_list = []
    percentage_label_list = []
    if show_fraction:
        # Plot 4 rings by default
        if fraction_list is None:
            fraction_list = FRACTION_LIST
        for f in fraction_list:
            factor = np.sqrt(f)
            if not use_actual_mass_fraction:
                factor = f
            a = plt.Circle((0, 0), factor * rmax, fill=False, ec="0.7", linewidth=1.2, zorder=500)
            ax.add_artist(a)
            circle_list.append(a)
        if show_fraction_labels:
            for f in fraction_list:
                t = ax.text(0.7 * factor * rmax, 0.7 * np.sqrt(f) * rmax, str(f), color="k",
                            fontsize=10, ha="left", va="bottom", **kwargs)
                fraction_label_list.append(t)
    if show_percentage:
        # TODO: add startangle and counterclock option
        if percentage_list is None:
            percentage_list = PERCENTAGE_LIST
        for p in percentage_list:
            x = rmax * np.sin(-p * 2 * np.pi)
            y = rmax * np.cos(-p * 2 * np.pi)
            l, = ax.plot([0, x], [0, y], "0.7", lw=1.2, zorder=500)
            rays_list.append(l)
            if show_percentage_labels:
                t = ax.text(loc * x, loc * y, str(p * 100) + "\%", fontsize=10, color="0.8", ha='center',
                            va="center", **kwargs)
                percentage_label_list.append(t)
    artist_list = [circle_list, fraction_label_list, rays_list, percentage_label_list]
    return artist_list


def add_time_label(age, ax, time_label_loc=None, time_unit="Myr"):
    """
    Add a time label in the upper left corner of a diagram
    :param age: float, age of the stellar object
    :param ax: matplotlib Axes object
    :param time_label_loc: None or tuple, default None. The custom location of the time label in units of the Axes
    coordinate; (0, 0) is bottom left of the axes, and (1, 1) is top right of the axes
    :param time_unit: Unit of the
    :return: matplotlib Artist object
    """
    # If location not specified, place it in the upper left corner
    if len(time_label_loc) == 0:
        time_label_loc = (0.05, 0.95)

    time = (age * u.yr).to(time_unit)
    text = ax.text(time_label_loc[0], time_label_loc[1], "t = " + time.round(3).to_string(),
                   transform=ax.transAxes)
    return text


def check_time_indeces(time_ind, star_age):
    """
    Check if time indices are correctly set and define start_ind and end_ind
    :param time_ind: int or tuple (start_index, end_index, step=1) or (start_index, end_index, step);
    if int: create the plot at the index time_ind.
    :return: start_ind, end_ind, ind_step
    """
    if type(time_ind) is not tuple and type(time_ind) is not list and type(time_ind) is not np.ndarray:
        start_ind = int(time_ind)
        if start_ind < 0:
            start_ind += len(star_age)
        end_ind = start_ind
        ind_step = 1
    elif len(time_ind) == 2 or len(time_ind) == 3:
        start_ind = int(time_ind[0])
        end_ind = int(time_ind[1])

        # Make sure all indices are positive
        if start_ind < 0:
            start_ind += len(star_age)
        if end_ind < 0:
            end_ind += len(star_age)

        if start_ind == end_ind:
            # Issue warning when same values for start and end index
            raise(Warning, "No animation will be created because the start and end index have the same value")

        ind_step = 1
        if len(time_ind) == 3:
            ind_step = int(time_ind[2])
            if ind_step <= 0:
                raise(ValueError, "ind_step must be an integer larger than 0")
    else:
        raise (TypeError, "time_index must be an integer or a tuple of integers (start_ind, end_ind, step=1)")

    return start_ind, end_ind, ind_step


def rescale_time(indices, m, time_scale_type="model_number"):
    """
    Rescale time indices depending on the time_type.
    :param indices: np.array or list of int containing selected indices
    :param m: mesaObject
    :param time_scale_type: str, one of "model_number", "linear", or "log_to_end"
    For model_number, the time follows the moment when a new MESA model was saved.
    For linear, the time follows linear steps in star_age
    For log_time_to_end, the time axis is tau = log10(t_final - t), where t_final is the final star_age of the model
    :return: new list of indices that reflect the rescaling in time
    """
    age = m.hist.star_age
    if time_scale_type == "model_number":
        return indices
    elif time_scale_type == "linear":
        val_select = np.linspace(age[indices[0]], age[indices[-1]], len(indices))
        ind_select = [find_closest(val, age) for val in val_select]
        return ind_select
    elif time_scale_type == "log_to_end":
        time_diff = (age[-1] - age)
        # Avoid invalid values for log
        time_diff[time_diff <= 0] = 1e-5
        logtime = np.log10(time_diff)
        # Find indices
        val_select = np.linspace(logtime[indices[0]], logtime[indices[-1]], len(indices))
        ind_select = [find_closest(val, logtime) for val in val_select]
        return ind_select
    else:
        raise(ValueError, 'Invalid time_type. Choose one of "model_number", "linear", or "log_to_end"')

