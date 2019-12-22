# Address Resolution Protocol (ARP)

[https://www.youtube.com/watch?v=NpiORFxyM4c](https://www.youtube.com/watch?v=NpiORFxyM4c)

- ARP is a protocol for mapping an IP address to a physical MAC address on a local area network.
- Program used by one device to find another device's MAC address based on that device's IP
- Device's maintain ARP Cache tables mapping IP to MAC
    - `arp -a` lists table

How does ARP work?

- `Client` (`192.168.1.10`) wants to communicate with `Server` (`192.168.1.50`)
- `Client` knows `Server` has IP of `192.168.1.50` and is local.
    1. `Client` _broadcasts_ packet to all IPs:
        - "Are you `192.168.1.50`? Please send MAC"
            - IP Source: `192.168.1.10`
            - MAC Source: `oe:cd:ef:12:34:56`
            - IP Dest: `192.168.1.50`
            - MAC Dest: `ff:ff:ff:ff:ff:ff` (broadcast)
        - For each device that 'hears' broadcast: if not `192.168.1.50` silently ignore packet
    1. `Server` 'hears' packet - sends Unicast (1-to-1 communication) to `Client`
        - IP Source: `192.168.1.50`
        - MAC Source: `fa:ed:db:91:11:19`
        - IP Dest: `192.168.1.10`
        - Mac Dest: `oe:cd:ef:12:34:56` (unicast)
    1. `Client` confirms by send `Server` a request
        - IP Source: `192.168.1.10`
        - MAC Source: `oe:cd:ef:12:34:56`
        - IP Dest: `192.168.1.50`
        - MAC Source: `fa:ed:db:91:11:19` (unicast)
        - `Client` updates ARP Cache table for future reference

## ARP Summary

1. Layer 2 protocol (aruably as Layer 2.5 as it exists between layers)
    - Uses Layer 3 IP address to find Layer 2 MAC address
1. Operates on LAN (same broadcast domain)
    - Relies on broadcasting
1. Uses/Updates ARP Table
