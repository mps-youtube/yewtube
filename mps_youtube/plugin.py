import os
import re
import collections
import pkgutil

from . import g, plugins, commands


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
    

def registerPlugin(plugin):
    """ Decorator to register a plugin with mps-youtube. """

    g.plugins[plugin.name] = plugin
    return plugin


def loadPlugins():
    """ Loads all mps-youtube plugins. """

    pluginpaths = plugins.__path__ + [g.PLUGINDIR]

    for loader, name, is_pkg in  pkgutil.iter_modules(pluginpaths):
        loader.find_module(name).load_module(name)


@commands.command(r'pluginload\s+([^./]+)\s*$')
def loadPlugin(name):
    #TODO: Make user friendly. This is just the testing interface.
    g.enabled_plugins[name] = g.plugins[name]()


@commands.command(r'pluginunload\s+([^./]+)\s*$')
def unloadPlugin(name):
    #TODO: Make user friendly. This is just the testing interface.
    g.enabled_plugins[name]._unload()
    del g.enabled_plugins[name]
