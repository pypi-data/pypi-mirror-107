#!/usr/bin/env python

import sys

from abipy.abilab import PhononBandsPlotter, abiopen

#with abiopen("ZnSe_hex_886.out_PHBST.nc") as abifile:
#    abifile.phbands.plotly()
#sys.exit(0)

plotter = PhononBandsPlotter()
plotter.add_phbands("foo bands", "ZnSe_hex_886.out_PHBST.nc")
plotter.add_phbands("bar bands", "ZnSe_hex_886.out_PHBST.nc")

plotter.plotly_expose()
#plotter.combiplotly()
#plotter.gridplotly()

