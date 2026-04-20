# Makefile providing useful commands to assist with development.
# See the make manual for more information:
# https://www.gnu.org/software/make/manual/html_node/

# To make a command appear in the help, provide a line of documentation after
# the target/prerequisites with ##.
help: ## Display this help message.
	@echo "Please provide a target from:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sed -n 's/^\(.*:\) \(.*\)##\(.*\)/  \1\3/p'

venv: requirements.txt ## Setup development environment.
	python3 -m venv ./venv
	. ./venv/bin/activate && python3 -m pip install --progress-bar='off' --requirement requirements.txt

build: venv ## Build website.
	. ./venv/bin/activate && python3 site-generator.py

clean: ## Delete all generated files.
	rm -rf ./build ./venv

test: ## Run linting.
	pre-commit run --all-files

# Mark targets as 'phony' to indicate they don't actually produce a file with
# the same name as their target. Basically for actions rather than files.
.PHONY: help build clean test
