from . import main


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Exclude the given IPv4 networks.')
    parser.add_argument('networks', metavar='net', type=str, nargs='+',
                        help='an IPv4 network')

    args = parser.parse_args()

    for net in exclude_networks_ipv4(*args.networks):
        print(format(net))

if __name__ == '__main__':
    main()
