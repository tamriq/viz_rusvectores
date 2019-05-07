import sys
import os
import requests
from requests.exceptions import HTTPError

html = """<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<meta name="description" content="wordplaceholder">
		<title>wordplaceholder</title>
		<script src="d3pathplaceholder"></script>
		<script>(function(){
'use strict';
document.addEventListener("DOMContentLoaded", function(e) {
  var width = 100, height = 100;
  var maincolor = "#F4B400";
  var splithyphen;
  var linksplaceholder;
  var thresholdplaceholder;
  var topn;
  var svg = d3.select("body").append("svg");
  var linkstrokewidth;
  var force = d3.layout.force().gravity(.05).distance(100).charge(-100);
  var datanodes = [], datalinks = [], i = 1;
  var delta = 0;
  var radius = 10;
  function buildGraph(inlinks, innodes) {
    d3.selectAll(".link").remove();
    d3.selectAll(".node").remove();
    d3.selectAll("circle").remove();
    var links = inlinks;
    force.nodes(innodes).links(inlinks).linkDistance(function(d) {
      var dv = d.value * 100;
      var df = Math.log(dv);
      var koef = isFinite(df) ? df : 1;
      return dv * koef + radius;
    }).start();
    var linksel = svg.selectAll(".link").data(inlinks);
    var link = linksel.enter().append("line").attr("stroke", "#aaa").style("stroke-width", linkstrokewidth || 1);
    var nodesel = svg.selectAll(".node").data(innodes);
    var node = nodesel.enter().append("g").call(force.drag);
    node.append("circle").attr("fill", function(d) {
      return d.color;
    }).style("stroke", "black").style("stroke-width", function(d) {
      return d.page ? 3 : 0;
    }).attr("r", function(d) {
      return d.color == maincolor ? radius * 1.5 : radius;
    }).on("click", function(d) {
      if (d.page) {
        window.open(d.name + ".html");
      }
    });
    node.append("text").text(function(d) {
      return splithyphen ? d.name.split("_")[0] : d.name;
    }).on("click", function(d) {
      if (d.page) {
        window.open(d.name + ".html");
      }
    }).attr("stroke", "#333").attr("dx", 12).attr("dy", ".35em").style("cursor", "default");
    nodesel.exit().remove();
    force.on("tick", function() {
      link.attr("x1", function(d) {
        return d.source.x;
      }).attr("y1", function(d) {
        return d.source.y;
      }).attr("x2", function(d) {
        return d.target.x;
      }).attr("y2", function(d) {
        return d.target.y;
      });
      node.attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
      });
    });
  }
  width = window.innerWidth, height = window.innerHeight;
  svg.attr("width", width).attr("height", height);
  force.size([width, height]);
  var data = dataplaceholder;
  var order = {};
  order[data[0]["source"]] = 0;
  datanodes.push({"name":data[0]["source"], color:maincolor});
  for (var k, k = 1; k < data.length; k++) {
    var dif = 1 - data[k]["value"];
    if (delta && delta > dif || !delta) {
      delta = dif;
    }
    var key = data[k]["target"];
    var src = 0;
    var tg = k;
    if (k > topn) {
      src = order[data[k]["source"]];
      tg = order[data[k]["target"]];
    } else {
      datanodes.push({"name":data[k]["target"], color:"#DB4437", page:pages.indexOf(data[k]["target"]) > -1});
      order[key] = k;
    }
    if (data[k]["value"] > threshold) {
      datalinks.push({"source":src, "target":tg, "value":dif, "key":key});
    }
  }
  buildGraph(datalinks, datanodes);
});

}).call(this)</script>
	</head>
	<body>
	</body>
</html>"""


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
        .replace("splithyphen;", "splithyphen = " + str(sep).lower() + ";")
        .replace("dataplaceholder", str(data))
        .replace("topn;", "topn = " + str(topn) + ";")
        .replace("thresholdplaceholder", "threshold = " + str(threshold))
        .replace("linksplaceholder", "pages = " + str(interlinks))
        .replace("linkstrokewidth;", "linkstrokewidth = " + str(edge) + ";")
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
