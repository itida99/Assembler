'''
Group Number: 80
Tutorial Group: 09

Group Member 1:
Aditi Gupta 
2019292

Group Member 2:
Kheya Ghosh Dastidar
2019367
'''
refrenceTable = {'CLA':'0000', 'LAC':'0001', 'SAC':'0010', 'ADD':'0011', 'SUB':'0100', 'BRZ':'0101', 'BRN':'0110', 'BRP':'0111', 'INP':'1000',\
'DSP':'1001', 'MUL':'1010', 'DIV':'1011', 'STP':'1100'}
foundLabel = {}
toBeFound = []
toBefoundVar = []
aliteral = {}
flag = True

class OpcodeType:
    '''
    A class whose each object is an entry in the opcode table
    '''
    def __init__(self,opcode,binEq,operand):
        self.opcode = opcode
        self.binEq = binEq
        self.operand = operand
    def __str__(self):
        return self.opcode+" "+self.binEq+" "+self.operand

class SymbolType:
    '''
    A class whose each object is an entry in the Symbol table
    '''
    def __init__(self,symbol,group,address):
        self.symbol = symbol
        self.group = group
        self.address = address
    def __str__(self):
        return self.symbol+" "+self.group+" "+self.address

def search_operand_in_symbolTable(operand):
    '''
    return boolean whether symbol already exists or not
    written to avoid multiple entries in Symbol table
    '''
    for i in symbolTable:
        if i.symbol == operand:
            return True
    return False

def give_address_from_symbolTable(operand):
    '''
    return address in form of string of symbol 
    if there is no operrand of that particular instruction it returns address '00000000'
    '''
    for i in symbolTable:
        # print(i.symbol,operand)
        if i.symbol == operand:
            # print("okkkk"+operand)
            return i.address
    if operand in aliteral:
        return  aliteral[operand] 
    return "00000000"

def check_valid_name(symbol):
    '''
    return boolean whether variable or label or literal
    has a valid name or not
    '''
    if(symbol=='R1' or symbol == 'R2' or symbol in refrenceTable):
        return False
    if(symbol[0].isalpha()):
        return symbol.isalnum()
    return False

def line_length_1(line,i):
    '''
    handels all the lines who after spliting has length 1
    '''
    global flag
    if(line[0] not in refrenceTable):
        # invalid opcode name
        print("Error: Opcode is not valid in line number",i)
        flag = False
        return
    if(line[0]=='CLA' or line[0]=='STP'):
        opcodeTable.append(OpcodeType(line[0],refrenceTable[line[0]],'NULL'))
        # if(line[0]=='STP' and flag==True):
        #     secondPass()
    else:
        flag = False
        if(line[0] in refrenceTable):
            # incorrect number of opcodes suplied for the operand
            print("Error: Operand not provided in line number",i)
            return 

def line_length_2(line,i):
    '''
    handels all the lines who after spliting has length 2
    '''
    global flag
    if(line[0].find(':')!=-1):
        l = line[0][:line[0].find(':')]
        if(search_operand_in_symbolTable(l) or l in foundLabel):
            # multiple definition of variable 
            print("Error: Multiple definition of a label in line number or label name coincides with a variable",i)  
            flag = False
            return 
        foundLabel[l]="{0:{fill}8b}".format(i, fill='0')
        operand = line[1]
        opcodeTable.append(OpcodeType(line[1],refrenceTable[line[1]],"NULL"))
        return

    if(line[0]=="DS"):
        if line[1].find('=')==-1:
            #Error
            print("Error: Variable not initialised with a value in line number",i)
            flag = False
            return

        line[1]=line[1][:line[1].find('=')]
        if not check_valid_name(line[1]):
            #error
            print("Error: variable name inavlid in line number",i)
            flag = False
            return
        if(search_operand_in_symbolTable(line[1]) and line[1]!='R1' and line[1]!='R2'):
            # multiple definition of variable 
            print("Error: Multiple definition of a variable in line number variable name coincides with a label",i)  
            flag = False
            return 
        if line[1] not in toBefoundVar:
            print("Warning: variable defined but not used in line number",i)
        else:
            address = "{0:{fill}8b}".format(i, fill='0')
            symbolTable.append(SymbolType(line[1],'Variable',address))
            i=0
            length = len(toBefoundVar)  #list length 
            while(i<length):
                if(toBefoundVar[i]==line[1]):
                    toBefoundVar.remove (toBefoundVar[i])	
                    length = length -1  
                    continue
                i = i+1
        return

    elif(line[0]=="DC"):
        if line[1].find('=')==-1:
            #Error
            print("Error: literal not initialised with a value in line number",i)
            flag = False
            return
        literal = line[1][:line[1].find('=')]
        if not check_valid_name(literal):
            #error
            print("Error: literal name inavlid in line number",i)
            flag = False
            return
        value = line[1][line[1].find('=')+1:]
        literalTable[literal]=int(value)
        address = "{0:{fill}8b}".format(i, fill='0')
        aliteral[literal]=address
        return

    if(line[0]=='CLA' or line[0]=='STP'):
        print('Error: More than required operands provided for the opcode in line number',i)
        flag = False
        return

    elif(line[0] not in refrenceTable):
        # invalid opcode name
        print("Error: Opcode is not valid in line number",i)
        flag = False
        return

    else:
        operand = line[1]  
        if not check_valid_name(operand) and operand != 'R1' and operand!='R2':
            #error
            print("Error: variable or label name inavlid in line number",i)
            flag = False
            return 

        if line[0] == 'BRP' or line[0] == 'BRN' or line[0] == 'BRZ':
            opcodeTable.append(OpcodeType(line[0],refrenceTable[line[0]],operand))
            if(operand in foundLabel):
                symbolTable.append(SymbolType(operand,'Label',foundLabel[operand]))
            else:
                toBeFound.append(operand)
        else:
            toBefoundVar.append(operand)
            opcodeTable.append(OpcodeType(line[0],refrenceTable[line[0]],operand))

