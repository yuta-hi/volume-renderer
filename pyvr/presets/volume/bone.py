import json
from collections import OrderedDict

color_transfer = [[-3024., 0., 0., 0.],
                  [-2800., 0., 0., 0.],
                  [90, 1., 1., 0.],
                  [150, 1., 0.1, 0.],
                  [280, 1., 0.77, 0.73],
                  [520, 1., 0.95, 0.6],
                  [700, 1., 1., 1.],
                  [2000, 1., 1., 1.],
                  [3071., 0., 0., 1.]]

color_transfer = [c + [0.5, 0.0] for c in color_transfer]

scalar_opacity = [[-3024, 0.],
                  [100, 0.],
                  [250, 0.2],
                  [430, 0.5],
                  [580, 0.8],
                  [1500, 1.0],
                  [3071, 0.6]]

scalar_opacity = [o + [0.5, 0.0] for o in scalar_opacity]

preset = OrderedDict()
preset['color_transfer'] = color_transfer
preset['scalar_opacity'] = scalar_opacity
preset['gradient_opacity'] = None
preset['specular'] = 0.5
preset['specular_power'] = 40
preset['ambient'] = 0.3
preset['diffuse'] = 0.6
preset['shade'] = True
preset['interpolation'] = True

with open('bone.json', 'w') as fp:
    json.dump(preset, fp, indent=2)

with open('bone.json') as f:
    data = json.load(f)
print(data)
print(data['scalar_opacity'])
