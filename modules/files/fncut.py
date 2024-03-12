from pathlib import Path
import os

import click


def fncut(root_dir: Path, cut_length: int, mode: str, regex: str) -> None:
    file_list = list(root_dir.glob(regex))
    for file in file_list:
        if mode == 'start':
            os.rename(file, root_dir.joinpath(file.name[cut_length:]))
        elif mode == 'end':
            os.rename(file, root_dir.joinpath(file.name.split('.')[0][:-cut_length] + ''.join(file.suffixes)))


@click.command('fncut', short_help='Remove parts of a filename.')
@click.help_option('--help', '-h')
@click.argument(
    'root_dir',
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    required=True
)
@click.argument(
    'cut_length',
    type=int,
    required=True
)
@click.option(
    '-m', '--mode',
    help='start: removes first n characters, end: removes last n characters before first dot.',
    type=click.Choice(['start', 'end'], case_sensitive=False),
    default='start',
    show_default=True,
    required=False
)
@click.option(
    '-r', '--regex',
    help='Input filename regular expression (example: *.orig.png).',
    type=str,
    default='*',
    show_default=True,
    required=False
)
def fncut_cli(root_dir: str, cut_length: int, mode: str, regex: str) -> None:
    """
    Removes first CUT_LENGTH characters from filenames.

    MODE set to start: removes first CUT_LENGTH characters.

    MODE set to end: removes last CUT_LENGTH characters before first dot.
    """
    fncut(
        root_dir=Path(root_dir),
        cut_length=cut_length,
        mode=mode,
        regex=regex
    )