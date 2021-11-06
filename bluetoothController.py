import dbus, dbus.mainloop.glib, sys
from gi.repository import GLib
import json

class BluetoothController:

    def __init__(self):
        self.data = {}

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SystemBus()
        obj = bus.get_object("org.bluez", "/")
        mgr = dbus.Interface(obj, "org.freedesktop.DBus.ObjectManager")
        self.player_iface = None
        self.transport_prop_iface = None
        while (not self.player_iface or not self.transport_prop_iface):
            for path, ifaces in mgr.GetManagedObjects().items():
                if "org.bluez.MediaPlayer1" in ifaces:
                    self.player_iface = dbus.Interface(
                            bus.get_object("org.bluez", path),
                            "org.bluez.MediaPlayer1")
                elif "org.bluez.MediaTransport1" in ifaces:
                    self.transport_prop_iface = dbus.Interface(
                            bus.get_object("org.bluez", path),
                            "org.freedesktop.DBus.Properties")
            if not self.player_iface:
                print("Error: Media Player not found.")
            if not self.transport_prop_iface:
                print("Error: DBus.Properties iface not found.")

        bus.add_signal_receiver(
                self.on_property_changed,
                bus_name="org.bluez",
                signal_name="PropertiesChanged",
                dbus_interface="org.freedesktop.DBus.Properties")
        GLib.io_add_watch(sys.stdin, GLib.IO_IN, self.on_playback_control)

    def serveForever(self):
        GLib.MainLoop().run()

    def on_property_changed(self, interface, changed, invalidated):
        if interface != "org.bluez.MediaPlayer1":
            return
        for prop, value in changed.items():
            print(f"{prop}: {value}")
            
            if prop == "Status":
                self.data["Status"] = value
                #print(f"Playback Status: {value}")

            elif prop == "Track":
                #print("Music Info:")
                self.data["Track"] = {}
                for key in ("Title", "Artist", "Album"):
                    val = value.get(key, "")
                    self.data["Track"][key] = val
                    #print(f"{key}: {val}")

        with open("data.json", "w") as f:
            f.write(json.dumps(self.data))

    def on_playback_control(self, fd, condition):
        str = fd.readline()
        if str.startswith("play"):
            self.player_iface.Play()
        elif str.startswith("pause"):
            self.player_iface.Pause()
        elif str.startswith("next"):
            self.player_iface.Next()
        elif str.startswith("prev"):
            self.player_iface.Previous()
        elif str.startswith("vol"):
            vol = int(str.split()[1])
            if vol not in range(0, 128):
                print("Possible Values: 0-127")
                return True
            self.transport_prop_iface.Set(
                    "org.bluez.MediaTransport1",
                    "Volume",
                    dbus.UInt16(vol))
        return True

    def play(self):
        self.player_iface.Play()

    def pause(self):
        self.player_iface.Pause()

    def next(self):
        self.player_iface.Next()

    def prev(self):
        self.player_iface.Previous()