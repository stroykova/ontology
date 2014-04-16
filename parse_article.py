import sys
from elementtree import ElementTree


def read_ontology(file_name):
    with open(file_name) as f:
        content = f.readlines()

    ontology = []
    odict = dict()

    i = 0
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

        odict[content[i].lower()] = content[i+1].lower()
        i += 2
    return ontology


def get_facts(article_file):
	facts = []
	source = open(article_file)
	context = ElementTree.iterparse(source, events=("start", "end"))
	context = iter(context)
	event, root = context.next()
	idx = 0
	for event, elem in context:
		if event == "end" and elem.tag == "Name":
			if "val" in elem.attrib:
				facts.append(elem.attrib["val"])
			root.clear()
			if idx % 10 == 0:
				print idx
			idx += 1
	return facts		
	

def search_by_value(ontology, query):
    print query
    for item in ontology:
        caption = item.itervalues().next()
        if query in caption:
            return item
    return None


def main():
    args_count = len(sys.argv)
    if args_count < 4:
        print "First command line argument must be ontology file name"
        print "Second command line argument must be article tomita output file name"
        print "Third command line argument must be output directory"
        return 0
	
    ontology_file = sys.argv[1]
    article_file = sys.argv[2]
    directory = sys.argv[3]
	
    import shutil
    shutil.rmtree(directory, True)
    import os
    os.makedirs(directory)
	
    ontology = read_ontology(ontology_file)
    facts = get_facts(article_file)
    
    for fact in facts:
        item = search_by_value(ontology, fact.encode('utf-8').lower())
        if item:
            output = open(directory + "/" + fact, 'w')
            for k, v in item.items():
                output.write(k + " " + v + "\n")
            output.close()
    return


main()