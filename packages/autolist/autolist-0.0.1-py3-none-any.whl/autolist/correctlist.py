#AutoLIST
ListOrString = None
def _first_value(data: ListOrString, m) -> str:
    if isinstance(data, list):
        return list(data[m])
    else:
        return list(data)


ptslist = []
def autocorrect_list(string : str, li : list):
    listlen = len(li)
    strlen = len(string)
    for j in range(0, listlen):
        pts = 0
        listring = li[listlen-1]
        for i in range(0, listlen):
            a = _first_value(li, j)[i]
            b = _first_value(string, j)[i]
            if a == b:
                pts += 2
            else:
                pts -= 1
        ptslist.append(pts)
    maxindex = ptslist.index(max(ptslist))
    no = li[maxindex]
    return no
