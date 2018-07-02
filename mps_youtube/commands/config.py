from .. import g, c, config, util
from . import command


@command(r'set|showconfig', 'set', 'showconfig')
def showconfig():
    """ Dump config data. """
    width = util.getxy().width
    longest_key = 17
    longest_val = 0
    has_temps = False

    for setting in config:
        val = config[setting]
        longest_val = max(longest_val, len(str(val.display)))
        has_temps = has_temps or val.temp_value is not None

    width -= 27
    s = "  %s%-{0}s%s : %-{1}s".format(longest_key, longest_val+1)

    if has_temps:
        width -= longest_val + 5
        out = "  %s%-{}s   %-{}s %s%s%s\n".format(longest_key, longest_val) % (
            c.ul, "Key", "Value", "Temporary", " " * width, c.w)
    else:
        out = "  %s%-{}s   %s%s%s\n".format(longest_key) % (c.ul, "Key", "Value", " " * width, c.w)

    for setting in config:
        val = config[setting]

        # don't show player specific settings if unknown player
        if not util.is_known_player(config.PLAYER.get) and \
                val.require_known_player:
            continue

        # don't show max_results if auto determined
        if g.detectable_size and setting == "MAX_RESULTS":
            continue

        if g.detectable_size and setting == "CONSOLE_WIDTH":
            continue

        out += s % (c.g, setting.lower(), c.w, val.display)

        if has_temps:
            out += "%s%s" % (c.w, val.display_temp)

        out += "\n"

    g.content = out
    g.message = "Enter %sset <key> <value>%s to change\n" % (c.g, c.w)
    g.message += "Enter %sset all default%s to reset all" % (c.g, c.w)


@command(r'set\s+-t\s*([-\w]+)\s*(.*)')
def setconfigtemp(key, val):
    setconfig(key, val, is_temp=True)


@command(r'set\s+([-\w]+)\s*(.*)')
def setconfig(key, val, is_temp=False):
    """ Set configuration variable. """
    key = key.replace("-", "_")
    if key.upper() == "ALL" and val.upper() == "DEFAULT":

        for ci in config:
            config[ci].value = config[ci].default

        config.save()
        message = "Default configuration reinstated"

    elif not key.upper() in config:
        message = "Unknown config item: %s%s%s" % (c.r, key, c.w)

    elif val.upper() == "DEFAULT":
        att = config[key.upper()]
        att.value = att.default
        att.temp_value = None
        message = "%s%s%s set to %s%s%s (default)"
        dispval = att.display or "None"
        message = message % (c.y, key, c.w, c.y, dispval, c.w)
        config.save()

    else:
        # config.save() will be called by config.set() method
        message = config[key.upper()].set(val, is_temp=is_temp)

    showconfig()
    g.message = message


@command(r'encoders?', 'encoder')
def show_encs():
    """ Display available encoding presets. """
    out = "%sEncoding profiles:%s\n\n" % (c.ul, c.w)

    for x, e in enumerate(g.encoders):
        sel = " (%sselected%s)" % (c.y, c.w) if config.ENCODER.get == x else ""
        out += "%2d. %s%s\n" % (x, e['name'], sel)

    g.content = out
    message = "Enter %sset encoder <num>%s to select an encoder"
    g.message = message % (c.g, c.w)
