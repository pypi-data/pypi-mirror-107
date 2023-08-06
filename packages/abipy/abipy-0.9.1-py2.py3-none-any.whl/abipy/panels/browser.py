""""Base classes and mixins for AbiPy panels."""

import param
import panel as pn
import panel.widgets as pnw

from abipy.panels.core import ButtonContext #, mpl, ply, dfc AbipyParameterized, HasStructureParams,


class Browser(param.Parameterized):

    analyze_btn = pnw.Button(name="Analyze files", button_type='primary')

    def __init__(self, cwd, **kwargs):
        self.files = pn.widgets.FileSelector(cwd, root_directory="/")
        super().__init__(**kwargs)

    @param.depends('analyze_btn.clicks')
    def on_analyze_btn(self):
        print(self.files.value)
        if self.analyze_btn.clicks == 0: return
        if not self.files.value: return

        with ButtonContext(self.analyze_btn):

            from abipy import abilab
            print("opening ", self.files.value)
            if len(self.files.value) == 1:
                abifile = abilab.abiopen(self.files.value[0])
                return abifile.get_panel()
            else:
                raise NotImplementedError("Multiple files!")
                #robot = abilab.Robot.from_files(self.files.value)
                #robot.get_panel()

    def get_panel(self):
        col = pn.Column(sizing_mode='stretch_width'); ca = col.append
        ca(pn.Row(self.files, self.analyze_btn))
        ca(pn.layout.Divider())
        ca(self.on_analyze_btn)
        #print(self.files.value)
        return col


def browser_app(cwd=None, **kwargs):
    if cwd is None:
        import os
        cwd = os.getcwd()
    from abipy import abilab
    abilab.abipanel()
    app = Browser(cwd).get_panel()
    app.show(**kwargs)
