import os as _os

AUTOGRAPH_REPO_FILE_SAVE_DIR = _os.getenv("AUTOGRAPH_REPO_FILE_SAVE_DIR")
if not AUTOGRAPH_REPO_FILE_SAVE_DIR:
    abspath = _os.path.abspath('.')
    idx = abspath.find("autograph-repo-file")
    if idx < 0:
        AUTOGRAPH_REPO_FILE_SAVE_DIR = _os.path.join(abspath, "workdir")
    else:
        AUTOGRAPH_REPO_FILE_SAVE_DIR = _os.path.join(abspath[:idx], "autograph-repo-file", "workdir")
    del abspath
    del idx

del _os