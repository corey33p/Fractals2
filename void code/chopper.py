class Parser:
    def __init__(self,in_string=None):
        if in_string != None: 
            self.in_string = in_string
            self.parser()
        else:
            self.in_string, self.parts = None, None
    def _print(self, d=None, indent=0, parent=''):
        if d == None: d = self.parts
        if parent == '': print("\n")
        if indent == 0: print("|----------|")
        for key, value in d.items():
            for _ in range(indent): print("-",end="")
            print(parent)
            if isinstance(value[1], dict):
                parent=value[0]
                self._print(value[1], indent+1, parent)
            else:
                print(str(value))
        if indent == 0: print("|----------|")
        print("\n")
    def parser(self,in_string=None):
        if in_string != None:
            self.in_string = in_string
            self.parts = self.recursive_parser(self.in_string)
        else:
            if self.in_string != None:
                self.parts = self.recursive_parser(self.in_string)
    def recursive_parser(self,input_string,parent="+"):
        # if not verify_string(convert_string(input_string)): return
        print("input_string: " + input_string)
        input_string = input_string.replace(" ","")
        splitters = ("+", "-", "/", "^",'*')
        chunkable = ('0','1','2','3','4','5','6','7','8','9','0','C','Z')
        functions = ('sin','cos','tan','asin','acos','atan','ln','log')
        dictionary_of_chunks = {}
        chunk_complete = False
        chunk = ''
        expression_A = ''
        parenthesis = 0
        previous_splitter = parent
        i = 0
        debug = False
        while i < len(input_string):
            character = input_string[i]
            if debug: print(character, end="; ")
            if character == "(":
                if debug: print("check 1")
                parenthesis += 1
                chunk += character
                i += 1
            # elif character == "_":
                # if debug: print("check 2")
                # dictionary_of_chunks[len(dictionary_of_chunks)] = [previous_splitter, chunk]
                # break
            elif parenthesis > 0: 
                if debug: print("check 3")
                if (character == ")"):
                    if debug: print("check 3.5")
                    parenthesis -= 1
                chunk += character
                i += 1
            elif character in chunkable:
                if debug: print("check 4")
                chunk += character
                i += 1
            elif (character in splitters) and (parenthesis == 0):
                if debug: print("check 5")
                dictionary_of_chunks[len(dictionary_of_chunks)] = [previous_splitter, chunk]
                previous_splitter = character
                chunk = ''
                i += 1
            elif input_string[i:i+2] in functions:
                if debug: print("check 6")
                chunk += input_string[i:i+2]
                i += 2
            elif input_string[i:i+3] in functions:
                if debug: print("check 7")
                chunk += input_string[i:i+3]
                i += 3
            elif input_string[i:i+4] in functions:
                if debug: print("check 8")
                chunk += input_string[i:i+4]
                i += 4
            else: 
                if debug: print("check 9")
                i += 1
        if parenthesis == 0:
            dictionary_of_chunks[len(dictionary_of_chunks)] = [previous_splitter, chunk]
        fully_chunked = False
        # pretty(dictionary_of_chunks)
        while not fully_chunked:
            fully_chunked = True #tentatively set to true
            for key, value in dictionary_of_chunks.items(): #to handle chunks which can be chunked further
                if debug: print("value: " + str(value))
                # value[1] = value[1].replace("_","")
                if "(" in dictionary_of_chunks[key][1]:
                    fully_chunked = False
                    if dictionary_of_chunks[key][1][:2] in functions:
                        if debug: print("check 10")
                        operator = dictionary_of_chunks[key][1][:2]
                        chunk = dictionary_of_chunks[key][1][3:len(dictionary_of_chunks[key][1])-1]
                        dictionary_of_chunks[key][1] = self.recursive_parser(chunk,parent=operator) #recursive call on parenthetic part without the parenthesis
                    elif dictionary_of_chunks[key][1][:3] in functions:
                        if debug: print("check 11")
                        operator = dictionary_of_chunks[key][1][:3]
                        chunk = dictionary_of_chunks[key][1][4:len(dictionary_of_chunks[key][1])-1]
                        dictionary_of_chunks[key][1] = self.recursive_parser(chunk,parent=operator)
                    elif dictionary_of_chunks[key][1][:4] in functions:
                        if debug: print("check 12")
                        operator = dictionary_of_chunks[key][1][:4]
                        chunk = dictionary_of_chunks[key][1][5:len(dictionary_of_chunks[key][1])-1]
                        dictionary_of_chunks[key][1] = self.recursive_parser(chunk,parent=operator)
                    else:
                        if debug: print("check 13")
                        chunk = dictionary_of_chunks[key][1][1:len(dictionary_of_chunks[key][1])-1]
                        dictionary_of_chunks[key][1] = self.recursive_parser(chunk)
                    break
        return dictionary_of_chunks
    def __len__(self):
        if self.parts != None:
            count = 0
            for key, value in self.parts.items():
                if isinstance(value[1], dict):
                    count += 2 # for parenthesis
                    if not (key == 0 and value[0] == '+'):
                        count += len(value[0]) # for the operator
                    temp = Parser()
                    temp.parts = value[1]
                    count += len(temp) # for the value
                else:
                    if not (key == 0 and value[0] == '+'): count += len(value[0])
                    count += len(value[1])
            return count
        else: return 0

a=["((1+C)*Z-C*Z^2)*((Z+sin(Z))^2+C)",
    "Z+sin(Z)+C",
    "sin(Z)",
    "sin(Z)+37",
    "Z+(C+3)",
    "(Z^2+C)/(ln(Z)-Z)"]
print("len(): " + str(len(a[0])))
a=Parser(a[0])
# a.parser()
print("\n\n\n\n")
for line in a.parts:
    print(a.parts[line])
print("len(a): " + str(len(a)))


