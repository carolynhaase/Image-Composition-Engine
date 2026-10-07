import json
from pathlib import Path

import yaml


def convert_yaml_to_json(yaml_path: str | Path, json_path: str | Path) -> None:
    yaml_path = Path(yaml_path)
    json_path = Path(json_path)

    with yaml_path.open(encoding="utf-8") as file:
        config = yaml.safe_load(file)

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=2, ensure_ascii=False)