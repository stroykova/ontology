run:
	python ontology.py docs category

clean:
	find . -name \*~ -delete
	find . -name \*.backup -delete

	find $(CDIR) -name \*~ -delete
	find $(CDIR) -name \*.backup -delete

