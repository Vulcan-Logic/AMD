""" Project: AllMediaHouse Programming Tasks
Title: Task 1
Description: Part 1 Develop a term calculator that can handle (), *, /, +, and -. For example, if the user enters the
    term (5 + 8) * 3/8 +3, the term calculator shall calculate and output the result according to the school
    rules of term calculations.
    These rules are: () before * and /, * and / before + and -. Several * and / are calculated from left to
    right, several + and - also from left to right.
    Important: The actual algorithm must be implemented itself. The use of functions like eval in
    JavaScript are not permitted.
Part:
Author: Vineet W. Singh
Reviewed by: VWS
Start Date: 21/3/21
Date of last edit: 21/3/21
Date of last review:
 """

#function - compute the equation after parsing & tokenising, converting to RPN and evaluating RPN
def computeEquation(equationString):
    #add a + sign in front of -signs
    equationString=addPlus(equationString)
    #convert string into array of characters for processing into tokens
    if len(equationString)==0:
        raise Exception("E001","Empty Equation passed")
    elif len(equationString)==1:
        if equationString[0] in ["0","1","2","3","4","5","6","7","8","9"]:
            return(float(equationString))
        else: 
            raise Exception("E002","invalid equation")
    else:
        equationList=list(equationString)
        try: 
            #tokenise into list of operands and operators dictionary
            tokenList=getTokenList(equationList)
            #process token list into RPN format
            tokenListRPN=getTokensinRPN(tokenList)
            #compute RPN list and get result
            result=processRPN(tokenListRPN)
        except Exception as inst:
            x,y=inst.args
            raise Exception(x,y)
        return(result)

#function - return token list in RPN form
def getTokensinRPN(tokenList):
    #convert proided list of infix tokens in dictionary form into 
    #list of RPN list of tokens
    outputQue=[]
    operatorStack=[]
    brackets=0
    for ctr in range(len(tokenList)):
        token=tokenList[ctr]
        if token["type"]=="Od":
            #token in operand
            outputQue.append(token)
        elif token["type"]=="OpOB":
            #token is opening bracket
            operatorStack.append(token)
            brackets+=1
        elif token["type"]=="OpCB":
            #token is closing bracket
            #check that there were opening brackets previously
            if brackets>0:
                #there were opening brackets
                while len(operatorStack)>0:
                    #while there are operators in the stack
                    nToken=operatorStack[len(operatorStack)-1]
                    if nToken["type"]=="OpOB":
                        #if the operator is a opening bracket remove it from the stack
                        operatorStack.pop()
                        #decrease the opening bracket count
                        brackets-=1
                        #brackets have been found break out of the loop to process operator stack
                        break
                    else:
                        #if the operator isn't a opening bracket, pop it onto the output que
                        outputQue.append(operatorStack.pop())
            else:
                #more closing brackets than opening ones
                raise Exception("E131","invalid equation: closing bracket without corresponding opening bracket")
        elif token["type"]=="Op":
            #token is an operator (^,/,* or +) negative values are associated with operands
            while len(operatorStack)>0:
                #in this loop process all operators on the top of the stack to place them in the right order with reference to 
                #the operator currently being assessed
                nToken=operatorStack[len(operatorStack)-1]
                #check if operator at the top of the stack is not an opening bracket AND 
                #has higher or same priority (or lower/same precedence) than the one at the top of the stack
                # if so pop it onto the que 
                if (nToken["type"]=="Op" and nToken["pr"]<token["pr"]) or\
                    (nToken["pr"]==token["pr"] and token["type"]=="Op" and token["As"]=="Left"):
                    outputQue.append(operatorStack.pop())
                else:
                    break
            #add the new operator to the stack
            operatorStack.append(token)
    #all tokens in the input list have been processed and added to the que or stack, add the remaining operators in the stack 
    #to the que
    while(len(operatorStack)!=0):
        outputQue.append(operatorStack.pop())
    #check for unbalanced opening brackets
    if brackets!=0:
        raise Exception("E132","invalid equation: unclosed opening brackets")
    #return the processed RPN que
    return(outputQue)

#function - evaluate RPN
def processRPN(tokenList):
    tokenList.reverse()
    stack=[]
    result=0
    opA=None    
    opB=None
    while len(tokenList)>0:
        item=tokenList.pop()
        if item["type"]=="Od":
            #item is an operand - push to stack
            stack.append(item["value"])
        elif item["type"]=="Op":
            #item is an operator - pop two operands from stack and do operation
            while len(stack)>0:
                if opB is None:
                    opB=stack.pop()
                    continue
                if opB is not None and opA is None: 
                    opA=stack.pop()
                    break    
            if opA is not None and opB is not None:
                #two valid operands found - do operation
                if item["value"] == "^":
                    result=opA**opB
                elif item["value"] == "/":
                    result=round(opA/opB,4)
                elif item["value"] == "*":
                    result=opA*opB
                elif item["value"] == "+":
                    result=opA+opB
                #push result back onto stack
                stack.append(result)
                opA=None
                opB=None
            else:
                #only one valid operand, need at least two - error
                raise Exception("E141","Error in equation")
    #tokenList is now empty - all tokens have been exausted
    if len(stack)>1:
        #there should be only one result in the stack at the end - more than one means an error in the equation
        raise Exception("E142","Error in equation")
    elif len(stack)==1: 
        #all has gone well  - only one value in stack pop stack and return 
        return(stack.pop())
    else:
        raise Exception("E143","Error in equation")

