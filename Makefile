VENV_NAME=qcc-venv
SHELL=bash

$(VENV_NAME):
	python3 -m venv $@


install: $(VENV_NAME)
	source $(VENV_NAME)/bin/activate && \
		pip3 install -r requirements.txt && \
		pip3 install -e qcc

clean:
	rm -rf $(VENV_NAME)


.PHONY: clean
