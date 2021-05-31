import os
from urllib.request import urlretrieve

weights_map = {
    'facenet': 'https://drive.google.com/uc?id=1971Xk5RwedbudGgTIrGAL4F7Aifu7id1',
    'darknet': 'https://drive.google.com/open?id=1cewMfusmPjYWbrnuJRuKhPMwRe_b9PaT'
}


def get_weights(name):
    url = weights_map[name]
    path = f'./weights/{name}.weights'

    if not os.path.isfile(path):
        print(f"'{path}' will be downloaded...")
        urlretrieve(url, path)
    print("DONE")
    return path
