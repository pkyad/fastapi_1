"""fastapi_v1 models."""
import pkgutil
from pathlib import Path


def load_all_models() -> None:
    """Load all models from this folder."""
    package_dir = Path(__file__).resolve().parent
    modules = pkgutil.walk_packages(
        path=[str(package_dir)],
        prefix="db.models.",
    )
    for module in modules:
        # print("module", module)
        __import__(module.name)  # noqa: WPS421
