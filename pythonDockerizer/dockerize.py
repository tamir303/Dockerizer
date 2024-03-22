import logging
from abc import ABC
from dependencies import get_dependencies
from template import create_dockerfile_template

logger = logging.getLogger(__name__)


class DefaultPaths(ABC):
    ENTRYPOINT: str = "main.py"
    VERSION: str = "latest"
    FILENAME: str = "Dockerfile"
    PORT: int = 80
    DEST_PATH: str = "./"


def create_docker_file(entrypoint: str = DefaultPaths.ENTRYPOINT,
                       version: str = DefaultPaths.VERSION,
                       filename: str = DefaultPaths.FILENAME,
                       port: int = DefaultPaths.PORT,
                       dest_path: str = DefaultPaths.DEST_PATH) -> None:
    """
    Creates a Dockerfile based on a Python version and dependency list.

    Args:
        version: The desired Python version (default: latest)
        entrypoint: The name of the entrypoint to use for the
        filename: The name of the generated Dockerfile (default: "dockerfile").
        port: exposed port for the Dockerfile (default: 80)
        dest_path: The destination path for the generated Dockerfile (default: ./)
    """

    dependencies: list[str] = get_dependencies()

    # Construct the Dockerfile content
    data = {
        'install_cond': "None" if len(dependencies) == 0 else f"""RUN pip install {" ".join(dependencies)}""",
        'entrypoint': entrypoint,
        'version': version,
        'port': port
    }

    # Write the Dockerfile template into a string
    dockerfile_content = create_dockerfile_template(data)

    # Write the Dockerfile content to a file
    with open("".join([dest_path, filename]), "w") as f:
        f.write(dockerfile_content)

    logger.info(f"Created Dockerfile: {filename}")
    logger.info(dockerfile_content)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate Dockerfile')
    parser.add_argument('--entrypoint', type=str,
                        default=DefaultPaths.ENTRYPOINT,
                        help='Name of the entrypoint file')

    parser.add_argument('--version', type=str,
                        default=DefaultPaths.VERSION,
                        help='Python version (default: latest)')

    parser.add_argument('--filename', type=str,
                        default=DefaultPaths.FILENAME,
                        help='Name of the Dockerfile (default: Dockerfile)')

    parser.add_argument('--port', type=int,
                        default=DefaultPaths.PORT,
                        help='Exposed port for the Dockerfile (default: 80)')

    parser.add_argument('--dest_path', type=str,
                        default=DefaultPaths.DEST_PATH,
                        help='Destination path for the Dockerfile (default: ./)')

    args = parser.parse_args()
    create_docker_file(args.entrypoint, args.version, args.filename, args.port, args.dest_path)