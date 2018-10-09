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
from lispat.base.manager import CommandManager

def main():
  # logging = Logger("Main")
  args = docopt.docopt(__doc__)
  if args['--doc.path']:
    user_path = args['--doc.path']
    manager = CommandManager(user_path)
    manager.run()

if __name__ == '__main__':
  main()
