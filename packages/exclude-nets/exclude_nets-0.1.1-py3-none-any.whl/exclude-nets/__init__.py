from ipaddress import IPv4Network, ip_network


def exclude_networks_ipv4(*mask_nets: list[IPv4Network]) -> list[IPv4Network]:
    mask_nets = [ip_network(net) for net in mask_nets]
    
    results = [ip_network('0.0.0.0/0')]
    for mask_net in mask_nets:
        allowed_nets, results = results, []
        for allowed_net in allowed_nets:
            if allowed_net.supernet_of(mask_net):
                results += list(allowed_net.address_exclude(mask_net))
                break
    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Exclude the given IPv4 networks.')
    parser.add_argument('networks', metavar='net', type=str, nargs='+',
                        help='an IPv4 network')

    args = parser.parse_args()

    for net in exclude_networks_ipv4(*args.networks):
        print(format(net))
