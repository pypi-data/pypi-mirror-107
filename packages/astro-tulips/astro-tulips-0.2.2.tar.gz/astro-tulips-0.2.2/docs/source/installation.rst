Installation
=============

The easiest way to install ``tulips`` and all its dependencies is through pip::

    pip install astro-tulips

**Note:** Python 2 is not supported

Installing from source
^^^^^^^^^^^^^^^^^^^^^^^
To install from source, git clone the directory, then install::

    git clone https://bitbucket.org/elaplace/tulips.git
    cd tulips
    python3 setup.py install

The latest development version is available on the ``development`` branch. To create a local installaion call::

    pip install -e .

Additional dependencies
^^^^^^^^^^^^^^^^^^^^^^^
You need to have mesaPlot installed for reading MESA output files (see `mesaPlot <https://github.com/rjfarmer/mesaplot>`_).
For creating the movies you also need ``ffmpeg`` and ``mencoder`` .

On Ubuntu, you can install these via::

    sudo apt install ffmpeg mencoder

For installation of ``ffmpeg`` on Windows, you can follow the steps explained `here <https://www.wikihow.com/Install-FFmpeg-on-Windows>`_.
To install ``mencoder`` on Windows, you can download `MPlayer <http://mplayerwin.sourceforge.net/downloads.html>`_.

You also need to have Latex installed to properly display the diagrams. The easiest way to do this is by installing `TexLive <https://www.tug.org/texlive/acquire-netinstall.html>`_.

Running on Windows
^^^^^^^^^^^^^^^^^^
When getting ``tulips`` installed on Windows, it is important to add the dependencies to your system environment variable 'Path'.
You can do this by going to Start > Settings > Info > Advanced > Environment Variables. Here you can add a new
variable to 'Path' in the System Variables. This variable should contain the path to the installed program.

