# Wagtail CLIP example project

A project that shows you how you can use [Wagtail CLIP](https://github.com/MattSegal/wagtail-clip).

## Setup

Running this project requires `docker` and `docker-compose`.

```bash
# Build the Docker container
docker build . --tag wagtail-clip:local -f docker/Dockerfile

# Run the setup script. If you're using Windows, give it a read,
# it should still be doable with Docker / docker-compose.
./setup.sh

# Run the server and visit http://localhost:8000/cms/images/
# Login using admin / 12345
docker-compose -f docker/docker-compose.local.yml up web
```

If you want to test the search using more images, like, say 1024, try:

```bash
docker-compose -f docker/docker-compose.local.yml run --rm web ./manage.py setup_images 1024
```

Note that the 1st query is a little slow as it loads the CLIP model into memory - the model is memoized after the 1st query.
