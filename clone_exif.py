import click
import os.path
from os import walk
import sys
import subprocess

@click.group()
def cli():
    pass

@cli.command('exif')
@click.option('--source', '-s', help='input folder, default c:\\asource')
@click.option('--target', '-t', help='target folder, default c:\\atarget')
def copy_exif_data(source, target):
    """Copies exif tags from photos in source folder to target folder. Based only on names, extensions do not matter """

    exif_tool_path = os.path.join(sys.path[0], 'bin', 'exif', 'exiftool.exe')

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

    target_names = {}
    source_names = {}

    for tphoto in target_photos:
        name = tphoto[:tphoto.find('.')]
        ext = tphoto[tphoto.find('.'):]
        target_names[name] = ext

    for sphoto in source_photos:
        name = sphoto[:sphoto.find('.')]
        ext = sphoto[sphoto.find('.'):]
        source_names[name] = ext

    click.echo(target_names)
    click.echo(source_names)
    for sphoto in source_names:
        if sphoto in target_names:
            file_to_change = target + '\\' + sphoto + target_names[sphoto]
            source_file = source + '\\' + sphoto + source_names[sphoto]
            click.echo('copying exif from %s to %s' %(source_file, file_to_change))
            subprocess.run(exif_tool_path + ' -tagsFromFile '+ source_file + ' ' + file_to_change)

if __name__ == '__main__':
    cli()
