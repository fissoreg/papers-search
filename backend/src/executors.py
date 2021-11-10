import re
import os

from typing import Sequence, List, Tuple
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
from jina import Executor, requests, Document, DocumentArray

from backend_config import top_k, embedding_model
from helpers import log


def get_model_dir():
    model_dir = f"./models/{embedding_model}"

    return model_dir


def load_embedding_model():
    model_dir = get_model_dir()

    # If the model is not already cached ...
    if not os.path.isdir(model_dir):
        log(f"{embedding_model} not found. Downloading...")

        model = SentenceTransformer(embedding_model)

        # # Saving model
        model.save(model_dir)

        log(f"{embedding_model} saved to {model_dir}")
    else:
        log(f"Loading {embedding_model} from {model_dir}")
        model = SentenceTransformer(model_dir)

    return model


class SpecterExecutor(Executor):
    def __init__(self, **kwargs):
        log("Initialising SpecterExecutor.")
        super().__init__()

        self.model = load_embedding_model()

    # All requests to SpecterExecutor run encode()
    @requests
    def encode(self, docs: DocumentArray, **kwargs) -> DocumentArray:

        # Loading a local model is cheap and when the finetuner is active we want up-to-date encodings
        self.model = load_embedding_model()

        log("Computing embeddings...")

        inputs = [
            doc.text for doc in docs
        ]  # doc.tags["title"] + "[SEP]" + doc.tags["abstract"] for doc in docs]

        embeddings = self.model.encode(inputs, show_progress_bar=True)

        for doc, embed in zip(docs, embeddings):
            doc.embedding = embed

        log("Embeddings computation completed.")
        return docs

    @requests(on="/finetune")
    def finetune(self, docs: DocumentArray, **kwargs) -> DocumentArray:

        log("Finetuning...")

        train_data = []

        for doc in docs:
            matches = doc.matches
            for match in doc.matches:
                train_data.append(
                    InputExample(
                        texts=[doc.text, match.text],
                        label=match.tags["finetuner"]["label"],
                    )
                )

        train_dataloader = DataLoader(train_data, shuffle=True, batch_size=len(docs))
        train_loss = losses.CosineSimilarityLoss(self.model)

        # Tune the model
        self.model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            epochs=5,
            warmup_steps=100,
        )

        self.model.save(get_model_dir())

        # Return the new embeddings given by the finetuned model
        return self.encode(docs)