def line_length_3(line,i):
    '''
    handels all the lines who after spliting has length 3
    '''
    global flag
    if(line[0].find(':')==-1):
        if(line[0] not in refrenceTable):
            # invalid opcode name
            print("Error: Opcode is not valid or label is not assigned properly in line number",i)
            flag = False
            return
        else:
            #error
            flag = False
            print("Error: More than one operands provided with opcode in line number",i)
    else:
        l = line[0][:line[0].find(':')]
        if(search_operand_in_symbolTable(l) or l in foundLabel):
            # multiple definition of variable 
            print("Error: Multiple definition of a label in line number label name coincides with a variable",i)  
            flag = False
            return 
        foundLabel[l]="{0:{fill}8b}".format(i, fill='0')
        operand = line[2]
        opcodeTable.append(OpcodeType(line[1],refrenceTable[line[1]],operand))

def firstPass():
    '''
    impliments first pass of the assembler 
    goes to second pass only if there is no error
    '''
    global flag
    if(len(listOfLines)>256):
        print("Error: memory overflow")
        flag = False
    if listOfLines[-1].find('STP') == -1:
        flag = False
        #error end of program not found
        print("Error: end of program not found")
    adr = "{0:{fill}8b}".format(len(listOfLines)+1, fill='0')
    symbolTable.append(SymbolType('R1','Variable',adr))
    adr = "{0:{fill}8b}".format(len(listOfLines)+2, fill='0')
    symbolTable.append(SymbolType('R2','Variable',adr))
    
    for i in range(len(listOfLines)):
        line = listOfLines[i]
        if line.find(';')==-1:
            if(line == '\n'):
                flag = False
                print('Error: No instruction provided in line number',i) 
                continue
            line = line[:line.find('\n')]
            line = line.split(" ")
        else:
            line = line[:line.find(';')-1]
            line = line.split(" ")   

        if(len(line)==1):
             line_length_1(line,i)

        elif(len(line)==2):
            line_length_2(line,i)

        elif(len(line)==3):
            line_length_3(line,i)

        else:
            #error
            flag = False
            print('Error: More than one operand provide in line number',i) 

    for i in toBeFound:
        if(i in foundLabel):
            symbolTable.append(SymbolType(i,'Label',foundLabel[i]))
        elif(i=="STP"):
            continue
        else:
            #error
            flag = False
            print("Error: Use of undefined label in branch statement, for label",i) 
    temp = 0
    length = len(toBefoundVar)
    while(temp<length):
        if toBefoundVar[temp] in literalTable or toBefoundVar[temp] == "R1" or toBefoundVar[temp] == "R2":
            toBefoundVar.remove(toBefoundVar[temp])
            length=length-1
            continue
        temp+=1
    if(len(toBefoundVar)!=0):
        for i in toBefoundVar:
            print("Error: undefined variable",i,"is used")
            flag = False
    if(flag):
        secondPass()
    print_opcodeTable()
    print()
    print_symbolTable()
    print()
    print_literalTable()
    print()
    print_labelTable()

def secondPass():
    '''
    impliments second pass of assembler
    '''
    binCode=open("BinaryFile.txt","w")
    for i in opcodeTable:
        binCode.write(i.binEq+" ")
        adr = give_address_from_symbolTable(i.operand)
        binCode.write(adr+"\n")
    binCode.close()

def print_opcodeTable():
    '''
    prints the opcode table
    '''
    print("***********************************************")
    print("\t\t OPCODE TABLE")
    print("Opcode"+"\t"" Binary Equivalent"+"\t"+"Operand")
    for i in opcodeTable:
        print(i.opcode+"\t\t"+i.binEq+"\t\t"+i.operand)
    print("***********************************************")

def print_symbolTable():
    '''
    prints the Symbol table
    '''
    print("****************************************")
    print("\t SYMBOL TABLE")
    print("Symbol"+"\t""Type"+"\t\t"+"Adresss")
    for i in symbolTable:
        if(i.group=="Variable"):
            print(i.symbol+"\t"+i.group+"\t"+i.address)
        else:
            print(i.symbol+"\t"+i.group+"\t\t"+i.address)
    print("*****************************************")

def print_literalTable():
    '''
    prints the literal table
    '''
    print("**********************")
    print("   LITERAL TABLE")
    print("Literal"+"\t""Value")
    for literal,value in literalTable.items():
            print(literal+"\t"+str(value))
    print("***********************")

def print_labelTable():
    '''
    prints the label table
    '''
    print("***********************")
    print("   LABEL TABLE")
    print("Label"+"\t""Address")
    for label,address in foundLabel.items():
            print(label+"\t"+address)
    print("***********************")

assemblyCode = open(r"AssemblyCode.txt","r")
listOfLines = assemblyCode.readlines()
assemblyCode.close()

opcodeTable = []
symbolTable = []
literalTable = {}
firstPass()




