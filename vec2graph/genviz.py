import sys
import os
import json
import requests
from requests.exceptions import HTTPError
from smart_open import smart_open
from shutil import copyfile


def get_data(model, word, depth=0, topn=10):
    datum = {}
    if not word:
        raise ValueError("Empty string!")
    if word not in model.vocab:
        print(word + " is not in model", file=sys.stderr)
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


def get_most_similar(model, word, topn=10, sim_func="similar_by_word"):
    arr = [{"source": word, "target": word, "value": 1}]
    neighbors = []

    mostsim = getattr(model, sim_func)(word, topn=topn)

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
            {"source": pair[0], "target": pair[1], "value": float(model.similarity(*pair))}
        )

    return [arr, neighbors]


def render(
        word, data, interlinks, topn=10, threshold=0, edge=1, sep=False, d3path=""
):
    html = smart_open('genviz.html', 'r').read()
    return (
        html.replace("d3pathplaceholder", d3path)
            .replace("wordplaceholder", word)
            .replace("splithyphen", str(sep).lower())
            .replace("dataplaceholder", json.dumps(data).replace("\'", "\\u0027"))
            .replace("topn", str(topn))
            .replace("thresholdplaceholder", str(threshold))
            .replace("linksplaceholder", json.dumps(interlinks).replace("\'", "\\u0027"))
            .replace("linkstrokewidth", str(edge))
    )


def vec2graph(
        path, model, words, depth=0, topn=10, threshold=0, edge=1, sep=False, library="web"
):
    d3webpath = "https://d3js.org/d3.v3.min.js"
    if threshold < 1:
        limit = threshold
    else:
        limit = threshold / 100
    data = {}
    if isinstance(words, list):
        for word in words:
            data.update(get_data(model, word, depth=depth, topn=topn))
    elif isinstance(words, str):
        data = get_data(model, words, depth=depth, topn=topn)
    else:
        raise ValueError("Wrong type!")

    pages = list(data.keys())

    d3path = d3webpath
    if library == "local":
        d3path = "d3.v3.min.js"
        fullpath = os.path.join(path, d3path)

        if not os.path.isfile(fullpath):
            try:
                response = requests.get(d3webpath)
                response.raise_for_status()
            except HTTPError as err:
                print(err, file=sys.stderr)
            except Exception as err:
                print(err, file=sys.stderr)
            else:
                response.encoding = "utf-8"
                with open(fullpath, "w", encoding="utf-8") as d3:
                    d3.write(response.text)

    copyfile('genviz.js', os.path.join(path, 'genviz.js'))
    for page in pages:
        fname = "".join([x for x in page])
        filepath = os.path.join(path, fname + ".html")
        with smart_open(filepath, "w") as f:
            f.write(
                render(
                    page,
                    data[page],
                    pages,
                    topn=topn,
                    threshold=limit,
                    edge=edge,
                    sep=sep,
                    d3path=d3path,
                )
            )

    return pages
