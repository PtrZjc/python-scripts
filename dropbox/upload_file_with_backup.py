import sys
import os
import datetime
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

# Add OAuth2 access token here.
TOKEN = os.environ.get('DROPBOX_API_TOKEN')

def format_backup_name(original_name, date_time):
    base, ext = os.path.splitext(original_name)
    return f"{base}_{date_time.strftime('%d%m%y_%H%M%S')}{ext}"

def download_file(dbx, path, local_path):
    dbx.files_download_to_file(local_path, path)

def upload_file(dbx, local_path, destination_path, overwrite=False):
    mode = WriteMode('overwrite') if overwrite else WriteMode('add')
    with open(local_path, 'rb') as f:
        dbx.files_upload(f.read(), destination_path, mode=mode)

def file_exists_and_different(dbx, local_path, destination_path):
    try:
        mtime = os.path.getmtime(fullname)
        mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
        size = os.path.getsize(fullname)

        metadata = dbx.files_get_metadata(destination_path)
        local_mtime = os.path.getmtime(local_path)
        local_mtime_dt = datetime.datetime.utcfromtimestamp(local_mtime)
        dropbox_mtime_dt = metadata.server_modified

        print(f"Local file modified: {local_mtime_dt}, Dropbox file server modified: {dropbox_mtime_dt}")
        
        return local_mtime_dt > dropbox_mtime_dt
    except ApiError as e:
        if e.error.is_path() and e.error.get_path().is_not_found():
            return False
        raise


def main(local_file, destination_path):
    if len(TOKEN) == 0:
        sys.exit("ERROR: Access token is required.")
    
    dbx = dropbox.Dropbox(TOKEN)

    try:
        dbx.users_get_current_account()
    except AuthError:
        sys.exit("ERROR: Invalid access token.")

    if file_exists_and_different(dbx, local_file, destination_path):
        backup_name = format_backup_name(local_file, datetime.datetime.now())
        download_file(dbx, destination_path, backup_name)
        print(f"Downloaded existing file to {backup_name}")

    upload_file(dbx, local_file, destination_path, overwrite=True)
    print(f"Uploaded {local_file} to {destination_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python script.py <local_file> <destination_path>")
        sys.exit(1)

    local_file = sys.argv[1]
    destination_path = sys.argv[2]
    main(local_file, destination_path)
