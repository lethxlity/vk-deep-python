import json


def parse_json(json_str: str,
               required_fields: list = None,
               keywords: list = None,
               keyword_callback: callable = print):
    if required_fields is None:
        return None
    if keywords is None:
        return None
    json_doc = json.loads(json_str)
    for field in required_fields:
        if field in json_doc.keys():
            for keyword in keywords:
                if keyword in json_doc[field]:
                    keyword_callback(keyword)
