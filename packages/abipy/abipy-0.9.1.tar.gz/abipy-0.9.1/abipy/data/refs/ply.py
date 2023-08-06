#!/usr/bin/env python

from abipy import abilab
import sys
from abipy.tools.plotting import plotly_wigner_seitz, plotly_brillouin_zone

def main():
    s = abilab.Structure.from_file(sys.argv[1])
    #fig = plotly_wigner_seitz(s.reciprocal_lattice)
    fig = plotly_brillouin_zone(s.reciprocal_lattice)
    fig.show()


if __name__ == "__main__":
    main()


