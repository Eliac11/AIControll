import json
import os

def GetAllPos():
    P ={}
    files = os.listdir("Poses")

    for i in files:
        with open(f"Poses/{i}", 'r',encoding="utf-8") as f:
             P[i[:-4]] = json.load(f)

    return P


def ComparePoses(p1:dict,p2:dict):
    
    znach = []

    for i in p1.keys():
        
        try:
            for i2 in p1[i].keys():
                d = abs(p1[i][i2] - p2[i][i2])
                if d == 0:
                    znach += [0]
                    continue
                znach += [1/d]
        except KeyError:
            znach += [0]


    return min(znach)
    



if __name__ == "__main__":
    print(GetAllPos())
    