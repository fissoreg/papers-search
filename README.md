# Papers search

[![build](https://github.com/fissoreg/papers-search/actions/workflows/build.yml/badge.svg)](https://github.com/fissoreg/papers-search/actions/workflows/build.yml)

Neural search engine for ML papers.

## Demo

Usage is simple: input an abstract, get the matching papers. The following demo also showcases the finetuning functionality (notice how the paper marked as "irrelevant" is assigned a lower score after finetuning).

![Search and finetuning demo](img/demo.gif)

## Dataset

We used a stripped-down version of the [Kaggle arXiv Dataset](https://www.kaggle.com/Cornell-University/arxiv/) in which only the following categories are retained: `cs.AI, cs.CL, cs.CV, cs.LG, cs.MA, cs.NE`

## Setting up the environment

Clone the repository

```bash
git clone https://github.com/fissoreg/papers-search/
cd papers-search
```

For both the folders `frontend` and `backend`, run the following commands

```bash
cd folder_to_go_into/ # `folder_to_go_into` is either `frontend` or `backend`

python3 -m venv env
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

## Indexing

The app works by suggesting papers whose abstract is similar to the one you provided. The suggestions come from a database of published papers: you need to index all the suggestions for the system to be able to function. This is a lenghty operation, but it needs to be performed only once:

```bash
cd backend
python src/app.py --index
```

For testing, you can index a small number of papers providing the `--n` argument:
```bash
python src/app.py --index --n 10
```


## Running the app

This can be run after indexing (section above).

Run the `backend`

```bash
cd backend
python3 src/app.py
```

In a new terminal, run the `frontend`

```bash
cd frontend
streamlit run app.py
```

Connect to `http://localhost:8501/` (with your favourite browser).

## Formatting, linting and testing

_Refer to the `Makefile` for the specific commands_

To format code following the [`black`](https://github.com/psf/black) standard
```
$ make format
```

Code linting with [`flake8`](https://github.com/PyCQA/flake8)
```
$ make lint
```

Testing
```
$ make testdeps
$ make test
```

Testing with coverage analysis
```
$ make coverage
```

Format, test and coverage
```
$ make build
```

## Acknowledgments

Made possible by:

- [Jina AI](https://jina.ai)
- [Sentence-Transformers](https://www.sbert.net/)
- [arXiv](https://arxiv.org): Thank you to arXiv for use of its open access interoperability.
- [Kaggle](https://kaggle.com)
