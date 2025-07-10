import os

varsdict = {}
labelsdict = {}
mode = "file"
programText = []
programCounter = 1

def Error(code, message, line):
    if line:
        print("On line {}:".format(line))
    print("ERROR Program exited with code {}.".format(code))
    print(message)
    input()
    quit()

def getVar(name, lineNum):
    if name in varsdict:
        return varsdict[name]
    return ""

def EvalText(string, lineNumber):
    components = str.split(string, " ")
    finalString = ""
    subEvalString = ""
    subEvallayers = 0
    for v in components:
        if v == "":
            continue
        elif v == "[":
            if subEvallayers > 0:
                subEvalString += "[ "
            else:
                subEvalString = ""
            subEvallayers += 1
        elif v == "]":
            subEvallayers -= 1
            if subEvallayers == 0:
                finalString += EvalText(subEvalString, lineNumber)
            elif subEvallayers > 0:
                subEvalString += " ]"
            else:
                Error(4, "Invalid text string - attempted to close string evaluation without opening one", lineNumber)
        elif subEvallayers > 0:
            if v == "-":
                subEvalString += " "
            elif v == "in":
                subEvalString += input()
            elif v.startswith("-"):
                subEvalString += v.removeprefix("-")
            else:
                subEvalString += getVar(v, lineNumber)
        else:
            if v == "-":
                finalString += " "
            elif v == "in":
                finalString += input()
            elif v.startswith("-"):
                finalString += v.removeprefix("-")
            else:
                finalString += getVar(v, lineNumber)
    
    if subEvallayers > 0:
        Error(5, "Invalid text string - unclosed string evaluation", lineNumber)
    

    return finalString


def InterpretInc(LineString, LineNum):
    varToInc = str.lstrip(LineString.removeprefix("+ "), " ")
    varToInc = EvalText(varToInc, LineNum)
    if varToInc in varsdict:
        if str.isnumeric(varsdict[varToInc]):
            varsdict[varToInc] = str(int(varsdict[varToInc]) + 1)

def InterpretDec(LineString, LineNum):
    varToDec = str.lstrip(LineString.removeprefix("- "), " ")
    varToDec = EvalText(varToDec, LineNum)
    if varToDec in varsdict:
        if str.isnumeric(varsdict[varToDec]):
            varsdict[varToDec] = str(int(varsdict[varToDec]) - 1)

def InterpretJump(LineString, LineNum):
    jumpPoint = str.lstrip(LineString.removeprefix("! "), " ")
    jumpPoint = EvalText(jumpPoint, LineNum)
    if jumpPoint in labelsdict:
        return labelsdict[jumpPoint]
    return LineNum + 1

def specialAssignments(VarName, NewValue, LineNum):
    if VarName == "out":
        print(NewValue)
        return True
    return False


def InterpretAssignment(LineString, LineNum):
    equationSides = str.split(LineString, " = ")
    assignTo = EvalText(equationSides[0], LineNum)
    assignVal = EvalText(equationSides[1], LineNum)
    if specialAssignments(assignTo, assignVal, LineNum):
        return
    varsdict[assignTo] = assignVal

def InterpretLine(LineString, LineNum):
    if str.startswith(LineString, "! "):
        return InterpretJump(LineString, LineNum)
    elif str.startswith(LineString, "+ "):
        InterpretInc(LineString, LineNum)
    elif str.startswith(LineString, "- "):
        InterpretDec(LineString, LineNum)
    elif str.find(LineString, " = ") != -1:
        InterpretAssignment(LineString, LineNum)
    return LineNum + 1



def FindLabels():
    for index, line in enumerate(programText):
        if line.startswith(": "):
            labelName = line.removeprefix(": ").lstrip(" ")
            if labelName.count(" ") > 0:
                Error(2, "Invalid label name - must not contain spaces", index)
            if labelName in labelsdict:
                Error(3, "Invalid label name - labels may only be defined once", index)    
            labelsdict[labelName] = index

print("Enter ""file"" to run a program from a file, otherwise programs will run from the input stream")
mode = input()

if mode == "file":
    os.chdir(os.path.dirname(os.path.abspath(__file__))) # set working directory to this file
    print("Enter program file (with extenstion): ")
    fileName = input()
    file = open(fileName)
    programText = str.splitlines(file.read())
    programText.insert(0, "") # add an empty line so all line numbers are correct
    file.close()
else:
    print("enter program into terminal, use ""EXIT"" to terminate program")
    programText = [""]
    lineIn = ""
    while lineIn != "EXIT":
        lineIn = input()
        programText.append(lineIn)

FindLabels()
print("Press Enter to run")
input()
print()

while programCounter < len(programText):
    programCounter = InterpretLine(programText[programCounter], programCounter)


print("Done!")
input() # pause at end of program
