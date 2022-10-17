from argparse import ArgumentParser
from pathlib import Path

from confuse import Configuration

config = Configuration("backend")

file_abs_path = Path(__file__).parent.resolve()
config.set_file(file_abs_path / "config.yaml")


def create_parser():

    parser = ArgumentParser()

    parser.add_argument(
        "--index",
        dest="index",
        default=False,
        action="store_true",
        help="index the available documents",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=0,
        help="when `--index` is used, specifies the number of documnts to index (0 indexes the full dataset)",
    )

    return parser.parse_args()
