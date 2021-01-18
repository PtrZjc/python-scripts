

import click
import shutil
import datetime
from pathlib import Path


@click.group()
def cli():
    pass


@cli.command('backup')
@click.option('--path', '-p', help='Target folder path with fwd slash as delim e.g. "C:/Users/John"')
def backup(path):
    """Backups target folder to ./BACKUP with timestamp added"""

    click.echo("Starting to backup folder")

    if path is None:
        click.echo("Target folder path is required")
        return
    else:
        folder = Path(path)
        if not folder.exists():
            click.echo("Target folder does not exist")
            return

    backupFolder = folder.parents[0] / 'BACKUP'

    if not backupFolder.exists():
        backupFolder.mkdir()

    timestamp = str(datetime.datetime.now())[2::].replace(
        '-', '').split('.')[0].replace(' ', '-').replace(':', '')

    shutil.copytree(folder, backupFolder /
                    (str(folder.parts[-1]) + '_' + timestamp), dirs_exist_ok=True)

    click.echo(f'Successfully backed up \"{folder.parts[-1]}\" folder with timestamp {timestamp}')


@cli.command('restore')
@click.option('--path', '-p', help='Target folder path with fwd slash as delim e.g. "C:/Users/John"')
def restore(path):
    """Replaces target folder by folder with backed up folder with last timestamp from ./BACKUP"""
    click.echo("Attempting to restore backed up folder")

    if path is not None:
        folder = Path(path)
    else:
        click.echo("Target folder path is required")
        return

    backupFolder = folder.parents[0] / 'BACKUP'
    lastBackup = sorted(backupFolder.glob('*'))[-1]

    shutil.rmtree(folder)
    shutil.copytree(lastBackup, folder)

    click.echo(f'Successfully restored \"{folder.parts[-1]}\" folder from copy {lastBackup.parts[-1]}')

if __name__ == '__main__':
    cli()
