"""
simplepkg main.
"""

from simplepkg.modules import skeleton
from simplepkg.modules import cli


def main():
    """
    Retrieves arguments, creates Skeleton instance, and scaffolds the
    new project.
    """
    args = cli.get_args()
    pkg_name = args.pkg_name
    if args.pkg_license:
        pkg_license = args.pkg_license
    else:
        pkg_license = 0
    git = args.git
    package = skeleton.Skeleton(pkg_name, pkg_license, git)
    package.scaffold()
    package.apply_template()
    package.show_pkg()


if __name__ == '__main__':
    main()
