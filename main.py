from pathlib import Path
from PIL import Image, ImageStat

TILE_SIZE = (10, 10)
IMAGE = input('Input way to main picture: \n')
IMAGE = Image.open(IMAGE).convert('RGB')
WIDTH, LENGTH = IMAGE.size
WIDTH = (WIDTH // TILE_SIZE[0]) * TILE_SIZE[0] * 10
LENGTH = (LENGTH // TILE_SIZE[1]) * TILE_SIZE[1] * 10
IMAGE = IMAGE.resize((WIDTH, LENGTH))

folder = Path(input('Input way to folder with tiles: \n'))
images = []
for file in folder.glob('*.jpg'):
    img = Image.open(file).convert('RGB')
    img = img.resize(TILE_SIZE)
    avg_color = tuple(map(int, ImageStat.Stat(img).mean))
    images.append((img.copy(), avg_color))


def closest_color(target_color, tiles_list):
    min_dist = float('inf')
    best_tile = None
    for tile_img, avg_color in tiles_list:
        dist = math.sqrt(
            (target_color[0] - avg_color[0]) ** 2 +
            (target_color[1] - avg_color[1]) ** 2 +
            (target_color[2] - avg_color[2]) ** 2
        )
        if dist < min_dist:
            min_dist = dist
            best_tile = tile_img
    return best_tile


mosaic = Image.new('RGB',(WIDTH, LENGTH))

for x in range(0, WIDTH, TILE_SIZE[0]):
    for y in range(0, LENGTH, TILE_SIZE[1]):
        box = (x, y, x + TILE_SIZE[0], y + TILE_SIZE[1])
        block = IMAGE.crop(box)
        avg_color = tuple(map(int, ImageStat.Stat(block).mean))
        tile = closest_color(avg_color, images)
        mosaic.paste(im=tile, box=box)

mosaic.save('result.jpg')
mosaic.show()