import json
from collections import OrderedDict
import matplotlib.cm as cm

scalar_range = [0., 1.0e-2]
cmap = cm.get_cmap('jet')

color_transfer = []
for i in range(255):
    r, g, b, _ = cmap(float(i)/255.)
    x = (scalar_range[1] - scalar_range[0]) / 255. * float(i) + scalar_range[0]
    color_transfer.append([x, r, g, b])

color_transfer = [c + [1.0, 0.0] for c in color_transfer]

scalar_opacity = []
scalar_opacity.append([(scalar_range[1] - scalar_range[0]) * 0.0, 0.0])
scalar_opacity.append([(scalar_range[1] - scalar_range[0]) * 0.05, 0.0])
scalar_opacity.append([(scalar_range[1] - scalar_range[0]) * 0.5, 0.3])
scalar_opacity.append([(scalar_range[1] - scalar_range[0]) * 1.0, 1.0])

scalar_opacity = [o + [1., 0.05] for o in scalar_opacity]

preset = OrderedDict()

preset['color_transfer'] = color_transfer
preset['scalar_opacity'] = scalar_opacity
preset['gradient_opacity'] = None
preset['specular'] = 0.2
preset['specular_power'] = 10
preset['ambient'] = 0.8
preset['diffuse'] = 0.8
preset['shade'] = True
preset['interpolation'] = True

with open('uncertainty.json', 'w') as fp:
    json.dump(preset, fp, indent=2)

with open('uncertainty.json') as f:
    data = json.load(f)

print(data)
