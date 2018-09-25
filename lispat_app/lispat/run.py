"""Lost in Space and Time

Usage:
    lispat --doc.path=<content-path>
    lispat [-h | --help]
    lispat --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
import docopt
from .base.manager import CommandManager

def main():
  args = docopt.docopt(__doc__)
  if args['--doc.path']:
    user_path = args['--doc.path']
    CommandManager(user_path)

if __name__ == '__main__':

  main()
