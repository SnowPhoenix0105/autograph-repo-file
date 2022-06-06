import logging
import traceback
from typing import List, Tuple, cast, Dict
import docx

logger = logging.getLogger(__name__)

def try_parse_as_docx(bin: bytes, fullpath: str) -> Tuple[List[str], bool]:
    try:
        doc = docx.Document(fullpath)

        ret = []
        for para in doc.paragraphs:
            text = para.text
            if not text:
                continue
            ret.append(text)
        
        return ret, True

    except:
        # logger.warning(traceback.format_exc())
        return [], False