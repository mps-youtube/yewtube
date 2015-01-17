# The MIT License (MIT)

# Copyright (c) 2015 Jiri Horner

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import subprocess

IDENTITY = 'mps-youtube'

BUS_NAME = 'org.mpris.MediaPlayer2.' + IDENTITY
ROOT_INTERFACE = 'org.mpris.MediaPlayer2'
PLAYER_INTERFACE = 'org.mpris.MediaPlayer2.Player'
PROPERTIES_INTERFACE = 'org.freedesktop.DBus.Properties'
MPRIS_PATH = '/org/mpris/MediaPlayer2'

class Mpris2Controller(object):

    """
        Controller for various MPRIS objects.
    """

    def __init__(self):
        """
            Constructs an MPRIS controller. Note, you must call acquire()
        """
        self.mpris = None
        self.bus = None
        self.main_loop = GLib.MainLoop()

    def release(self):
        """
            Releases all objects from D-Bus and unregisters the bus
        """
        if self.mpris is not None:
            self.mpris.remove_from_connection()
        self.mpris = None
        if self.bus is not None:
            self.bus.get_bus().release_name(self.bus.get_name())

    def acquire(self):
        """
            Connects to D-Bus and registers all components
        """
        self._acquire_bus()
        self._add_interfaces()

    def run(self):
        """
            Runs main loop, processing all calls
        """
        self.main_loop.run()

    def _acquire_bus(self):
        """
            Connect to D-Bus and set self.bus to be a valid connection
        """
        if self.bus is not None:
            self.bus.get_bus().request_name(BUS_NAME)
        else:
            self.bus = dbus.service.BusName(BUS_NAME, 
                bus=dbus.SessionBus(mainloop=DBusGMainLoop()))

    def _add_interfaces(self):
        """
            Connects all interfaces to D-Bus
        """
        self.mpris = Mpris2MediaPlayer(self.bus)


