import shlex
import sysfetch_win
import sys

from . import argpar, sysfetch


def shell():
    arguments = argpar.getarg()
    parser = argpar.Arguments(description="SysFetch-Windows")
    parser.add_argument('-a', '--about', action='store_true', help='Show Info About This Module')
    parser.add_argument('-s', '--simple', action='store_true', help='Shows System Info Without Ascii Art')
    parser.add_argument('-v', '--version', action='store_true', help='Show The Installed Version Of This Module')
    parser.add_argument('-f', '--filter', nargs='+', default=[], help='Filter and remove the unwanted outputs ex- sysfetch -f ram')

    try:
        args = parser.parse_args(shlex.split(arguments))
    except Exception as e:
        print(e)
        sys.exit(1)

    if args.version:
        print(sysfetch_win.__version__)
        sys.exit(0)

    if args.about:
        print("Sysfetch-win Module Is Created By NandyDark.. It Fetches System Info And Prints It Out")
        sys.exit(0)

    if args.simple:
        display_art = False
    else:
        display_art = True

    colour = "red"
    artcolour = "cyan"
    
    nf = sysfetch.Sysfetch(
        colour=colour,
        art_colour=artcolour,
        display_art=display_art,
    )

    print(
        nf.pretty_print(ignore_list=args.filter),
        file=nf.stream
    )


def main():
    try:
        shell()
    except KeyboardInterrupt:
        print('\nCancelling...')


if __name__ == '__main__':
    main()
