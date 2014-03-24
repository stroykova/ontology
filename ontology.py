import sys
import os
from elementtree import ElementTree


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
    files = os.listdir(in_dir)

    categories = set()
    articles = []

    for idx, file_name in enumerate(files):
        print idx + 1, "/", len(files)
        source = open(in_dir + '/' + file_name)
        context = ElementTree.iterparse(source, events=("start", "end"))
        context = iter(context)
        event, root = context.next()
        idx = 0
        for event, elem in context:
            tag = elem.tag.split('}')[1]
            if event == "end" and tag == "text":
                if not elem.text:
                    continue

                start = elem.text.find("{{", )
                end = elem.text.find("}}")
                if start != -1 and end != -1:
                    # print elem.text[start+2:end].split('|')[0], "\n"
                    parts = elem.text[start+2:end].lower().split('|')
                    text_c = parts[0].encode('utf-8')

                    if text_c.startswith(category):
                        # print(elem.text)
                        articles.append(elem.text.encode('utf-8'))
                    categories.add(text_c)

                root.clear()
                if idx % 1000 == 0:
                    print idx
                idx += 1

                # if idx > 200000:
                #     break

    f = open("categories", "w")
    for c in categories:
        f.write(c + "\n")
    f.close()

    f = open("articles", "w")
    for a in articles:
        f.write(a + "\n\n")
    f.close()

    print idx
    print len(articles)

    return


main()