import math
import sys


class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def show_arg_err(argv=None):
    if argv is None:
        print(f'{Color.RED}Invalid number of arguments! Use "-h" or "--help" for help.{Color.END}')
    else:
        print(f'{Color.RED}Invalid arguments: "{argv}"! Use "-h" or "--help" for help.{Color.END}')


def show_file_err(filename):
    print(f'{Color.RED}Could not open file "{filename}"!{Color.END}')


def show_help():
    print(f'''Usage:
    {Color.BOLD}-n <value> -e <value> -c <filename> [-v]{Color.END}
        Takes contents of RSA-encrypted file and tries to decrypt it using Fermat's attack.
        Parameters need to be positive integers. Use option "-v" for verbose output.
    {Color.BOLD}-h, --help{Color.END}
        Displays this message.''')


def decrypt(n, e, filename, verbose=False):
    try:
        file = open(filename, 'r', encoding='utf8')
        x = int(math.sqrt(n))
        i = 0

        print(f'Will try to decrypt file {Color.BOLD}{filename}{Color.END}')
        print(f'Finding {Color.BOLD}p{Color.END} and {Color.BOLD}q{Color.END} '
              f'for {Color.BOLD}n{Color.END} = {Color.BLUE}{n}{Color.END}...')

        while True:
            try:
                y = math.sqrt(x ** 2 - n)
                if verbose:
                    print(f'{Color.BOLD}x{i}{Color.END} = {Color.BLUE}{x}{Color.END}, '
                          f'{Color.BOLD}y{i}{Color.END} = {Color.BLUE}{y}{Color.END}')
                if y % 1 == 0:
                    break
            except ValueError:
                if verbose:
                    print(f'{Color.BOLD}x{i}{Color.END} = {Color.BLUE}{x}{Color.END}, '
                          f'{Color.BOLD}y{i}{Color.END} = {Color.RED}NaN{Color.END}')
            x = x + 1
            i = i + 1

        p = x + int(y)
        q = x - int(y)
        print(f'Found {Color.BOLD}p{Color.END} = {Color.BLUE}{p}{Color.END}, '
              f'{Color.BOLD}q{Color.END} = {Color.BLUE}{q}{Color.END}!')

        phi = (p - 1) * (q - 1)
        d = pow(e, -1, phi)
        print(f'Found {Color.BOLD}phi{Color.END} = {Color.BLUE}{phi}{Color.END}, '
              f'{Color.BOLD}d{Color.END} = {Color.BLUE}{d}{Color.END} '
              f'for {Color.BOLD}e{Color.END} = {Color.BLUE}{e}{Color.END}!')

        message = ""
        print(f'Decrypting...')
        for i, c in enumerate(file.readlines()):
            try:
                c = int(c)
            except ValueError:
                print(f'{Color.RED}Non-digit character found at line {i}! Exiting.{Color.END}')
                file.close()
                exit(-1)
            m = pow(c, d, n)
            part = m.to_bytes(4, byteorder='big').decode('cp1251')
            message += part

        print(f"Success! Decrypted message: {Color.YELLOW}{message}{Color.END}")
        file.close()
    except FileNotFoundError:
        show_file_err(filename)


if __name__ == '__main__':
    argc = len(sys.argv)
    argv = sys.argv
    if argc == 2:
        if argv[1] == "-h" or argv[1] == "--help":
            show_help()
        else:
            show_arg_err(argv[1])
    elif argc == 7 or argc == 8:
        try:
            N = int(argv[2])
            e = int(argv[4])
            if argv[1] == "-n" and N > 0 and argv[3] == "-e" and e > 0 and argv[5] == "-c" and (
                    argc == 7 or argv[7] == "-v"):
                decrypt(N, e, argv[6], argc == 8)
            else:
                raise ValueError
        except ValueError:
            show_arg_err(' '.join(sys.argv[1:]))
    else:
        show_arg_err()
