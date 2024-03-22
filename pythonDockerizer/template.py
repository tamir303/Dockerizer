from jinja2 import Template

def create_dockerfile_template(data: dict) -> str:
    """
    Creates a Dockerfile template by rendering a Jinja2 template.

    Args:
        data (dict): A dictionary containing data to render the template.

    Returns:
        str: Rendered Dockerfile template as a string.
    """
    with open('pythonDockerizer/dockerfile_template.j2', 'r') as f:
        template_string = f.read()

    template = Template(template_string)
    output = template.render(data)
    return output


