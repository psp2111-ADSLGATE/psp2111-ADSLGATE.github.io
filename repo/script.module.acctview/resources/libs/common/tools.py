import xbmc
import xbmcaddon
import xbmcgui
import os
import random
import re
import shutil
import string
import sys

from resources.libs.common.config import CONFIG

#########################
#  File Functions       #
#########################


def read_from_file(file, mode='r'):
    f = open(file, mode, encoding='utf-8')
    a = f.read()
    f.close()
    return a


def write_to_file(file, content, mode='w'):
    f = open(file, mode, encoding='utf-8')
    f.write(content)
    f.close()


def remove_folder(path):
    from resources.libs.common import logging

    logging.log("Deleting Folder: {0}".format(path))
    try:
        shutil.rmtree(path, ignore_errors=True, onerror=None)
    except:
        return False


def remove_file(path):
    from resources.libs.common import logging

    logging.log("Deleting File: {0}".format(path))
    try:
        os.remove(path)
    except:
        return False


def empty_folder(folder):
    total = 0
    for root, dirs, files in os.walk(folder, topdown=True):
        dirs[:] = [d for d in dirs if d not in CONFIG.EXCLUDES]
        file_count = 0
        file_count += len(files) + len(dirs)
        if file_count == 0:
            shutil.rmtree(os.path.join(root))
            total += 1

            from resources.libs.common import logging
            logging.log("Empty Folder: {0}".format(root))
    return total


def copytree(src, dst, symlinks=False, ignore=None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()
    if not os.path.isdir(dst):
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                shutil.copy2(srcname, dstname)
        except EnvironmentError as why:
            errors.append((srcname, dstname, str(why)))
        except Exception as err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except OSError as why:
        errors.extend((src, dst, str(why)))
    if errors:
        raise Exception


def file_count(home, excludes=True):
    item = []
    for base, dirs, files in os.walk(home):
        if excludes:
            dirs[:] = [d for d in dirs if os.path.join(base, d) not in CONFIG.EXCLUDE_DIRS]
            files[:] = [f for f in files if f not in CONFIG.EXCLUDE_FILES]
        for file in files:
            item.append(file)
    return len(item)
    

#########################
#  Utility Functions    #
#########################


def busy_dialog():
    xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
    try:
        yield
    finally:
        xbmc.executebuiltin('Dialog.Close(busydialognocancel)')


def convert_size(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G']:
        if abs(num) < 1024.0:
            return "%3.02f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.02f %s%s" % (num, 'G', suffix)


def get_keyboard(default="", heading="", hidden=False):
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return keyboard.getText()
    return default


def get_size(path, total=0):
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total += os.path.getsize(fp)
    return total


def percentage(part, whole):
    return 100 * float(part)/float(whole)


def get_date(days=0, formatted=False):
    import time

    value = time.time() + (days * 24 * 60 * 60)  # days * 24h * 60m * 60s

    return value if not formatted else time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(value))


def basecode(text, encode=True):
    import base64
    if encode:
        msg = base64.encodestring(text)
    else:
        msg = base64.decodestring(text)
    return msg


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def chunks(s, n):
    for start in range(0, len(s), n):
        yield s[start:start+n]


#########################
#  Add-on Functions     #
#########################


def get_addon_by_id(id):
    try:
        return xbmcaddon.Addon(id=id)
    except:
        return False


def get_addon_info(id, info):
    addon = get_addon_by_id(id)
    if addon:
        return addon.getAddonInfo(info)
    else:
        return False


def get_info_label(label):
    try:
        return xbmc.getInfoLabel(label)
    except:
        return False
