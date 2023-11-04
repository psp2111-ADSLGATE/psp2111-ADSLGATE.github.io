import xbmc, xbmcgui, xbmcvfs
import xml.etree.ElementTree as ET
from xml.dom import minidom

KEYMAP_LOCATION = "special://userdata/keymaps/"
POSSIBLE_KEYMAP_NAMES = ["gen.xml", "keyboard.xml", "keymap.xml"]


def set_image():
    image_file = xbmcgui.Dialog().browse(
        2, "Choose Custom Background Image", "network", ".jpg|.png|.bmp", False, False
    )
    if image_file:
        xbmc.executebuiltin("Skin.SetString(CustomBackground,%s)" % image_file)


def fix_black_screen():
    if xbmc.getCondVisibility("Skin.HasSetting(TrailerPlaying)"):
        xbmc.executebuiltin("Skin.ToggleSetting(TrailerPlaying)")


# def get_current_keymap_path():
#     for keymap_name in POSSIBLE_KEYMAP_NAMES:
#         keymap_path = xbmcvfs.translatePath(KEYMAP_LOCATION + keymap_name)
#         if xbmcvfs.exists(keymap_path):
#             return keymap_path
#     return None


def make_backup(keymap_path):
    backup_path = f"{keymap_path}.backup"
    if not xbmcvfs.exists(backup_path):
        xbmcvfs.copy(keymap_path, backup_path)


def restore_from_backup(keymap_path):
    backup_path = f"{keymap_path}.backup"
    if xbmcvfs.exists(backup_path):
        xbmcvfs.delete(keymap_path)
        xbmcvfs.rename(backup_path, keymap_path)


def get_all_existing_keymap_paths():
    existing_paths = []
    for name in POSSIBLE_KEYMAP_NAMES:
        path = xbmcvfs.translatePath(f"special://profile/keymaps/{name}")
        if xbmcvfs.exists(path):
            existing_paths.append(path)
    return existing_paths


def get_parent_map(tree):
    return {c: p for p in tree.iter() for c in p}


def modify_keymap():
    keymap_paths = get_all_existing_keymap_paths()
    setting_value = xbmc.getCondVisibility("Skin.HasSetting(Enable.OneClickTrailers)")
    for keymap_path in keymap_paths:
        if not setting_value:
            restore_from_backup(keymap_path)
            continue
        make_backup(keymap_path)
        tree = ET.parse(keymap_path)
        root = tree.getroot()

        def has_play_trailer_tag(tag):
            return tag.text == "RunScript(script.fentastic.helper, mode=play_trailer)"

        play_pause_tags = root.findall(".//play_pause[@mod='longpress']")
        t_key_tags = root.findall(".//t")
        global_tag = root.find("global")
        if global_tag is None:
            global_tag = ET.SubElement(root, "global")
        keyboard_tag = global_tag.find("keyboard")
        if keyboard_tag is None:
            keyboard_tag = ET.SubElement(global_tag, "keyboard")
        if setting_value:
            if t_key_tags:
                t_key_tags[
                    0
                ].text = "RunScript(script.fentastic.helper, mode=play_trailer)"
                for tag in t_key_tags[1:]:
                    keyboard_tag.remove(tag)
            else:
                t_key_tag = ET.SubElement(keyboard_tag, "t")
                t_key_tag.text = "RunScript(script.fentastic.helper, mode=play_trailer)"
            if play_pause_tags:
                play_pause_tags[
                    0
                ].text = "RunScript(script.fentastic.helper, mode=play_trailer)"
                for tag in play_pause_tags[1:]:
                    keyboard_tag.remove(tag)
            else:
                play_pause_tag = ET.SubElement(
                    keyboard_tag, "play_pause", mod="longpress"
                )
                play_pause_tag.text = (
                    "RunScript(script.fentastic.helper, mode=play_trailer)"
                )
        else:
            for tag_list in [play_pause_tags, t_key_tags]:
                for tag in tag_list:
                    if has_play_trailer_tag(tag):
                        keyboard_tag.remove(tag)
        xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")
        pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="  ")
        pretty_xml = "\n".join(
            [line for line in pretty_xml.split("\n") if line.strip()]
        )
        with xbmcvfs.File(keymap_path, "w") as xml_file:
            xml_file.write(pretty_xml)
    xbmc.executebuiltin("Action(reloadkeymaps)")
