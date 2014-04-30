from setuptools import setup

exec(open('version.py').read())

setup(
    name = 'crefi',
    version = __version__,
    author = 'Vijaykumar Koppad',
    author_email = 'vijaykumar.koppad@gmail.com',
    url='https://github.com/vijaykumar-koppad/Crefi',
    license = 'BSD',
    description = ("A tool to generate different IO's and create files" +
                   " on any mount point"),
    py_modules = ['crefi','crefi_helper','logger'],
    requires = ["xattr"],
    entry_points = """
    [console_scripts]
    crefi = crefi:main
    """
)
