# Makefile for evaluating python code
# Author: Christiam Camacho (christiam.camacho@gmail.com)
# Created: Wed Oct 16 13:38:05 2019

SHELL=/bin/bash
.PHONY: all clean distclean check
VPATH=data
VENV=.env

export TAXADB_CONFIG=${PWD}/etc/taxadb.cfg

# Creates results for all test data files in *.out files
all: taxidlineage.dmp ${VENV}
	for f in data/*.tsv; do \
		source ${VENV}/bin/activate && ./dtrt.py $$f -show_tree > `basename -s .tsv $$f`.out; \
	done

# Test code
check: check_python taxidlineage.dmp ${VENV}
	[ -f taxadb.sqlite ] || make init_taxadb
	source ${VENV}/bin/activate && ./check_taxadb.py 9606 2 10090 2157
	source ${VENV}/bin/activate && ./dtrt.py data/pfam10339-components.tsv -show_tree
	source ${VENV}/bin/activate && ./test.py

taxidlineage.dmp:
	wget -O data/$@ https://ftp.ncbi.nlm.nih.gov/blast/temp/model2taxid/$@
	#curl -L https://ftp.ncbi.nlm.nih.gov/blast/temp/model2taxid/$@ -o data/$@


#########################################################################
# Python support

anaconda_ete:
	#wget -q http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O Miniconda3-latest-Linux-x86_64.sh
	#bash Miniconda3-latest-Linux-x86_64.sh -b -p ${PWD}/$@
	curl -L 'http://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh' -o Miniconda3-latest-MacOSX-x86_64.sh
	bash Miniconda3-latest-MacOSX-x86_64.sh -b -p ${PWD}/$@
	PATH=${PWD}/$@/bin:${PATH} conda install -c etetoolkit ete3 ete_toolchain python=2.7
	PATH=${PWD}/$@/bin:${PATH} ete3 build check

##################################

.PHONY: init_taxadb
init_taxadb: ${VENV}
	source ${VENV}/bin/activate && \
		taxadb download -t taxa -o taxadb && \
		taxadb create -c 200 -d taxa -i taxadb --dbname taxadb.sqlite && \
		${RM} -r taxadb

##################################

check_python: ${VENV}
	source ${VENV}/bin/activate && \
	for f in $(wildcard *.py); do python -m py_compile $$f ; done 
	#python3 -m unittest $(subst .py,,$(filter-out setup.py, $(wildcard *.py)))
	#python3 -m unittest discover -s tests
	#time -p python3 -m doctest map.py
	#time -p py.test *.py
	#time -p py.test tests

${VENV}: requirements.txt
	[ -d ${VENV} ] || virtualenv -p python3 $@
	source ${VENV}/bin/activate && pip install -r $^

clean:
	$(RM) -r *.log *.pyc 
	find . -name __pycache__ | xargs ${RM} -fr

distclean: clean
	${RM} -r ${VENV} data/*.dmp taxadb*
