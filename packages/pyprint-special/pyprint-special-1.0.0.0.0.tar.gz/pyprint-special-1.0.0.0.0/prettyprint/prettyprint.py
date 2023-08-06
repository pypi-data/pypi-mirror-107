class prettyprint:
    def __init__(self,ml):
        l = len(ml[0])
        for i in ml:
            if len(i) != l:
                raise ValueError(f"Must be 2 dimension list with equal length in nestedlist\nAccording to your slist {ml} are not equal")
        self.l = ml
    def prettyprint(self):
        length = []
        l = 0
        m = [0]*len(self.l[0])
        for i in range(len(self.l)):
            for j in range(len(self.l[i])):
                self.l[i][j] = str(self.l[i][j])
                l+=len(self.l[i][j])
                if len(self.l[i][j])>m[j]:
                    m[j]=len(self.l[i][j])
            length.append(l)
            l = 0
        string = ""
        for i in range(len(self.l)):
            string+=" "+"-"*(sum(m)+(5*len(self.l[0]))-1)+"\n|  "
            for j in range(len(self.l[i])):
                string+=" "*(m[j]  - len(self.l[i][j]))
                string+=(self.l[i][j])
                string+="  |  "
            string+="\n"
        string+=" "+"-"*(sum(m)+(5*len(self.l[0]))-1)
        return string
