from pathlib import Path
import os

import click


def extedit(root_dir: Path, old_ext: str, new_ext: str, blacklist: tuple, recursive: bool) -> None:
    file_list = [x.absolute() for x in root_dir.glob(f'{"**/" if recursive else ""}*{old_ext}')]
    if blacklist:
        fl = list(filter(lambda p: not any(bl in p.name for bl in blacklist), fl))
    file_list.sort()
    with click.progressbar(file_list, label='Change extension', show_pos=True, item_show_func=lambda x: f'{f"({x.name})" if x is not None else ""}') as files:
        for file in files:
            os.rename(file, file.as_posix().replace(old_ext, new_ext))


@click.command('extedit', short_help='Edit file extensions.')
@click.help_option('--help', '-h')
@click.argument(
    'root_dir',
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    required=True
)
@click.argument(
    'old_ext',
    type=str,
    required=True
)
@click.argument(
    'new_ext',
    type=str,
    required=True
)
@click.option(
    '-b', '--blacklist',
    help='Blacklist extensions, multiple items are allowed.',
    type=str,
    multiple=True,
    required=False,
)
@click.option(
    '-r', '--recursive',
    help='Include subdirectories.',
    is_flag=True,
    type=bool,
    required=False
)
def extedit_cli(root_dir: str, old_ext: str, new_ext: str, blacklist: tuple, recursive: bool) -> None:
    """
    Edit file extensions.

    Ingores files with BLACKLISTed extensions.
    """
    extedit(
        root_dir=Path(root_dir),
        old_ext=old_ext,
        new_ext=new_ext,
        blacklist=blacklist,
        recursive=recursive
    )
