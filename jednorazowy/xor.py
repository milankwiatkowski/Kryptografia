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
# elif args.crypto:
