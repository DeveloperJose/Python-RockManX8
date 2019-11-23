from PIL import Image


def split1(im):
    return [im]


def split2(im):
    return [im]


def split3(im: Image):
    return [
        im.crop((0, 0, 128, 128)),
        im.crop((0, 128, 128, 257)),
        im.crop((128, 0, 257, 128))
    ]


def split4(im):
    return [
        im.crop((0, 0, 128, 128)),
        im.crop((0, 128, 128, 257)),
        im.crop((128, 0, 257, 128)),
        im.crop((128, 128, 257, 257))
    ]


if __name__ == '__main__':
    from pathlib import Path
    import pickle

    pkl_path = 'mugshots.pkl'

    # Split depending on the number of mugshots in the image
    images_path = Path('images')
    results = [
        split4(Image.open(images_path / 'X.png')),
        split3(Image.open(images_path / 'Zero.png')),
        split4(Image.open(images_path / 'Axl.png')),
        split3(Image.open(images_path / 'Alia.png')),
        split3(Image.open(images_path / 'Layer.png')),
        split4(Image.open(images_path / 'Pallette.png')),
        split1(Image.open(images_path / 'Signas.png')),
        split1(Image.open(images_path / 'Light.png')),
        split1(Image.open(images_path / 'Sunflower.png')),
        split1(Image.open(images_path / 'Antonion.png')),
        split1(Image.open(images_path / 'Mantis.png')),
        split1(Image.open(images_path / 'Man-o-War.png')),
        split1(Image.open(images_path / 'Rooster.png')),
        split1(Image.open(images_path / 'Yeti.png')),
        split1(Image.open(images_path / 'Trilobyte.png')),
        split1(Image.open(images_path / 'Pandamonium.png')),
        split1(Image.open(images_path / 'Vile.png')),
        split2(Image.open(images_path / 'Sigma.png')),
        split3(Image.open(images_path / 'Lumine.png')),
        split3(Image.open(images_path / 'Alia.png')),
        split3(Image.open(images_path / 'Layer.png')),
        split4(Image.open(images_path / 'Pallette.png')),
    ]
    pickle.dump(results, open(pkl_path, 'wb'))