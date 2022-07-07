import pandas as pd
import xml.etree.ElementTree as ET
import glob
import csv
folder='C:\Users\TECH SENATI\Ciencia de Datos_Python\VRP\DataSet_en_XML\A-n32-k5.xml'
allFiles = glob.glob(folder)

def f(elem, result):
    result[elem.tag] = elem.text
    cs = elem.getchildren()
    for c in cs:
        result = f(c, result)
    return result

for file in allFiles:
    xmllist = [file]
    for xmlfile in xmllist:
        tree = ET.parse(xmlfile)
        root = tree.getroot()

    d = f(root, {})
    df = pd.DataFrame(d, index=['values'])

print (df)