import sys

file = sys.argv[1]

f = open(file)
table = f.read()
f.close()

table = table.split("\n")
for x in range(len(table)):
    table[x] = table[x].split("\t")

class Ability_Type:
    def __init__(self,name,d,f,a,p,m,description):
        self.name = name
        self.sources = []
        if(d == "TRUE"): self.sources.append("d")
        if(f == "TRUE"): self.sources.append("f")
        if(a == "TRUE"): self.sources.append("a")
        if(p == "TRUE"): self.sources.append("p")
        if(m == "TRUE"): self.sources.append("m")
        self.description = description
        self.subtypes = []

    def subtype(self, Subtype):
        self.subtypes.append(Subtype)

    def print(self):
        string = self.name + " ("
        for letter in self.sources: string += letter + ", "
        string = string[:len(string)-2] + ")\n"
        if(len(self.description)>0): string += self.description + "\n"
        for subtype in self.subtypes:
            string += subtype.string()
        print(string)

    def gmbinder(self):
        string = "#### " + self.name + " &nbsp;<span class=\"div-sh4\">"
        for letter in self.sources: string += letter + " "
        string = string[:len(string)-1] + "</span>\n"
        if(len(self.description)>0): string += self.description + "\n"
        string += "___\n"
        for subtype in self.subtypes:
            string += subtype.gmbinder()
        return string


class Subtype:
    def __init__(self,name,costSP,typeSP,repeatable,costAP,costAPC,description):
        self.name = name
        if(len(costSP)>0): self.costSP = int(costSP)
        else: self.costSP = 0
        self.typeSP = typeSP
        if(len(costAP)>0): self.costAP = int(costAP)
        else: self.costAP = 0
        if(len(costAPC)>0): self.costAPC = int(costAPC)
        else: self.costAPC = 0
        if(repeatable == "TRUE"): self.repeatable = True
        else: self.repeatable = False
        self.description = description
        self.modifiers = []
    
    def modifier(self,name,costSP,typeSP,repeatable,costAP,costAPC,description):
        self.modifiers.append(Modifier(name,costSP,typeSP,repeatable,costAP,costAPC,description))

    def string(self):
        symbol = {"Permanent":"■","Transient":"□","Either":"◩","AP":"♢"}
        string = "\t"
        for _ in range(self.costSP): string += symbol[self.typeSP]
        string += " " + self.name
        for _ in range(self.costAP): string += symbol["AP"]
        if(self.costAPC > 0): 
            string += " ("
            for _ in range(self.costAPC): string += symbol["AP"]
            string += ")"
        string += ": " + self.description + "\n"
        for modifier in self.modifiers:
            string += modifier.string()
        return string

    def gmbinder(self):
        symbol = {"Permanent":"■","Transient":"□","Either":"◩","AP":"♢"}
        string = "- "
        for _ in range(self.costSP): string += symbol[self.typeSP]
        if(self.repeatable): string += "\*"
        string += " **" + self.name + " "
        for _ in range(self.costAP): string += symbol["AP"]
        if(self.costAPC > 0): 
            string += "("
            for _ in range(self.costAPC): string += symbol["AP"]
            string += ")"
        string += ":** " + self.description.replace("*","\*") + "\n"
        for modifier in self.modifiers:
            string += modifier.gmbinder()
        return string
        
class Modifier:
    def __init__(self,name,costSP,typeSP,repeatable,costAP,costAPC,description):
        self.name = name
        if(len(costSP)>0): self.costSP = int(costSP)
        else: self.costSP = 0
        self.typeSP = typeSP
        self.repeatableAP = False
        if(len(costAP)>0): 
            if("*" in costAP):
                self.repeatableAP = True
                self.costAP = int(costAP[costAP.index("*")+1:])
            else: self.costAP = int(costAP)
        else: self.costAP = 0
        if(len(costAPC)>0): self.costAPC = int(costAPC)
        else: self.costAPC = 0
        if(repeatable == "TRUE"): self.repeatable = True
        else: self.repeatable = False
        self.description = description
    
    def string(self):
        symbol = {"Permanent":"■","Transient":"□","Either":"◩","AP":"♢"}
        string = "\t\t"
        for _ in range(self.costSP): string += symbol[self.typeSP]
        string += " " + self.name
        for _ in range(self.costAP): string += symbol["AP"]
        if(self.costAPC > 0): 
            string += " ("
            for _ in range(self.costAPC): string += symbol["AP"]
            string += ")"
        string += ": " + self.description + "\n"
        return string

    def gmbinder(self):
        symbol = {"Permanent":"■","Transient":"□","Either":"◩","AP":"♢"}
        string = "- &nbsp;&nbsp;"
        for _ in range(self.costSP): string += symbol[self.typeSP]
        if(self.repeatable): string += "\*"
        string += " " + self.name
        if(self.repeatableAP): string += "\*"
        if(self.costAP > 0): string += " "
        for _ in range(self.costAP): string += symbol["AP"]
        if(self.costAPC > 0): 
            string += " ("
            for _ in range(self.costAPC): string += symbol["AP"]
            string += ")"
        string += ": " + self.description.replace("*","\*") + "\n"
        return string

table.pop(0)
abilities = []
while(len(table)>0):
    if(len(table[0][0]) > 1):
        abilities.append(Ability_Type(table[0][0],table[0][1],table[0][2],table[0][3],table[0][4],table[0][5],table[0][13]))
        table.pop(0)
        while(len(table[0][6]) > 0):
            subtype = Subtype(table[0][6],table[0][8],table[0][9],table[0][10],table[0][11],table[0][12],table[0][13])
            table.pop(0)
            while(len(table[0][7]) > 0):
                subtype.modifier(table[0][7],table[0][8],table[0][9],table[0][10],table[0][11],table[0][12],table[0][13])
                table.pop(0)
            abilities[len(abilities)-1].subtype(subtype)
    else: table.pop(0)

for ability in abilities:
    print(ability.gmbinder())