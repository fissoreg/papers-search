from jina import Flow

from config import config
from executors import SpecterExecutor

# Using a standard indexer: https://hub.jina.ai/executor/zb38xlt4
indexer = "jinahub://SimpleIndexer"


def index_flow():
    flow = (
        Flow(protocol="grpc")
        .add(uses=SpecterExecutor)
        .add(
            uses=indexer,
        )
    )

    return flow


def search_flow():
    flow = (
        Flow(port_expose=config["search_port"].get(), protocol="http")
        .add(uses=SpecterExecutor)
        .add(
            uses=indexer,
            uses_with={
                "match_args": {
                    "metric": "cosine",
                    "limit": config["top_k"].get(),
                },
            },
        )
    )

    return flow
