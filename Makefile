# Makefile

PYTHON := python3

.PHONY: index analyze

index:
	cd src && $(PYTHON) main.py --index

analyze:
	cd src && $(PYTHON) main.py --analyze
