
import click
import os.path
import sys
import pyautogui
from pyautogui import ImageNotFoundException
import pyscreeze
from time import sleep


@click.group()
def cli():
    pass


@cli.command('copy-exif-data')

@click.option('--source', '-s', help='input folder, default c:\\asource')
@click.option('--target', '-t', help='target folder, default c:\\atarget')
def copy_exif_data(source, target):
    """Automatically find and select approvers in MR when >Add aproval rule< window is active """

    pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = True

    try:
        imageToBaseOn = os.path.join(
            sys.path[0], 'media', 'add_screenshot_snip.png')
        c = pyautogui.locateCenterOnScreen(imageToBaseOn)
    except ImageNotFoundException:
        click.echo(
            'The snip of "Add" word in the add approval rule window not found')
        return

    pyautogui.click(c)
    pyautogui.click(c.x + 120, c.y + 90)
    pyautogui.write(group)

    for approver in approvers:
        pyautogui.click(c.x + 330, c.y + 200)
        pyautogui.write(approver)
        sleep(0.6)
        pyautogui.click(c.x + 330, c.y + 250)

    pyautogui.click(c.x + 400, c.y + 440)


if __name__ == '__main__':
    cli()
