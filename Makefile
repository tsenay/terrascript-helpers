NOSE := python3 -m nose --failed --verbose --with-coverage --cover-package=terraformvspherevm --stop --no-byte-compile --logging-level=DEBUG --detailed-errors

# The tests must be executed in this order!!
TESTS := tests/tests.py
TEST_ISSUES := $(wildcard tests/test_issue*.py)

NOSEIDS = $(shell ./.read_noseids.py)


all: help

help:
	@echo "make test"
	@echo "make test_issues"
	@echo "make debug"
	@echo "make debug_issues"
	@echo "make code"
	@echo "make package"
	@echo "make install"

noseids:
	python3 -m nose --collect-only --with-id --id-file=.noseids $(TESTS)

test: clean
	python3 setup.py nosetests

test_issues:
	$(NOSE) --with-id $(TEST_ISSUES)

debug:
	$(NOSE) --with-id --pdb $(TESTS) $(TEST_ISSUES)

debug_issues:
	$(NOSE) --with-id --pdb $(TEST_ISSUES)

package: clean
	python3 setup.py clean
	python3 setup.py sdist bdist_wheel

install: clean
	python3 setup.py install --user

deploy: clean
	python3 setup.py clean
	python3 setup.py sdist bdist_wheel
	twine upload dist/*

clean:
	rm -f tests/*.pyc
	rm -f .coverage
	rm -f .noseid*
	rm -rf build/*
	rm -rf dist/*

setup:
	python3 -m venv venv
	source ./venv/bin/activate
	pip install -r requirements.txt
	