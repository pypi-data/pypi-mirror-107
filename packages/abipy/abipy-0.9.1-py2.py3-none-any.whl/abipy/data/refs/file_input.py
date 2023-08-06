#!/usr/bin/env python

def main():
    import panel as pn
    pn.extension()

    file_input = pn.widgets.FileInput()

    #@pn.depends(file_input)


    file_input.show()





if __name__ == "__main__":
    main()
