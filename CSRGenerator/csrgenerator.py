#!/usr/bin/python
from OpenSSL import crypto
import os
import sys
import datetime

#Variables
TYPE_RSA = crypto.TYPE_RSA
TYPE_DSA = crypto.TYPE_DSA
HOME = os.getenv("HOME")
now = datetime.datetime.now()
d = now.date()

#Pull these out of scope
cn = input("Enter FQDN: ")
key = crypto.PKey()
keypath = HOME + "/" + cn + '-' + str(d) + '.key'
csrpath = HOME + "/" + cn + '-' + str(d) + '.csr'

#Generate the key

def generatekey():

    if os.path.exists(keypath):
        print ("Certificate file exists, aborting.")
        print (keypath)
        sys.exit(1)
    #Else write the key to the keyfile
    else:
        print("Generating Key Please standby")
        key.generate_key(TYPE_RSA, 2048)
        f = open(keypath, "wb")
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
        f.close()

#return key

generatekey()

def generatecsr():

    print ("How would you like to generate csr data?\n" \
          "1) Default BT-Salesforce CSR\n" \
          "2) Specify your own \n" )
    option = int(input("Choose (1/2): "))
    if option == 1:
        c = 'US'
        st = 'California'
        l = 'San Francisco'
        o = 'Salesforce.com Inc.'
        ou = 'BT'
        em = 'bt-networking@salesforce.com'
    elif option == 2:
        c = input('Enter your country(ex. US): ')
        st = input("Enter your state(ex. California): ")
        l = input("Enter your location(City): ")
        o = input("Enter your organization: ")
        ou = input("Enter your organizational unit(ex. BT): ")
        em = input("Enter Email: ")
    else:
        print ('Wrong Choice')
        sys.exit(1)
 
    req = crypto.X509Req()
    req.get_subject().C = c
    req.get_subject().ST = st
    req.get_subject().L = l
    req.get_subject().O = o
    req.get_subject().OU = ou
    req.get_subject().CN = cn
    req.get_subject().emailAddress = em
    req.set_pubkey(key)
    req.sign(key, "sha256")

    if os.path.exists(csrpath):
        print ("Certificate File Exists, aborting.")
        print (csrpath)
    else:
        f = open(csrpath, "wb")
        f.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, req))
        f.close()
        print("Success")

generatecsr()

print ("Key Stored Here :" + keypath)
print ("CSR Stored Here :" + csrpath)
