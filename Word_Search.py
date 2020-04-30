def word_search(doc_list, keyword):
    keyword=keyword.lower()
    l=len(keyword)
    c=0
    f=[]
    v=0
    for i in range(len(doc_list)):
        a=doc_list[i]
        a=a.split()
        for j in range(len(a)):
            c=0
            v=0
            for p in range(len(a[j])):
                b=a[j]
                if b[p]=="," or b[p]==".":
                    v=len(a[j])-1
            if l==len(a[j]) or l==v:
                for k in range(l):
                    b=a[j]
                    b=b.lower()
                    if keyword[k]==b[k]:
                        c+=1
                    if c==l:
                        if len(f)==0:
                            f.append(i)
                        if len(f)!=0 :
                            for z in range(len(f)):
                                if f[z]==i:
                                    break
                                else:
                                    f.append(i)

    return f


def multi_word_search(doc_list, keywords):
    keyword_to_indices = {}
    for keyword in keywords:
        keyword_to_indices[keyword] = word_search(doc_list, keyword)
    return keyword_to_indices