class Mpris2MediaPlayer(dbus.service.Object):

    """
        implementing interfaces:
            org.mpris.MediaPlayer2
            org.mpris.MediaPlayer2.Player
    """

    def __init__(self, bus):
        dbus.service.Object.__init__(self, bus, MPRIS_PATH)
        self.properties = {
            ROOT_INTERFACE : {
                'read_only' : {
                    'CanQuit' : False,
                    'CanSetFullscreen' : False,
                    'CanRaise' : False,
                    'HasTrackList' : False,
                    'Identity' : IDENTITY,
                    'SupportedUriSchemes' : ['file', 'http'],
                    'SupportedMimeTypes' : ['audio/mpeg'],
                },
                'read_write' : {
                    'Fullscreen' : False,
                },
            },
            PLAYER_INTERFACE : {
                'read_only' : {
                    'PlaybackStatus' : 'Stopped',
                    'Metadata' : { 'mpris:trackid' : dbus.ObjectPath(
                                '/CurrentPlaylist/UnknownTrack', variant_level=1) },
                    'Position' : dbus.Int64(0),
                    'MinimumRate' : 1.0,
                    'MaximumRate' : 1.0,
                    'CanGoNext' : True,
                    'CanGoPrevious' : True,
                    'CanPlay' : True,
                    'CanPause' : True,
                    'CanSeek' : False,
                    'CanControl' : True,
                },
                'read_write' : {
                    'LoopStatus' : 'None',
                    'Rate' : 1.0,
                    'Shuffle' : False,
                    'Volume' : 1.0,
                },
            },
        }

    """
        implementing org.mpris.MediaPlayer2
    """

    @dbus.service.method(dbus_interface=ROOT_INTERFACE)
    def Raise(self):
        """
            Brings the media player's user interface to the front using
            any appropriate mechanism available.
        """
        pass

    @dbus.service.method(dbus_interface=ROOT_INTERFACE)
    def Quit(self):
        """
            Causes the media player to stop running.
        """
        pass

    """
        implementing org.mpris.MediaPlayer2.Player
    """

    @dbus.service.method(dbus_interface=PLAYER_INTERFACE)
    def Next(self):
        """
            Skips to the next track in the tracklist.
        """
        subprocess.Popen(['xdotool', 'search', '--class', 'mpsyt', 'key', 'n'])

    @dbus.service.method(PLAYER_INTERFACE)
    def Previous(self):
        """
            Skips to the previous track in the tracklist.
        """
        subprocess.Popen(['xdotool', 'search', '--class', 'mpsyt', 'key', 'p'])

    @dbus.service.method(PLAYER_INTERFACE)
    def Pause(self):
        """
            Pauses playback.
            If playback is already paused, this has no effect.
        """
        subprocess.Popen(['xdotool', 'search', '--class', 'mpsyt', 'key', 'space'])

    @dbus.service.method(PLAYER_INTERFACE)
    def PlayPause(self):
        """
            Pauses playback.
            If playback is already paused, resumes playback.
        """
        subprocess.Popen(['xdotool', 'search', '--class', 'mpsyt', 'key', 'space'])

    @dbus.service.method(PLAYER_INTERFACE)
    def Stop(self):
        """
            Stops playback.
        """
        subprocess.Popen(['xdotool', 'search', '--class', 'mpsyt', 'key', 'q'])

    @dbus.service.method(PLAYER_INTERFACE)
    def Play(self):
        """
            Starts or resumes playback.
        """
        subprocess.Popen(['xdotool', 'search', '--class', 'mpsyt', 'key', 'space'])

    @dbus.service.method(PLAYER_INTERFACE, in_signature='x')
    def Seek(self, offset):
        """
            Offset - x (offset)
                The number of microseconds to seek forward.

            Seeks forward in the current track by the specified number
            of microseconds.
        """
        pass

    @dbus.service.method(PLAYER_INTERFACE, in_signature='ox')
    def SetPosition(self, track_id, position):
        """
            TrackId - o (track_id)
                The currently playing track's identifier.
                If this does not match the id of the currently-playing track, the call is ignored as "stale".
            Position - x (position)
                Track position in microseconds.

            Sets the current track position in microseconds.
        """
        pass

    @dbus.service.method(PLAYER_INTERFACE, in_signature='s')
    def OpenUri(self, uri):
        """
            Uri - s (uri)
                Uri of the track to load.

            Opens the Uri given as an argument.
        """
        pass

    @dbus.service.signal(PLAYER_INTERFACE, signature='x')
    def Seeked(self, position):
        """
            Position - x (position)
                The new position, in microseconds.

            Indicates that the track position has changed in a way that
            is inconsistant with the current playing state.
        """
        pass

    """
        implementing org.freedesktop.DBus.Properties
    """

    @dbus.service.method(dbus_interface=PROPERTIES_INTERFACE,
                         in_signature='ss', out_signature='v')
    def Get(self, interface_name, property_name):
        return self.GetAll(interface_name)[property_name]

    @dbus.service.method(dbus_interface=PROPERTIES_INTERFACE,
                         in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface_name):
        if interface_name in self.properties:
            t = self.properties[interface_name]['read_only'].copy()
            t.update(self.properties[interface_name]['read_write'])

            return t
        else:
            raise dbus.exceptions.DBusException(
                'com.example.UnknownInterface',
                'This object does not implement the %s interface'
                    % interface_name)

    @dbus.service.method(dbus_interface=PROPERTIES_INTERFACE,
                         in_signature='ssv')
    def Set(self, interface_name, property_name, new_value):
        if interface_name in self.properties:
            if property_name in self.properties[interface_name]['read_write']:
                self.properties[interface_name]['read_write'][property_name] = new_value
                self.PropertiesChanged(interface_name,
                    { property_name: new_value }, [])
        else:
            raise dbus.exceptions.DBusException(
                'com.example.UnknownInterface',
                'This object does not implement the %s interface'
                    % interface_name)

    @dbus.service.signal(dbus_interface=PROPERTIES_INTERFACE,
                         signature='sa{sv}as')
    def PropertiesChanged(self, interface_name, changed_properties,
                          invalidated_properties):
        pass

mpris = Mpris2Controller()
mpris.acquire()
mpris.run()