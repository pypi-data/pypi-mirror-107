
# Copyright (c) 2019, Eva Laplace e.c.laplace@uva.nl

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

import mesaPlot as mp
import tulips
import matplotlib.pyplot as plt
import numpy as np
# # Use LaTeX in the plots
from matplotlib import rc

fsize = 30
SMALL_SIZE = 25
MEDIUM_SIZE = 25
BIGGER_SIZE = 30
rc('font', **{'family': 'DejaVu Sans', 'serif': ['Times'], 'size': fsize})
rc('text', usetex=True)
plt.rc('font', size=MEDIUM_SIZE)  # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

EXAMPLE_DIR = "/home/laplace/Documents/PycharmProjects/tulips/tulips/MESA_DIR_EXAMPLE/"
ARTICLE_DIR = "/home/laplace/Desktop/Link to articles/my_articles/manuscript_single_and_binary_prog_of_cc_sne/current_draft/figures/"
DATA_DIR_BINARY = "/home/laplace/Data/grids/single_vs_binary/example_profiles/binary_M11/"
if __name__ == "__main__":
    m = mp.MESA()
    # Read the history file only
    m.loadHistory(filename_in=EXAMPLE_DIR + 'history.data',
                  # max_num_lines=1500
                  )

    # Test the aspect of a movie of the change in radius and effective temperature
    # ind = np.where(m.hist.center_h1 < 1e-4)[0][0]
    # ind = np.where(m.hist.log_R > 2.2)[0][0]
    ind = np.where(m.hist.center_he4 < 1e-4)[0][0]
    fig, ax = tulips.animated_hist_test(m, time_index=ind, hrd_inset=True
                                    # raxis="star_mass"
                                    )

    plt.subplots_adjust(top=0.99, left=0.12, right=0.89, hspace=0, wspace=0, bottom=0.1)
    # fig.savefig(EXAMPLE_DIR + "example_hrd_3.png")
    plt.show()
    #
    # # Create movie of change in radius and effective temperature
    # tulips.animated_hist(m, plot_name_base="test_single_M10.5", plot_dir=EXAMPLE_DIR, raxis="log_R", time_index_step=20,
    #                      fps=15)

    # # # Test the aspect of a movie of the change in interior composition
    # fig, ax = tulips.animated_hist_interior_test(m, time_index=0, show_mix=False)
    # fig.savefig(EXAMPLE_DIR + "example_animated_hist_interior_test.png")
    # plt.show()
    #
    # # Test movie of change in interior burning
    # tulips.animated_hist_interior(m, plot_name_base="test_single_M10.5_interior", plot_dir=EXAMPLE_DIR,
    #                               time_index_step=20, fps=15, show_mix=False)
    #
    # # Test the aspect of a movie of the change in interior composition
    # tulips.animated_interior_composition_test(m, time_index=-1)
    # plt.show()

    # Test interior composition plots based on profiles
    # m.loadHistory(EXAMPLE_DIR + "LOGS")
    # fig, ax = tulips.animated_prof_interior_composition_test(m, prof_index=0, show_total_mass=True, hrd_inset=True,
    #                                                          )
    # fig.savefig(EXAMPLE_DIR + "comp_test.png")
    # plt.show()
    # import numpy as np
    # m.loadProfile(num=-1)
    # prof = m.prof
    #
    # # Test radius
    # fig = plt.figure()
    # fig.set_size_inches(9, 7)
    # fig.patch.set_alpha(1)
    # ax = plt.gca()
    #
    # ind_lim = np.where(prof.mass <= prof.he_core_mass)[0][0]
    # radius_lim = prof.radius[ind_lim]
    # print(radius_lim)
    # elem_list, cmap_list = tulips.make_pie_composition_plot(ax, prof, width=0.03, raxis="logR",
    #                                                         scale=3, num_rings=1000,
    #                                                         boundary=0
    #                                                         )
    # ax.set_xscale("log")
    # ax.set_yscale("log")
    # plt.show()

    # Test mass
    # fig = plt.figure()
    # fig.set_size_inches(9, 7)
    # fig.patch.set_alpha(1)
    # ax = plt.gca()
    #
    # elem_list, cmap_list = tulips.make_pie_composition_plot(ax, prof, width=0.03, raxis="mass",
    #                                                         boundary=prof.he_core_mass, num_rings=700,
    #                                                         scale=np.sqrt(prof.he_core_mass))
    # print(len(prof.mass))
    # plt.show()

    # tulips.animated_prof_interior_composition(m, prof_index_start=100, prof_index_end=200, hrd_inset=True,
    #                                           plot_name_base="test_single_M11_composition_new", plot_dir=EXAMPLE_DIR)
    #
    # tulips.animated_prof_interior_composition(m, prof_index_start=-1, prof_index_end=-1, hrd_inset=True,
    #                                           plot_name_base="test_single_M11_composition_new", plot_dir=EXAMPLE_DIR)

    # m2 = mp.MESA()
    # m2.loadHistory(filename_in=DATA_DIR_BINARY + 'pre_he_depl/LOGS/history.data',)
    # tulips.animated_prof_interior_composition(m2, prof_index_start=-1, prof_index_end=-1, hrd_inset=True,
    #                                           plot_name_base="test_binary_M11_composition_new", plot_dir=EXAMPLE_DIR)

    # Create a Kippenhahn to compare
    # fig = plt.figure()
    # fig.set_size_inches(11, 9)
    # ax = plt.gca()
    # p = mp.plot()
    # p.plotKip3(m, fig=fig, ax=ax, show_mass_loc=False, show_mix_labels=False, mod_max=4000,
    #            zaxis="signed_log_eps_grav",
    #            xaxis="star_age", yaxis="mass", age_lookback=True, age_log=True, xlabel="Time / yr", mix_hatch=True,
    #            hatch_color="#9E9E9E",
    #            cbar_label="$\epsilon$", show=False, colorbar=True)
    # ax.set_ylabel("Mass / $\\rm{M}_{\odot}$")
    # ax.set_xlabel("$\log_{10}(\\tau_{\\rm{cc}} - \\tau) / \\rm{yr}$")
    # plt.show()

    # Test property evolution plot
    # m.loadHistory(EXAMPLE_DIR + "LOGS")
    # fig, ax = tulips.animated_prof_interior_property_test(m, property="c12", prof_index=-1, num_rings=300,
    #                                                       show_total_mass=True, cmin=0, cmax=1)
    # # fig.savefig(ARTICLE_DIR + "ev_comp_10.png")
    # plt.show()


    # Test comparison plot

    # m1 = mp.MESA()
    # # Read the history file only
    # m1.loadHistory(filename_in=EXAMPLE_DIR + 'history_single_15Msun_to_cc.data')
    #
    # m2 = mp.MESA()
    # # Read the history file only
    # m2.loadHistory(filename_in=EXAMPLE_DIR + 'history_binary_15Msun_to_cc.data')
    # tulips.animated_hist_comp_test(m2, m1, label1="Single", label2="Binary", time_index1=0, time_index2=0)
    # plt.show()

    # Test comparison animation
    # stop_ind1 = int(np.where((m2.hist.center_o16 > 0.1) & (m2.hist.center_c12 < 1e-4))[0][0])
    # stop_ind2 = int(np.where((m1.hist.center_o16 > 0.1) & (m1.hist.center_c12 < 1e-4))[0][0])
    # animated_hist_comp(m2, m1, label1="$Z_{\odot}$", label2="Z_{\\rm{low}", plot_name_base="test_comp_Zsun_Zlow",
    #                    time_index_end1=stop_ind1, time_index_end2=stop_ind2)