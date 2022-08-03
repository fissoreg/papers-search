import argparse
import os

from docarray import DocumentArray
from docarray.document.generators import from_csv

from backend_config import papers_data_path, papers_data_url
from flows import index_flow, search_flow
from helpers import download_csv, log, maximise_csv_field_size_limit


# boolean args:
# https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse/36031646
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def get_args():
    # Command line arguments definitions
    parser = argparse.ArgumentParser()
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


def index(n):
    if not os.path.exists(papers_data_path):
        log("Downloading data...")
        download_csv(papers_data_url, papers_data_path)

    maximise_csv_field_size_limit()

    with open(papers_data_path, encoding="utf-8") as data_file:
        docs_generator = from_csv(
            data_file,
            field_resolver={"source_id": "id"},
        )
        papers = DocumentArray(docs_generator)

        for paper in papers:
            paper.text = paper.tags["title"] + "[SEP]" + paper.tags["abstract"]

    if n != 0:
        papers = papers[:n]

    log(f"Loaded {len(papers)} papers from {papers_data_path}.")

    log("Building index...")
    indexer = index_flow()
    with indexer:
        indexer.index(papers, request_size=32)


args = get_args()

if args.index:
    index(args.n)

# running the search/finetuning flow as a service
flow = search_flow()
flow.expose_endpoint("/finetune", summary="Finetune documents.", tags=["Finetuning"])

with flow:
    log("Ready for searching.")
    flow.block()
