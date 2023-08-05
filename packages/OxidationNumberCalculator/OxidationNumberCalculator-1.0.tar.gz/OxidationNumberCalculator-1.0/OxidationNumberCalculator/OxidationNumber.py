#Author: Harold J. Iwen
#Project: Oxidation Number Calculator
#Company: Inventorsniche
#Date Started: May 20th, 2021


#Purpose: The purpose of this calculator is to provide a method of calculating oxidation numbers
#         so students can check their answers...


#Section for importing necessary
#modules....
################################
################################
################################

#periodictable module for looking
#up info on elements...
import mendeleev as per

#use regular expressions to
#make sure the input is secure...
import re


#Section for writing core and helper
#functions...
####################################
####################################
####################################

#take in input from the user and process...
def processI(stringI,peroxide):

    #run security check...
    stringI, flag = Security(stringI)

    #a is a temporary variable that will
    #hold an oxidation number list...
    a = None
    
    #See what the value of flag is...
    if(flag == 1):
    
        #oxidation number calculator
        #for compound/element...
        a = RedoxONot(stringI,peroxide)

        #return the oxidation number list...
        return stringI, a

    elif(flag == 2):

        #Take -> out of stringI...
        #First, make a copy of stringI...
        equCopy = stringI

        #Now, add a space before and after
        #->...
        cr = equCopy[0:equCopy.index('>')-1]
        tr = equCopy[equCopy.index('>')+1:]
        equCopy = cr + " -> " + tr

        #replace all positive charges with 'p'..
        equCopy = replacePos(equCopy)
        
        #Now replace all '+' instances that
        #aren't charges...
        equCopy = re.sub(r"\++"," ",equCopy)
        
        #Now, split the string into a list...
        equCopy = equCopy.split()

        #create reactant element dictionary...
        reactant = {}

        #create product element dictionary...
        product = {}

        #create reactant oxidation number dictionary...
        reactantNum = {}

        #create product oxidation number dictionary...
        productNum = {}

        #equation arrow flag...
        flag = 0

        #equation a...
        a = None
        
        #now loop through the list and create a list
        #of oxidation numbers for each compound/element...
        for x in range(len(equCopy)):

            #assign the list a to the correct dictionary...
            if(equCopy[x] == "->"):

                #change flag value...
                flag = 10

            elif(flag == 0):

                #now assign oxidation numbers for each element/compound...
                if(peroxide == x):
                    a = RedoxONot(equCopy[x],peroxide)
                else:
                    a = RedoxONot(equCopy[x], -1)

                #get each individual element in a list and assign to dictionary...
                b = elementBreakDown(equCopy[x])
                
                #assign oxidation number list to dictionary...
                reactantNum[equCopy[x]] = a

                #assign element list to reactant element dictionary...
                reactant[equCopy[x]] = b

            elif(flag == 10):

                #now assign oxidation numbers for each element/compound...
                if(peroxide == x):
                    a = RedoxONot(equCopy[x], peroxide)
                else:
                    a = RedoxONot(equCopy[x], -1)
                
                #get each individual element in a list and assign to dictionary...
                b = elementBreakDown(equCopy[x])

                #assign oxidation number list to dictionary...
                productNum[equCopy[x]] = a

                #assign element list to product element dictionary...
                product[equCopy[x]] = b

        #return the oxidation number information...
        return equCopy, reactant, reactantNum, product, productNum

    else:

        #throw a error since the security check failed...
        return -1



    
