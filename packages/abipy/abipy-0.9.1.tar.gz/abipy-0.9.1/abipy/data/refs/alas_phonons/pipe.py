#!/usr/bin/env python

#from abipy.panels.pipelines import analyze_file_app
#analyze_file_app(debug=True)

#from abipy.panels.pipelines import analyze_files_app
#analyze_files_app(debug=True)

from abipy.panels.browser import browser_app

#from abipy import abilab
#abilab.abipanel()
#import os
#cwd = os.getcwd()
#app = Browser(cwd).get_panel()
#app.show(debug=True)

browser_app(debug=True)
