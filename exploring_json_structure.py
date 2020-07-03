"""Чернетка / Draft"""

import json
import sys

RAW_JSON = {
    '21': '{"hash":-867186180,"data":[{"rId":843,"dvs":[{"id":5284,"loc":{"lat":48.90283,"lng":24.727563},"spd":0,"azi":309,"gNb":"АТ 0382 СІ","dis":false,"rad":false},{"id":5371,"loc":{"lat":48.92748,"lng":24.723808},"spd":0,"azi":287,"gNb":"АТ 6651 ВН","dis":true,"rad":false},{"id":5892,"loc":{"lat":48.94507,"lng":24.692708},"spd":18,"azi":275,"gNb":"АТ 6901 СА","dis":true,"rad":false},{"id":5388,"loc":{"lat":48.92516,"lng":24.709861},"spd":6,"azi":345,"gNb":"АТ 5589 ВІ","dis":false,"rad":false},{"id":5190,"loc":{"lat":48.9347,"lng":24.746428},"spd":13,"azi":315,"gNb":"АТ 1692 АА","dis":true,"rad":false},{"id":5886,"loc":{"lat":48.934064,"lng":24.706681},"spd":22,"azi":160,"gNb":"АТ 1126 АА","dis":true,"rad":false}]}]}'
    , '': ''  # template
}
for route_number, route_json_raw in RAW_JSON.items():
    print(route_json_raw)
    # route_json_raw = route_json_raw.replace('"', "'")  # " supported, ' not
    print(route_json_raw)
    route_json_raw_enc_dec = route_json_raw.encode(
        sys.getfilesystemencoding(), errors='surrogateescape'
    ).decode('utf-8')
    print(route_json_raw)
    route_json_serialized = json.loads(route_json_raw)
    print(route_json_serialized)
    print(f"{route_number:<11}\n"
          f"{json.dumps(route_json_serialized, indent=4, ensure_ascii=False)}")