#Security check function...
def Security(UserInput):
    
    #first check to see if the input
    #resembles a chemical equation or
    #a compound...
    if("->" in UserInput):

        #check to see if the chemical equation
        #is legit...

        #Begin by removing -> from the equation...
        #make a copy of User Input first...
        temp = UserInput

        #count the number of carrot characters...
        count = countCarrot(UserInput)

        #check count..
        if(count == -1):
            
            #return -1...
            return -1, -1
        
        #Now remove ->...
        temp = splitList(temp)

        #see if the length of the split list is two...
        if(temp == -1):
            
            #return -1...
            return -1, -1

        #change positive charges to negative...
        temp = re.sub(r"(\[\+[0-9]*\])","",temp)

        #remove all + signs...
        temp = re.sub(r"\++"," ",temp)

        #split the list...
        temp = temp.split()
        
        #temp variables 
        one, two = None, None
        
        #go through the list and check each compound
        #recursively...
        for x in range(len(temp)):

            #recursive call...
            one, two = Security(temp[x])

            #see if one or two is equal to -1...
            if(one == -1):
                
                #return -1
                return -1, -1

        #return userinput and value 2...
        return UserInput, 2

    else:

        #see if the element/compund/equation is the correct form
        #by comparing the length of the original user
        #input with the length of the returned match...
        length = len(UserInput)

        #now get the returned group match string...
        try:
            
            temp = re.search("((([A-Z]+[a-z][0-9]*)|([A-Z]+[0-9]*)|([(]([A-Z][a-z][0-9]*|[A-Z][0-9]*)+[)][0-9]*))+(\[[-+][0-9]+\]){0})",UserInput)[0]

        except:

            #failed, return -1
            return -1, -1
            
        #now see if the lengths match...
        if(len(temp) != length):

            #try again with {0} switched to {1}
            try:
                
                temp = re.search("((([A-Z]+[a-z][0-9]*)|([A-Z]+[0-9]*)|([(]([A-Z][a-z][0-9]*|[A-Z][0-9]*)+[)][0-9]*))+(\[[-+][0-9]+\]){1})",UserInput)[0]

            except:

                #failed...
                return -1, -1

            #make another comparison...
            if(len(temp) != length):
                
                #return -1 since the input failed...
                return -1, -1
        
        #remove any charges...
        temp = re.sub("[+-]*[0-9]*\[*\]*","",UserInput)

        #check to see if the element is legit...
        if(len(temp) == 1 or (len(temp) == 2 and temp[1].islower())):

            #run the UserInput through the
            #element method within the mendeleev
            #module to see if it is a legit element...
            element = elementV(temp,temp)

            #see if the element contains -1...
            if(element == -1):

                #return -1...
                return -1, -1

            else:

                #return the original input and flag = 1
                return element, 1

        else:

            #check to see if the compound is legit...
            element = ""
            
            #begin by spacing out all elements...
            for x in range(len(UserInput)):

                #pull each element and check...
                if(UserInput[x].isupper() and element == ""):

                    #append element letter to string...
                    element = element + UserInput[x]

                elif(UserInput[x].islower() and len(element) == 1 and element.isupper()):

                    #append element letter to string...
                    element = element + UserInput[x]

                    #see if the element is legit...
                    element = elementV(element, "")

                elif(UserInput[x].isupper() and len(element) == 1 and element.isupper()):

                    #check to see if the current symbol is legit...
                    element = elementV(element,UserInput[x])

                #see if element is -1...
                if(element == -1):

                    #return -1...
                    return -1, -1

            #Now check to see if theres any unchecked element left in
            #element...
            if(element != ""):
                
                element = elementV(element,"")

            #check if element is -1...
            if(element == -1):

                #return -1
                return -1, -1

            else:

                #return success message...
                return UserInput, 1



            
#assign oxidation numbers in the form of lists
def RedoxONot(elComp, peroxide):

    #oxidnation number list...
    oxidation = []

    #group 1 elements...
    groupO = ['H','Li','Na','K','Rb','Cs','Fr']

    #group 2 elements...
    groupT = ['Be','Mg','Ca','Sr','Ba','Ra']

    #group 15 elements...
    groupFif = ['N','P','As','Sb','Bi','Mc']

    #group 16 elements...
    groupSix = ['S','Se','Te','Po','Lv']

    #group 17 elements...
    groupSev = ['Cl','Br','I','At','Ts']

    #undo any + to p conversions...
    elComp = pToPlus(elComp)
    
    #breakdown
    breakdown = elementBreakDown(elComp)
    
    #begin by seing if it is an individual element with no charge...
    if(not('[' in elComp) and ((len(elComp) == 2 and elComp[1].islower()) or len(elComp) == 1)):

        #append oxidation number of 0...
        oxidation.append(0)

    elif('[' in elComp and ((len(elComp[0:elComp.index('[')]) == 2 and elComp[0:elComp.index('[')][1].islower()) or len(elComp[0:elComp.index('[')]) == 1)):

        #get the charge and append to oxidation...
        temp = elComp[elComp.index('[')+1:elComp.index(']')]

        #now append the int() version of the temp string...
        oxidation.append(int(temp))

    elif(not('[' in elComp) and (len(re.sub("\[[+-][0-9]*\]|[0-9]*","",elComp)) == 1 or (len(re.sub("\[[+-][0-9]*\]|[0-9]*","",elComp)) == 2 and re.sub("\[[+-][0-9]*\]|[0-9]*","",elComp)[1].islower()))):
                                 
        #append oxidation number of 0...
        oxidation.append(0)

    else:

        #group one/two flag...
        grOT = 0

        #group 15-17 flag...
        grMax = 0
        
        #go through each element and assign oxidation number...
        for x in range(len(breakdown)):

            #see if group1...
            if(breakdown[x] in groupO):

                #assign oxidation number...
                oxidation.append(+1)

                #change flag...
                if(grOT == 0):

                    #change grOT...
                    grOT = 10

            elif(breakdown[x] in groupT):

                #assign oxidation number...
                oxidation.append(+2)

                #change flag...
                if(grOT == 0):

                    #change grOT...
                    grOT = 10

            elif(breakdown[x] == 'F'):

                #assign oxidation number...
                oxidation.append(-1)

            elif(breakdown[x] == 'O'):

                #assign oxidation number...
                oxidation.append(-2)

            elif(breakdown[x] == 'H' and flag == 10):

                #assign oxidation number...
                oxidation.append(-1)

            elif(breakdown[x] == 'H'):

                #assign oxidation number...
                oxidation.append(+1)

            elif(breakdown[x] in groupSix):

                oxidation.append(-2)

                grMax = 16

            elif(breakdown[x] in groupSev):

                oxidation.append(-1)

                grMax = 17

            elif(breakdown[x] in groupFif):

                oxidation.append(-3)

                grMax = 15

            else:

                #assign "Null" value...
                oxidation.append("NULL")

        #now confirm all values...
        oxidation = confirmOx(oxidation, elComp, breakdown, grMax, peroxide)

    #return the oxidation number list...
    return oxidation

        


