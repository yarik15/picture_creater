from pathlib import Path
from PIL import Image, ImageStat, ImageFile
import math
import os
from typing import Optional

SUPPORTED_EXTENSIONS : list[str] = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.webp']

class TileSizeConstant:
    WIDTH: int = 5
    LENGTH: int = 5

    @classmethod
    def get_width_length(cls) -> tuple[int, int]:
        return (cls.WIDTH, cls.LENGTH)


base_image: Optional[ImageFile] = None
flag: bool = False
while flag == False:
    base_image_path : str = 'картинка.jpg' #Input path to picture: \n
    if os.path.exists(base_image_path):
        flag = True
    else: print('Wrong path')


base_image = Image.open(base_image_path).convert('RGB')
base_width, base_length = base_image.size

try:
    target_width = int(input('Enter desired output width (or 0 to skip): ') or 0)
    target_height = int(input('Enter desired output width (or 0 to skip): ') or 0)
except ValueError:
    print("Invalid input. Using original size.")
    target_width = target_height = 0


folder: Optional[Path] = None
flag: bool = False
while flag == False:
    images_for_pixels_path: str = '../Изображения' #Input path to folder with tiles: \n
    if os.path.exists(images_for_pixels_path):
        flag = True
    else:
        print('Wrong path')

folder = Path(images_for_pixels_path)

if target_width > 0 and target_height > 0:
    scale_w = target_width / base_width
    scale_h = target_height / base_length
    scale = min(scale_w, scale_h)
    new_width = int(base_width * scale)
    new_height = int(base_length * scale)
elif target_width > 0:
    new_width = target_width
    new_height = int(base_length * (target_width / base_width))
elif target_height > 0:
    new_height = target_height
    new_width = int(base_width * (target_height / base_length))
else:
    new_width, new_height = base_width, base_length

new_width = (new_width // TileSizeConstant.WIDTH) * TileSizeConstant.WIDTH
new_height = (new_height // TileSizeConstant.LENGTH) * TileSizeConstant.LENGTH

resized_image = base_image.resize((new_width, new_height), Image.LANCZOS)

tiles: list[tuple[ImageFile, tuple]] = []
for exp in SUPPORTED_EXTENSIONS:
    for file in folder.glob(exp):
        img: ImageFile = Image.open(file).convert('RGB')
        img = img.resize(TileSizeConstant.get_width_length())
        avg_color = tuple(map(int, ImageStat.Stat(img).mean))
        tiles.append((img, avg_color))


def closest_color(target_color: tuple, tiles_list: tuple):
    if not tiles:
        raise ValueError("No valid tile images found...")

    min_dist = float('inf')
    best_tile: ImageFile = None
    for tile_img, avg_color in tiles_list:
        dist: float = math.sqrt(
            (target_color[0] - avg_color[0]) ** 2 +
            (target_color[1] - avg_color[1]) ** 2 +
            (target_color[2] - avg_color[2]) ** 2
        )
        if dist < min_dist:
            min_dist = dist
            best_tile = tile_img
    return best_tile


mosaic: ImageFile = Image.new('RGB',(new_width, new_height))

for x in range(0, new_width, TileSizeConstant.WIDTH):
    for y in range(0, new_height, TileSizeConstant.LENGTH):
        box: tuple = (x, y, x + TileSizeConstant.WIDTH, y + TileSizeConstant.LENGTH)
        block: ImageFile = resized_image.crop(box)
        avg_color: tuple = tuple(map(int, ImageStat.Stat(block).mean))
        tile: ImageFile = closest_color(avg_color, tiles)
        mosaic.paste(im=tile, box=box)

result : str = input('Input the name of mosaic: \n')
mosaic.save(f'{result}.jpg')
print(f'Mosaic saved as "{result}.jpg"')
mosaic.show()
