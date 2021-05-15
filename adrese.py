import numpy as np
import copy
from functools import cmp_to_key

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
        last_octet = ip_slices[3].split("/")
        octets = []
        for i in range(3):
            octets += [int(ip_slices[i])]
        octets += [int(last_octet[0])]
        nm = int(last_octet[1])
        return octets, nm

    def add_one(self):
        ip_temp = copy.deepcopy(self)
        if ip_temp.octets[3] < 255:
            ip_temp.octets[3] += 1
            return ip_temp
        else:
            pos = 3
            while pos > 0 and ip_temp.octets[pos] == 255:
                ip_temp.octets[pos] = 0
                pos -= 1
            ip_temp.octets[pos] += 1
            return ip_temp


class Network:
    def __init__(self, NA = None, BA = None, users = None):
        self.NA = NA
        self.BA = BA
        self.users = users
        self.name = ""


    # Metoda pt cand da o adresa daia mare de pe care sa calculezi ip-urile pt
    # toate celelalte retele
    @staticmethod
    def from_random_ip(ip_string):
        ip = IP(ip_string)
        ip_na = IP()
        ip_ba = IP()
        ip_na.nm = ip.nm
        ip_ba.nm = ip.nm
        # mai intai, calculez ip-ul network address ului
        nm_temp = ip.nm
        for ip_octet in ip.octets:
            # calculez octetul cu care sa fac si logic
            if nm_temp >= 8:
                nm_temp -= 8
                octet = 255
            else:
                octet_arr = np.arange(8)
                octet_arr = octet_arr[8 - nm_temp:]
                octet = np.sum(2**octet_arr)
                nm_temp = 0
            ip_na.octets += [ip_octet & octet]
        # acum broadcast address, destul de simplu, pur si simplu fac ce e mai sus,
        # dar pe invers + adaug pe octetii din na
        nm_temp = ip.nm
        for ip_na_octet in ip_na.octets:
            # calculez octetul cu care sa fac si logic
            if nm_temp >= 8:
                nm_temp -= 8
                octet = 0
            else:
                octet_arr = np.arange(8)
                octet_arr = octet_arr[:8 - nm_temp]
                octet = np.sum(2 ** octet_arr)
                nm_temp = 0
            ip_ba.octets += [ip_na_octet + octet]
        return Network(ip_na, ip_ba, 0)

    def __str__(self):
        return "nume: " + self.name + "\n" +\
               "N.A.: " + str(self.NA) + "\n" +\
               "B.A.: " + str(self.BA) + "\n" +\
               "users: " + str(self.users)

    @staticmethod
    def find_closest_two(users):
        pow = 0
        while 2 ** pow < users + 2:
            pow += 1
        return pow

    # network_raw e o lista cu urm elemente
    # [0]: name
    # [1]: users
    # [2]: puterea lui 2 relevanta
    @staticmethod
    def build_from_first_ip(first_ip, network_raw):
        network = Network()
        network.users = network_raw[1]
        network.name = network_raw[0]
        network.NA = first_ip
        network.NA.nm = 32 - network_raw[2]

        nm_temp = network.NA.nm
        ip_ba = IP()
        ip_ba.nm = network.NA.nm
        for ip_na_octet in network.NA.octets:
            # calculez octetul cu care sa fac si logic
            if nm_temp >= 8:
                nm_temp -= 8
                octet = 0
            else:
                octet_arr = np.arange(8)
                octet_arr = octet_arr[:8 - nm_temp]
                octet = np.sum(2 ** octet_arr)
                nm_temp = 0
            ip_ba.octets += [ip_na_octet + octet]
        network.BA = ip_ba
        return network


print("-------------------------------------------")
print("|                                         |")
print("|                                         |")
print("|     Formatul pt IP-uri e a.b.c.d/nm     |")
print("|                                         |")
print("|                                         |")
print("-------------------------------------------")
ip_initial = input("De la ce IP pornim?")
print("Reteaua de la pasul 1 e:")
retea_initiala = Network.from_random_ip(ip_initial)
print(retea_initiala)

n_retele = int(input("Cate retele a dat Dragan?"))
print("-------------------")
retele_date = []
index = 0
while n_retele > 0:
    name = input("cum se numeste?")
    users = int(input("cati useri are?"))
    wifi = input("are wifi?d/n")
    order = index # order e necesar pt retelele de conexiune intre doua routere
    print("-------------------")
    # adaug retelele alea de conexiune
    if index >= 1:
        inter_name = retele_date[index - 1][0] + "-" + name
        inter_users = 2
        inter_wifi = "n"
        retele_date += [(inter_name, inter_users, inter_wifi, order + 1)]
        index += 1
    if wifi == "d":
        inter_name = name + "-" + "WIFI-" + name
        inter_users = 2
        inter_wifi = "n"
        retele_date += [(inter_name, inter_users, inter_wifi, order)] # la wifi vrem acelasi ordin ca reteaua originala, ca sa o ia prima
        index += 1


    retele_date += [(name, users, wifi, order)]

    index += 1
    n_retele -= 1

def cmp_raw_net(x, y): # pe poz 1 e nr de users si pe 3 order pt conexiuni
    if x[1] < y[1]:
        return 1
    if x[1] == y[1]:
        return x[3] < y[3]
    return -1

retele_date = sorted(retele_date, key= cmp_to_key(cmp_raw_net))
networks = []
next_ip = retea_initiala.NA
for (name, users, wifi, order) in retele_date:
    pow = Network.find_closest_two(users)
    networks += [Network.build_from_first_ip(next_ip, (name, users, pow))]
    next_ip = networks[len(networks) - 1].BA.add_one()
for network in networks:
    print(network)
    print("-------------------")