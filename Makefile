# Makefile

PYTHON := python3
SRC_DIR := src

.PHONY: index analyze index-inspect pipeline help

help:  ## Show help for each command
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

index: ## Reads the dataset and saves it in a repository
	cd $(SRC_DIR) && $(PYTHON) main.py --index

index-inspect: ## Same as index, but also stops execution every time a query is done to an llm, or a response is obtained, showing the query and response
	cd $(SRC_DIR) && $(PYTHON) main.py --index --inspect-query

analyze: ## Placeholder
	cd $(SRC_DIR) && streamlit run presenter.py

pipeline: ## Runs index and analyze
	cd $(SRC_DIR) && $(PYTHON) main.py --index
	cd $(SRC_DIR) && $(PYTHON) main.py --analyze

invalidate-cache: ## Removes the cache created by index
	@if [ -e src/db ]; then \
		echo "Removing src/db..."; \
		rm -rf src/db; \
	else \
		echo "src/db does not exist. Skipping removal."; \
	fi
