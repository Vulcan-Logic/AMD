""" 
Project: AllMediaHouse Programming Tasks
Title: Task 2
Description: Part 2 Peter likes numbers. As a meditation exercise, he likes to write down all the numbers starting
    with 1 whose digits are sorted in ascending order. For example, 11235888 is such a number. After a
    while, he stops.
    Write an efficiently designed program which, after entering a number between 1 and 10 ^ 18,
    represents the last number checked by Peter, outputs the last number written down by Peter.
    Examples:
        Input: 23245 Output:22999
        Input: 11235888 Output:11235888
        Input: 111110 Output:99999
    Input: 33245 Output:29999
    Tip: Going through the numbers one by one and testing them is not efficient enough.
Part:
Author: Vineet W. Singh
Reviewed by: VWS
Start Date: 21/3/21
Date of last edit: 21/3/21
Date of last review:
"""

#function
def computeNumber(num):
    number=str(num)
    outStr=number[0]
    indx=1
    rFlag=False
    while indx<=len(number)-1:
        no1=number[indx-1]
        no2=number[indx]
        if int(no1)<=int(no2):
        #digit is greater than previous digit, nothing to do, copy to output number
           outStr+=no2
           result=outStr
        else:
            #digit2 is less than digit1
            #drop digit1 by 1 and pad rest of the string with 9 to get a valid number
            if len(outStr)-1==0:
                outStr=""
            else:
                outStr=outStr[0:len(outStr)-1]
            no1=str(int(no1)-1)
            #get number of 9's to pad
            chnCt=len(number[indx:])
            #create the new number
            outStr+=no1+"9"*chnCt
            #set recursion flag to true
            rFlag=True
            break
        indx+=1
    if rFlag is True:
        #test the number before returning it
        result=computeNumber(outStr)
    return(result)

#main entry point
if __name__=='__main__':
    while True:
        print("Enter a number to test or q/Q to exit")
        #accept an input string
        equationString=input()
        #check to quit
        if equationString=="Q" or equationString=="q":
            exit()
        else:
            try:
                validNo=int(equationString)
                #check for valid value
                if 1<=validNo<=10**18:
                    #check number
                    result=computeNumber(str(validNo))
                    print("Answer: {0}".format(int(result)))
            except Exception as inst:
                x,y=inst.args
                print("Error No {0}: {1}".format(x,y))