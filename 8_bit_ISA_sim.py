def saveJumpLabel(asm, labelIndex, labelName, labelAddr):
    lineCount = 0
    for line in asm:
        line = line.replace(" ", "")
        if (line.count(":")):
            labelName.append(line[0:line.index(":")])  # append the label name
            labelIndex.append(lineCount)  # append the label's index\
            labelAddr.append(lineCount * 4)
            # asm[lineCount] = line[line.index(":")+1:]
        lineCount += 1
    for item in range(asm.count('\n')):  # Remove all empty lines '\n'
        asm.remove('\n')


def regNameInit(regName):
    i = 0
    while (i <= 4):
        regName.append(str(i))
        i = i + 1
    regName.append('lo')
    regName.append('hi')

def splitText(text):
    return text.split("\n")

def readIn(s):
    text = ""
    with open(s, "r") as f:
        for line in f:
            if line != "\n":
                text += line

    return text


def main():
    # starting with 100 spots in MEM
    MEM = [0] * 256
    labelIndex = []
    labelName = []
    labelAddr = []
    regName = []
    PC = 0
    regNameInit(regName)
    regval = [0] * 6  # 0-4, lo and hi
    LO = 5
    HI = 6
    good_in = False


    #TODO: update op code to same bits
    initli = "00"
    initui = "01"  # has to be checked after ld and st(last ones)
    srl = "0010"
    sinc2b = "0011"
    l8 = "0100"
    s8 = "0101"
    add = "0110"
    addiu = "0111"
    and1 = "1000"
    xor = "1001"
    andi = "1010"
    bezR0 = "1011"
    jmp = "1100"
    Fold = "1101"
    branch = "1110"

    while (good_in == False):

        file_Name = input("Please type file name, enter for default, or q to quit:\n")

        if (file_Name == "q"):
            print("Bye!")
            return
        if (file_Name == ""):
            file_Name = "test.asm"
        try:
            f = open(file_Name)
            f.close()
            good_in = True
        except FileNotFoundError:
            print('File does not exist')

    f = open("output.txt", "w+")

    text = readIn(file_Name)
    t = splitText(text)

    lineCount = 0
    while (lineCount < len(t)):

        line = t[lineCount]


        f.write('------------------------------ \n')
        if (not (':' in line)):
            f.write('MIPS Instruction: ' + line + '\n')


        if(line[0:4] == srl):
            PC += 4
            S = int(line[7:8])
            regval[int(line[5:6])] = regval[int(line[5:6])] >> S


        elif (line[0:4] == sinc2b):
            PC += 4
            X = regval[int(line[5:6])]
            MEM[regval[int(line[7:8])]] = X
            f.write('Operation: MEM[$' + line[7:8] + '] = ' + line[5:6] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')


        elif(line[0:4] == add):
            PC += 4
            regval[int(line[5:6])] += regval[int(line[7:8])]

        # addiu
        elif (line[0:4] == addiu):
            PC += 4
            regval[int(line[5:6])] = regval[int(line[5:6])] + int(line[7:8])
            f.write('Operation: MEM[$' + line[1] + '] = ' + line[0] + '; ' + '\n')

        #andi
        elif(line[0:4] == andi):
            PC += 4
            regval[int(line[5:6])] = regval[int(line[5:6])] & int(line[7:8])
            f.write('Operation: MEM[$' + line[5:6] + '] = ' + line[7:8] + '; ' + '\n')

        # xor
        elif (line[0:4] == xor):
            PC += 4
            regval[int(line[5:6])] = regval[int(line[5:6])] ^ regval[int(line[7:8])]

        elif (line[0:4] == l8):
            PC += 4

            regval[int(line[4:6], 2)] = MEM[regval[int(line[6:8], 2)]]
            f.write('Operation: $' + str(int(line[5:6], 2)) + ' = ' + 'MEM[$' + str(int(line[7:8], 2)) + ']; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + str(int(line[5:6], 2)) + ' = ' + str(regval[int(line[5:6])]) + '\n')

        elif (line[0:4] == s8):
            print(line)
            PC += 4
            X = regval[int(line[4:6], 2)]
            MEM[regval[int(line[6:], 2)]] = X
            f.write('Operation: MEM[' + str(MEM[regval[int(line[6:], 2)]]) + '] = ' + str(X) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            # ask about regs that changed

        #initli: lower 4
        elif (line[0:2] == initli):
            PC += 4
            reg = int(line[2:4], 2)
            imm = int(line[4:], 2)
            regval[reg] += imm
            f.write('Operation: $' + str(reg) + ' = ' + str(imm) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + str(regval[reg]) + ' = ' + str(imm) + '\n')

        #initui: upper 4
        elif(line[0:2] == "01"):
            PC +=4
            reg = int(line[2:4], 2)
            imm = int(line[4:], 2)
            regval[reg] = imm << 4
            f.write('Operation: $' + str(reg) + ' = ' + str(imm) + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + str(regval[reg]) + ' = ' + str(imm) + '\n')




        elif (line[0:5] == bezR0):  # Beq
            try:
                imm = int(line[5:7], 16)
            except:
                f.write("ERROR: Invalid Instruction")
                break
            if (regval[0] == 0):
                PC = PC + (4 * imm)
                lineCount = lineCount + imm
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('No Registers have changed. \n')
                continue
            f.write('No Registers have changed. \n')
            PC += 4


        elif (line[0:3] == "jmp"):  # jmp
            line = line.replace("jmp", "")
            line = line.split(",")
            try:
                imm = int(line[0], 16)
            except:
                f.write("ERROR: Invalid Instruction")
                break
            PC = PC + (4 * imm)
            lineCount = lineCount + imm
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('No Registers have changed. \n')

            continue


        lineCount += 1

    print("REGISTERS:")
    print("-----------")

    for x in range(len(regval)):
        if (x == 4):
            print("lo: ", hex(regval[x]))
        elif (x == 5):
            print("hi: ", hex(regval[x]))
        else:
            print("$", x, ": ", hex(regval[x]))
    print("PC: ", hex(PC))

    print("\n")
    print("Used Memory values:\n")
    print("            ", end="")
    for x in range(0, 8, 1):
        print("0x" + format((x * 4), "08x"), end=" ")
    print("\n")
    print("--------------------------------------------------------------------------------------------------", end="")
    count = 0
    print("\n")
    for x in range(0x0000, 0x0100, 4):
        if ((x - 0x3) % 0x20 == 0):
            print("0x" + format(x - 0x3, "08x") + '|', end=" ")
        print("0x", end="")
        for y in range(0, 4, 1):
            print(format(MEM[x - y], "02x"), end="")
        print(" ", end="")
        count += 1
        if (count == 8):
            count = 0
            print("\n")

    f.close()


main()
