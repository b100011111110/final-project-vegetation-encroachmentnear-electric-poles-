from DataStoreSet import DataStore

data = DataStore()
data.import_from_csv('./data/data.csv')

addData = 1
while addData == 1:
    place = input('enter Place')
    tll = float(input('top left lat'))
    tlo = float(input('top left lon'))
    brl = float(input('bottom right lat'))
    bro = float(input('bottom right lon'))
    pal = float(input('point a lat'))
    pao = float(input('point a lon'))
    pbl = float(input('point b lat'))
    pbo = float(input('point b lon'))
    tl = (tll,tlo)
    br = (brl,bro)
    pa = (pal,pao)
    pb = (pbl,pbo)
    data.add_value(place,tl,br,pa,pb)
    print(data.data)
    addData = 1 if input('do you want to continue').strip().lower() in ['y','yes'] else 0

data.export_to_csv('./data/data.csv')