import os
import re
import sys
import copy
import pickle
import json
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode

try:
    import pylast
    has_pylast = True
except ImportError:
    has_pylast = False

from . import g, c, paths, util


mswin = os.name == "nt"

class ConfigItem:

    """ A configuration item. """

    def __init__(self, name, value, minval=None, maxval=None, check_fn=None,
            require_known_player=False, allowed_values=None):
        """ If specified, the check_fn should return a dict.

        {valid: bool, message: success/fail mesage, value: value to set}

        """
        self.default = self.value = value
        self.temp_value = None
        self.name = name
        self.type = type(value)
        self.maxval, self.minval = maxval, minval
        self.check_fn = check_fn
        self.require_known_player = require_known_player
        self.allowed_values = []
        if allowed_values:
            self.allowed_values = allowed_values

    @property
    def get(self):
        """ Return value. """
        if self.temp_value is None:
            return self.value
        else:
            return self.temp_value

    @property
    def display(self):
        """ Return value in a format suitable for display. """
        return self.display_helper(self.value)

    @property
    def display_temp(self):
        if self.temp_value is None: return ""
        return self.display_helper(self.temp_value)

    def display_helper(self, retval):
        if self.name == "max_res":
            retval = str(retval) + "p"

        if self.name == "encoder":
            retval = str(retval) + " [%s]" % (str(g.encoders[retval]['name']))

        return retval

    def set(self, value, is_temp=False):
        """ Set value with checks. """
        # note: fail_msg should contain %s %s for self.name, value
        #       success_msg should not
        # pylint: disable=R0912
        # too many branches

        success_msg = fail_msg = ""
        value = value.strip()
        value_orig = value

        # handle known player not set

        if self.allowed_values and value not in self.allowed_values:
            fail_msg = "%s must be one of * - not %s"
            allowed_values = copy.copy(self.allowed_values)
            if '' in allowed_values:
                allowed_values[allowed_values.index('')] = "<nothing>"
            fail_msg = fail_msg.replace("*", ", ".join(allowed_values))

        if self.require_known_player and \
                not util.is_known_player(Config.PLAYER.get):
            fail_msg = "%s requires mpv or mplayer, can't set to %s"

        # handle true / false values

        elif self.type == bool:

            if value.upper() in "0 OFF NO DISABLED FALSE".split():
                value = False
                success_msg = "%s set to False" % c.c("g", self.name)

            elif value.upper() in "1 ON YES ENABLED TRUE".split():
                value = True
                success_msg = "%s set to True" % c.c("g", self.name)

            else:
                fail_msg = "%s requires True/False, got %s"

        # handle int values

        elif self.type == int:

            if not value.isdigit():
                fail_msg = "%s requires a number, got %s"

            else:
                value = int(value)

                if self.maxval and self.minval:

                    if not self.minval <= value <= self.maxval:
                        m = " must be between %s and %s, got "
                        m = m % (self.minval, self.maxval)
                        fail_msg = "%s" + m + "%s"

                if not fail_msg:
                    dispval = value or "None"
                    success_msg = "%s set to %s" % (c.c("g", self.name),
                                                    dispval)

        # handle space separated list

        elif self.type == list:
            success_msg = "%s set to %s" % (c.c("g", self.name), value)
            value = value.split()

        # handle string values

        elif self.type == str:
            dispval = value or "None"
            success_msg = "%s set to %s" % (c.c("g", self.name),
                                            c.c("g", dispval))

        # handle failure

        if fail_msg:
            failed_val = value_orig.strip() or "<nothing>"
            colvals = c.y + self.name + c.w, c.y + failed_val + c.w
            return fail_msg % colvals

        elif self.check_fn:
            checked = self.check_fn(value)
            value = checked.get("value") or value

            if checked['valid']:
                value = checked.get("value", value)
                set_save(self, value, is_temp)
                return checked.get("message", success_msg)

            else:
                return checked.get('message', fail_msg)

        elif success_msg:
            set_save(self, value, is_temp)
            return success_msg

def set_save(self, value, is_temp):
    if not is_temp:
        self.temp_value = None
        self.value = value
        Config.save()
    else:
        self.temp_value = value

