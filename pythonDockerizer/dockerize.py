import logging
import subprocess
from enum import Enum

logger = logging.getLogger(__name__)


class DefaultPaths(Enum):
    VERSION = "latest"
    FILENAME = "Dockerfile"
    PORT = 80
    DEST_PATH = "./"


def create_docker_file(entrypoint: str,
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

    def get_dependencies() -> list[str]:
        """
        Retrieve a list of installed Python dependencies using pip freeze.

        Returns:
            list[str]: A list of strings, each representing an installed Python dependency.

        Raises:
            RuntimeError: If there's an error running pip freeze or capturing its output.
        """
        try:
            process = subprocess.Popen(["pip", "freeze"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()

            if process.returncode != 0:
                raise RuntimeError("Error running pip freeze: " + error.decode())

            return output.decode("utf-8").splitlines()
        except Exception as e:
            raise RuntimeError("Error getting dependencies: " + str(e))

    dependencies: list[str] = get_dependencies()

    # Construct the Dockerfile content
    install_condition = "" if len(dependencies) == 0 else f"""RUN pip install {" ".join(dependencies)}"""
    dockerfile_content = f"""\
FROM python:{version}
WORKDIR /app
COPY . /app
{install_condition}
EXPOSE {port}
CMD [ "python", "{entrypoint}.py" ]
"""
    # Write the Dockerfile content to a file
    with open(dest_path + filename, "w") as f:
        f.write(dockerfile_content)

    logger.info(f"Created Dockerfile: {filename}")
    logger.info(f"Created Dockerfile: {dockerfile_content}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate Dockerfile')
    parser.add_argument('--entrypoint', type=str, help='Name of the entrypoint file', required=True)
    parser.add_argument('--version', type=str, default=DefaultPaths.VERSION, help='Python version (default: latest)')
    parser.add_argument('--filename', type=str, default=DefaultPaths.FILENAME,
                        help='Name of the Dockerfile (default: Dockerfile)')
    parser.add_argument('--port', type=int, default=DefaultPaths.PORT, help='Exposed port for the Dockerfile ('
                                                                            'default: 80)')
    parser.add_argument('--dest_path', type=str, default=DefaultPaths.DEST_PATH, help='Destination path for the '
                                                                                      'Dockerfile (default: ./)')

    args = parser.parse_args()

    create_docker_file(args.entrypoint, args.version, args.filename, args.port, args.dest_path)
