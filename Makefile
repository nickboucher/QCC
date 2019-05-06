VENV_NAME=qcc-venv
SHELL=bash

$(VENV_NAME):
	python3 -m venv $@


install: $(VENV_NAME)
	source $(VENV_NAME)/bin/activate && \
		pip3 install -e qcc

clean:
	rm -rf $(VENV_NAME)

test:
	source $(VENV_NAME)/bin/activate && python3 test/run_tests.py

.PHONY: clean test
