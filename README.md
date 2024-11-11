# Project 6: Dijkstra's and ARP Sniffing # Daniel Lounsbury
# Brian Hall
# CS372
# Collaborator(s): Brandon Nelson

## Page used for reference 
https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/ 

## Function(s) Documentation

### `ipv4_to_value(ipv4_addr)`
Convert a dots-and-numbers IP address to a single 32-bit numeric value of integer type. Returns an integer type.

### `value_to_ipv4(addr)`
Convert a single 32-bit numeric value of integer type to a dots-and-numbers IP address. Returns a string type.

### `get_subnet_mask_value(slash)`
Given a subnet mask in slash notation, return the value of the mask as a single number of integer type. The input can contain an IP address optionally, but that part should be discarded. Returns an integer type.

### `ips_same_subnet(ip1, ip2, slash)`
Given two dots-and-numbers IP addresses and a subnet mask in slash notation, return true if the two IP addresses are on the same subnet. Returns a boolean. This function utilizes `get_subnet_mask_value()` and `ipv4_to_value()`.

### `get_network(ip_value, netmask)`
Return the network portion of an address value as integer type.

### `find_router_for_ip(routers, ip)`
Search a dictionary of routers (keyed by router IP) to find which router belongs to the same subnet as the given IP. Return `None` if no router is on the same subnet as the given IP. This function calls `ips_same_subnet()`.

### `dijkstras_shortest_path(routers, src_ip, dest_ip)`
This function takes a dictionary representing the network, a source IP, and a destination IP, and returns a list with all the routers along the shortest path.