from typing import Any, Dict, List

def find_packages() -> List[str]: ...
def setup(
        name : str,
        version : str,
        author : str,
        description : str,
        long_description : str,
        url : str,
        packages : List[str],
        entry_points : Dict[str, List[str]],
        install_requires : List[str],
        classifiers : List[str],
        include_package_data : bool
) -> None: ...
