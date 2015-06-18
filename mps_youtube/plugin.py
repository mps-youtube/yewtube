import os
import collections
import pkgutil

from . import g, plugins

Command = collections.namedtuple('Command', 'regex category usage function')
EventHandler = collections.namedtuple('EventHandler', 'name function')


class Plugin:
    """ A plugin for mps_youtube. """

    _commands = []
    _eventhandlers = []

    def __init__(self):
        g.commands.extent(self._commands)
        g.eventhandlers.extent(self._eventhandlers)

    @classmethod
    def command(cls, regex, category, usage):
        """ Decorator to register an mps-youtube command. """

        def decorator(function):
            command = Command(regex, category, usage, function)
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
        g.commands = [i for i in g.plugin_command if i not in self._commands]
        g.eventhandlers = [i for i in g.eventhandlers
                if i not in self._eventhandlers]

        self.unload()

    def unload(self):
        """ Implement in subclass for custom behavior plugin is unloaded. """

        pass
    

def registerPlugin(plugin):
    """ Decorator to registor a plugin with mps-youtube. """

    g.plugins[plugin.name] = plugin
    return plugin


def loadPlugins():
    """ Loads all mps-youtube plugins. """

    pluginpaths = plugins.__path__ + [g.PLUGINDIR]

    for loader, name, is_pkg in  pkgutil.iter_modules(pluginpaths):
        loader.find_module(name).load_module(name)
