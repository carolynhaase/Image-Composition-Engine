from pathlib import Path
import sys

from img_comp_engine.config import convert_yaml_to_json
from img_comp_engine.engine import run


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    yaml_path = project_dir / "conf.yml"
    json_path = project_dir / "Thomas_config.json"

    convert_yaml_to_json(yaml_path, json_path)
    run(json_path, project_dir / "Images", project_dir / "output")


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        red = "\033[1;31m" if sys.stderr.isatty() else ""
        reset = "\033[0m" if red else ""
        print(f"{red}Erreur : {error}{reset}", file=sys.stderr)
        raise SystemExit(1)