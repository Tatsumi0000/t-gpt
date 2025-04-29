.PHONY: setup

dev/setup:
	docker build . -t t-gpt --no-cache ; \
	cp env.example .env ; \
	docker run -it --rm -v $(PWD):/app t-gpt /bin/bash -c "python -m venv .venv & poetry install"

dev/run:
	docker run -it --rm -v $(PWD):/app t-gpt /bin/bash 
