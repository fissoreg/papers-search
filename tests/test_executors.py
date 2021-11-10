# Make the application source reachable
import sys

sys.path.append("../")
sys.path.append("./backend/src/")

from executors import *
from flows import *
from jina import Document, DocumentArray

papers = [
    "Relative gradient optimization of the Jacobian term in unsupervised deep learning[SEP]Efficient training of linear flows",
    "Attention Is All You Need[SEP]Introducing the Transformer architecture for state-of-the-art results in Natural Language Processing",
]


docs = DocumentArray([Document(text=seq) for seq in papers])


def label_doc(docs):
    """Label first `doc` with the following `docs`"""

    d = Document(text=papers[0])

    matches = DocumentArray(
        [Document(text=seq, tags={"finetuner": {"label": 1}}) for seq in papers[1:]]
    )

    d.matches.extend(matches)

    return d


def encode_sequences(docs):
    embedded_docs = SpecterExecutor().encode(docs)

    return embedded_docs


# def test_Specter_encoding():
#    embedded_docs = encode_sequences(docs)


def test_index():
    indexer = index_flow()

    with indexer:
        indexer.index(docs, request_size=len(docs))


def test_search():
    flow = search_flow()

    with flow:
        results = flow.search(docs)

    return results
