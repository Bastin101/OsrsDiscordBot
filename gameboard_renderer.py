from PIL import Image, ImageDraw, ImageFont
import os

board_offset = 25
tile_width = 15
player_circle_diameter = 7


def render(player_ids: list[str], player_positions: list[int], player_levels: list[int], level_lengths: list[int]) -> Image:
    file_path = "board.jpg"
    image_size = (1024, 256)

    if not os.path.exists(file_path):
        with open(file_path, "w"):
            pass

    with Image.new("RGB", image_size) as im:
        draw = ImageDraw.Draw(im)
        render_board(im, draw)
        for player_id, position, level in zip(player_ids, player_positions, player_levels):
            draw_player(im, draw, player_id, position, level)

    assert im.fp is None
    im.save(file_path)

def render_board(im, draw: ImageDraw.Draw):
    fnt = ImageFont.truetype("/usr/share/fonts/droid/DroidSans.ttf", 40)
    for level, level_length in enumerate(level_lengths):
        for i in range(level_length):
            xy = (board_offset + i * tile_width,
                  board_offset + level * tile_width,
                  board_offset + i * tile_width + tile_width,
                  board_offset + level * tile_width + tile_width)
            draw_tile(im, draw, xy)

def draw_tile(im, draw: ImageDraw.Draw, xy: tuple[int]):
    draw.rectangle((xy), width=1, fill=None, outline=(255, 255, 255, 255))

def draw_player(im, draw: ImageDraw.Draw, player_id: str, position: int, level: int):
    circle_diameter = 6
    xy = (board_offset + position * tile_width + (tile_width - circle_diameter) / 2,
          board_offset + level * tile_width + (tile_width - circle_diameter) / 2)
    draw.ellipse(xy, fill=(0, 255, 0, 255))

player_ids = [0, 1, 2]
positions = [0, 5, 10]
player_levels = [0, 2, 1]
level_lengths= [60, 60, 60, 60]
render(player_ids, positions, player_levels, level_lengths)
