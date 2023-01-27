import os

mswin = os.name == "nt"


def get_default_ddir():
    """ Get system default Download directory, append mps dir. """
    user_home = os.path.expanduser("~")
    join, exists = os.path.join, os.path.exists

    if mswin:
        return join(user_home, "Downloads", "yewtube")

    USER_DIRS = join(user_home, ".config", "user-dirs.dirs")
    DOWNLOAD_HOME = join(user_home, "Downloads")

    # define ddir by (1) env var, (2) user-dirs.dirs file,
    #                (3) existing ~/Downloads dir (4) ~

    if 'XDG_DOWNLOAD_DIR' in os.environ:
        ddir = os.environ['XDG_DOWNLOAD_DIR']

    elif exists(USER_DIRS):
        lines = open(USER_DIRS).readlines()
        defn = [x for x in lines if x.startswith("XDG_DOWNLOAD_DIR")]

        if len(defn) == 1:
            ddir = defn[0].split("=")[1].replace('"', '')
            ddir = ddir.replace("$HOME", user_home).strip()

        else:
            ddir = DOWNLOAD_HOME if exists(DOWNLOAD_HOME) else user_home

    else:
        ddir = DOWNLOAD_HOME if exists(DOWNLOAD_HOME) else user_home

    ddir = ddir
    return os.path.join(ddir, "mps")


def get_config_dir():
    """ Get user's configuration directory. Migrate to new mps name if old."""
    if mswin:
        confdir = os.environ["APPDATA"]

    elif 'XDG_CONFIG_HOME' in os.environ:
        confdir = os.environ['XDG_CONFIG_HOME']

    else:
        confdir = os.path.join(os.path.expanduser("~"), '.config')

    mps_confdir = os.path.join(confdir, "mps-youtube")

    os.makedirs(mps_confdir, exist_ok=True)

    return mps_confdir
