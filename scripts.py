
import click
import os.path
from os import walk
import sys
import subprocess

@click.group()
def cli():
    pass

@cli.command('copy-exif-data')
@click.option('--source', '-s', help='input folder, default c:\\asource')
@click.option('--target', '-t', help='target folder, default c:\\atarget')
def copy_exif_data(source, target):
    """Copies exif tags from photos in source folder to target folder. Based only on names, extensions do not matter """

    exif_tool_path = os.path.join(sys.path[0], 'bin', 'exif', 'exiftool.exe')

    # subprocess.run(exif_tool_path)
    # usage: exiftool.exe -tagsFromFile" c:\asource\IMG_20201025_164020.jpg c:\atarget\IMG_20201025_164020.jpg

    if source == None:
        source = 'C:\\asource'

    if target == None:
        target = 'C:\\atarget'

    source_photos = []
    target_photos = []

    for _, _, filenames in os.walk(source):
        source_photos.extend(filenames)
        break

    for _, _, filenames in os.walk(target):
        target_photos.extend(filenames)
        break

    source_photo_names = list(map(lambda x: x[:x.find('.')], source_photos))
    target_photo_names = list(map(lambda x: x[:x.find('.')], target_photos))

    target_names = {}

    for tphoto in target_photos:
        name = tphoto[:tphoto.find('.')]
        ext = tphoto[tphoto.find('.'):]
        target_names[name] = ext

    click.echo(target_names)
    click.echo(target_photo_names)
    for sphoto in source_photo_names:
        if sphoto in target_photo_names:
            click.echo('TBD / file to change:')
            click.echo(source + '\\' + sphoto + target_names[sphoto])


if __name__ == '__main__':
    cli()
