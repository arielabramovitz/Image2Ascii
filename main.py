from PIL import Image, ImageOps
import numpy as np
import argparse as arg
import os

greyscale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "


def tile_to_letter(tile):
    lum = np.average(tile.reshape(tile.shape[0] * tile.shape[1]))
    return ord(greyscale[int((lum * 69 / 255))])


def create_file(filepath, letters):
    output = filepath.split("/")[-1].split(".")[0] + ".txt"
    with open(output, "w") as file:
        for i in range(len(letters)):
            file.writelines(letters[i])
            file.write("\n")


def create_html(filepath, letters):
    output = filepath.split("/")[-1].split(".")[0] + ".html"
    with open(output, "w") as file:
        file.write('<!DOCTYPE html>\n<html>\n<body style="COLOR:#000000; TEXT-ALIGN:center; FONT-SIZE:1px;">\n'
                   '<div style="white-space:pre; FONT-FAMILY:monospace; FONT-SIZE:1rem; '
                   'LETTER-SPACING:0.15em; LINE-HEIGHT:0.800000em;">\n')
        for i in range(len(letters)):
            let = "".join(letters[i])
            let = let.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
            file.write(let + "\n")
        file.write('</div>\n</body>\n</html>\n')


def get_tile(image, row, col, tile_width, tile_height):
    width, height = image.size
    x1, x2, y1, y2 = int(row * tile_width), int((row + 1) * tile_width), int(col * tile_height), int(
        (col + 1) * tile_height)
    x2, y2 = min(x2, width), min(y2, height)
    return image.crop((x1, y1, x2, y2))


def convert(image, args):
    width, height = image.size
    tile_width = width / args["cols"]
    tile_height = tile_width / args["scale"]
    if args["rows"] == 0:
        args["rows"] = int(height / tile_height)
    if not (1 <= args["rows"] <= height and 1 <= args["cols"] <= width):
        print("Row/Column number is invalid")
        return
    converted = np.ndarray(shape=(args["rows"], args["cols"]), dtype=int)
    for i in range(args["rows"]):
        for j in range(args["cols"]):
            tile = get_tile(image, j, i, tile_width, tile_height)
            converted[i, j] = tile_to_letter(np.array(tile))
    letters = [[chr(letter) for letter in row] for row in converted[:]]
    if args["format"] == "html":
        create_html(args["file-path"], letters)
    else:
        create_file(args["file-path"], letters)


def arg_parser_init():
    parser = arg.ArgumentParser()
    parser.add_argument("file-path", help="Path for an image file.")
    parser.add_argument("--rows", type=int, default=0,
                        help="Number of rows to split the image by (optional - default is "
                             "calculated using columns ).")
    parser.add_argument("--cols", type=int, default=128,
                        help="Number of columns to split the image by (optional - default is "
                             "128).")
    parser.add_argument("--scale", type=float, default=0.5, help="Output scale (optional - default is 0.5).")
    parser.add_argument("--format", type=str, default="html", help="Output format (optional - default is html)",
                        choices=["html",
                                 "txt"])
    args = vars(parser.parse_args())
    return args


if __name__ == "__main__":
    args = arg_parser_init()
    if os.path.isfile(args["file-path"]):
        with Image.open(args["file-path"]) as img:
            bw = ImageOps.grayscale(img)
        convert(bw, args)
