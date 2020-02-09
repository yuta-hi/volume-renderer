from pyvr.preset import VolumePreset
from pyvr.preset import LabelPreset

if __name__ == '__main__':

    preset = VolumePreset('muscle')
    print(preset.preset)
    print(preset.color_transfer)

    preset = LabelPreset('muscle')
    print(preset.preset)
    print(preset.color)
    print(preset.legend)
    print(preset.colormap)
