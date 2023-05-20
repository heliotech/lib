#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module for miscellaneous functions for working with text/string

khaz
2023.05.20
"""

# from softdev.dbg import printd

import numpy as np

ftitle = __file__.split('/')[-1].split('.')[0]


def getcol(text, width=30):
    """ Splitting text into parts of length of `width` """

    parts = []
    # printd(f"{text = }, {len(text) = }")
    # printd(f"{np.arange(np.ceil(len(text)/width)) = }")
    for i in np.arange(np.ceil(len(text)/width)):
        span0, span1 = int(width*i), int(width*(i + 1))
        part = text[span0:span1]
        parts.append(part)
        # print(f"{i}) {span0 = }, {span1 = }, {part = }, {int(width*i) = }")
        # print(f"\t{span1 + int(width*i) = }")
        # print(f"| {part:{width}} |")

    return parts


def printhead(heading, level=0, tab=3, marker=None, xlines=(1, 1),
              media="screen", prefix=None, center=False, file=None, mode="w"):
    """Printing a heading text, with an underline.

    :param heading: text to print.
    :param level: level of the 'heading', from 0 to 4.
    :param tab: indentation of the heading.
    :param marker: marker used to underline.
    :param xlines: adds extra lines, (below, under the heading);
            None for no extra lines (or (0, 0))
    :param media: medium to print for -- 'screen' or 'rst'.
    :param prefix: (some prefix?).
    :param center: (?).
    :param file: output file name.

    :returns: None (prints the text).
    """
    # print(f"D: 'printhead' starting...[{ftitle}]")

    # Opening ouptut file:
    if file:
        output = open(file, mode=mode)
    else:
        from sys import stdout
        output = stdout

    # Determining extra lines:
    xlines = xlines if xlines else (0, 0)
    xlines = tuple("" if not item else "\n" for item in xlines)
    # printing the first of extra lines:
    print(xlines[0], end="")

    # if not xlines:
    #     xlines = (0, 0)
    # else:
    #     xline = xlines
    # if isinstance(xline, bool):
    #     if xline:
    #         xlines = [1, 1]
    #     else:
    #         xlines = [0, 0]
    # elif hasattr(xline, "__iter__"):
    #     try:
    #         xlines = [xline[0], xline[1]]
    #     except IndexError:
    #         xlines = [0, 0]
    # else:
    #     xlines = [0]
    # for i in range(xlines[0]):
    #     print("\n", end="", file=output)

    # Determining symbol:
    # symbols_0 = ['=', '━', '═', '─', '╌', '~', '…']  # ⎺ hor. scan line 1
    # #  U+2026 or “…”.
    # symbols_rst = ['#', '*', '=', '-', '^', '"']  # :first ver.
    symbols_0 = ['═', '━', '═', '─', '╌', '~', '…']  # ⎺ hor. scan line 1
    #  U+2026 or “…”.
    symbols_rst = ['#', '*', '=', '-', '^', '"']
    if media == "rst":
        markers = dict(zip((i for i in range(len(symbols_rst))), symbols_rst))
    elif media == "screen":
        markers = dict(zip((i for i in range(len(symbols_0))), symbols_0))

    if marker is None and level in markers:
        marker = markers[level]

    if not center:
        if not prefix:
            dl = 2 if tab > 0 else 0
            underlineLen = (len(str(heading))+dl)
        else:
            dl = 2
            underlineLen = len(f"{prefix}: {heading}") + dl
        if underlineLen > 80:
            underlineLen = 78
            print("D:", ftitle, ".printhead(...): underlineLen =",
                  underlineLen)

        if level < 2:
            print(f"{' '*(tab-1) + marker*underlineLen}", file=output)  # overline
        if not prefix:
            print(f"{' '*tab + heading}", file=output)
        else:
            print(f"{' '*tab + prefix + ': ' + heading}", file=output)
        if marker is not None:
            # underline:
            print(f"{' '*(tab-1) + marker*underlineLen}", file=output)
        else:
            pass
    else:
        # original version:
        # screenWd = 80
        # if center is True:
        #     width = 60
        # elif isinstance(center, int):
        #     width = center
        # textAdjusted = []
        # i = 0
        # heading = heading.replace("\n", "")
        # while i < len(heading):
        #     start = i
        #     end = i + width
        #     textAdjusted.append(heading[start:end])
        #     i += width
        # for line in textAdjusted:
        #     print(f"{line: ^{screenWd}}", file=output)

        # new version:

        screenWd = 80
        heading = heading.split("\n")
        headLen = max(map(len, heading))
        if marker is None and level in markers:
            marker = markers[level]
        # print(f"{heading:^{screenWd}}")
        if level < 2:
            print(f"{marker*min(screenWd, headLen):^{screenWd}}")
        for line in heading:
            print(f"{line:^{screenWd}}")
        print(f"{marker*min(screenWd, headLen):^{screenWd}}")
        # min(screenWd, headLen) <== adjustment for width of 80
    print(xlines[1], end="")  # extra empty line

    # closing the file output, if opened:
    if file:
        try:
            output.close()
        except:
            pass


def printhead_demo():
    text = "Demo heading"
    for i in range(7):
        printhead(f"{text}: level = {i}", i)

    prefix = "bla"
    printhead(f"`printhead` with `{prefix=}`", 3, prefix=prefix)
    prefix = "blabla"
    printhead(f"`printhead` with `{prefix=}`", 3, prefix=prefix)
    printhead("`printhead` with `center=True` (lv. 0)", 0, center=True)
    printhead("`printhead` with `center=True` (lv. 1)", 1, center=True)
    printhead("`printhead` with `center=True` (lv. 3)", 3, center=True)
    longotext = ("longo, longo, very long text... "
                 "longo, longo, very long text... "
                 "longo, longo, very long text... "
                 "longo, longo, very long text... ")
    printhead(f"`printhead` with `center=True` and {longotext} (lv. 2)", 2,
              center=True)
    printhead(f"`printhead` with `center=True` and {longotext} (lv. 1)", 1,
              center=True)

    longoCols = "\n".join(row for row in getcol(longotext))
    printhead(f"with `getcol`, lv. 3 and {longoCols}", 3, 0, center=True)
    printhead(f"with `getcol`, lv. 0 and {longoCols}", 0, 0, center=True)
    printhead(f"with `getcol`, lv. 1 and {longoCols}", 1, 0, center=True)
    # print(longoCols)
    # print("\n".join(row for row in longoCols))

    print("...spacer...")
    center = False
    xlines = None
    thehead = f"Heading with: {center = }, {xlines = }"
    printhead(f"{thehead}", center=center, xlines=xlines)
    print("...spacer...")
    center = True
    xlines = (None)
    thehead = f"Heading with: {center = }, {xlines = }"
    printhead(f"{thehead}", center=center, xlines=xlines)
    print("...spacer...")
    center = False
    xlines = (0, 1)
    thehead = f"Heading with: {center = }, {xlines = }"
    printhead(f"{thehead}", center=center, xlines=xlines)
    print("...spacer...")
    center = True
    xlines = (0, 1)
    thehead = f"Heading with: {center = }, {xlines = }"
    printhead(f"{thehead}", center=center, xlines=xlines)
    print("...spacer...")
    center = False
    xlines = (1, 0)
    thehead = f"Heading with: {center = }, {xlines = }"
    printhead(f"{thehead}", center=center, xlines=xlines)
    print("...spacer...")
    center = True
    xlines = (1, 0)
    thehead = f"Heading with: {center = }, {xlines = }"
    printhead(f"{thehead}", center=center, xlines=xlines)
    print("...spacer...")
    center = False
    xlines = (1, 1)
    thehead = f"Heading with: {center = }, {xlines = }"
    printhead(f"{thehead}", center=center, xlines=xlines)
    print("...spacer...")
    center = True
    xlines = (1, 1)
    thehead = f"Heading with: {center = }, {xlines = }"
    printhead(f"{thehead}", center=center, xlines=xlines)
    print("...spacer...")


def main():
    printhead_demo()


if __name__ == '__main__':
    main()
