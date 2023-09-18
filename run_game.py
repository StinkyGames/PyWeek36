import sys

# check python version requirement
min_ver = (3, 7)
if sys.version_info[:2] < min_ver:
    sys.exit(
        'This game requires Python {}.{}.'.format(*min_ver)
    )

try:
    import arcade
except:
    sys.exit(
        'Arcade is required to run'
    )

try:
    import main
except:
    sys.exit(
        'Your installation is corrupt'
    )
main.main()