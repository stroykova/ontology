build:
	python ontology.py docs category

parse:
	python parse_article.py ontology tomita/output.txt

clean:
	find . -name \*~ -delete
	find . -name \*.backup -delete

	find $(CDIR) -name \*~ -delete
	find $(CDIR) -name \*.backup -delete

