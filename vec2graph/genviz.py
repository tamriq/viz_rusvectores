import sys
import os
import requests
from requests.exceptions import HTTPError

path = os.path.dirname(os.path.abspath(__file__))

html = open(path + '/genviz.html', 'r').read()

def get_data(model, word, depth=0, topn=10):
    datum = {}

    if not word:
        raise ValueError("empty string")
    if "gensim" in sys.modules:
        if word not in model.vocab:
            print(word + " is not in model")
            return datum
    res = get_most_similar(model, word, topn)
    datum[word] = res[0]
    get_neighbors(model, datum, res[1], depth, topn)

    return datum


def get_neighbors(model, datum, stack, depth, topn):
    if depth > 0:
        depth -= 1
        for neighbor in stack:

            res = get_most_similar(model, neighbor, topn)
            datum[neighbor] = res[0]
            get_neighbors(model, datum, res[1], depth, topn)
    return


def get_most_similar(model, word, topn=10, function="similar_by_word"):
    arr = [{"source": word, "target": word, "value": 1}]
    neighbors = []

    mostsim = getattr(model, function)(word, topn=topn)

    for item in mostsim:
        arr.append({"source": word, "target": item[0], "value": item[1]})
        neighbors.append(item[0])

    pairs = [
        (neighbors[ab], neighbors[ba])
        for ab in range(len(neighbors))
        for ba in range(ab + 1, len(neighbors))
    ]
    for pair in pairs:
        arr.append(
            {"source": pair[0], "target": pair[1], "value": model.similarity(*pair)}
        )

    return [arr, neighbors]


def render(
    word, data, topn=10, threshold=0, interlinks=[], edge=1, sep=False, d3path=""
):
    return (
        html.replace("d3pathplaceholder", d3path)
        .replace("wordplaceholder", word)
        .replace("splithyphen", str(sep).lower())
        .replace("dataplaceholder", str(data))
        .replace("topn", str(topn))
        .replace("thresholdplaceholder", str(threshold))
        .replace("linksplaceholder", str(interlinks))
        .replace("linkstrokewidth", str(edge))
    )


def vec2graph(
    path, model, words, depth=0, topn=10, threshold=0, edge=1, sep=False, library="web"
):
    d3webpath = "https://d3js.org/d3.v3.min.js"
    limit = threshold if threshold < 1 else threshold / 100
    data = {}
    if isinstance(words, list):
        for word in words:
            data.update(get_data(model, word, depth=depth, topn=topn))
    elif isinstance(words, str):
        data = get_data(model, words, depth=depth, topn=topn)
    else:
        raise ValueError("wrong type")

    pages = list(data.keys())

    if library == "web":
        d3path = d3webpath
    elif library == "local":
        d3path = "d3.v3.min.js"
        fullpath = os.path.join(path, d3path)

        if not os.path.isfile(fullpath):
            try:
                response = requests.get(d3webpath)
                response.raise_for_status()
            except HTTPError as err:
                print(err)
            except Exception as err:
                print(err)
            else:
                response.encoding = "utf-8"
                with open(fullpath, "w", encoding="utf-8") as d3:
                    d3.write(response.text)

    for page in pages:
        fname = "".join([x if x.isalnum() else "_" for x in page])
        filepath = os.path.join(path, fname + ".html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(
                render(
                    page,
                    data[page],
                    topn=topn,
                    threshold=limit,
                    interlinks=pages,
                    edge=edge,
                    sep=sep,
                    d3path=d3path,
                )
            )

    pass
