import sys
import os
import dropbox
from dropbox.exceptions import AuthError

TOKEN = os.environ.get('DROPBOX_API_TOKEN')

def download_folder(dbx, folder_path, local_path):
    try:
        for entry in dbx.files_list_folder(folder_path).entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                local_file_path = os.path.join(local_path, entry.name)
                with open(local_file_path, "wb") as f:
                    metadata, res = dbx.files_download(entry.path_lower)
                    f.write(res.content)
            elif isinstance(entry, dropbox.files.FolderMetadata):
                new_folder = os.path.join(local_path, entry.name)
                os.makedirs(new_folder, exist_ok=True)
                download_folder(dbx, entry.path_lower, new_folder)
    except Exception as e:
        print("Error downloading folder:", e)

def main():
    print(TOKEN)
    print(sys.argv)
    if len(sys.argv) != 2:
        print("Expected only 1 argument: source dir, e.g. /path/to/Dropbox/folder")
        sys.exit(1)

    dropbox_folder_path = sys.argv[1]
    local_directory = os.getcwd()

    if len(TOKEN) == 0:
        sys.exit("ERROR: Missing Dropbox API token. Set your TOKEN in the script.")

    try:
        dbx = dropbox.Dropbox(TOKEN)
        dbx.users_get_current_account()
    except AuthError:
        sys.exit("ERROR: Invalid access token.")

    download_folder(dbx, dropbox_folder_path, local_directory)
    print("Download completed.")

if __name__ == "__main__":
    main()
