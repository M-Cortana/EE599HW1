import BasicClasses as bc
import json
import random as rd

# Defination
Nbit = 512

# Initialization (Load curve data, Load points on the curve)
# The curve data, i.e. a, b, p, G(x, y), are stored in a file called "Curve.json"
CurveFile = open("Curve.json", "r")
CurveJson = CurveFile.read()
CurveData = json.loads(CurveJson)

a = CurveData['a']
b = CurveData['b']
p = CurveData['p']
G = bc.point(CurveData['Gx'], CurveData['Gy'], a, b, p)

# Some points on the curve are stored in a file called "Points.json"
PointsFile = open("Points.json", "r")
PointsJson = PointsFile.read()
PointsData = json.loads(PointsJson)
PointsOnCurve = []
DecipherDict = {}
for i in PointsData:
    DecipherDict[i[0], i[1]] = len(PointsOnCurve)
    PointsOnCurve.append(bc.point(i[0], i[1], a, b, p))

# Encryption
kA = int(input("Input the private key (kA): ")) % p
PA = kA * G     # Calculate public key
msg = input("Input the message you want to encrypt: ")
EncryptedMsg = []
EMFile = open("EncryptedMsg.txt", "w")
for i in msg:
    k = rd.randint(2**Nbit, 2**(Nbit + 4))
    Pm = PointsOnCurve[ord(i) - 32]     # Assume the message don't contain any control characters, so minus 32.
    Cm = [k*G, Pm + k*PA]  
    EncryptedMsg.append(Cm)
    print("{%s, %s}" % (str(Cm[0]), str(Cm[1])), file = EMFile)
print("EncryptedMessage is stored in \"EncryptedMsg.txt\"")

# Decryption
dmsg = ""
for i in EncryptedMsg:
    Pm = i[1] - kA * i[0]
    ordn = DecipherDict[Pm.x.n, Pm.y.n]
    dmsg = dmsg + (chr(ordn + 32))
print("The decrypted message:", msg)