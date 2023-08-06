"""
Skeleton class.
"""

import configparser
import os
from pathlib import Path


class Skeleton:
    """
    Prepare and scaffold new project.

    Parameters
    ----------
    pkg_name : str
        Name of generated package, positional argument for simplepkg.

    pkg_license : int
        Optional argument for choosing the applied license. Default is
        MIT.

    git : bool
        Optional argument for initalizing new git repository.

    Attributes
    ----------
    root : str
        String representation of <class 'pathlib.PosixPath'> for
        current working directory.

    pkg_name : str
        Name of generated package.

    lic : str
        String representation of the optional license argument.
        Default is MIT.

    git : bool
        Optional argument for initializing new git repository. Default
        is False.

    default_files : list
        Default files for root of project. Pulled from config.

    dirs : list
        Default directories for project. Pulled from config.

    files : list
        Additonal files for project. Pulled from config.

    Methods
    -------
    scaffold(self)
        Creates project structure based on config entries.

    apply_template(self)
        Applies templates to the scaffolded files, modifies files
        according to applied parameters.

    show_pkg(self)
        Prints new project directory structure.

    Examples
    --------
    >>> package = skeleton.Skeleton(pkg_name, pkg_license, git)
    >>> package.scaffold()
    >>> package.apply_template()
    >>> package.show_pkg()
    """

    def __init__(self, pkg_name='new_simple_pkg', pkg_license=0, git=False):
        """
        Skeleton init method.
        """
        root = str(Path(__file__).parent.parent)
        config = configparser.ConfigParser()
        config_path = f'{root}/data/config'
        config.read(config_path)
        default_files = dict(config.items('DEFAULT_FILES'))
        dirs = dict(config.items('DIRS'))
        files = dict(config.items('FILES'))
        self.root = root
        self.pkg_name = pkg_name
        self.lic = str(pkg_license)
        self.git = git
        self.default_files = list(default_files.values())
        self.dirs = [w.replace('pkg', pkg_name) for w in dirs.values()]
        self.files = [w.replace('pkg', pkg_name)
                      for w in files.values()]

    def scaffold(self):
        """
        Creates project structure based on config entries.
        """
        root = f'{self.pkg_name}/'
        Path(root).mkdir(parents=True, exist_ok=True)
        for df in self.default_files:
            Path(f'{root}{df}').touch()
        for d in self.dirs:
            Path(f'{root}{d}').mkdir(parents=True, exist_ok=True)
        for f in self.files:
            Path(f'{root}{f}').touch()

    def apply_template(self):
        """
        Applies templates to the scaffolded files, modifies files
        according to applied parameters.
        """
        template_path = f'{self.root}/templates'

        insert_templates = {
            f'{template_path}/app.tmpl': f'{self.pkg_name}/{self.pkg_name}/app.py',
            f'{template_path}/config.tmpl': f'{self.pkg_name}/{self.pkg_name}/data/config',
            f'{template_path}/init.tmpl': f'{self.pkg_name}/{self.pkg_name}/__init__.py',
            f'{template_path}/main.tmpl': f'{self.pkg_name}/{self.pkg_name}/__main__.py',
            f'{template_path}/make.tmpl': f'{self.pkg_name}/Makefile',
            f'{template_path}/manifest.tmpl': f'{self.pkg_name}/MANIFEST.in',
            f'{template_path}/module.tmpl': f'{self.pkg_name}/{self.pkg_name}/modules/{self.pkg_name}_module.py',
            f'{template_path}/readme.tmpl': f'{self.pkg_name}/README.md',
            f'{template_path}/setup.tmpl': f'{self.pkg_name}/setup.py'
        }

        for k, v in insert_templates.items():
            insert_template(k, v)

        license_tmpl_path = {
            '0': f'{template_path}/mit_lic.tmpl',
            '2': f'{template_path}/apache_lic.tmpl',
            '2': f'{template_path}/bsd2_lic.tmpl',
            '3': f'{template_path}/bsd3_lic.tmpl',
            '4': f'{template_path}/gplv2_lic.tmpl',
            '5': f'{template_path}/gplv3_lic.tmpl',
            '6': f'{template_path}/unlicense_lic.tmpl',
            '100': None
        }

        license_tmpl_path = license_tmpl_path[self.lic]

        if license_tmpl_path is not None:
            Path(f'{self.pkg_name}/LICENSE').touch()
            insert_template(license_tmpl_path, f'{self.pkg_name}/LICENSE')
        elif license_tmpl_path is None:
            with open(f'{self.pkg_name}/MANIFEST.in', 'r') as manifest:
                lines = manifest.readlines()
            with open(f'{self.pkg_name}/MANIFEST.in', 'w') as manifest:
                manifest.writelines(lines[1:])

        if self.git:
            Path(f'{self.pkg_name}/.gitignore').touch()
            insert_template(f'{template_path}/gitignore.tmpl',
                            f'{self.pkg_name}/.gitignore')
            os.popen(f'cd {self.pkg_name} && git init')

        files_with_pkg_placeholder = {
            'app': f'{self.pkg_name}/{self.pkg_name}/app.py',
            'main': f'{self.pkg_name}/{self.pkg_name}/__main__.py',
            'manifest':  f'{self.pkg_name}/MANIFEST.in',
            'readme': f'{self.pkg_name}/README.md',
            'setup': f'{self.pkg_name}/setup.py',
            'test_app': f'{self.pkg_name}/{self.pkg_name}/test/test_app.py',
            'test_pkg': f'{self.pkg_name}/{self.pkg_name}/test/test_{self.pkg_name}.py',
            'test_module': f'{self.pkg_name}/{self.pkg_name}/test/test_{self.pkg_name}_module.py'
        }

        for f in [v for k, v in files_with_pkg_placeholder.items() if k.startswith('test')]:
            insert_template(f'{template_path}/test.tmpl', f)

        replace_file_terms = [
            (f'{self.pkg_name}/{self.pkg_name}/test/test_app.py',
             'TESTIMPORT', 'from pkg import app'),
            (f'{self.pkg_name}/{self.pkg_name}/test/test_app.py', 'TESTCLASS', 'App'),
            (f'{self.pkg_name}/{self.pkg_name}/test/test_{self.pkg_name}.py',
             'TESTIMPORT', 'import pkg'),
            (f'{self.pkg_name}/{self.pkg_name}/test/test_{self.pkg_name}.py',
             'TESTCLASS', f'{self.pkg_name.title()}'),
            (f'{self.pkg_name}/{self.pkg_name}/test/test_{self.pkg_name}_module.py',
             'TESTIMPORT', f'from pkg.modules import pkg_module'),
            (f'{self.pkg_name}/{self.pkg_name}/test/test_{self.pkg_name}_module.py',
             'TESTCLASS', f'{self.pkg_name.title()}Module'),
            (f'{self.pkg_name}/{self.pkg_name}/__init__.py',
             'SIMPLELOG', f'{self.pkg_name}.log')
        ]

        for replace_tuple in replace_file_terms:
            file_path, search_term, replace_term = replace_tuple
            replace_file_term(file_path, search_term, replace_term)

        for f in files_with_pkg_placeholder.values():
            replace_file_term(f, 'pkg', self.pkg_name)

    def show_pkg(self):
        """
        Prints new project directory structure.
        """
        print('SUCCESS!\n\nDemo new package:\n')
        print(f'$ cd {self.pkg_name}\n$ python3 -m {self.pkg_name}\n')
        for root, dirs, files in os.walk(self.pkg_name):
            dirs[:] = [d for d in dirs if d not in '.git']
            files[:] = [f for f in files if f not in '.gitignore']
            level = root.replace(self.pkg_name, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print(f'{subindent}{f}')


def insert_template(tmpl_path, file_path):
    """
    Apply templates to generic scaffolded files.

    Parameters
    ----------
    tmpl_path : str
        Path to template.

    file_path : str
        Path to file.
    """
    with open(tmpl_path) as tmpl:
        with open(file_path, 'w') as f:
            for line in tmpl:
                f.write(line)


def replace_file_term(file_path, search_term, replace_term):
    """
    Modifies files by replacing a search term with a replacement term.

    Parameters
    ----------
    file_path : str
        Path to file.

    search_term : str
        Term to search for and replace.

    replace_term : str
        Term to be substituted for search term.
    """
    with open(file_path, 'r') as f:
        content = f.read()
    content = content.replace(search_term, replace_term)
    with open(file_path, 'w') as f:
        f.write(content)
