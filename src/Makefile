# Makefile for evaluating python code
# Author: Christiam Camacho (christiam.camacho@gmail.com)
# Created: Wed Oct 16 13:38:05 2019

SHELL=/bin/bash
.PHONY: all clean distclean check
VPATH=data
VENV=.env

all: taxidlineage.dmp
	for f in data/*.tsv; do \
		./notebook.py $$f > `basename -s .tsv $$f`.out; \
	done


check: taxidlineage.dmp ${VENV}
	source ${VENV}/bin/activate && ./notebook.py data/pfam10339-components.tsv


taxidlineage.dmp:
	wget -O data/$@ ftp://ftp.ncbi.nlm.nih.gov/blast/temp/model2taxid/$@
	#curl -L ftp://ftp.ncbi.nlm.nih.gov/blast/temp/model2taxid/$@ -o data/$@


#########################################################################
# Python support
MODULE_NAME?=model2taxid

anaconda_ete:
	#wget -q http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O Miniconda3-latest-Linux-x86_64.sh
	#bash Miniconda3-latest-Linux-x86_64.sh -b -p ${PWD}/$@
	curl -L 'http://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh' -o Miniconda3-latest-MacOSX-x86_64.sh
	bash Miniconda3-latest-MacOSX-x86_64.sh -b -p ${PWD}/$@
	PATH=${PWD}/$@/bin:${PATH} conda install -c etetoolkit ete3 ete_toolchain python=2.7
	PATH=${PWD}/$@/bin:${PATH} ete3 build check

##################################
check_biopython: ${VENV}
	source ${VENV}/bin/activate && ./check_biopython.py 9606 10090 2 2789
##################################

#check_python: ${VENV}
#	source ${VENV}/bin/activate && \
#	for f in $(wildcard *.py); do python -m py_compile $$f ; done && \
#	python3 -m unittest $(subst .py,,$(filter-out setup.py, $(wildcard *.py))) && \
#	python3 -m unittest discover -s tests
#	#time -p python3 -m doctest map.py
#	#time -p py.test *.py
#	#time -p py.test tests

${VENV}: requirements.txt
	[ -d ${VENV} ] || virtualenv -p python3 $@
	source ${VENV}/bin/activate && pip install -r $^

#PYTHON_MODULE_VERSION=$(shell grep version setup.py | cut -d= -f 2 | tr -d \'  | tr -d , )
#dist/${MODULE_NAME}-${PYTHON_MODULE_VERSION}.tar.gz:
#	python setup.py sdist

# twine --repository assumes ~/.pypirc settings include username/password; --repository-url prompts them
TEST_PYPI=https://test.pypi.org
.PHONY: deploy
deploy: dist/${MODULE_NAME}-${PYTHON_MODULE_VERSION}.tar.gz
	#twine upload --repository-url ${TEST_PYPI}/legacy/ $<
	twine upload --repository testpypi $<
	#twine upload $<

clean:
	$(RM) -r *.dat *.[ao] *.log *.pyc
	find . -name __pycache__ | xargs ${RM} -fr

distclean: clean
	${RM} -r ${VENV}
	${RM} cscope.* tags vim.paths
