import textdistance as td

def match(resume, job_des):
    j = td.jaccard.similarity(resume, job_des)
    #print(f"\n\nMATCH-jaccard----------------> :{j}\n\n")
    s = td.sorensen_dice.similarity(resume, job_des)
    #print(f"\n\nMATCH-sorsen----------------> :{s}\n\n")
    c = td.cosine.similarity(resume, job_des)
    #print(f"\n\nMATCH-cosine----------------> :{c}\n\n")
    o = td.overlap.normalized_similarity(resume, job_des)
    #print(f"\n\nMATCH-overlap----------------> :{o}\n\n")
    total = (j + s + c + o) / 4
    # total = (s+o)/2
    return total * 100
