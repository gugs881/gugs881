import os
import re
import json
import subprocess
from collections import Counter
from jinja2 import Template

# Cores para combinar com seu tema
BG = "0d1117"
TITLE = "0abde3"
TEXT = "ffffff"
ICON = "1dd1a1"

def run(cmd):
    return subprocess.check_output(cmd, text=True).strip()

def repo_name():
    return os.getenv("GITHUB_REPOSITORY", "repo").split("/")[-1]

def total_commits():
    # total de commits no repo (todos os branches se possível)
    try:
        return int(run(["git", "rev-list", "--count", "--all"]))
    except subprocess.CalledProcessError:
        return int(run(["git", "rev-list", "--count", "HEAD"]))

def contributors():
    # lista (autor, n_commits)
    out = run(["git", "shortlog", "-s", "-n", "--all", "--no-merges"])
    rows = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) == 2:
            try:
                n = int(parts[0])
            except ValueError:
                continue
            name = parts[1]
            rows.append((name, n))
    return rows

def lines_added_removed():
    """
    Soma inserções/remoções a partir do `git log --shortstat`.
    Exemplo de linha:
      " 1 file changed, 20 insertions(+), 3 deletions(-)"
    """
    try:
        out = run(["git", "log", "--shortstat", "--pretty=tformat:"])
    except subprocess.CalledProcessError:
        return 0, 0

    add_total = 0
    del_total = 0
    re_ins = re.compile(r"(\d+)\s+insertion")
    re_del = re.compile(r"(\d+)\s+deletion")

    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        m_ins = re_ins.search(line)
        m_del = re_del.search(line)
        if m_ins:
            add_total += int(m_ins.group(1))
        if m_del:
            del_total += int(m_del.group(1))

    return add_total, del_total

def _fallback_top_languages():
    """
    Fallback sem pygount: conta linhas por extensão rastreada pelo Git.
    Não é perfeito, mas entrega um top-langs estável.
    """
    try:
        files = run(["git", "ls-files"]).splitlines()
    except subprocess.CalledProcessError:
        files = []

    ext2lang = {
        ".py": "Python", ".ipynb": "Jupyter Notebook",
        ".js": "JavaScript", ".ts": "TypeScript",
        ".jsx": "JavaScript", ".tsx": "TypeScript",
        ".java": "Java", ".kt": "Kotlin",
        ".c": "C", ".h": "C", ".cpp": "C++", ".hpp": "C++",
        ".rs": "Rust", ".go": "Go", ".rb": "Ruby",
        ".php": "PHP", ".cs": "C#", ".swift": "Swift",
        ".r": "R", ".m": "MATLAB/Octave",
