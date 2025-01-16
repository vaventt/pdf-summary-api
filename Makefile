.PHONY: build run test clean

# Variables
DOCKER_IMAGE = pdf-summary-api
CONTAINER_NAME = pdf-summary-container
PORT = 8000

# Build Docker image
build:
	docker build -t $(DOCKER_IMAGE) .

# Run Docker image
run:
	docker run -it --name $(CONTAINER_NAME) \
	-p $(PORT):$(PORT) \
	--env-file .env \
	$(DOCKER_IMAGE)

# Run container with development mode (auto-reload)
dev:
	docker run -it --name $(CONTAINER_NAME) \
		-p $(PORT):$(PORT) \
		--env-file .env \
		-v $(PWD)/app:/app \
		$(DOCKER_IMAGE)

# Stop and remove container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Clean everything
clean: stop
	docker rmi $(DOCKER_IMAGE) || true

# Run tests
test:
	python test_api.py

# Build and run
up: build run

# Stop and clean
down: stop clean