import os
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path

import setuptools
import toml

NODE_DIR = Path("./frontend")

FRONTEND_DIR = Path("./forager_frontend")
BACKEND_DIR = Path("./forager_server")
EMBEDDING_SERVER_DIR = Path("./forager_embedding_server")
KNN_DIR = Path("./forager_knn")
CLIP_DIR = Path("./3rdparty/CLIP")

DEBUG_FRONTEND = False
UPLOAD = True


def read_poetry_deps(path):
    data = toml.load(path)
    dependencies = data["tool"]["poetry"]["dependencies"]
    setup_deps = []
    for package_name, version in dependencies.items():
        if package_name == "python":
            continue
        if isinstance(version, dict):
            # No direct references for uploaded packages
            if UPLOAD:
                continue
            if "url" in version:
                ver_str = f" @ {version['url']}"
            elif "path" in version:
                ver_str = f" @ file:///{version['path']}"
        elif version == "*":
            ver_str = ""
        elif version[0] == "^":
            vs = version[1:].split(".")
            if vs[0] == "0" and len(vs) > 1:
                if len(vs) > 2 and vs[1] == "0":
                    upper = f",<0.0.{str(int(vs[2]) + 1)}"
                else:  # len == 2 or 3, and vs[1] is not zero
                    upper = f",<0.{str(int(vs[1]) + 1)}.0"
            else:
                upper = f",<{str(int(vs[0]) + 1)}.0.0"
            if len(vs) == 1:
                ver_str = f">={vs[0]}.0.0{upper}"
            elif len(vs) == 2:
                ver_str = f">={vs[0]}.{vs[1]}.0{upper}"
            else:
                ver_str = f">={version[1:]}{upper}"
        elif version.startswith("==") or version.startswith(">="):
            ver_str = version
        else:
            raise Exception("Error!")
        setup_deps.append(f"{package_name}{ver_str}")
    return setup_deps


def build_frontend(cmd):
    class CommandWrapper(cmd):
        def run(self):
            # Build react frontend
            if not DEBUG_FRONTEND and (FRONTEND_DIR / "package.json").exists():
                # Don't build if we are inside an sdist
                npm_env = os.environ.copy()
                npm_env.update({"REACT_APP_SERVER_URL": "http://localhost:8000"})
                subprocess.run(args=["npm", "install"], cwd=FRONTEND_DIR, check=True)
                subprocess.run(
                    args=["npm", "run", "build"],
                    cwd=FRONTEND_DIR,
                    env=npm_env,
                    check=True,
                )
                # Regen package data after build
                self.distribution.package_data = find_package_data()
            cmd.run(self)

    return CommandWrapper


PACKAGES = [
    ("forager", "forager"),
    ("forager_frontend", "forager_frontend"),
    ("forager_server_api", "forager_server/forager_server_api"),
    ("forager_server", "forager_server/forager_server"),
    ("forager_embedding_server", "forager_embedding_server"),
    ("forager_knn", "forager_knn/src/forager_knn"),
    ("clip", "3rdparty/CLIP"),
]


def find_packages():
    packages = [p[0] for p in PACKAGES]
    for name, path in PACKAGES:
        packages += [name + "." + pk for pk in setuptools.find_packages(where=path)]
    print("packages", packages)
    return packages


def find_package_dirs():
    packages = {p[0]: p[1] for p in PACKAGES}
    for name, path in PACKAGES:
        packages.update(
            {
                name + "." + pk: path + "/" + pk
                for pk in setuptools.find_packages(where=path)
            }
        )
    print("package_Dirs", packages)
    return packages


def package_files(root):
    paths = []
    for (path, directories, filenames) in os.walk(root):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


def find_package_data():
    data = defaultdict(list)
    data["forager_frontend"] += package_files("forager_frontend/build")
    for name, path in PACKAGES:
        data[name] += ["pyproject.toml"]
    data["clip"] += ["clip/bpe_simple_vocab_16e6.txt.gz", "requirements.txt"]
    print("package_data", data)
    return data


def find_package_deps():
    install_deps = ["uvicorn", "sanic"]
    for package_path in [
        BACKEND_DIR,
        EMBEDDING_SERVER_DIR,
        KNN_DIR,
        FRONTEND_DIR,
    ]:
        install_deps += read_poetry_deps(package_path / "pyproject.toml")
    with open(str(CLIP_DIR / "requirements.txt"), "r") as f:
        install_deps += [x.strip() for x in f.readlines()]
    print("Install deps:", install_deps)
    return install_deps
