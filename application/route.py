import http
import io
import logging
from typing import Dict, Tuple, cast, Callable, List
import flask
from file.save import FileManager
from file.docx import try_parse_as_docx
from file.plain import try_parse_as_plain
from file.json import try_parse_as_json
import json

logger = logging.getLogger(__name__)

def build(app: flask.Flask, file_manager: FileManager):

    @app.route("/coffee")
    def coffee() -> Tuple[str, int]:
        return "I'm a teapot!", http.HTTPStatus.IM_A_TEAPOT

    filetype_dict = cast(Dict[str, Callable[[bytes, str], Tuple[List[str], bool]]], {
        "docx": try_parse_as_docx,
        "json": try_parse_as_json,
        "txt": try_parse_as_plain,
    })
    @app.route("/save", methods=['POST'])
    def save_file():
        bytes = flask.request.get_data()
        logger.info(flask.request.headers)

        if len(bytes) == 0:
            return {}, http.HTTPStatus.BAD_REQUEST
        
        fullpath, hash_str, url = file_manager.save_file(bytes)

        text_list = []
        file_type = "unk"
        for typ, try_parse in filetype_dict.items():
            res, ok = try_parse(bytes, fullpath)
            if ok:
                text_list = res
                file_type = typ
                break

        return {
            "url": url,
            "type": file_type,
            "hash": hash_str,
            "text_list": text_list,
        }

    @app.route("/delete", methods=['POST'])
    def delete_file():
        req = flask.request.get_json()

        url = req["url"]

        ok = file_manager.delete_file(url)

        return {
            "deleted": ok,
        }

    @app.route("/get", methods=['POST'])
    def get_file():
        req = flask.request.get_json()

        url = req["url"]

        bin = file_manager.read_file(url)

        return flask.send_file(io.BytesIO(bin), mimetype="multipart/form-data")

    @app.route("/raw/<path:url>", methods=['GET'])
    def get_file_by_url(url):
        bin = file_manager.read_file(url)

        return flask.send_file(io.BytesIO(bin), mimetype="multipart/form-data")


