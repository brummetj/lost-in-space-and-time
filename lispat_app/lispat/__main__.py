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

def main():
    args = docopt.docopt(__doc__)
    print(args)

if __name__ == '__main__':
    main()
