# $Id:$
# Copyright (C) 2001-2009 KDS software, 42 coffee cups.

include Makefile.def

# Targets
.PHONY: test clean dist todo

test: clean nosetests

ntest: 
	./runm.sh make

gitsubmodules:
	-git submodule init
	-git submodule add  github.com/42/tddspry.git lib/tddspry
	git submodule update
	#fix for updating git submodules
	#cd tests/tddspry; git pull origin master

nosetests:
	$(MAKE) -C $(app) build test

clean:
	-[ -d db ] && $(MAKE) -C db clean
	$(MAKE) -C $(app) clean
	-rm *~*
	-find . -name '*.pyc' -exec rm {} \;

dist: clean test #pylint
	$(MAKE) clean
	git tag -a -f -m "Making release $(ver)" rel-$(ver)
	git archive --prefix=$(proj)-$(ver)/ rel-$(ver) | bzip2 > ../$(proj)-$(ver).tar.bz2

deploy: dist
	scp ../$(proj)-$(ver).tar.bz2 deploy.sh $(deployto):
	ssh $(deployto) sh ./deploy.sh $(proj)-$(ver) $(prevver)
	./increment_version.py .version
	git add .version
	git commit -m "Version update"

todo:
	find . -type f -not -name '*~*' -not -name 'Makefile*' -print0 | xargs -0 -e grep -n -e 'todo'

pep8:
	python pep8.py --filename=*.py --ignore=W --statistics --repeat $(app) 

pylint:
	pylint $(app)  --max-public-methods=50 --include-ids=y --ignored-classes=Item.Meta --method-rgx='[a-z_][a-z0-9_]{2,40}$$'

fresh_syncdb:
	-rm $(app).db
	PYTHONPATH=$(PYTHONPATH) python $(app)/manage.py syncdb --noinput
	PYTHONPATH=$(PYTHONPATH) python $(app)/manage.py init_permissions

syncdb:
	PYTHONPATH=$(PYTHONPATH) python $(app)/manage.py syncdb --noinput
	PYTHONPATH=$(PYTHONPATH) python $(app)/manage.py init_permissions

run:
	PYTHONPATH=$(PYTHONPATH) python $(app)/manage.py runserver

### Local variables: ***
### compile-command:"make" ***
### tab-width: 2 ***
### End: ***
