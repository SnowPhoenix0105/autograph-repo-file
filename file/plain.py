from typing import List, Tuple

_valid_encoding = ["UTF-8", "GBK"]

def try_parse_as_plain(bin: bytes, fullpath: str) -> Tuple[List[str], bool]:
    for enc in _valid_encoding:
        try:
            text = bin.decode(enc)
            return text.split('\n'), True
        except:
            pass
    
    return [], False