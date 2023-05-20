# dbg.py

"""
Module for debugging

khaz
2023.05.20
"""

from softdev.m_iters import flatten
from m_utils.printing import printhead
from sys import stdin

mdChar = chr(0x00b7)  # middle dot
# ANSI codes
ARST = "\033[0m"  # resets all effects
ABLD = "\033[1m"  # bold
AITC = "\033[3m"  # italic
ABC = "\033[1;3m"  # italic + bold
AUND = "\033[4m"  # underline
ABLK = "\033[5m"  # blink
ARVS = "\033[7m"  # reversed


ARED = "\033[31m"
AORG = "\033[38;5;221m"
AYEL = "\033[33m"
AGRN = "\033[32m"
AWTH = "\033[37m"
# range for GRY: (blakc) 232 -- 235 (white)
AGRY = "\033[251"

AREDWHT = "\033[1;31;47m"
AREDGRY = "\033[38;5;196m\033[48;5;249m"
AWHTBLU = "\033[1;97;44m"
AORGWHT = "\033[48;5;15m\033[38;5;202m"
AORGVLT = "\033[48;5;18m\033[38;5;226m"
AREDBLU = "\033[48;5;20m\033[38;5;196m"

# bb codes (basic):
bbcodes = [("[b]", "[/b]"),
           ("[i]", "[/i]"),
           ("[u]", "[/u]"),
           ("[r]", "[/r]"),  # my bb code, reversed
           ("[red]", "[/red]"),  # colors
           ("[green]", "[/green]"),  # colors
           ("[blue]", "[/blue]"),  # colors
           ("[/]"),  # reset
           ]

bbcodesAscii = ["\033[1m", "\033[0m",  # bold
                "\033[3m", "\033[0m",  # italic]
                "\033[4m", "\033[0m",  # underilne
                "\033[7m", "\033[0m",  # reversed
                "\033[31m", "\033[0m",  # red
                "\033[32m", "\033[0m",  # green
                "\033[34m", "\033[0m",  # blue
                "\033[0m",
                ]

bb2ascii = {k: v for (k, v) in zip(flatten(bbcodes), flatten(bbcodesAscii))}


def inidle():
    """ Determine if in IDLE """

    try:
        return stdin.__module__.startswith('idlelib')
    except AttributeError:
        return False


def printd(*args, level=0, nohead=False, filename=None,
           loop=False, marker=mdChar,
           ascii=True, src="", src1="", **kwargs):
    """ `print` for debugging

    Args:
        level: int - if message is to report an error (1, 2), deft. False,
        nohead: bool - if should be without opening,
        src1: str - extra source,
    """
    # tab = int(kwargs["tab"]) if "tab" in kwargs else 0
    # print(f"D: {tab = } of type {type(tab)}")

    from sys import stdout, stdin

    INIDLE = inidle()

    if loop:
        nohead = True
        startwith = ".... "
    else:
        startwith = ""

    if "DBG" in kwargs and kwargs["DBG"] is True:
        IF_CODES = (ascii and stdout.isatty() and not INIDLE)
        if not IF_CODES:
            aITC, aBLD, aRST, aCLRS = "", "", "", ""
        else:
            aITC, aBLD, aRST, aCLRS = AITC, ABLD, ARST, AREDGRY
            # aCLRS previous value: AREDWHT

        fmt = kwargs['fmt'] if 'fmt' in kwargs else None
        # print(kwargs["DBG"])
        # message = "\t"*tab
        message = "" if not level else "[b]"
        if 'xline' not in kwargs:
            xline0, xline1 = '', ''
        else:
            xlines = kwargs['xline']
            try:
                xline0 = "\n" if xlines[0] else ""
                xline1 = "\n" if xlines[1] else ""
            except TypeError:  # assuming xline was int or bool
                xline0 = ""
                xline1 = "\n" if xlines else ""

        if "end" in kwargs:
            end = kwargs["end"]
        else:
            end = "\n"
        if "tab" in kwargs:
            nrTabs = kwargs["tab"]
        else:
            nrTabs = 0
        tabs = marker*4*nrTabs + " "
        # ERR = "DBG:" if not level else "DBG-ERR:"
        # ERR = "DBG:" if not level else "DBG-ERR 👾"
        # ERR = "DBG:" if not level else "DBG-ERR 💩"
        # ERR = "DBG:" if not level else "DBG-ERR 🛑 "
        # 🧻 Zwoje papieru toaletowego (U+1F9FB)
        errs = {0: "DBG:", 1: "DBG-ERR 🧻", 2: "DBG-ERR 💩"}
        ERR = errs[level]
        opening = f"{aBLD}{aCLRS} {ERR} {aRST}"
        # for i in range(len(args)):
        #     if fmt:
        #         try:
        #             message += f"{args[i]:{fmt}}"
        #         except (ValueError, Exception):
        #             message += f"{args[i]}"
        #     else:
        #         message += f"{args[i]}"
        #     if i == 0:
        #         message += " " if not level else "[/b]"
        # new: join
        try:
            message += "" + ", ".join(f"{arg:{fmt}}" for arg in args)
        except (ValueError, Exception):
            message += "" + ", ".join(str(arg) for arg in args)
        message = replace_tag(message + "[/]", IF_CODES)
        if src != "" or src1 != "":
            message += f" [{aITC}{src + src1}{aRST}]"
        if filename:
            with open(filename, "a") as fileOut:
                print(f"{xline0}{tabs} DBG: {message}{xline1}",
                      end=end, file=fileOut)
        else:
            if not nohead:
                print(f"{xline0}{tabs}{opening} {message}{xline1}", end=end)
            else:
                print(f"{tabs}{startwith}{message}{xline1}", end=end)
    else:
        # print("no DBG")
        pass  # <- def printd(...)


