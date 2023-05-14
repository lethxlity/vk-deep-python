import json


def parse_json(json_str: str = None,
               required_fields: list = None,
               keywords: list = None,
               keyword_callback: callable = None):
    if required_fields is None:
        raise TypeError
    if keywords is None:
        raise TypeError
    if keyword_callback is None:
        raise TypeError
    json_doc = json.loads(json_str)
    for field in required_fields:
        if field in json_doc.keys():
            for keyword in keywords:
                if keyword.lower() == json_doc[field].lower():
                    keyword_callback((field, keyword))
                else:
                    if json_doc[field].lower().startswith((keyword.lower() + " ")):
                        keyword_callback((field, keyword))
                    if json_doc[field].lower().endswith((" " + keyword.lower())):
                        keyword_callback((field, keyword))
                    if " " + keyword.lower() + " " in json_doc[field].lower():
                        keyword_callback((field, keyword))
