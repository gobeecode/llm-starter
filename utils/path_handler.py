from pathlib import Path

def get_project_root() -> Path:
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent
    return project_root

def get_output_directory() -> Path:
    project_root = get_project_root()
    output_directory = Path(project_root, "output")
    return output_directory
