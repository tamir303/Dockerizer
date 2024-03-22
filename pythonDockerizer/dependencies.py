import subprocess

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