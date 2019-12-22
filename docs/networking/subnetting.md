# Subnetting

## IPv4 Classes

- Notes on [https://www.youtube.com/watch?v=vcArZIAmnYQ&list=PLSNNzog5eydt_plAtt3k_LYuIXrAS4aDZ](https://www.youtube.com/watch?v=vcArZIAmnYQ&list=PLSNNzog5eydt_plAtt3k_LYuIXrAS4aDZ)

Class|First Octet decimal (range)|First Octet binary (range)|IP Range|Subnet Mask|Hosts per Network ID|# of Networks
-|-|-|-|-|-|-|-
Class A|0-127|0XXXXXXX|0.0.0.0 - 127.255.255.255|255.0.0.0|2<sup>24</sup>-2|2<sup>7</sup>
Class B|128-191|10XXXXXX|128.0.0.0 - 191.255.255.255|255.255.0.0|2<sup>16</sup>-2|2<sup>14</sup>
Class C|192-223|110XXXXX|192.0.0.0 - 223.255.255.255|255.255.255.0|2<sup>8<sup>-2|2<sup>21</sup>
Class D (Multicast)|224-239|1110XXXX|224.0.0.0 - 239.255.255.255||
Class E (Experimental)|240-255|1111XXXX|240.0.0.0 - 255.255.255.255||
||||||h = 2<sup>x</sup>-2|n = 2<sup>y</sup>

- h = 2<sup>x</sup>-2 ; `x` is the number of 0's (in binary) in the subnet mask
- n = 2<sup>y</sup> ; `y` is the number of 1's (in binary) in the subnet mask - only including _unfixed_ values.
    - The fixed values in the First Octet (in binary) are not counted towards `y`

## Subnet Masks

[https://www.youtube.com/watch?v=yLeuGOOrUvo&list=PLSNNzog5eydt_plAtt3k_LYuIXrAS4aDZ&index=4](https://www.youtube.com/watch?v=yLeuGOOrUvo&list=PLSNNzog5eydt_plAtt3k_LYuIXrAS4aDZ&index=4)

- Why do we need them?
    - Indicates which devices are local vs remote.
- How?
    - Compare Device IPs (in binary) where Subnet Mask (in binary) == `1`
    - Subnet Mask indicates which binary values from each device's IP should be used to decide if devices are local/remote.

### Example

- Device `A` Subnet Mask: `255.255.255.0`
- Device `A` IP Address: `10.1.151.2`
- Device `B` IP Address: `10.1.151.3`
- Device `C` IP Address: `64.227.160.23`

Convert Subnet Masks and IPs into Binary

Label|1st Octet|2nd Octet|3rd Octet|4th Octet
-|-|-|-|-
`A`'s Subnet Mask|`11111111`|`11111111`|`11111111`|`00000000`
`A`'s IP Address:|`00001010`|`00000001`|`10010111`|`00000010`
`B`'s IP Address:|`00001010`|`00000001`|`10010111`|`00000011`
Compare `A` to `B`|Matches|Matches|Matches|N/A - Subnet Mask is `0`
`C`'s IP Address:|`01000000`|`11100011`|`10100000`|`00010111`
|Compare `A` to `C`|Doesn't Match|Doesn't Match|Doesn't Match|N/A - Subnet Mask is `0`

- Device `A` and `B` are on **same** network.
- Device `A` and `C` are on **different** networks.

## Remote vs Local Protocol

- Device `A` wants to communicate with Device `B` (local)
    1. `A` uses **ARP** to ask for `B`'s MAC Address via `B`'s IP
        - ARP: [https://www.youtube.com/watch?v=NpiORFxyM4c](https://www.youtube.com/watch?v=NpiORFxyM4c)
    1. `B` replies with `B`'s MAC Address
    1. `A` uses `B`'s MAC to make Frames and communicate with `B`
    - All communication between `A` & `B` via Switch (layer 2 Device)
- Device `A` wants to communicate with Device `C` (remote network)
    1. `A` uses **ARP** to ask for Default Gateway's MAC Address based on Default Gateway's IP address.
    1. Default Gateway replies to `A` with Default Gateway's MAC Address
    1. `A` sends packets (for `C`) to Default Gateway's MAC Address, which delivers `A`'s packets to remote computer `C`

- ARP used in both Remote and Local communications
- IP Address used for remote communications
- MAC Address used for local communications
- Switch (layer 2 device) used for Local communications
- Default Gateway (layer 3 device) used for Remote communications

### Subnet Shorthand

`Shorthand` is the count of `1`'s in the binary form of the subnet mask.

Shorthand|Binary|Decimal
-|-|-
/8|11111111.00000000.00000000.00000000|255.0.0.0
/16|11111111.11111111.00000000.00000000|255.255.0.0
/5|11111000.00000000.00000000.00000000|248.0.0.0
/20|11111111.11111111.11110000.0000|255.255.240.0
/25|11111111.11111111.11111111.10000000|255.255.255.128

## Subnetting Table

|||||||||
|-|-|-|-|-|-|-|-|
Subnet|1|2|4|8|16|32|64|128|256
Host|256|128|64|32|16|8|4|2|1
Subnet Mask|/24|/25|/26|/27|/28|/29|/30|/31|/32

## Example Problems

### Example 1

- IP Address Given: 192.168.1.0
- Hosts Needed: 60
- Subnets Needed: 4

```bash
                      ___
SUBS:            2 |   4 |   8 |  16 | 32 |  64 | 128 | 256
192.168.1.X:   128 |  64 |  32 |  16 |  8 |   4 |   2 |   1
HOST:          256 | 128 |  64 |  32 | 16 |   8 |   4 |   2
                            ^^
CLASS: C                                     {    HOST IPS   }
DEFAULT SNM: /24     192.168.1 { .0    +1 => | .1   <-> .62  | <= -1 .63  }
CUSTOM SNM: /26                { .64   +1 => | .65  <-> .126 | <= -1 .127 } BROAD
HOSTS(#-2): 62             NET { .128  +1 => | .129 <-> .190 | <= -1 .191 } CAST
SUBNETS: 4                     { .192  +1 => | .192 <-> .254 | <= -1 .255 }
                               { .256
                                  ^^^ Invalid
```
