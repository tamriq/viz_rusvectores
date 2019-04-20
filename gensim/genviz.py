#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def default_html():
    html = """<!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta name="description" content="wordplaceholder">
            <title>wordplaceholder</title>
            <script src="https://d3js.org/d3.v3.min.js"></script>
    
            <script>
                document.addEventListener("DOMContentLoaded", function(e) {
                  var width = 100, height = 100;
                  var maincolor = "#F4B400";
                  var linksplaceholder;
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
                      return d.name;
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
                    if (k > 10) {
                      src = order[data[k]["source"]];
                      tg = order[data[k]["target"]];
                    } else {
                      datanodes.push({"name":data[k]["target"], color:"#DB4437", page:pages.indexOf(data[k]["target"]) > -1});
                      order[key] = k;
                    }
                    datalinks.push({"source":src, "target":tg, "value":dif, "key":key});
                  }
                  buildGraph(datalinks, datanodes);
                });        
            </script>
        </head>
        <body>
        </body>
    </html>"""
    return html


def recurs(model, word, depth=0, topn=10):
    datum = {}
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


def get_most_similar(model, word, topn=10):
    mostsim = model.similar_by_word(word, topn=topn)
    arr = [{"source": word, "target": word, "value": 1}]
    neighbors = []
    for item in mostsim:
        arr.append({"source": word, "target": item[0], "value": item[1]})
        neighbors.append(item[0])
    pairs = [(neighbors[ab], neighbors[ba]) for ab in range(len(neighbors))
             for ba in range(ab + 1, len(neighbors))]
    for pair in pairs:
        arr.append({"source": pair[0], "target": pair[1], "value": model.similarity(*pair)})
    return [arr, neighbors]


def make_html(word, data, interlinks=None, edge=1):
    return default_html().replace(
        "wordplaceholder", word).replace("dataplaceholder",
                                         str(data)).replace("linksplaceholder",
                                                            "pages = " + str(interlinks)). \
        replace("linkstrokewidth;", "linkstrokewidth = " + str(edge) + ";")


def visualize_str(model, word, depth=1, topn=10, edge=1):
    res = get_most_similar(model, word, topn)
    return make_html(word, res[0])


def visualize_file(filename, model, word, topn=10, depth=1, edge=1):
    if not filename:
        raise ValueError('filename is empty')
    html = visualize_str(model, word, depth, topn, edge)
    print(html, file=open(filename, "w", encoding='utf-8'), end='')
    pass


def visualize_dir(directory, model, word, depth=0, topn=10, edge=1):
    data = recurs(model, word, depth=depth, topn=topn)
    pages = list(data.keys())

    for k in pages:
        html = make_html(k, data[k], pages, edge)
        print(html, file=open(os.path.join(directory, k + ".html"), "w", encoding='utf-8'), end='')
    pass