def check_console_width(val):
    """ Show ruler to check console width. """
    valid = True
    message = "-" * val + "\n"
    message += "console_width set to %s, try a lower value if above line ove"\
        "rlaps" % val
    return dict(valid=valid, message=message)


# def check_api_key(key):
#     """ Validate an API key by calling an API endpoint with no quota cost """
#     url = "https://www.googleapis.com/youtube/v3/i18nLanguages"
#     query = {"part": "snippet", "fields": "items/id", "key": key}
#     try:
#         urlopen(url + "?" + urlencode(query)).read()
#         message = "The key, '" + key + "' will now be used for API requests."
#
#         # Make pafy use the same api key
#         pafy.set_api_key(Config.API_KEY.get)
#
#         return dict(valid=True, message=message)
#     except HTTPError:
#         message = "Invalid key or quota exceeded, '" + key + "'"
#         return dict(valid=False, message=message)


def check_ddir(d):
    """ Check whether dir is a valid directory. """
    expanded = os.path.expanduser(d)
    if os.path.isdir(expanded):
        message = "Downloads will be saved to " + c.y + d + c.w
        return dict(valid=True, message=message, value=expanded)

    else:
        message = "Not a valid directory: " + c.r + d + c.w
        return dict(valid=False, message=message)


def check_win_pos(pos):
    """ Check window position input. """
    if not pos.strip():
        return dict(valid=True, message="Window position not set (default)")

    pos = pos.lower()
    reg = r"(TOP|BOTTOM).?(LEFT|RIGHT)"

    if not re.match(reg, pos, re.I):
        msg = "Try something like top-left or bottom-right (or default)"
        return dict(valid=False, message=msg)

    else:
        p = re.match(reg, pos, re.I).groups()
        p = "%s-%s" % p
        msg = "Window position set to %s" % p
        return dict(valid=True, message=msg, value=p)


def check_win_size(size):
    """ Check window size input. """
    if not size.strip():
        return dict(valid=True, message="Window size not set (default)")

    size = size.lower()
    reg = r"\d{1,4}x\d{1,4}"

    if not re.match(reg, size, re.I):
        msg = "Try something like 720x480"
        return dict(valid=False, message=msg)

    else:
        return dict(valid=True, value=size)


def check_encoder(option):
    """ Check encoder value is acceptable. """
    encs = g.encoders

    if option >= len(encs):
        message = "%s%s%s is too high, type %sencoders%s to see valid values"
        message = message % (c.y, option, c.w, c.g, c.w)
        return dict(valid=False, message=message)

    else:
        message = "Encoder set to %s%s%s"
        message = message % (c.y, encs[option]['name'], c.w)
        return dict(valid=True, message=message)


def check_player(player):
    """ Check player exefile exists and get mpv version. """
    if util.has_exefile(player):
        print(player)
        util.assign_player(player)
        if "mpv" in player:
            version = "%s.%s.%s" % g.mpv_version
            fmt = c.g, c.w, c.g, c.w, version
            msg = "%splayer%s set to %smpv%s (version %s)" % fmt
            return dict(valid=True, message=msg, value=player)

        else:
            msg = "%splayer%s set to %s%s%s" % (c.g, c.w, c.g, player, c.w)
            return dict(valid=True, message=msg, value=player)

    else:
        if mswin and not (player.endswith(".exe") or player.endswith(".com")):
            # Using mpv.exe has issues; use mpv.com
            if "mpv" in player:
                retval = check_player(player + ".com")
                if retval["valid"]:
                    return retval
            return check_player(player + ".exe")

        else:
            msg = "Player application %s%s%s not found" % (c.r, player, c.w)
            return dict(valid=False, message=msg)


def check_lastfm_password(password):
    if not has_pylast:
        msg = "pylast not installed"
        return dict(valid=False, message=msg)
    password_hash = pylast.md5(password)
    return dict(valid=True, value=password_hash)


