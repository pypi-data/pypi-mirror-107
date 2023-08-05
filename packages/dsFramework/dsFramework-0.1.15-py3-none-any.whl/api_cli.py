import click
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        try:
            cmd_name = ALIASES[cmd_name].name
        except KeyError:
            pass
        return super().get_command(ctx, cmd_name)

@click.group(cls=AliasedGroup)
def cli():
    """DS framework cli"""
# @click.option("--type", prompt="type", help="type of component")
# @click.option("--project_name", prompt="project_name", help="project_name")
# def apis(type, project_name):


@cli.command()
@click.argument('type')
@click.argument('project_name')
def generate(type, project_name):
    """List all cataloged APIs."""
    try:
        f = globals()["generate_%s" % type]
    except Exception as e:
        click.echo('type ' + type + ' not found')
        return
    f(project_name)

ALIASES = {
    "g": generate
}

def generate_project(projectName):
    projectName = clean_project_name(projectName)
    click.echo('project generated ' + projectName)
    create_project(projectName)

def generate_p(projectName):
    projectName = clean_project_name(projectName)
    click.echo('project generated ' + projectName)
    create_project(projectName)

def clean_project_name(projectName):
    projectName = projectName.replace('-', '_')
    return projectName
def create_project(projectName):
    create_folders(projectName)
    create_pipeline_file(projectName, 'preprocessor')
    create_pipeline_file(projectName, 'postprocessor')
    create_pipeline_file(projectName, 'labelizer')
    create_pipeline_file(projectName, 'pipeline')

    create_preproccesor_vocab_folder()
    create_project_config_yaml()

    create_testet_file(projectName, 'dataset')
    create_testet_file(projectName, 'reporter')
    create_testet_file(projectName, 'tester')
    create_testet_file(projectName, 'tester_server')

def create_folders(projectName):
    global directory
    directory = projectName + '_pipeline'
    if not os.path.exists(directory):
        os.mkdir(directory)

    global tester_directory
    tester_directory = directory + '/tester/'
    if not os.path.exists(tester_directory):
        os.mkdir(tester_directory)

def create_pipeline_file(projectName, pipelineType):
    with open(os.path.join(__location__, 'cli/' + pipelineType + '_template.py'), 'r') as file:
        data = file.read()
        projectNameNoUnderscore = ''.join(elem.capitalize() for elem in projectName.split('_'))
        className = projectNameNoUnderscore + pipelineType.capitalize()
        classNameFotBaseObject = projectNameNoUnderscore + '_' + pipelineType
        data = data.replace('generatedClassName', classNameFotBaseObject)
        data = data.replace('generatedClass',className)
        data = data.replace('generatedProjectName',projectNameNoUnderscore)
        data = data.replace('generatedDirectory',directory)
        current_dir = directory + '/' + pipelineType
        if not os.path.exists(current_dir):
            os.mkdir(current_dir)
        new_file = current_dir + "/" + pipelineType + ".py"
        new_init_file = current_dir + "/__init__.py"
        new_init_export = "from " + directory + "." + pipelineType + "." + pipelineType + " import " + className
        if not os.path.exists(new_file):
            f = open(new_file, "w")
            f.write(data)
            f.close()
        create_pipeline_init_file(new_init_file, new_init_export)

def create_testet_file(projectName, pipelineType):
    with open(os.path.join(__location__, 'cli/tester/' + pipelineType + '_template.py'), 'r') as file:
        data = file.read()
        projectNameNoUnderscore = ''.join(elem.capitalize() for elem in projectName.split('_'))
        pipelineTypeNoUnderscore = ''.join(elem.capitalize() for elem in pipelineType.split('_'))
        className = projectNameNoUnderscore + pipelineTypeNoUnderscore
        classNameFotBaseObject = projectNameNoUnderscore + '_' + pipelineType
        data = data.replace('generatedClassName', classNameFotBaseObject)
        data = data.replace('generatedClass',className)
        data = data.replace('generatedProjectName',projectNameNoUnderscore)
        data = data.replace('generatedDirectory',directory)
        current_dir = tester_directory
        new_file = current_dir + "/" + pipelineType + ".py"
        new_init_file = current_dir + "/__init__.py"
        new_init_export = "from " + tester_directory.replace('/', '.') + pipelineType + " import " + className
        if not os.path.exists(new_file):
            f = open(new_file, "w")
            f.write(data)
            f.close()
        create_tester_init_file(new_init_file, new_init_export)

def create_pipeline_init_file(init_path, init_export):
    if not os.path.exists(init_path):
        f = open(init_path, "w")
        f.write(init_export)
        f.close()

def create_tester_init_file(init_path, init_export):
    f = open(init_path, "a")
    f.write(init_export)
    f.write("\n")
    f.close()

def create_preproccesor_vocab_folder():
    currentDir = directory + '/preprocessor/vocab'
    if not os.path.exists(currentDir):
        os.mkdir(currentDir)

def create_project_config_yaml():
    with open(os.path.join(__location__, 'cli/config.yaml'), 'r') as file:
        data = file.read()
        data = data.replace('generatedDirectory', directory)
        new_file = directory + '/pipeline/config.yaml'
        if not os.path.exists(new_file):
            f = open(new_file, "w")
            f.write(data)
            f.close()
if __name__ == '__main__':
    cli(prog_name='cli')
