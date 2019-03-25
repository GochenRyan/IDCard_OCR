file = open(r'datas\ChineseNations.txt','r')
s = file.read()
nations = s.split(',')
for nation in nations:
    print nation