class _Config:

    """ Holds various configuration values. """

    _configitems = [
            ConfigItem("order", "relevance",
                allowed_values="relevance date views rating title".split()),
            ConfigItem("user_order", "", allowed_values =
                [""] + "relevance date views rating".split()),
            ConfigItem("max_results", 19, maxval=50, minval=1),
            ConfigItem("console_width", 80, minval=70,
                maxval=880, check_fn=check_console_width),
            ConfigItem("max_res", 2160, minval=360, maxval=2160),
            ConfigItem("player", "vlc" + ".exe" * mswin,
                check_fn=check_player),
            ConfigItem("playerargs", ""),
            ConfigItem("encoder", 0, minval=0, check_fn=check_encoder),
            ConfigItem("notifier", ""),
            ConfigItem("checkupdate", True),
            ConfigItem("show_player_keys", True, require_known_player=True),
            ConfigItem("fullscreen", False, require_known_player=True),
            ConfigItem("show_status", True),
            ConfigItem("always_repeat", False),
            ConfigItem("columns", "date user"),
            ConfigItem("ddir", paths.get_default_ddir(), check_fn=check_ddir),
            ConfigItem("overwrite", True),
            ConfigItem("show_video", True),
            ConfigItem("search_music", False),
            ConfigItem("window_pos", "", check_fn=check_win_pos,
                require_known_player=True),
            ConfigItem("window_size", "",
                check_fn=check_win_size, require_known_player=True),
            ConfigItem("download_command", ''),
            ConfigItem("lookup_metadata", True),
            ConfigItem("lastfm_username", ''),
            ConfigItem("lastfm_password", '', check_fn=check_lastfm_password),
            ConfigItem("lastfm_api_key", ''),
            ConfigItem("lastfm_api_secret", ''),
            ConfigItem("audio_format", "auto",
                allowed_values="auto webm m4a".split()),
            ConfigItem("video_format", "auto",
                allowed_values="auto webm mp4 3gp".split()),
            ConfigItem("pages", 3, minval=1, maxval=100),
            ConfigItem("autoplay", False),
            ConfigItem("set_title", True),
            ConfigItem("mpris", not mswin),
            ConfigItem("show_qrcode", False),
            ConfigItem("history", True), 
            ConfigItem("input_history", True),
            ConfigItem("vlc_dummy_interface", False)
            ]

    def __getitem__(self, key):
        # TODO: Possibly more efficient algorithm, w/ caching
        for i in self._configitems:
            if i.name.upper() == key:
                return i
        raise KeyError

    def __getattr__(self, name):
        try:
            # todo: remove this later
            if name != 'API_KEY':
                return self[name]
        except KeyError:
            raise AttributeError

    def __iter__(self):
        return (i.name.upper() for i in self._configitems)

    def save(self):
        """ Save current config to file. """
        config = {setting: self[setting].value for setting in self}

        with open(g.CFFILE, "w") as cf:
            json.dump(config, cf, indent=2)

        util.dbg(c.p + "Saved config: " + g.CFFILE + c.w)

    def convert_old_cf_to_json(self):
        """
        check if old-style config exists,
        convert old-style pickled binary config to json and save to disk,
        delete old-style config
        """
        if os.path.exists(g.OLD_CFFILE):
            with open(g.OLD_CFFILE, "rb") as cf:
                with open(g.CFFILE, "w") as cfj:
                    json.dump(pickle.load(cf), cfj, indent=2)
            os.remove(g.OLD_CFFILE)

    def load(self):
        """ Override config if config file exists. """
        if os.path.exists(g.CFFILE):
            with open(g.CFFILE, "r") as cf:
                saved_config = json.load(cf)

            for k, v in saved_config.items():

                try:
                    self[k].value = v

                except KeyError:  # Ignore unrecognised data in config
                    util.dbg("Unrecognised config item: %s", k)

            # Update config files from versions <= 0.01.41
            if isinstance(self.PLAYERARGS.get, list):
                self.WINDOW_POS.value = "top-right"
                redundant = ("-really-quiet --really-quiet -prefer-ipv4 -nolirc "
                             "-fs --fs".split())

                for r in redundant:
                    util.dbg("removing redundant arg %s", r)
                    util.list_update(r, self.PLAYERARGS.value, remove=True)

                self.PLAYERARGS.value = " ".join(self.PLAYERARGS.get)
                self.save()

Config = _Config()
del _Config # _Config is a singleton and should not have more instances
# Prevent module from being deleted
# http://stackoverflow.com/questions/5365562/why-is-the-value-of-name-changing-after-assignment-to-sys-modules-name
ref = sys.modules[__name__]
# Any module trying to import config will get the Config object instead
sys.modules[__name__] = Config
