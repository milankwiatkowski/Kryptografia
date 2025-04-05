# MILAN KWIATKOWSKI 292658
import os, argparse

parser = argparse.ArgumentParser(description="Cezar z własnymi flagami")
parser.add_argument("--prep", "-p", action="store_true", help="Przygotowanie pliku")
parser.add_argument("--szyfr", "-e", action="store_true", help="Szyfrowanie")
parser.add_argument("--crypto", "-k", action="store_true", help="Kryptoanaliza wyłącznie w oparciu o kryptogram")
args = parser.parse_args()
if args.prep:
    fd = os.open("orig.txt", os.O_RDONLY)
    data = os.read(fd, os.path.getsize("orig.txt"))
    os.close(fd)
    napisy = str(data.decode())
    tab_wyrazow=[]
    napis=""
    for i in range(len(napisy)):
        if len(napis) < 64:
            napis+=napisy[i]
            if(i==len(napisy)-1):
                for j in range(64-len(napis)):
                    napis+=" "
                tab_wyrazow.append(napis)
                napis=""
        elif len(napis)==64:
            tab_wyrazow.append(napis)
            napis=""
            napis+=napisy[i]
    plain = os.open("plain.txt", os.O_WRONLY | os.O_CREAT, 0o644)
    for elems in tab_wyrazow:
        os.write(plain, (str(elems) + "\n").encode("utf-8"))
elif args.szyfr:
    with open("plain.txt") as plain:
        teksty = [line.rstrip("\n") for line in plain]
    with open("key.txt") as key:
        klucz = [line.rstrip("\n") for line in key]
        klucz=klucz[0]
    tab=[]
    for i in range(len(teksty)):
        napis=""
        for j in range(len(klucz)):
            org_zamieniony = ord(teksty[i][j])
            key_zamieniony = ord(klucz[j])
            xor = org_zamieniony ^ key_zamieniony
            znak = f"0x{(xor << 13):08x}/"
            napis+=znak
        tab.append(napis)
        napis=""
    crypto = os.open("crypto.txt", os.O_WRONLY | os.O_CREAT, 0o644)
    for elems in tab:
        os.write(crypto, (str(elems) + "\n").encode("utf-8"))
elif args.crypto:
    with open("crypto.txt") as crypto:
        zaszyfrowane = [line.rstrip("\n") for line in crypto]
    bajty_int=[]
    for i in range(len(zaszyfrowane)):
        zaszyfrowane[i] = zaszyfrowane[i].split("/")
        zaszyfrowane[i] = [b for b in zaszyfrowane[i] if b]
        bajty_int.append([int(b, 16) >> 13 for b in zaszyfrowane[i]])
    decrypt = [["_" for _ in range(64)] for _ in range(len(zaszyfrowane))]
    podejrzenia=[]
    for i in range(len(zaszyfrowane)):
        linia = []
        for k in range(len(zaszyfrowane[i])):
            linia.append({})
        podejrzenia.append(linia)
    for i in range(len(bajty_int)):
        for j in range(len(bajty_int)):
            if i != j:
                xor_linia = [x ^ y for x, y in zip(bajty_int[i], bajty_int[j])]
                for k in range(len(xor_linia)):
                    if (xor_linia[k] & 0b11100000 == 0b01000000):
                        litera = bajty_int[i][k] ^ 32
                        if (96 < litera < 123):
                            if podejrzenia[i][k].get(chr(litera)):
                                podejrzenia[i][k][chr(litera)] += 1
                            else:
                                podejrzenia[i][k][chr(litera)] = 1
                        else:
                            litera = bajty_int[j][k] ^ 32
                            if (96 < litera < 123):
                                if podejrzenia[i][k].get(chr(litera)):
                                    podejrzenia[i][k][chr(litera)] += 1
                                else:
                                    podejrzenia[i][k][chr(litera)] = 1
    for i in range(len(podejrzenia)):
        print(podejrzenia[i])
        # for (litera, liczba) in podejrzenia[i].items():
        #     faworyt="_"
        #     najwiecej=0
        #     print(litera,liczba)