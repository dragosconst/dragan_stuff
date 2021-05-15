import numpy as np

# clasa asta IP e slightly diferita de cea din adrese, aici nu mai folosesc network mask
class IP:
    def __init__(self, ip=None):
        if ip is not None:
            self.octets, self.nm = IP.from_string(ip)
        else:
            self.octets, self.nm = [], None
    def __str__(self):
        retval = ""
        pos = 0
        for octet in self.octets:
            retval += str(octet)
            if pos == len(self.octets) - 1:
                retval += "/"
            else:
                retval += "."
            pos += 1
        retval += str(self.nm)
        return retval

    # Formatul acceptat momentan (si pe veci probabil)
    # e a.b.c.d/nm, unde a,b,c,d sunt numere intre 0 si 255
    # si nm e network mask sau cum ii zice
    # Orice alt format crapa si nu am chef sa scriu exception handling
    @staticmethod
    def from_string(ip):
        ip_slices = ip.split(".")
        # ip_slices are 4 componente, ultimul are si network mask
        octets = []
        for i in range(4):
            octets += [int(ip_slices[i])]
        nm = None
        return octets, nm

# nm e un int intre 0-32, returneaza network mask ul in forma de ip
def mask_to_ip(nm):
    octets = np.empty(4)
    index = 0
    while index < 4:
        if nm >= 8:
            octets[index] = 255
            nm -= 8
        else:
            octet_arr = np.arange(8)
            octet_arr = octet_arr[8 - nm:]
            octet = np.sum(2**octet_arr)
            octets[index] = octet
            nm = 0
        index += 1
    octets = octets.astype(int)
    for i in range(octets.shape[0]):
        if i != len(octets) - 1:
            print(str(octets[i]) + ".", end="")
        else:
            print(octets[i])

# ia un string ip si da inapoi masca ca int
def ip_to_mask(ip):
    ip_add = IP(ip)
    nm = 0
    for octet in ip_add.octets:
        nm += bin(octet).count('1')
    print(nm)

mask_to_ip(20)
ip_to_mask("255.255.240.0")