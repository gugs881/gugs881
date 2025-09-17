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
                add += int(parts[parts.index("insertions")-1] if "insertions" in parts else parts[parts.index("insertion")-1])
            if "deletions" in parts or "deletion" in parts:
                rem += int(parts[parts.index("deletions")-1] if "deletions" in parts else parts[parts.index("deletion")-1])
    return add, rem

def top_languages():
    tmp = "pygount_out.json"
    run(["pygount","--format=json","--suffix=all","--dir",".","--out",tmp,"--verbose=0"])
    with open(tmp,"r",encoding="utf-8") as f:
        data = json.load(f)
    os.remove(tmp)
    lang_counter = Counter()
    for fobj in data:
        if fobj.get("group") == "empty":
            continue
        lang = fobj.get("language") or "Other"
        code = int(fobj.get("code_count") or 0)
        lang_counter[lang] += code
    total = sum(lang_counter.values()) or 1
    top = lang_counter.most_common(8)
    top = [(k, v, round(100*v/total,2)) for k,v in top]
    return total, top

CARD_TPL_STATS = Template("""
<svg width="495" height="195" viewBox="0 0 495 195" xmlns="http://www.w3.org/2000/svg">
  <rect width="495" height="195" rx="10" fill="#{{bg}}"/>
  <text x="25" y="35" fill="#{{title}}" font-size="18" font-family="Segoe UI, Ubuntu, Sans-Serif" font-weight="600">{{repo}}</text>
  <text x="25" y="75" fill="#{{text}}" font-size="14" font-family="Segoe UI, Ubuntu, Sans-Serif">Commits: {{commits}}</text>
  <text x="25" y="100" fill="#{{text}}" font-size="14" font-family="Segoe UI, Ubuntu, Sans-Serif">Autores: {{authors}}</text>
  <text x="25" y="125" fill="#{{text}}" font-size="14" font-family="Segoe UI, Ubuntu, Sans-Serif">Linhas +: {{added}}  Linhas -: {{removed}}</text>
  <text x="25" y="160" fill="#{{icon}}" font-size="12" font-family="Segoe UI, Ubuntu, Sans-Serif">local-readme-stats</text>
</svg>
""".strip())

CARD_TPL_LANGS = Template("""
<svg width="495" height="195" viewBox="0 0 495 195" xmlns="http://www.w3.org/2000/svg">
  <rect width="495" height="195" rx="10" fill="#{{bg}}"/>
  <text x="25" y="35" fill="#{{title}}" font-size="18" font-family="Segoe UI, Ubuntu, Sans-Serif" font-weight="600">Top Languages</text>
  {% set x0 = 25 %}{% set y0 = 65 %}{% set barw = 445 %}{% set bh = 14 %}{% set gap = 6 %}
  {% for name, val, pct in items %}
    <text x="{{x0}}" y="{{y0 + (bh+gap)*loop.index0 - 2}}" fill="#{{text}}" font-size="12" font-family="Segoe UI, Ubuntu, Sans-Serif">{{name}} ({{pct}}%)</text>
    <rect x="{{x0 + 200}}" y="{{y0 + (bh+gap)*loop.index0 - 13}}" width="{{(barw-220) * pct/100.0}}" height="{{bh}}" rx="4" fill="#{{icon}}"/>
  {% endfor %}
  <text x="25" y="180" fill="#{{text}}" font-size="12" font-family="Segoe UI, Ubuntu, Sans-Serif">Total linhas de código: {{total}}</text>
</svg>
""".strip())

def main():
    os.makedirs("cards", exist_ok=True)
    commits = total_commits()
    authors = len(contributors())
    added, removed = lines_added_removed()
    total_code, langs = top_languages()

    with open("cards/stats.svg","w",encoding="utf-8") as f:
        f.write(CARD_TPL_STATS.render(
            bg=BG, title=TITLE, text=TEXT, icon=ICON,
            repo=repo_name(), commits=commits, authors=authors,
            added=added, removed=removed
        ))

    with open("cards/top-langs.svg","w",encoding="utf-8") as f:
        f.write(CARD_TPL_LANGS.render(
            bg=BG, title=TITLE, text=TEXT, icon=ICON,
            items=langs, total=total_code
        ))

if __name__ == "__main__":
    main()

