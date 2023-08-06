import argparse
import os
import shutil

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('steamdir', type=str, help='Path to the steam workshop directory of starbound ("*STEAM_LIBRARY_PATH*/steamapps/workshop/content/211820")')
    ap.add_argument('sbdir', type=str, help='Path to the starbound mods directory ("*STEAM_LIBRARY_PATH*/steamapps/common/Starbound/mods")')
    args = ap.parse_args()

    for mod in os.listdir(args.steamdir):
        if os.path.isfile(os.path.join(args.steamdir, mod, 'contents.pak')):
            shutil.copy2(os.path.join(args.steamdir, mod, 'contents.pak'), os.path.join(args.sbdir, mod + '.pak'))
        else:
            print('Skipping ' + mod + ' (no "contents.pak" found)!')