#function-parse and tokenise
def getTokenList(rawEquationList):
    outputList=[]
    #process all characters in input list 
    while len(rawEquationList)>0:
        #process individual character as item
        item=rawEquationList[0]
        addendum=1
        if item=="(":
            #item is a bracket - operator 
            newItem={"type":"OpOB", "value": item, "pr":1, "As":None}
            outputList.append(newItem)
        elif item==")":
            #item is a bracket - operator 
            newItem={"type":"OpCB", "value": item, "pr":1, "As":None}
            outputList.append(newItem)
        elif item =="/":
            #item is division, multiplication, addition left association operator
            newItem={"type":"Op", "value": item, "pr":3, "As":"Left"}
            outputList.append(newItem)
        elif item =="*":
            #item is division, multiplication, addition left association operator
            newItem={"type":"Op", "value": item, "pr":3, "As":"Left"}
            outputList.append(newItem)
        elif item == "+":
            #item is division, multiplication, addition left association operator
            newItem={"type":"Op", "value": item, "pr":4, "As":"Left"}
            outputList.append(newItem)
        elif item == "^":
            #item is a power - right association operator
            newItem={"type":"Op", "value": item, "pr":2, "As":"Right"}
            outputList.append(newItem)
        elif item in ["0","1","2","3","4","5","6","7","8","9",".","-"]:
            #item is a number, decimal or negative sign 
            try:    
                #convert sequence of strings into a operand string     
                operandString, addendum=getNextOperandString(rawEquationList,0)
                if len(operandString)!=0:
                    #convert to float and add to dictionary list
                    newItem={"type":"Od", "value": float(operandString)}
                    outputList.append(newItem)
            except Exception:
                raise Exception("E101","invalid or blank operand in equation")
        elif item==" ":
            #skip spaces
            pass
        else: 
            #invalid character raise exception
            raise Exception("E102","invalid characters/opertors in equation")
            #remove processed item from input list - reset input list 
        rawEquationList=rawEquationList[addendum:]
    return(outputList)

#function-get operand out of equation
def getNextOperandString(equationList,eleCtr):
    ctr=0
    indx=eleCtr
    operandStack=[]
    validFlg=False
    while True:
        if indx==len(equationList) and validFlg:
            #at the end of the input string and a valid operand was found 
            break
        elif indx==len(equationList) and validFlg is False:
            #already at end of input list without a valid operand string being found
            raise Exception("E111","invalid operand in equation")
        #test item x 
        x=equationList[indx]
        if x in ["0","1","2","3","4","5","6","7","8","9","."]:
            #item is a number and begining of an operand
            ctr+=1
            operandStack.append(x)
            validFlg=True
        elif x=="-" and indx<=(len(equationList)-1) and \
            equationList[indx+1] in ["0","1","2","3","4","5","6","7","8","9"]:
            #item is a negative sign followed by a number, this is a valid operand
            ctr+=1
            operandStack.append(x)
            validFlg=True
        elif x=="-" and indx<=(len(equationList)-2) and \
            equationList[indx+1]=="." and \
                equationList[indx+2] in ["0","1","2","3","4","5","6","7","8","9"]:
            #item is a negative number followed by a valid decimal number
            ctr+=1
            operandStack.append(x)
            validFlg=True
        elif validFlg and x in ["+","/","*","(",")"," ","^"]:
            #item is a blank space or a valid operator, which means that the operand string is finished 
            break
        elif validFlg is False and x in ["+","/","*","(",")"," ","^"]:
            #no valid operand was found instead a operator has been found which means that the equation has an error 
            raise Exception("E112","invalid operand in equation")
        else:
            #trap other cases - might mean that the equation has an error 
            raise Exception("E113","invalid operand in equation")
        indx+=1
    return("".join(operandStack),ctr)

#function-add a plus sign in front of all '-' signs
def addPlus(equation):
    # add a plus sign in front of negative signs to give us a valid equation for processing 
    nsEquation=""
    returnEquation=""
    #strip out all blank spaces
    for indx in range(len(equation)):
        if equation[indx]!=" ":
            nsEquation+=equation[indx]
    #test for a blank string
    if len(nsEquation)==0:
            return("")
    #test for a single character that might be a number
    elif len(nsEquation)==1:
        if nsEquation[0] not in ["0","1","2","3","4","5","6","7","8","9"]:
            return("")
        else:
            return(nsEquation)
    #process input string that is more than one character
    elif len(nsEquation)>1:
        for indx in range(len(nsEquation)):
            if ((indx!=0) and (indx<=len(nsEquation)-2)):
                if (nsEquation[indx]=="-") and\
                    (nsEquation[indx+1] in ["0","1","2","3","4","5","6","7","8","9",".","("]) and\
                        (nsEquation[indx-1] not in ["*","/","+"]):
                    #if current character is a negative sign followed by a number, decimal or bracket add a + in front of it
                    returnEquation+="+"
                    returnEquation+=nsEquation[indx]
                else:
                    #just add the character as it is 
                    returnEquation+=nsEquation[indx]
            else:
                if indx==len(nsEquation)-1 and nsEquation[indx]=="-":
                    #a negative sign at the last character - invalid equation
                    return("E")
                else:
                    #a character at the last position return it as it is
                    returnEquation+=nsEquation[indx]
    return(returnEquation)

#main entry point
if __name__=='__main__':
    while True:
        print("Enter a valid equation, Enter Q to quit:")
        #accept an input string
        equationString=input()
        #check to quit
        if equationString=="Q" or equationString=="q":
            exit()
        else:
            try:
                result=computeEquation(equationString)
                print("Answer: {0}".format(result))
            except Exception as inst:
                x,y=inst.args
                print("Error No {0}: {1}".format(x,y))