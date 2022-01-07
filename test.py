import locale
from dialog import Dialog
import os

Version = 1.0
# This is almost always a good thing to do at the beginning of your programs.
locale.setlocale(locale.LC_ALL, '')

# You may want to use 'autowidgetsize=True' here (requires pythondialog >= 3.1)
d = Dialog(dialog="dialog")


def get_args():
    parser = argparse.ArgumentParser(description="Python TUI Upload Project")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(str(Version)))
    parser.parse_args()
    return True

def find_file(path):
    files = []
    for dirpath, dirname, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    return files

if __name__ == '__main__':
    get_args()
    files_list = []
    files = find_file("/mnt")
    for file in files:
        files_list.append((file, "", True))

    code, tags = d.checklist("Please select the file(s) you want to upload:", choices=files_list, title="Select files")
    if code == d.OK:
        for tag in tags:
            file_size = os.path.getsize(tag)
            target_size = 0
            record_size = file_size / 100
            text = "Uploading {} ....".format(tag)
            d.gauge_start(text, percent=0, title="Uploading")
            for i in range(1, 101):
                d.gauge_update(i, update_text=False)
            exit_code = d.gauge_stop()
    else:
        print("You cancelled the dialog!")

    print(files)
