import dbus, dbus.mainloop.glib, sys
from gi.repository import GLib
import json
import os

class BluetoothController:

    def __init__(self):
        self.data = {}

    def serveForever(self):
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
        GLib.MainLoop().run()

    def on_property_changed(self, interface, changed, invalidated):
        if interface != "org.bluez.MediaPlayer1":
            return
        print(invalidated)
        for prop, value in changed.items():
            print(f"{prop}: {value}")
            
            if prop == "Status":
                self.data["Status"] = value

            elif prop == "Track":
                self.data["Track"] = {}
                for key in ("Title", "Artist", "Album"):
                    val = value.get(key, "")
                    self.data["Track"][key] = val

            elif prop == "Position":
                self.data["Position"] = value

        with open("data.json", "w") as f:
            f.write(json.dumps(self.data))

    def on_playback_control(self, fd, condition):
        if os.path.exists(f"{os.getcwd()}/rpiBluetoothPlayer/status.txt"):
            with open(f"{os.getcwd()}/rpiBluetoothPlayer/status.txt", "r") as f:
                data = f.read()[0]
                print(data)
                if (data == "1"):
                    self.player_iface.Play()
                elif (data == "0"):
                    print("PAUSE")
                    self.player_iface.Pause()
                elif (data == "3"):
                    self.player_iface.Next()
                elif (data == "2"):
                    self.player_iface.Previous()
                elif (data == "5"):
                    vol = int(str.split()[1])
                    if vol not in range(0, 128):
                        print("Possible Values: 0-127")
                        return True
                    self.transport_prop_iface.Set(
                            "org.bluez.MediaTransport1",
                            "Volume",
                            dbus.UInt16(vol))
            os.remove(f"{os.getcwd()}/rpiBluetoothPlayer/status.txt")
        return True

    def play(self):
        self.player_iface.Play()

    def pause(self):
        self.player_iface.Pause()

    def next(self):
        self.player_iface.Next()

    def prev(self):
        self.player_iface.Previous()