#replace positive charges with 'p'...
def replacePos(strInput):

    #turn string into list since the string
    #is immutable...
    strInput = list(strInput)
    
    #loop through the entire string...
    for x in range(len(strInput)):

        #see if the character is equal to '['...
        if(strInput[x] == '['):

            #check what the next character is...
            if(strInput[x+1] == '+'):

                #replace the '+' character...
                strInput[x+1] = 'p'

    #now join together all of the elements...
    strInput = "".join(strInput)

    #now return the string input...
    return strInput


#check element validity...
def elementV(Input, newI):

    #check to see if the current symbol is legit...
    try:

        #get the element...
        temp = per.element(Input).name

        #assign UserInput[x] to element...
        return newI

    except:

        #return -1 since the input is bad...
        return -1


    
#count all occurrences of '>' character...
def countCarrot(UserInput):

    #carrot count...
    count = 0
    
    #now count all occurrences of '>'...
    for x in range(len(UserInput)):

        #count '>'...
        if(UserInput[x] == '>'):

            #increment counter...
            count = count + 1

            #see if count = 2...
            if(count == 2):

                #return -1...
                return -1

    #return the count..
    return count



#split the list by getting rid of ->...
def splitList(Input):

    #Now remove ->...
    Input = re.sub(r"->"," ",Input)

    #see if the length of the split list is two...
    if(len(Input.split()) != 2):

        #return -1...
        return -1

    #return 1 since this test didn't fail...
    return Input


#break the elements down and return a list...
def elementBreakDown(compound):

    #element variable...
    element = ""

    #copy compound...
    cTwo = compound

    #element list
    E = []
    
    #see if there is an external charge...
    if('[' in compound):
    
        #take out the charge...
        cTwo = re.sub(r"\[[+-][0-9]*\]","",cTwo)

    #Loop through and add all elements...
    for x in range(len(cTwo)):

        #start adding elements...
        if(cTwo[x].isupper() and len(element) == 0):

            #concatenate character...
            element = element + cTwo[x]

        elif(cTwo[x].isupper() and len(element) == 1):

            #append first element...
            E.append(element)

            #assign new value...
            element = cTwo[x]

        elif(cTwo[x].islower() and len(element) == 1):

            #concatenate new character...
            element = element + cTwo[x]

            #Now append new element...
            E.append(element)

            #renew element...
            element = ""

    #append any leftover elements still in element...
    if(element != "" and element[0].isupper()):

        #append new element...
        E.append(element)

    #return the list...
    return E


