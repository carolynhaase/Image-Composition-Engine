from pathlib import Path

from img_comp_engine.config import convert_yaml_to_json
from img_comp_engine.engine import run


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    yaml_path = project_dir / "conf.yml"
    json_path = project_dir / "config.json"

    convert_yaml_to_json(yaml_path, json_path)
    run(json_path, project_dir / "Images", project_dir / "output")


if __name__ == "__main__":
    main()