init python:
    import math

style button_text:
    color "#FFF"

default numlist = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
default cols = 2
default rows = 2
default page = 0
default max_page = 0

screen test():
    modal True
    grid cols rows:
        xalign 0.5
        yalign 0.5
        spacing 20
        transpose True

        for i in range(cols * rows):
            $ offset = page * cols * rows
            if(len(numlist) > i+offset):
                text (numlist[i+offset])
            else:
                text "-"

    hbox:
        xalign 0.5
        yalign 0.6
        textbutton("<"):
            if(page == 0):
                action NullAction()
            else:
                action SetVariable("page", page-1)
        textbutton (">"):
            if(page < max_page):
                action SetVariable("page", page+1)
            else:
                action NullAction()

label start:
    $ max_page = math.ceil(len(numlist) / (cols * rows)) - 1
    show screen test
    pause
