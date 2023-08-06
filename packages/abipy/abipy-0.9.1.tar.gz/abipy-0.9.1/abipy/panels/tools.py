""""Utilities for AbiPy panels."""

import panel as pn


def btn_open_link(url, new_tab=True, **btn_kwargs):
    """Return button to open link in a new tab."""

    if new_tab:
        code = f"window.open('{url}')"
    else:
        code = f"window.location.href='{url}'"

    name = btn_kwargs.get("name", "Open Link")
    btn = pn.widgets.Button(name=name, **btn_kwargs)
    btn.js_on_click(code=code)

    return btn
