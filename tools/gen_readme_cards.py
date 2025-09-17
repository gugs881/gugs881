import os, subprocess, json
from collections import Counter
from jinja2 import Template

BG = "0d1117"
TITLE = "0abde3"
TEXT = "ffffff"
ICON = "1dd1a1"

def run(cmd):
    return subprocess.check_output(cmd, text=True).strip()

def repo_name():
    return os.getenv("GITHUB_REPOSITORY", "repo").split("/")[-1]

def total_commits():
    try:
        return int(run(["git","rev-list","--count","--all"]))
    except:
        return int(run(["git","rev-list","--count","HEAD"]))

def contributors():
    out = run(["git","shortlog","-s","-n","--all","--no-merges"])
    rows = []
    for line in out.splitlines():
        parts = line.strip().split("\t")
        if len(parts) == 2:
            n = int(parts[0]); name = parts[1]
            rows.append((name,n))
    return rows

def lines_added_removed():
    try:
        out = run(["git","log","--shortstat","--pretty=tformat:"])
    except:
        return 0,0
    add = rem = 0
    for line in out.splitlines():
        line = line.strip().replace(",","")
        parts = line.split()
        if "insertion" in line or "deletion" in line:
            if "insertions" in parts or "insertion" in parts:
                add += int(parts[parts.index("inse]()
