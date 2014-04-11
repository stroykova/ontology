import sys


def read_ontology(file_name):
    with open(file_name) as f:
        content = f.readlines()

    ontology = []
    odict = dict()

    i = 0
    # while i + 1 < len(content):
    while i + 1 < len(content):
        if content[i].startswith("article"):
            if odict:
                ontology.append(odict)
                odict = dict()
            i += 1
            continue
        if content[i+1].startswith("article"):
            i += 1
            continue

        odict[content[i]] = content[i+1]
        i += 2
    return ontology


def search_by_value(ontology, query):
    for item in ontology:
        for k, v in item.items():
            if query in v:
                return item
    return None


def main():
    args_count = len(sys.argv)
    if args_count < 3:
        print "First command line argument must be ontology file name"
        print "Second command line argument must be article file name"
        return 0
    ontology_file = sys.argv[1]
    article_file = sys.argv[2]

    ontology = read_ontology(ontology_file)

    print(search_by_value(ontology, "Fate of Two Worlds"))

    return


main()