def printinfo(*args, src="", importance=0, startwith="",
              nohead=False, loop=False,
              end="\n", xline=False, filename=None, DBG=True,
              marker=mdChar, tab=0, fmt=None, asciicodes=True, src1=""):
    """ Prints information

        kwargs
            nohead: bool - if should be without opening,
                deft. False, i.e. with opening,
            loop: if inside a loop,
            importance: int - 0: neutral, 1: moderate, 2: important,
            fmt: str - format for args,
            ascii: bool - if ascii codes should be printed,
            src1: str - extra source,
     """

    from sys import stdout

    INIDLE = inidle()

    if loop:
        nohead = True
        if startwith == "":
            startwith = "...."

    importanceClrs = {0: AWTH, 1: AORG, 2: AREDBLU}
    if DBG:
        # if not ascii:if not ascii:
        IF_CODES = (asciicodes and stdout.isatty() and not INIDLE)
        if not IF_CODES:
            aITC, aBC, aBLD, aRST, aUND, aCLRS = "", "", "", "", "", ""
        else:
            aITC, aBC, aBLD, aRST, aUND = AITC, ABC, ABLD, ARST, AUND
            aCLRS = importanceClrs[importance]
        message = ''
        # for i in range(len(args)):  # old: for loop
        #     if fmt:
        #         try:
        #             message += f"{args[i]:{fmt}}"
        #         except (ValueError, Exception):
        #             message += f"{args[i]}"
        #     else:
        #         message += f"{args[i]}"
        #     if i < len(args) - 1:
        #         message += ", "
        # new: join
        try:
            message += "" + ", ".join(f"{arg:{fmt}}" for arg in args)
        except (ValueError, Exception):
            message += "" + ", ".join(str(arg) for arg in args)
        if src != "" or src1 != "":
            # src = "'" + src + "'"
            src = f"[{aITC}{src + src1}{aRST}]"
        if DBG:
            tabs = marker*4*tab + " "
            message = replace_tag(message, IF_CODES)
            if filename:
                with open(filename, "a") as fileOut:
                    nl = "\n" if xline else ""
                    print(f"{nl}{tabs}{aBC}{aUND} INFO: {aRST} "
                          f"{message} [{src}]",
                          end=end, file=fileOut)
            else:
                opening = ""
                thehead = f"{tabs}"
                if not nohead:
                    if xline:
                        opening += f"\n{startwith}"
                    else:
                        opening += f"{startwith}"
                    thehead = f"{aCLRS}{aBLD}{aUND} INFO: {aRST} "
                else:
                    opening += f"{startwith}"
                print(f"{tabs}{opening}{thehead}{message} {src}", end=end)
    else:
        pass  # <- def printinfo(...)


def replace_tag(inputText, codes=True):
    """ Replacing bb codes in tekst

        Args:
            inputText: str - string with bb tags to be replaced,
            codes: bool - flag if tags are to be
                replaced with ascii codes, deft. True
        Returns:
            outputText: str - inputText with tags replaced.

        [b]tekst[/b] - pogrubienie tekstu
        [i]tekst[/i] - kursywa tekstu
        [u]tekst[/u] - podkreślenie tekstu
        [s]tekst[/s] - przekreślenie tekstu
        [url]adres[/url] - link do strony
        [img]adres[/img] - wstawienie obrazka
        [color=wartość]tekst[/color] - zmiana koloru tekstu
        [size=wartość]tekst[/size] - zmiana rozmiaru tekstu

        bbcodes = [("[b]", "[/b]"),
           ("[i]", "[/i]"),
           ("[u]", "[/u]")]
    """

    for k, v in bb2ascii.items():
        # print(f"D: {codes = }, {k = }, {v = }, src='replace_tag'")
        vTarget = v if codes else ""
        # True case:
        # vTarget = v
        # print(f"D: True case, {k = !r} -> {vTarget!r} = vTarget")
        # False case:
        # vTarget = ""
        # print(f"D: False case, {k = !r} -> {vTarget!r} = vTarget")
        inputText = inputText.replace(k, vTarget)

    return inputText


def printd_demo():
    printhead("printd_demo", 3, 1)
    printd("bla", "ble", "blu", "bli", level=0, DBG=True)
    printd(1, 2, 3, 4, 5, level=0, DBG=True)
    printd(1, 2, 3, 4, 5, level=1, DBG=True)
    print("...abc...")
    printd("bla for level=0", level=0, DBG=True)
    print("(test print)")
    printd("bla for level=1", level=1, DBG=True)
    print("(test print)")
    printd("bla for level=2", level=2, DBG=True)
    print("(test print)")
    printd("xline = 0", xline=0, DBG=True)
    printd("xline = 1", xline=1, DBG=True)
    print("...")
    printd("xline = (0, 1)", xline=(0, 1), DBG=True)
    print("...")
    printd("xline = (1, 1)", xline=(1, 1), DBG=True)
    print("...")
    printd("xline = (0, 0)", xline=(0, 0), DBG=True)
    print("...")


def printinfo_demo():
    printhead("printinfo_demo", 3, 1)
    printinfo("bla", DBG=True)
    printinfo("bla", "ble", "blu", "bli", DBG=True)
    printinfo(*[x for x in range(5)], fmt=".1f", DBG=True)
    printinfo("bla", "ble", "blu", "bli", "with `importance=1`", importance=1,
              DBG=True)
    printinfo("bla", "ble", "blu", "bli", "with `importance=2`", importance=2,
              DBG=True)


def main():
    printd_demo()
    printinfo_demo()


if __name__ == '__main__':
    main()
