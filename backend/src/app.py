import argparse
import os

from docarray import DocumentArray
from docarray.document.generators import from_csv

from config import config, create_parser
from flows import index_flow, search_flow
from helpers import download_csv, log, maximise_csv_field_size_limit

papers_data_path = config["papers_data_path"].get()
papers_data_url = config["papers_data_url"].get()


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


args = create_parser()
config.set_args(args)

if args.index:
    index(args.n)

    # running the search/finetuning flow as a service
flow = search_flow()
flow.expose_endpoint("/finetune", summary="Finetune documents.", tags=["Finetuning"])

with flow:
    log("Ready for searching.")
    flow.block()
