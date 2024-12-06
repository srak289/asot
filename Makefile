server:
	python3.11 -m asot.server

database:
	podman run -d --name pg --rm -v pg:/var/lib/postgres/data:rw,Z docker.io/library/postgres:latest
	python3.11 -m asot.db --setup
