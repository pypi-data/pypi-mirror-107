"""
Module for controlling cli interaction.
"""


import argparse


def get_args():
    """
    Simple argparse implementation.

    Returns
    -------
    args : <class 'argparse.Namespace'>
    """
    usage = 'simplepkg <pkg_name> [options]'
    parser = argparse.ArgumentParser(description='Simple python package scaffolding utility',
                                     usage=usage)

    # GENERAL
    parser.add_argument('pkg_name', action='store',
                        help='name of your new package')

    parser.add_argument('-g', '--git', action='store_const', const=True, dest='git',
                        help='git init this package upon creation (requires git)')

    # LICENSE
    parser.add_argument('-nl', '--no-license', action='store_const', const=100, dest='pkg_license',
                        help='do _NOT_ include a license, package will not meet official PyPI requirements')

    parser.add_argument('--mit', action='store_const', const=0, dest='pkg_license',
                        help='include MIT license, default')

    parser.add_argument('--apache', action='store_const', const=1, dest='pkg_license',
                        help='include Apache license')

    parser.add_argument('--bsd2', action='store_const', const=2, dest='pkg_license',
                        help='include BSD2 license')

    parser.add_argument('--bsd3', action='store_const', const=3, dest='pkg_license',
                        help='include BSD3 license')

    parser.add_argument('--gplv2', action='store_const', const=4, dest='pkg_license',
                        help='include GPLv2 license')

    parser.add_argument('--gplv3', action='store_const', const=5, dest='pkg_license',
                        help='include GPLv3 license')

    parser.add_argument('--unlicense', action='store_const', const=6, dest='pkg_license',
                        help='include Unlicense license')

    # parser.add_argument('-a', '--author', action='store', dest='author',
    #                     help='enclose in quotes \'FULL NAME\'')

    # parser.add_argument('-e', '--email', action='store', dest='email',
    #                     help='email address')

    # parser.add_argument('-d', '--description', action='store', dest='description',
    #                     help='package description')

    # parser.add_argument('-u', '--url', action='store', dest='url',
    #                     help='project url/homepage')

    args = parser.parse_args()

    return args
