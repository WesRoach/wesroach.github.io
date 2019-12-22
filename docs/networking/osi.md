# OSI Model

[https://www.youtube.com/watch?v=nFnLPGk8WjA](https://www.youtube.com/watch?v=nFnLPGk8WjA)

## Layers

Layer|Name|Mnemonic|Mnemonic|Mnemonic
-|-|-|-|-
7|Application|<b>A</b>ll|<b>A</b>ll|<b>A</b>way
6|Presentation|<b>P</b>eople|<b>P</b>eople|<b>P</b>izza
5|Session|<b>S</b>eem|<b>S</b>hould|<b>S</b>ausage
4|Transport|<b>T</b>o|<b>T</b>ry|<b>T</b>hrow
3|Network|<b>N</b>eed|<b>N</b>ew|<b>N</b>ot
2|Data Link|<b>D</b>omino|<b>D</b>r.|<b>D</b>o
1|Physical|<b>P</b>izza|<b>P</b>epper|<b>P</b>lease

## Physical Path

1. Sending device starts with Application (Layer 7)
1. Data moves **down** Layers from 7 => 1
1. Data moves along Network medium
1. Data moves **up** Layers from 1 => 7 to receiving device

## Logical Path

Layer|Sender|Receiver
-|-|-
Application|Generates Data|Receives Data
Presentation|Encrpyts/Compresses|Decrypts/Decompresses
Session||
Transport|Chops into Segments|Puts segments together
Network|Makes Packets|Opens Packets
Data Link|Makes Frames|Opens Frames
Physical||

## Layer Notes

### Application (Layer 7)

- non-technical
    - About user's application
        - Chrome/Firefox/Outlook/etc
- technically
    - refers to application protocols
        - HTTP, SMTP, POP3, IMAP4, etc
        - facilitate communications between application and operating system
- Application data generated here

### Presentation (Layer 6)

- Provides variety of coding/conversion functions on application data
- Ensures information sent from app layer of client is understood by app layer of server
- trys to translate app data into certain format that every system can understand

### Session (Layer 5)

- Establish, manage, terminate connectiosn between sender and receiver

### Transport (Layer 4)

- Accepts data from Session
- Chops data into smaller segments
- Adds Header information
    - Destination Port Number
    - Source Port Number
    - Sequence Number
        - used by receiver to put segments back in order
- Main Protocols:
    - TCP (dominant protocol)
    - UDP

### Network (Layer 3)

- Primary Protocol: IP
- Takes segments and adds actual header information
    - Senders IP address
    - Receivers IP address
    - Packets are created
- All about IP address and routing

### Data Link (Layer 2)

- More Header information added
    - Adds Frame Header
        - Source MAC Address
        - Desination MAC Address
    - Adds Trailing FCS
- Exists @ NIC

### Physical (Layer 1)

- Accepts Frames from Data Link layers
- Generates Bits
    - Bits made of electrical pulses or light
        - depends on medium (copper vs fiber etc)
