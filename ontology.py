import sys
import os
from elementtree import ElementTree


def get_articles(category, in_dir):
    articles = []
    categories = set()
    idx = 0
    files = os.listdir(in_dir)
    for idx_f, file_name in enumerate(files):
        print idx_f + 1, "/", len(files)
        source = open(in_dir + '/' + file_name)
        context = ElementTree.iterparse(source, events=("start", "end"))
        context = iter(context)
        event, root = context.next()

        for event, elem in context:
            tag = elem.tag.split('}')[1]
            if event == "end" and tag == "text":
                if not elem.text:
                    continue

                start = elem.text.find("{{", )
                end = elem.text.find("}}")
                if start != -1 and end != -1:
                    parts = elem.text[start+2:end].lower().split('|')
                    text_c = parts[0].encode('utf-8')

                    if text_c.startswith(category):
                        articles.append(elem.text.encode('utf-8'))
                    categories.add(text_c)

                root.clear()
                if idx % 1000 == 0:
                    print idx
                idx += 1

    f = open("categories", "w")
    for c in categories:
        f.write(c + "\n")
    f.close()
    return articles


def print_articles(articles):
    f = open("ontology", "w")
    for a in articles:
        parts = a.split("}}")
        if not parts:
            continue

        short = parts[0]
        short = short.replace("{{", "")
        short = short.replace("}}", "")

        pairs = short.split("|")
        f.write("article\n")
        for pair in pairs:
            if not "=" in pair:
                continue
            tuple = pair.split("=")
            if len(tuple) < 2 or tuple[1].isspace():
                continue

            f.write(tuple[0].strip()+"\n")
            f.write(tuple[1].strip()+"\n")
    f.close()


def main():
    args_count = len(sys.argv)
    if args_count < 3:
        print "First command line argument must be directory with input files"
        print "Second command line argument must be category name"
        return 0
    in_dir = sys.argv[1]
    category_file = sys.argv[2]
    print "Input dir: " + in_dir

    f = open(category_file)
    category = f.readline().rstrip('\n')

    print "Category: " + category

    articles = get_articles(category, in_dir)

    print_articles(articles)

    print "articles in category:", len(articles)

    return


main()