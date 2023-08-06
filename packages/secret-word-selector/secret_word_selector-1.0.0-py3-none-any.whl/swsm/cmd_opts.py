import argparse

'''
sws get word -p 1 2 3
sws get-from-file -p 1 2 3 -l label
sws save word -l label
sws show-all
sws reset
'''

# create the top-level parser
parser = argparse.ArgumentParser(prog='sws')

# create the top-level sub-parser
subparsers = parser.add_subparsers(help='sub-command help',dest='subparsers')

# create the parser for the get command
get = subparsers.add_parser('get', help='get positions from secret')

get.add_argument('word',
                help="secret to process")

get.add_argument('-p', '--positions',
                    type=int,
                    nargs='+',
                    help='the positions to get from secret',
                    required=True)

# create the parser for get-from-file command
get_from_file = subparsers.add_parser('get-from-file',
                    help="get secret positions from secrets file")

get_from_file.add_argument('-p','--positions',
                help="the positions to get from secrets file",
                type=int,
                nargs='+',
                required=True)

get_from_file.add_argument('-l','--label',
                    help="the secret's label",
                    required=True)

# create the parser for the  save command
save = subparsers.add_parser('save',
                            help='save a secret to disk with a label.')

save.add_argument('word',
                help="secret to be saved to disk")

save.add_argument('-l','--label',
                    help='give the saved secret a label',
                    required=True)

# create the parser for the show-all command
show_all = subparsers.add_parser('show-all',
                    help = 'Show all secrets available in secrets file')

# create the parser for the reset command
reset = subparsers.add_parser('reset',
                help='reset sws config and delete secrets file from disk')

args = parser.parse_args()