#confirm/solidify oxidation number values...
def confirmOx(oxidation, compound, breakdown, flag, peroxide):
    
    #charge...
    charge = 0

    #group 1 elements...
    groupO = ['H','Li','Na','K','Rb','Cs','Fr']

    #group 2 elements...
    groupT = ['Be','Mg','Ca','Sr','Ba','Ra']
    
    #get the net charge of the compound...
    if('[' in compound):

        #retrieve charge...
        charge = int(compound[compound.index('[')+1:compound.index(']')])

    #get subscripts for each element...
    subscript = []
    subscript = re.sub("[A-Z][a-z]*"," p",compound)
    subscript = re.sub("\[[+-][0-9]*\]"," ",subscript)
    subscript = subscript.split()
    for x in range(len(subscript)):

        if(len(subscript[x]) == 1):

            subscript[x] = 1

        elif(len(subscript) > 1):

            subscript[x] = subscript[x][1:]
    
    #sum
    sum = 0

    #Null flag...
    N = 0
    
    #add all charges together...
    for x in range(len(oxidation)):
        
        if(oxidation[x] != "NULL"):

            #summation...
            sum = sum + int(subscript[x])*int(oxidation[x])

        elif(oxidation[x] == "NULL" and N == 0):

            #set N...
            N = 9

    #check if the sum is equal to charge...
    if(sum == charge):

        #return oxidation...
        return oxidation

    else:

        #see if hydrogen is in the compound...
        if('H' in breakdown and not("NULL" in oxidation)):

            #change oxidation number...
            if(oxidation[breakdown.index('H')] == 1):

                oxidation[breakdown.index('H')] = -1

                oxidation = chargeCheck(oxidation, subscript, breakdown, charge, flag, peroxide)

        elif('O' in breakdown and not("NULL" in oxidation)):

            #change oxidation number of oxygen...
            oxidation[breakdown.index('O')] = -1

            oxidation = chargeCheck(oxidation, subscript, breakdown, charge, flag,peroxide)

        elif("NULL" in oxidation):

            #leftover variable...
            left = (charge - sum) / int(subscript[oxidation.index("NULL")])

            #assign leftover charge...
            oxidation[oxidation.index("NULL")] = left

    #return oxidation...
    return oxidation


#convert all positive charges from p to +...
def pToPlus(Input):

    #convert Input to list...
    Input = list(Input)

    #left bracket flag...
    bFlag = 0
    
    #go through all characters and convert p to plus
    #in brackets...
    for x in range(len(Input)):

        #see if a left bracket has been confronted...
        if(Input[x] == '['):

            #set flag...
            bFlag = 10

        elif(Input[x] == 'p' and bFlag == 10):

            #assign '+'...
            Input[x] = '+'

            #reset flag...
            bFlag = 0

    #convert back to string...
    Input = "".join(Input)

    #return Input...
    return Input

#check charge...
def chargeCheck(oxidation, subscript, breakdown, charge, flag, peroxide):

    #sum variable...
    sum = 0
    
    #check the new charge...
    for x in range(len(oxidation)):

        #summation...
        sum = sum + int(subscript[x])*int(oxidation[x])

    #check sum and charge...
    if(sum == charge):

        #return oxidation
        return oxidation

    else:

        #group 1 elements...
        groupO = ['H','Li','Na','K','Rb','Cs','Fr']

        #group 2 elements...
        groupT = ['Be','Mg','Ca','Sr','Ba','Ra']

        #group 15 elements...
        groupFif = ['N','P','As','Sb','Bi','Mc']

        #group 16 elements...
        groupSix = ['S','Se','Te','Po','Lv']
    
        #group 17 elements...
        groupSev = ['Cl','Br','I','At','Ts']

        #change oxidation number...
        if('O' in breakdown and oxidation[breakdown.index('O')] != -2):
            
            oxidation[breakdown.index('O')] = -2

        elif('H' in breakdown and oxidation[breakdown.index('H')] != 1):

            oxidation[breakdown.index('H')] = 1

        #rules list...
        rules = []

        #loop through...
        for x in range(len(breakdown)):

            #check if element is hydrogen...
            if(breakdown[x] == 'H'):

                #append rule...
                rules.append(5)

            elif(breakdown[x] == 'O'):

                #append rule...
                rules.append(6)

            elif(breakdown[x] in groupFif or breakdown[x] in groupSix or breakdown in groupSev):

                #append rule...
                rules.append(7)

            elif(breakdown[x] in groupO or breakdown[x] in groupT):

                #append rule...
                rules.append(3)

        #Now make propper evaluation based on rules...
        if('H' in breakdown and 3 in rules):

            #change oxidation number...
            oxidation[breakdown.index('H')] = -1

        if(peroxide != -1):

            #change oxidation number of oxygen...
            oxidation[breakdown.index('O')] = -1

        #check if rule seven is present...
        if(7 in rules):

            oxidation[rules.index(7)] = "NULL"

            #reset sum...
            sum = 0
            
            #re-sum...
            for x in range(len(oxidation)):

                if(oxidation[x] != "NULL"):
                
                    #summation...
                    sum = sum + int(subscript[x])*int(oxidation[x])

            #change NULL...
            oxidation[oxidation.index("NULL")] = (charge - sum) / subscript[oxidation.index("NULL")]

    return oxidation
