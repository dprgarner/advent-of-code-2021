"""
15:58-16:57
"""


def read_links():
    links = {}
    try:
        while True:
            a, b = input().split("-")
            if a not in links:
                links[a] = set()
            if b not in links:
                links[b] = set()
            links[a].add(b)
            links[b].add(a)
    except EOFError:
        pass
    return links


def find_routes_with_one_visit(links, start):
    if start == "end":
        return [["end"]]

    new_links = {k: v.copy() for k, v in links.items()}
    if start == start.lower():
        # Remove all links to this
        for dead_link in new_links.pop(start):
            new_links[dead_link].remove(start)

    routes = []
    for next_ in links[start]:
        routes += [
            [start] + x for x in find_routes_with_one_visit(new_links, next_) if x
        ]

    return routes


def find_routes_with_one_double_visit(links, start):
    if start == "end":
        return [["end"]]

    new_links = {k: v.copy() for k, v in links.items()}
    routes = []

    if start == start.lower():
        if start != "start":
            # This is the cave that can be visited twice; add one-visit routes
            for next_ in links[start]:
                routes += [
                    [start] + x
                    for x in find_routes_with_one_visit(new_links, next_)
                    if x
                ]

        # This cave cannot be visited twice; remove.
        for dead_link in new_links.pop(start):
            new_links[dead_link].remove(start)

    for next_ in links[start]:
        routes += [
            [start] + x
            for x in find_routes_with_one_double_visit(new_links, next_)
            if x
        ]

    return routes


def main_a():
    links = read_links()
    routes = find_routes_with_one_visit(links, "start")
    for route in routes:
        print(",".join(route))
    print("number of routes:", len(routes))


def main_b():
    links = read_links()
    routes = set(
        [",".join(route) for route in find_routes_with_one_double_visit(links, "start")]
    )
    # for route in routes:
    #     print(route)
    print("number of routes:", len(routes))


if __name__ == "__main__":
    # main_a()
    main_b()
