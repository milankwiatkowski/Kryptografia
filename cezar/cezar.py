# MILAN KWIATKOWSKI 292658
import os, argparse

parser = argparse.ArgumentParser(description="Cezar z własnymi flagami")
parser.add_argument("--cezar", "-c", action="store_true", help="Użycie szyfru cezara")
parser.add_argument("--afiniczny", "-a", action="store_true", help="Użycie szyfru afinicznego")
parser.add_argument("--szyfr", "-e", action="store_true", help="Szyfrowanie")
parser.add_argument("--odszyfr", "-d", action="store_true", help="Odszyfrowanie")
parser.add_argument("--crypto", "-j", action="store_true", help="Kryptoanaliza z tekstem jawnym")
parser.add_argument("--kcrypto", "-k", action="store_true", help="Kryptoanaliza wyłącznie w oparciu o kryptogram")
args = parser.parse_args()
def zapisz_do_decrypt(txt):
    if txt is not None:
        decrypt = os.open("decrypt.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
        os.write(decrypt, (str(txt) + "\n").encode("utf-8"))
        os.close(decrypt)
def zapisz_do_decrypt_append(txt):
    if txt is not None:
        decrypt = os.open("decrypt.txt", os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
        os.write(decrypt, (str(txt) + "\n").encode("utf-8"))
        os.close(decrypt)
def zapisz_do_crypto(txt):
    crypto = os.open("crypto.txt", os.O_WRONLY | os.O_CREAT)
    data_write = str(txt)
    os.write(crypto, data_write.encode("utf-8"))
    os.close(crypto)
def cezar_kryptoJawny(tekst_jawny,tekst_zaszyfrowany):
    for i in range(1,26):
        odszyfrowane = cezar_odsz(i,tekst_zaszyfrowany)
        if(tekst_jawny.lower() in odszyfrowane):
            data_write = str(odszyfrowane)
            zapisz_do_decrypt(data_write)
            kfound = os.open("key-found.txt",os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
            data_write = f"{i}"
            os.write(kfound,data_write.encode("utf-8"))
            os.close(kfound)
            return 0
    print("Nie udalo sie znalezc klucza")
def cezar_kryptoGram(tekst):
    for i in range(1,26):
        data = f"Odszyfrowane : {cezar_odsz(i, tekst)} Przesunięcie: {i}\n"
        if(i==1):
            zapisz_do_decrypt(data)
        else:
            zapisz_do_decrypt_append(data)
def cezar_zasz(klucz, tekst):
    szyfr = ""
    tekst = tekst.lower()
    for i in tekst:
        asc = ((ord(i))+(klucz)%26)
        if(asc>122):
            asc = asc-26
        if(i!=" "):
            szyfr += chr(asc)
        else:
            szyfr +=" "
    zapisz_do_crypto(str(szyfr))
    return szyfr
def cezar_odsz(klucz, tekst):
    szyfr = ""
    tekst = tekst.lower()
    for i in tekst:
        asc = ((ord(i))-(klucz)%26)
        if(asc<97):
            asc = 122-(96-asc)
        if(i!=" "):
            szyfr += chr(asc)
        else:
            szyfr +=" "
    return szyfr
def afiniczny_zasz(a,klucz,tekst):
    szyfr = ""
    tekst = tekst.lower()
    for i in tekst:
        asc = ((a * (ord(i)-97)) + klucz)%26 + 97
        if (i != " "):
            szyfr += chr(asc)
        else:
            szyfr += " "
    zapisz_do_crypto(str(szyfr))
    return szyfr
def afiniczny_odsz(a,klucz,tekst):
    szyfr = ""
    tekst = tekst.lower()
    a2 = 0
    for i in range(1,26):
        if((a*i)%26 == 1):
            a2 = i
            break
    for i in tekst:
        asc = a2*((ord(i)-97-klucz))%26+97
        if (i != " "):
            szyfr += chr(asc)
        else:
            szyfr += " "
    return szyfr
def afiniczny_kryptoJawny(tekst_jawny,tekst_zaszyfrowany):
    for i in range(1,26):
        if(i%2!=0 and i%13 != 0):
            for j in range(1, 27):
                odszyfrowane = afiniczny_odsz(i, j, tekst_zaszyfrowany)
                if (tekst_jawny.lower() in odszyfrowane):
                    data_write = str(odszyfrowane)
                    zapisz_do_decrypt(data_write)
                    kfound = os.open("key-found.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
                    data_write = f"a: {i}, b: {j}"
                    os.write(kfound, data_write.encode("utf-8"))
                    os.close(kfound)
                    return 0
    print("Nie udalo sie znalezc klucza")
def afiniczny_kryptoGram(tekst):
    for i in range(1,26):
        if (i % 2 != 0 and i % 13 != 0):
            for j in range(1, 27):
                data = f"Odszyfrowane : {afiniczny_odsz(i, j, tekst)} a: {i} b: {j}"
                if (i == 1 and j == 1):
                    zapisz_do_decrypt(data)
                else:
                    if(i!=1):
                        zapisz_do_decrypt_append(data)
                    else:
                        if(j!=26):
                            zapisz_do_decrypt_append(data)
if args.cezar:
    if args.szyfr:
        fd = os.open("key.txt", os.O_RDONLY)
        data = os.read(fd, os.path.getsize("key.txt"))
        os.close(fd)
        klucze = list(map(int, data.decode().split()))
        if(isinstance(klucze[0],int)==True):
            fd_1 = os.open("plain.txt", os.O_RDONLY)
            data_1 = os.read(fd_1, os.path.getsize("plain.txt"))
            os.close(fd_1)
            data_1_1 = data_1.decode()
            cezar_zasz(klucze[0],data_1_1)
        else:
            print("Błąd - podaj prawidłowy klucz!")
    elif args.odszyfr:
        fd = os.open("key.txt", os.O_RDONLY)
        data = os.read(fd, os.path.getsize("key.txt"))
        os.close(fd)
        klucze = list(map(int, data.decode().split()))
        if (isinstance(klucze[0],int) == True):
            fd_1 = os.open("crypto.txt", os.O_RDONLY)
            data_1 = os.read(fd_1, os.path.getsize("crypto.txt"))
            os.close(fd_1)
            data_1_1 = data_1.decode()
            zapisz_do_decrypt(str(cezar_odsz(klucze[0], data_1_1)))
        else:
            print("Błąd - podaj prawidłowy klucz!")
    elif args.crypto:
        fd_1_2 = os.open("crypto.txt", os.O_RDONLY)
        data_1_2 = os.read(fd_1_2, os.path.getsize("crypto.txt"))
        os.close(fd_1_2)
        data_1_2 = data_1_2.decode("utf-8")
        fd_1_2_1 = os.open("extra.txt", os.O_RDONLY)
        data_1_2_1 = os.read(fd_1_2_1, os.path.getsize("extra.txt"))
        os.close(fd_1_2_1)
        data_1_2_1 = data_1_2_1.decode("utf-8")
        cezar_kryptoJawny(data_1_2_1,data_1_2)
    elif args.kcrypto:
        fd_3 = os.open("crypto.txt", os.O_RDONLY)
        data_3 = os.read(fd_3, os.path.getsize("crypto.txt"))
        os.close(fd_3)
        data_3 = data_3.decode()
        cezar_kryptoGram(data_3)
    else:
        print("Error!")
elif args.afiniczny:
    if args.szyfr:
        fd = os.open("key.txt", os.O_RDONLY)
        data = os.read(fd, os.path.getsize("key.txt"))
        os.close(fd)
        klucze = list(map(int, data.decode().split()))
        fd_1 = os.open("plain.txt", os.O_RDONLY)
        data_1 = os.read(fd_1, os.path.getsize("plain.txt"))
        os.close(fd_1)
        data_1 = data_1.decode()
        afiniczny_zasz(klucze[1],klucze[0],data_1)
    elif args.odszyfr:
        fd = os.open("key.txt", os.O_RDONLY)
        data = os.read(fd, os.path.getsize("key.txt"))
        os.close(fd)
        klucze = list(map(int, data.decode().split()))
        fd_1 = os.open("crypto.txt", os.O_RDONLY)
        data_1 = os.read(fd_1, os.path.getsize("crypto.txt"))
        os.close(fd_1)
        data_1_1 = data_1.decode()
        zapisz_do_decrypt(str(afiniczny_odsz(klucze[1],klucze[0], data_1_1)))
    elif args.crypto:
        fd1 = os.open("crypto.txt", os.O_RDONLY)
        data1 = os.read(fd1, os.path.getsize("crypto.txt"))
        os.close(fd1)
        data1 = data1.decode()
        fd2 = os.open("extra.txt", os.O_RDONLY)
        data2 = os.read(fd2, os.path.getsize("extra.txt"))
        os.close(fd2)
        data2 = data2.decode("utf-8")
        afiniczny_kryptoJawny(data2,data1)
    elif args.kcrypto:
        fd3 = os.open("crypto.txt", os.O_RDONLY)
        data3 = os.read(fd3, os.path.getsize("crypto.txt"))
        os.close(fd3)
        data3 = data3.decode()
        afiniczny_kryptoGram(data3)
    else:
        print("Error!")
else:
    print("Podaj jakiego szyfru chcesz uzyc!")