"""Lists public Fish Audio voices matching a search: voces.py "texto" [n]. Prints id, title, likes, languages."""
import json, os, sys, urllib.parse, urllib.request

q = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 15
url = "https://api.fish.audio/model?" + urllib.parse.urlencode(
    {"title": q, "page_size": n, "sort_by": "score", "language": "es"})
req = urllib.request.Request(url, headers={"Authorization": "Bearer " + os.environ["FISH_API_KEY"]})
data = json.load(urllib.request.urlopen(req, timeout=30))
for m in data.get("items", []):
    print(m["_id"], "|", m.get("title"), "|", m.get("like_count"), "likes |", m.get("task_count"), "usos |", ",".join(m.get("languages", [])),
          "|", (m.get("description") or "").replace("\n", " ")[:90])
