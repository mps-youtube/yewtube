import os
import re
import collections
import importlib
import json
from zipfile import ZipFile
from zipimport import zipimporter

from pkg_resources import Requirement, resource_filename

from . import g, commands

coreplugin_dir = resource_filename(
        Requirement.parse("mps-youtube"),
        "core_plugins.zip")

EventHandler = collections.namedtuple('EventHandler', 'name function')


class Plugin:
    """ A plugin for mps_youtube. """

    _commands = []
    _eventhandlers = []

    def __init__(self):
        g.commands.extend(self._commands)
        g.eventhandlers.extend(self._eventhandlers)

    @classmethod
    def command(cls, regex, category, usage):
        """ Decorator to register an mps-youtube command. """

        def decorator(function):
            command = commands.Command(re.compile(regex),
                    category, usage, function)
            cls._commands.append(command)
            return function
        return decorator

    @classmethod
    def eventHandler(cls, event_name):
        """ Decorator to register an mps-youtube event handler. """

        def decorator(function):
            eventhandler = EventHandler(event_name, function)
            cls.eventhandlers.append(eventhandler)
            return function
        return decorator

    def _unload(self):
        g.commands = [i for i in g.commands if i not in self._commands]
        g.eventhandlers = [i for i in g.eventhandlers
                if i not in self._eventhandlers]

        self.unload()

    def unload(self):
        """ Implement in subclass for custom behavior plugin is unloaded. """

        pass
    

def registerPlugin(name):
    """ Decorator to register a plugin with mps-youtube. """

    def decorator(plugin):
        g.plugins[name] = plugin
        return plugin
    return decorator


def loadPlugins():
    """ Loads all mps-youtube plugins. """
    pass


@commands.command(r'pluginload\s+([^./]+)\s*$')
def loadPlugin(name):
    #TODO: Make user friendly. This is just the testing interface.

    pluginpaths = [coreplugin_dir] + [g.PLUGINDIR + i
            for i in os.listdir(g.PLUGINDIR)]
    loader = importlib.find_loader(name, path=pluginpaths)

    if isinstance(loader, zipimporter):
        with ZipFile(loader.archive, 'r') as pkgzip:
            metadata = json.loads(pkgzip.open('metadata.json', 'r'
                ).read().decode("utf-8"))[name]
    else:
        with open(os.path.split(loader.path)[0] + 'metadata.json') as pkgmeta:
            metadata = json.loads(pkgmeta.read())[name]

    loader.load_module(name)

    g.enabled_plugins[name] = g.plugins[name]()


@commands.command(r'pluginunload\s+([^./]+)\s*$')
def unloadPlugin(name):
    #TODO: Make user friendly. This is just the testing interface.
    g.enabled_plugins[name]._unload()
    del g.enabled_plugins[name]
