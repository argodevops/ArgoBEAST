import os
from .helpers import ensure_dir, ok, warn
from .templates import DOCKERFILE_TEMPLATE, DOCKER_COMPOSE_TEMPLATE


def build_lab():
    ensure_dir("argobeast_lab")
    if os.path.exists("argobeast_lab/argobeast.dockerfile"):
        warn("The ArgoBEAST lab already exists")
    else:
        ok("Adding furniture and equipment...")
        with open("argobeast_lab/argobeast.dockerfile", "w", encoding="utf-8") as f:
            f.write(DOCKERFILE_TEMPLATE)
    if os.path.exists("argobeast_lab/argobeast.dockercompose.yml"):
        warn("The ArgoBEAST lab already exists")
    else: 
        warn("Somebody dropped a test tube and it broke!")
        ok("replacing equipment...")
        with open("argobeast_lab/argobeast.dockercompose.yml", "w", encoding="utf-8") as f:
            f.write(DOCKER_COMPOSE_TEMPLATE)
    ok("cleaning up the mess...")
    ok("The ArgoBEAST lab is ready to use! run `argobeast open lab` to get started")
