import json
from collections import OrderedDict

color_transfer = [[-3024., 0., 0., 0.],
                  [-320., 1., 0.5, 0.5],
                  [-200., 0.5, 0., 0.],
                  [-220., 1., 1., 0.],
                  [-40, 0.98, 0.98, 0.82],
                  [50, 0.7, 0., 0.],
                  [100, 1., 1., 1.],
                  [250, 1., 0.9, 0.9],
                  [540, 1., 1., 0.3],
                  [1400, 1., 1., 1.],
                  [3071., 0., 0.2, 1.]]

color_transfer = [c + [0.5, 0.0] for c in color_transfer]

scalar_opacity = [[-3024, 0.],
                  [-400, 0.],
                  [-60, 0.],
                  [180, 0.3],
                  [500, 0.65],
                  [950, 0.65],
                  [1300, 0.65],
                  [2000, 0.2],
                  [3071, 0.]]

scalar_opacity = [o + [0.25, 0.0] for o in scalar_opacity]

preset = OrderedDict()
preset['color_transfer'] = color_transfer
preset['scalar_opacity'] = scalar_opacity
preset['gradient_opacity'] = None
preset['specular'] = 0.2
preset['specular_power'] = 10
preset['ambient'] = 0.2
preset['diffuse'] = 0.8
preset['shade'] = True
preset['interpolation'] = True

with open('muscle.json', 'w') as fp:
    json.dump(preset, fp, indent=2)

with open('muscle.json') as f:
    data = json.load(f)
print(data)
print(data['scalar_opacity'])
