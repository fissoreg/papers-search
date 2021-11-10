from jina import Flow

from executors import SpecterExecutor
from backend_config import top_k, search_port

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
        Flow(port_expose=search_port, protocol="http")
        .add(uses=SpecterExecutor)
        .add(
            uses=indexer,
            uses_with={
                "match_args": {
                    "metric": "cosine",
                    "limit": top_k,
                },
            },
        )
    )

    return flow
