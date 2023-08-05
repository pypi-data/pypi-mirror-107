def hierarchical_to_linear(hierarchical):
    linear = []

    def linearize(child, parent):
        name = child['name']
        linear.append({'name': name, 'parent': parent})

        try:
            children = child['children']
            for child in children:
                linearize(child, name)
        except:
            pass

    linearize(hierarchical, None)

    return linear


def linear_to_hierarchical(linear):
    paths = [None] * len(linear)
    for i, v in enumerate(linear):
        paths[i] = []

        parent = v['parent']
        while parent != linear[0]['name'] and parent != None:
            paths[i].insert(0, parent)
            parent = next(x for x in linear if x['name'] == parent)['parent']

    hierarchical = {}
    for i, v in enumerate(linear):
        reference = hierarchical

        if i == 0:
            reference['name'] = v['name']

            continue

        path = paths[i]
        for j in range(len(path)):
            try:
                reference = [x for x in reference['children']
                             if x['name'] == path[j]][0]
            except:
                pass

        if not 'children' in reference:
            reference['children'] = []

        reference['children'].append({'name': linear[i]['name']})

    return hierarchical