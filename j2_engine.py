from jinja2 import Environment, FileSystemLoader

# Load the template from the current directory
env = Environment(loader=FileSystemLoader('.'))

def render_template(user_inputs):
    """
    Render the NDA template with the provided context.
    
    :param context: Dictionary containing the values to render in the template.
    :return: Rendered NDA document as a string.
    """
    template = env.get_template('nda_template_disclosing.j2') if user_inputs['first_party_role'] == 'Disclosing Party' else env.get_template('nda_template_receiving.j2')
    return template.render(user_inputs)