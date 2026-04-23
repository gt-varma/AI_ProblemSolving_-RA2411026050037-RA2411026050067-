from flask import Flask, render_template, request

app = Flask(__name__)

# BFS Algorithm
def bfs(graph, start, goal):
    visited = []
    queue = [[start]]

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node not in visited:
            if node == goal:
                return path

            for neighbour in graph.get(node, []):
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

            visited.append(node)
    return None


# DFS Algorithm
def dfs(graph, start, goal, path=None):
    if path is None:
        path = []

    path = path + [start]

    if start == goal:
        return path

    for neighbour in graph.get(start, []):
        if neighbour not in path:
            new_path = dfs(graph, neighbour, goal, path)
            if new_path:
                return new_path
    return None


@app.route('/', methods=['GET', 'POST'])
def index():
    bfs_result = None
    dfs_result = None
    error = None

    if request.method == 'POST':
        try:
            start = request.form['start'].strip()
            goal = request.form['goal'].strip()
            edges = request.form['edges']

            graph = {}

            for edge in edges.split(','):
                a, b = edge.strip().split('-')
                a, b = a.strip(), b.strip()

                graph.setdefault(a, []).append(b)
                graph.setdefault(b, []).append(a)

            bfs_result = bfs(graph, start, goal)
            dfs_result = dfs(graph, start, goal)

            if not bfs_result:
                error = "No path found!"

        except:
            error = "Invalid input format! Use A-B, B-C"

    return render_template('index.html', bfs=bfs_result, dfs=dfs_result, error=error)


if __name__ == '__main__':
    app.run(debug=True)