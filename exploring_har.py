"""Чернетка / Draft
city.dozor.tech.har - log file
format: json-like
task: explore its structure and find useful key-value pairs

todo: improve naming"""

import re
import json


with open("city.dozor.tech.har", "rt", encoding='utf-8') as file_handle:
    log_text = file_handle.read()
    log_json = json.loads(log_text)
    # print(json.dumps(contents_as_json, indent=4))
    print(len(log_json["log"]["entries"]))
    entries_response_content_text = {}  # refactor it
    for entry in log_json["log"]["entries"]:
        if entry["response"]["content"]["text"].startswith('{"hash":'):  # filter
            # print(entry["startedDateTime"])
            # print(entry["response"]["content"]["text"])
            entries_response_content_text[entry["startedDateTime"]] = \
                json.loads(entry["response"]["content"]["text"])
    print(len(entries_response_content_text))
    # print(*entries_response_content_text.items(), sep='\n')
    for record in entries_response_content_text.items():
        print(f"===={record[0]}====")
        for subrecord in record[1]['data']:
            print("\t", subrecord)
            if "dvs" in subrecord.keys():
                for dvs_item in subrecord["dvs"]:
                    print("\t\t", dvs_item)
            else:
                pass  # !
    # pattern = re.compile(r'"(.*?)":')
    # all_keys = sorted(set(pattern.findall(contents)))
    # print(*all_keys, sep='\n')
    # all_keys - keys on various hierarchical levels in city.dozor.tech.har data structure"
