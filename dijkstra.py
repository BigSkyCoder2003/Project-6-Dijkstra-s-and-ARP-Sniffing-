import sys
import json
import math  # If you want to use math.inf for infinity

def ipv4_to_value(ipv4_addr):

    octets = map(int, ipv4_addr.split('.'))
    return sum(octet << (8 * (3 - i)) for i, octet in enumerate(octets))


def value_to_ipv4(addr):

    return '.'.join(str((addr >> (8 * (3 - i))) & 0xFF) for i in range(4))


def get_subnet_mask_value(slash):

    prefix_length = int(slash.strip('/'))
    mask = (1 << 32) - (1 << (32 - prefix_length))
    return mask


def ips_same_subnet(ip1, ip2, slash):

    ipval1 = ipv4_to_value(ip1)
    ipval2 = ipv4_to_value(ip2)
    netmask = get_subnet_mask_value(slash)
    return (get_network(ipval1, netmask)) == (get_network(ipval2, netmask))


def get_network(ip_value, netmask):

    return ip_value & netmask


def find_router_for_ip(routers, ip):

    for router_ip, router_info in routers.items():
        if ips_same_subnet(ip, router_ip, router_info["netmask"]):
            return router_ip
    return None

def dijkstras_shortest_path(routers, src_ip, dest_ip):
    """
    This function takes a dictionary representing the network, a source
    IP, and a destination IP, and returns a list with all the routers
    along the shortest path.

    The source and destination IPs are **not** included in this path.

    Note that the source IP and destination IP will probably not be
    routers! They will be on the same subnet as the router. You'll have
    to search the routers to find the one on the same subnet as the
    source IP. Same for the destination IP. [Hint: make use of your
    find_router_for_ip() function from the last project!]

    The dictionary keys are router IPs, and the values are dictionaries
    with a bunch of information, including the routers that are directly
    connected to the key.

    This partial example shows that router `10.31.98.1` is connected to
    three other routers: `10.34.166.1`, `10.34.194.1`, and `10.34.46.1`:

    {
        "10.34.98.1": {
            "connections": {
                "10.34.166.1": {
                    "netmask": "/24",
                    "interface": "en0",
                    "ad": 70
                },
                "10.34.194.1": {
                    "netmask": "/24",
                    "interface": "en1",
                    "ad": 93
                },
                "10.34.46.1": {
                    "netmask": "/24",
                    "interface": "en2",
                    "ad": 64
                }
            },
            "netmask": "/24",
            "if_count": 3,
            "if_prefix": "en"
        },
        ...

    The "ad" (Administrative Distance) field is the edge weight for that
    connection.

    **Strong recommendation**: make functions to do subtasks within this
    function. Having it all built as a single wall of code is a recipe
    for madness.
    """
    src_router = find_router_for_ip(routers, src_ip)
    dest_router = find_router_for_ip(routers, dest_ip)

    if not src_router or not dest_router:
        return[]
    
    if ips_same_subnet(src_ip, dest_ip, routers[src_router]["netmask"]):
        return[]
    
    dist = {router_ip: math.inf for router_ip in routers}
    parents = {router_ip: None for router_ip in routers}
    dist[src_router] = 0
    to_visit = set(routers.keys())

    while to_visit:
        current = min(to_visit, key = lambda x: dist[x])
        to_visit.remove(current)

        for neighbor, connection in routers[current]['connections'].items():
            alt = dist[current] + connection['ad']

            if alt < dist[neighbor]:
                dist[neighbor] = alt
                parents[neighbor] = current
    path = []
    current_node = dest_router
    while current_node != src_router:
        if current_node is None:
            return []
        path.append(current_node)
        current_node = parents[current_node]
    path.append(src_router)
    path.reverse()

    return path





#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
