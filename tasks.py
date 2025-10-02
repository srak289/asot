from invoke import task

@task
def pod(c):
    c.run("podman pod create --name asot")

@task
def server(c):
    c.run("python3.13 -m asot.server")

@task
def database(c):
    c.run("podman run -d --name pg --rm -v pg:/var/lib/postgres/data:rw,Z docker.io/library/postgres:latest")
    c.run("python3.13 -m asot.db --setup")

