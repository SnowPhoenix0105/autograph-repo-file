import flask
import logging
from application.route import build
import config
from file.save import FileManager
from utils.log import config_logging, print_const_configs


if __name__ == '__main__':
    config_logging("test.log", logging.INFO, logging.DEBUG)
    print_const_configs()

    file_manager = FileManager(base_dir=config.AUTOGRAPH_REPO_FILE_SAVE_DIR)

    app = flask.Flask(__name__)

    build(app, file_manager=file_manager)

    app.run(host="localhost", port=8001, debug=True)



