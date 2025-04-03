# MILAN KWIATKOWSKI 292658
import os, argparse

parser = argparse.ArgumentParser(description="Cezar z własnymi flagami")
parser.add_argument("--prep", "-p", action="store_true", help="Użycie szyfru cezara")
parser.add_argument("--szyfr", "-e", action="store_true", help="Szyfrowanie")
parser.add_argument("--cryptojawny", "-k", action="store_true", help="Kryptoanaliza wyłącznie w oparciu o kryptogram")
args = parser.parse_args()
# if args.p:
#