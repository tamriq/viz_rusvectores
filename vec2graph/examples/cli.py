#!/usr/bin/env python
import sys
import os
import glob
import gensim
import logging
import pathlib
import random
import argparse
import zipfile
from datetime import datetime
import time

dir = sys.path[0]
sys.path.insert(0, os.path.dirname(dir))
# is needed to import module from file (dev time solution)
from genviz import *

time_start = time.monotonic()

logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "-t",
    "--token",
    help="token to look for in model. If omitted, random token is used",
    default="",
)
parser.add_argument(
    "-n",
    "--nbr",
    help="amount of neighbors to show. Default is 10",
    default=10,
    type=int,
)
parser.add_argument(
    "-e",
    "--edge",
    help="width of an edge (link) between nodes. Default is 1",
    default=1,
    type=int,
)
parser.add_argument(
    "-d",
    "--depth",
    help="recursion depth to build graphs also of neighbors of target word."
    " Default is 0 (no neighbors)",
    default=0,
    type=int,
)
parser.add_argument(
    "-l",
    "--lim",
    help="limit (threshold) of similarity which should be surpassed by"
    " neighbors to be rendered as connected. Scale is either more "
    "than 0 and less than 1 (as real range for similarities), or"
    " from 1 to 100 as percents. Default is 0 (no link is cut)",
    default=0,
    type=float,
)
parser.add_argument(
    "-m",
    "--model",
    help="path to vector model file. If ommited, first model with extension "
    "bin.gz (as binary) or .vec.gz (as non-binary) in working directory"
    " is loaded",
    default="",
)
parser.add_argument(
    "-o",
    "--output",
    help="path to ouptut directory where to store files of visualization."
    " If ommited, in current directory new one will be made, with a name"
    " based on a timestamp",
    default="",
)

parser.add_argument(
    "-s",
    "--sep",
    help="if this parameter is used, token is split by a separator"
    "(underscore), and only first part is shown in visualization (E.g. "
    "it is useful when PoS is attached to a word). By now, this "
    "parameter accepts no value",
    action="store_true",
)

parser.add_argument(
    "-js",
    "--javascript",
    help="path to D3.js library, can be 'web' (link to version at the D3.js "
    "site) or 'local' (file in the directory with generated HTML, if not"
    " present, it is downloaded from web). Default is 'web'",
    choices=("web", "local"),
    default="web",
)
args = parser.parse_args()

if not args.output:
    dt = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    new_dir = os.path.join(dir, dt)
    pathlib.Path(new_dir).mkdir(parents=True, exist_ok=True)
    args.output = new_dir

if not args.model:
    first = glob.glob(os.path.join(dir, "*.[vecbin]*.gz"))[0]
    args.model = first

if args.model.endswith(".zip"):
    with zipfile.ZipFile(args.model, "r") as archive:
        args.model = archive.open("model.bin")
        binaryMode = True
else:
    binaryMode = args.model.endswith(".bin.gz")

model = gensim.models.KeyedVectors.load_word2vec_format(args.model, binary=binaryMode)

model.init_sims(replace=True)
token = args.token if args.token else random.choice(model.index2entity)

time_load = time.monotonic()

vec2graph(
    args.output,
    model,
    token,
    depth=args.depth,
    topn=args.nbr,
    threshold=args.lim,
    edge=args.edge,
    sep=args.sep,
    library=args.javascript,
)
time_end  = time.monotonic()

interval_load = time_load - time_start
interval_data  = time_end - time_load
print("Model load time:\t", round(interval_load, 2), " sec\nModel query time:\t", round(interval_data, 2), " sec")