""" Project: AllMediaHouse Programming Tasks
Title: Task 3
Description: Part 3, based on Part 1 Allow the term calculator to accept lines in the form y = <TERM> with x as an
    additional possible character in the term. If such a complete equation is given, you display a simple x /
    y graph. For each value on the x axis, calculate y and plot the point (a continuous line is even better).
Part:
Author: Vineet W. Singh
Reviewed by: VWS
Start Date: 21/3/21
Date of last edit: 22/3/21
Date of last review:
 """
import matplotlib.pyplot as plt 
import task1try2 as compEq

# function - strip spaces from input string
def stripSpaces(equationString):
    outString=""
    for x in equationString:
        if x!=[" "]:
            outString+=x
    return(outString)

#function - get Dependent Variable label
def getDpVar(equationString):
    indx=0
    found=False
    foundIndx=0
    retVal=""
    while indx<len(equationString):   
        if equationString[indx]=="=":
            retVal=equationString[0:indx]
            found=True
            foundIndx=indx
        indx+=1
    if found:
        return(retVal,foundIndx)
    else: 
        raise Exception("E201","invalid quadartic equation") 

#function - get independent variable label from input equation 
def getIndpVar(equationString,indx):
    eqRHS=equationString[indx+1:]
    ctr=0
    startVar=False
    varName=""
    while ctr<=len(eqRHS):
        if eqRHS[ctr] not in ["0","1","2","3","4","5","6","7","8","9",".","+","/","*","^","-","(",")"] and \
            startVar is False:
            #variable name has started
            startVar=True
            varName+=eqRHS[ctr]
        elif eqRHS[ctr] not in ["0","1","2","3","4","5","6","7","8","9",".","+","/","*","^","-","(",")"] and\
            startVar:
            #variable name continues
            varName+=eqRHS[ctr]
        elif eqRHS[ctr] in ["0","1","2","3","4","5","6","7","8","9",".","+","-","(",")"] and \
            startVar:
            #variable name has ended
            startVar=False
            break
        ctr+=1
    if len(varName)!=0:
        return(varName)
    else: 
        raise Exception("E211", "Invalid Equation - no independent variable found")

#function - replace independent variable label with the variable value
def getSubstitutedEquation(equationString,indpVar,inputValue):
    #process until label is not found in equation    
    while True:
        stPos=equationString.find(indpVar)
        if stPos==-1:
            #finsihed 
            break
        elif stPos==0:
            #first label is at the beginning of the equation string
            lenIndpVar=len(indpVar)
            equationString="1*"+str(inputValue)+equationString[stPos+lenIndpVar:]
        else:
            #label is within the string
            lenIndpVar=len(indpVar)
            equationString=equationString[:stPos]+"*"+str(inputValue)+equationString[stPos+lenIndpVar:]
    return(equationString)

#function - get range of dependent variable values    
def getRange(inputString):
    #split input into three strings
    values=inputString.split(":")
    #check for right number of values
    if len(values)!=3:
        raise Exception("E221", "invalid dependent range values provided, please enter in the following format start:step:stop \
            with stop>start and step>0")
    #convert to int values
    try: 
        start=int(values[0])
        step=int(values[1])
        stop=int(values[2])
    except ValueError:
        raise Exception('E222', "invalid dependent range values provided, start stop end values should be numbers only")
    #check for validity of converted numbers    
    if start>=stop:
        raise Exception("E223", "invalid dependent range values:start has to be less than stop, please enter in the following \
            format start:step:stop with stop>start and step>0")
    elif step<=0: 
        raise Exception("E224", "invalid dependent range values:step has to be positive and small, please enter in the following\
            format start:step:stop with stop>start and step>0")
    else:
        return(start,step,stop)

#main entry point
if __name__=='__main__':
    print("Enter a valid quadratic equation of one variables in the form of y=20x^2+2x+10 to plot")
    print("default is y=20x^2+2x+10, press enter for default")
    #accept an input string
    inp1=stripSpaces(input())
    if len(inp1)==0:
        equationString="y=20x^2+2x+10"
    else:
        equationString=inp1
    print("Enter domain range for independent variable i.e.integers for x above in the form starting value:step:stoping value")
    print("default is 1:1:100, press enter for default")
    #accept an input string
    inp2=stripSpaces(input())
    if len(inp2)==0:
        indpRangeString="1:1:100"
    else:
        indpRangeString=inp2
    try:
        dpVar,indx=getDpVar(equationString)
        indpVar=getIndpVar(equationString,indx)
        start,step,stop=getRange(indpRangeString)
        indpVarValues=[]
        dpVarValues=[]
        #for loop to make values
        for x in range(start,stop,step+1):
            eqToEval=getSubstitutedEquation(equationString[indx+1:],indpVar,x)
            result=compEq.computeEquation(eqToEval)
            indpVarValues.append(x)
            dpVarValues.append(result)
        # prepare the plot
        plt.plot(indpVarValues,dpVarValues)  
        plt.xlabel(indpVar)  
        plt.ylabel(dpVar)  
        plt.title('Task 3 Graph') 
        # show the plot 
        plt.show() 
    except Exception as inst:
        x,y=inst.args
        print("Error No {0}: {1}".format(x,y))
