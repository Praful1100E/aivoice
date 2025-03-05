from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc

class SystemController:
    def __init__(self):
        self.setup_audio()

    def setup_audio(self):
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume.iid, CLSCTX_ALL, None)
            self.volume = interface.QueryInterface(IAudioEndpointVolume)
        except Exception as e:
            print(f"Audio setup error: {e}")
            self.volume = None

    def set_volume(self, level):
        try:
            if self.volume:
                self.volume.SetMasterVolumeLevelScalar(level / 100, None)
                return True
            return False
        except Exception as e:
            print(f"Volume control error: {e}")
            return False

    def set_brightness(self, level):
        try:
            sbc.set_brightness(level)
            return True
        except Exception as e:
            print(f"Brightness control error: {e}")
            return False
