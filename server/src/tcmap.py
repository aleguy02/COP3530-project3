"""
this is for the tcm base, uses a dfs to
work all the way down the graph and not
only get immediate neighbors

"""

import re, json

class Graph:
    def __init__(self):
        self.adj = {}

    def edge_insertion(self, prereq, course):
        if prereq not in self.adj:
            self.adj[prereq] = []
        self.adj[prereq].append(course)
        if course not in self.adj:
            self.adj[course] = []

    def dfs(self, course, visited):
        for neighbor in self.adj.get(course, []):
            if neighbor not in visited:
                visited.add(neighbor)
                self.dfs(neighbor, visited)

    def closureMap(self):
        closure = {}
        for course in self.adj:
            visited = set()
            self.dfs(course, visited)
            closure[course] = visited
        return closure

def extraction(text):
    course_re = re.compile(r"\b[A-z]{3}\s?\d{4}\b")
    return [code.replace(" ", "") for code in course_re.findall(text or "")]

if __name__ == "__main__":
    from pathlib import Path

    path = Path(__file__).parents[1] / "src" / "json" / "soc_dummy.json"
    with open(path, encoding ="utf-8") as f:
        data = json.load(f)["courses"]

    g = Graph()
    for course in data:
        code = course["code"].replace(" ", "")
        prereqs = extraction(course.get("prerequisites", ""))
        for prereq in prereqs:
            g.edge_insertion(prereq.upper(), code.upper())

    closure_map = g.closureMap()

    print("Post-reqs of MAC2311:", closure_map.get("MAC2311", set()))

"""
attempted to write test in the same file, might need some new files 
"""
""