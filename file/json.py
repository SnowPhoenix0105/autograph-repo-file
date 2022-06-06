import logging
from typing import Any, List, Tuple, cast

_valid_encoding = ["UTF-8", "GBK"]
logger = logging.getLogger(__name__)

def _json_load(json_str: str) -> Any:
    return eval(json_str, {"__builtins__":{}})

def _parse_json(json_str: str) -> List[str]:
    ret = cast(List[str], [])

    def dfs(node: Any):
        if isinstance(node, str):
            try:
                tmp = _json_load(node)
                dfs(tmp)
            except:
                pass

            node = node.strip()

            if len(node) > 20:
                ret.append(node)
            return
        
        if isinstance(node, list):
            for e in node:
                dfs(e)
            return

        if isinstance(node, dict):
            for k, v in node.items():
                dfs(k)
                dfs(v)
            return

    try:
        obj = _json_load(json_str)
        dfs(obj)
        return ret

    except:
        pass


    lines = json_str.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        obj = _json_load(line)
        dfs(obj)
    return ret    

def try_parse_as_json(bin: bytes, fullpath: str) -> Tuple[List[str], bool]:
    for enc in _valid_encoding:
        try:
            text = bin.decode(enc)

            res = _parse_json(text)

            return res, True
        except:
            pass
    
    return [], False