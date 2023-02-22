import sys

n = ""
c = ""
mode = True
s = 0
for line in sys.stdin:
    for char in line:
        try:
            int(char)
            n += char
        except ValueError:
            if not mode:
                n = ""
                
            if n != "": 
                n = int(n)
                s += n
                n = ""

            c += char
            if "=" in c:
                print("Resultado : " + str(s))
                c = ""

            if "on" in c or "On" in c or "oN" in c or "ON" in c:
                mode = True
                c = ""

            elif "OFF" in c or "OFf" in c or "OfF" in c or "Off" in c or "oFF" in c or "oFf" in c or "ofF" in c or "off" in c:
                mode = False
                c = ""

