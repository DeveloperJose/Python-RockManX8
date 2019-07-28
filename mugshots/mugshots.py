import numpy as np
from PIL import Image


def split1(arr):
    return [arr]


def split2(arr):
    return [arr]


def split3(arr):
    return [arr[0:128, 0:128], arr[128:257, 0:128], arr[0:128, 128:257]]


def split4(arr):
    return [arr[0:128, 0:128], arr[128:257, 0:128], arr[0:128, 128:257], arr[128:257, 128:257]]


if __name__ == '__main__':
    from pathlib import Path

    path = Path(r'.')
    npz_path = path / 'mugshots.npz'
    results = [
        split4(np.array(Image.open(path / 'X.png'), dtype=np.uint8)),
        split3(np.array(Image.open(path / 'Zero.png'), dtype=np.uint8)),
        split4(np.array(Image.open(path / 'Axl.png'), dtype=np.uint8)),
        split3(np.array(Image.open(path / 'Alia.png'), dtype=np.uint8)),
        split3(np.array(Image.open(path / 'Layer.png'), dtype=np.uint8)),
        split4(np.array(Image.open(path / 'Pallette.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Signas.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Light.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Sunflower.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Antonion.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Mantis.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Man-o-War.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Rooster.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Yeti.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Trilobyte.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Pandamonium.png'), dtype=np.uint8)),
        split1(np.array(Image.open(path / 'Vile.png'), dtype=np.uint8)),
        split2(np.array(Image.open(path / 'Sigma.png'), dtype=np.uint8)),
        split3(np.array(Image.open(path / 'Lumine.png'), dtype=np.uint8)),
        split3(np.array(Image.open(path / 'Alia.png'), dtype=np.uint8)),
        split3(np.array(Image.open(path / 'Layer.png'), dtype=np.uint8)),
        split4(np.array(Image.open(path / 'Pallette.png'), dtype=np.uint8)),
    ]
    results = np.array(results, dtype=np.ndarray)
    np.savez_compressed(npz_path, mugshots=results)
    d = np.load(npz_path, allow_pickle=True)['mugshots']