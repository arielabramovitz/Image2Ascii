CLI tool that takes an image, and converts it to ASCII.

usage: main.py [-h] [--rows ROWS] [--cols COLS] [--scale SCALE] [--format {html,txt}] file-path

positional arguments:
  file-path             Path for an image file.

options:
  -h, --help            show this help message and exit
  --rows ROWS, --r ROWS
                        Number of rows to split the image by (optional - default is calculated using columns).
  --cols COLS           Number of columns to split the image by (optional - default is 128).
  --scale SCALE         Output scale (optional - default is 0.5).
  --format {html,txt}   Output format (optional - default is html)

