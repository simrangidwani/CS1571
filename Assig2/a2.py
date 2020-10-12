# -*- coding: utf-8 -*-
import logic
import planning
import search

""" A2 Part A

    giveFeedback is a function that reads in a student state and 
    returns a feedback message using propositional logic and proof by resolution. The rules
    for how to decide which message to return are given in the assignment description.

    studentState:   a String representing a conjunction of five possible symbols: 
    CorrectAnswer, NewSkill, MasteredSkill, CorrectStreak, IncorrectStreak
                    For example, you could call giveFeedback('CorrectAnswer') or 
                    giveFeedback('MasteredSkill & CorrectStreak')

    feedbackMessage:a String representing one of eight feedback messages (M1 through M8 below). 

    Feel free to refactor the code to move M1 through M8 into a class, but the function call and 
    return values should remain as specified below for our grading.

   CorrectAnswer => (Message1 v Message2 v Message3 v Message7)
   ~CorrectAnswer => (Message4 v Message5 v Message6 v Message8)
   (MasteredSkill & ~CorrectAnswer) v (MasteredSkill & CorrectStreak) => IsBored
   NewSkill v IncorrectStreak => Message6
   (IncorrectStreak & CorrectAnswer) v (NewSkill & CorrectStreak) => NeedsEncouragement
   NeedsEncouragement => Message2 v Message4
   IsBored => Message3 v Message5
   (NewSkill & CorrectAnswer) v CorrectStreak => Message1

should use resolution to decide what feedback message to give
lower number messages have higher priority


"""

M1 = 'Correct. Keep up the good work!'
M2 = 'Correct. I think you’re getting it!'
M3 = 'Correct. After this problem we can switch to a new problem.'
M4 = 'Incorrect. Keep trying and I’m sure you’ll get it!'
M5 = 'Incorrect. After this problem, we can switch to a new activity.'
M6 = 'Incorrect. The following is the correct answer to the problem.'
M7 = 'Correct.'
M8 = 'Incorrect.'

messageList = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']

S1 = 'add a positive variable term to both sides'  # (e.g., add 3x to both sides)
S2 = 'add a negative variable term to both sides'  # (e.g., add -3x to both sides)
S3 = 'add a positive constant term to both sides'  # (e.g., add +3 to both sides)
S4 = 'add a negative constant term from both sides'  # (e.g., add -3 to both sides)
S5 = 'divide both sides by a positive constant'  # (e.g., divide by 3)
S6 = 'divide both sides by a negative constant'  # (e.g., divide by -3)
S7 = 'combine two variable terms on a side to get a positive number'  # (e.g., combine 3x+6x to make 9x)
S8 = 'combine two variable terms on a side to get a negative number'  # (e.g., combine 3x-6x to make -9x)
S9 = 'combine two constant terms'  # (e.g., combine 3-6 to make -3)

#add if right side is just one constant or variable
#add if left side is just one constant or variable

def main():
    giveFeedback("IncorrectStreak & CorrectAnswer")
    solveEquation("3x+2=6+3x")
    predictSuccess(['S8', 'S9'], '3+5x=8+3')
    stepThroughProblem("3x+2=8", "add -2", ['S8', 'S9'])


feedback_KB = logic.PropKB()
class createKB(logic.PropKB):
    CorrectAnswer, NewSkill, MasteredSkill, CorrectStreak, IncorrectStreak, NeedsEncouragement, IsBored, M1, M2, M3, M4, M5, M6, M7, M8 = logic.expr(
        'CorrectAnswer, NewSkill, MasteredSkill, CorrectStreak, IncorrectStreak, NeedsEncouragement, IsBored, M1, M2, M3, M4, M5, M6, M7, M8')
    feedback_KB.tell(CorrectAnswer | '==>' | M1 | M2)
    feedback_KB.tell(CorrectAnswer | "==>" | (~M4 & ~M5))
    feedback_KB.tell(~CorrectAnswer | "==>" | (~M2 & ~M3))
    feedback_KB.tell(~CorrectAnswer | '==>' | M4)
    feedback_KB.tell((MasteredSkill & ~CorrectAnswer) | (MasteredSkill & CorrectStreak) | '==>' | IsBored)
    feedback_KB.tell(NewSkill | IncorrectStreak | '==>' | M6)
    feedback_KB.tell((IncorrectStreak & CorrectAnswer) | (NewSkill & CorrectStreak) | '==>' | NeedsEncouragement)
    feedback_KB.tell(NeedsEncouragement | '==>' | M2)
    feedback_KB.tell(IsBored | '==>' | M3)
    feedback_KB.tell(((NewSkill & CorrectAnswer) | CorrectStreak) | '==>' | M1)


def giveFeedback(studentState):
    feedback_KB.tell(logic.expr(studentState))
    if studentState == "CorrectAnswer":
        feedbackMessage = M7
    elif studentState == "~CorrectAnswer":
        feedbackMessage = M8
    if studentState.__contains__("~CorrectAnswer"):
        if logic.pl_resolution(feedback_KB, logic.expr('M4')):
            feedbackMessage = M4
        elif logic.pl_resolution(feedback_KB, logic.expr('M5')):
            feedbackMessage = M5
        elif logic.pl_resolution(feedback_KB, logic.expr('M6')):
            feedbackMessage = M6
        elif logic.pl_resolution(feedback_KB, logic.expr('M8')):
            feedbackMessage = M8
    elif studentState.__contains__("Correct"):
        if logic.pl_resolution(feedback_KB, logic.expr('M1')):
            feedbackMessage = M1
        elif logic.pl_resolution(feedback_KB, logic.expr('M2')):
            feedbackMessage = M2
        elif logic.pl_resolution(feedback_KB, logic.expr('M3')):
            feedbackMessage = M3
        elif logic.pl_resolution(feedback_KB, logic.expr('M7')):
            feedbackMessage = M7
    else:
        if logic.pl_resolution(feedback_KB, logic.expr('M1')):
            feedbackMessage = M1
        elif logic.pl_resolution(feedback_KB, logic.expr('M2')):
            feedbackMessage = M2
        elif logic.pl_resolution(feedback_KB, logic.expr('M3')):
            feedbackMessage = M3
        if logic.pl_resolution(feedback_KB, logic.expr('M4')):
            feedbackMessage = M4
        elif logic.pl_resolution(feedback_KB, logic.expr('M5')):
            feedbackMessage = M5
        elif logic.pl_resolution(feedback_KB, logic.expr('M6')):
            feedbackMessage = M6
        elif logic.pl_resolution(feedback_KB, logic.expr('M7')):
            feedbackMessage = M7
        elif logic.pl_resolution(feedback_KB, logic.expr('M8')):
            feedbackMessage = M8
    #print(feedbackMessage)
    return feedbackMessage

""" A2 Part B

    solveEquation is a function that converts a string representation of an equation to a 
    first-order logic representation, and then
    uses a forward planning algorithm to solve the equation. 
    planning.py -- forward planning algorithm

    equation:   a String representing the equation to be solved. 
    "x=3", "-3x=6", "3x-2=6", "4+3x=6x-7" are all possible Strings.
                For example, you could call solveEquation('x=6') or solveEquation('-3x=6')

    plan:   return a list of Strings, where each String is a step in the plan. The Strings should reference the core actions described in the
            Task Domain part of the assignment description.

"""
firstLeftNeg = None
def solveEquation(equation):
    initExprL = ""
    initExpr = ""
    preCondDivR = ""
    preCondCombAdd = ""
    preCondDivL = ""
    preCondAdd = ""
    combineConstExprLeft = ""
    combineVarsExprLeftPos = ""
    combineVarsExprLeftNeg = ""
    combineConstExprRight = ""
    combineVarsExprLeftPos = ""
    combineVarsExprLeftNeg = ""
    values = equation.split("=")
    leftSide = values[0]
    rightSide = values[1]
    for terms in leftSide:
        if terms == "+":
            termVals = leftSide.split("+")
            # IF FIRST VALUE IN EQUATION ON LEFT SIDE IS X
            if termVals[0].__contains__("x"):
                xVal = termVals[0]
                coef1 = xVal.split("x")
                initExpr = "Coef(" + coef1[0] + ", left)"
                # IF SECOND VALUE AFTER + ALSO CONTAINS AN X (3x+2X)
                if termVals[1].__contains__("x"):
                    xVal = termVals[1]
                    coef2 = xVal.split("x")
                    initExpr += " & Coef(" + coef2[0] + ", left)"
                    combinedCoef = int(coef1[0]) + int(coef2[0])
                    #PRECONDITION FOR COMBINING VARIABLES ON LEFT
                    if (combinedCoef > 0):
                        combineVarsExprLeftPos = "CombineVarsLeftPos(" + coef1[0] + ", " + coef2[0] + ")"
                        initExpr += " & " + combineVarsExprLeftPos
                    else:
                        combineVarsExprLeftNeg = "CombineVarsLeftNeg(" + coef1[0] + ", " + coef2[0] + ")"
                        initExpr += " & " + combineVarsExprLeftNeg
                    #PRECONDITION FOR DIVIDING IS THAT THERE IS A COEFFICIENT ON THE LEFT
                    preCondDivL = "Coef(" + str(combinedCoef) + ", left)"
                    divCond = combinedCoef
                    addCond = 0
                # IF SECOND VALUE AFTER + IS A CONSTANT (3x+2)
                else:
                    const = termVals[1]
                    preCondDivL = "Coef(" + coef1[0] + ", left)"
                    divCond = coef1[0]
                    preCondAdd = "Const(" + const + ", left)"
                    addCond = const
                    initExpr += " & Const(" + const + ", left)"
            #IF FIRST TERM IS A CONST
            else:
                const1 = termVals[0]
                initExpr = "Const(" + const1 + ", left)"
                #SECOND TERM IS VARIABLE -- (3+2x)
                if termVals[1].__contains__("x"):
                    coef = termVals[1].split("x")
                    preCondAdd = "Const(" + const1 + ", left)"
                    addCond = const1
                    preCondDivL = "Coef(" + coef[0] + ", left)"
                    divCond = coef[0]
                    initExpr += " & Coef(" + coef[0] + ", left)"
                #SECOND TERM IS ALSO A CONST (3+2)
                else:
                    const2 = termVals[1]
                    initExpr += " & Const(" + const2 + ", left)"
                    #PRECONDITION FOR COMBINING CONST ON LEFT
                    combineConstExprLeft = "CombineConstExprLeft(" + const1 + ", " + const2 + ")"
                    combinedConst = int(const1) + int(const2)
                    preCondAdd = "Const(" + const1 + ", left)"
                    addCond = const1
                    preCondCombAdd = "Const(" + str(combinedConst) + ", left)"
                    combineCondAdd = combinedConst
                    initExpr += " & " + combineConstExprLeft
        elif terms == "-" and terms!= leftSide[0][0]:
            termVals = leftSide.split("-")
            # IF FIRST VALUE IN EQUATION ON LEFT SIDE IS A NEG VAR
            if termVals[0] == "":
                termVals[0] += "-"
                #IF FIRST TERM IS A NEG VARIABLE
                if termVals[1].__contains__("x"):
                    xVal = termVals[1].split("x")
                    coef1 = termVals[0] + xVal[0]
                    initExpr = "Coef(" + coef1 + ", left)"
                    #IF SECOND TERM IS A VARIABLE
                    if termVals[2].__contains__("x"):
                        xVal = termVals[2]
                        co = xVal.split("x")
                        coef2 = "-" + co[0]
                        initExpr += " & Coef(" + coef2 + ", left)"
                        combinedCoef = int(coef1) + int(coef2)
                        #COMBINE THE VARIABLES ON LEFT SIDE
                        if (combinedCoef > 0):
                            combineVarsExprLeftPos = "CombineVarsLeftPos(" + coef1 + ", " + coef2 + ")"
                            initExpr += " & " + combineVarsExprLeftPos
                        else:
                            combineVarsExprLeftNeg = "CombineVarsLeftNeg(" + coef1 + ", " + coef2 + ")"
                            initExpr += " & " + combineVarsExprLeftNeg
                        preCondDivL = "Coef(" + str(combinedCoef) + ", left"
                        divCond = combinedCoef
                    # IF SECOND TERM IS A CONSTANT
                    else:
                        const = "-" + termVals[2]
                        preCondDivL = "Coef(" + coef1 + ", left)"
                        divCond = coef1
                        preCondAdd = "Const(" + const + ", left)"
                        addCond = const
                        initExpr += " & Const(" + const + ", left)"
                # IF FIRST TERM IS A NEG CONSTANT
                else:
                    const1 = "-" + termVals[1]
                    initExpr = "Const(" + const1 + ", left)"
                    # IF SECOND TERM IS A VARIABLE
                    if termVals[2].__contains__("x"):
                        xVal = termVals[2].split("x")
                        coef = "-" + xVal[0]
                        initExpr += " & Coef(" + coef + ", left)"
                        preCondDivL = "Coef(" + coef + ", left"
                        divCond = coef
                        preCondAdd = "Const(" + const1 + ", left"
                        addCond = const1
                    # IF SECOND TERM IS ALSO A NEGATIVE CONSTANT
                    else:
                        const2 = "-" + termVals[2]
                        initExpr += " & Const(" + const2 + ", left)"
                        combineConstExprLeft = "CombineConstExprLeft(" + const1 + ", " + const2 + ")"
                        combinedConst = int(const1) + int(const2)
                        combineCondAdd = combinedConst
                        preCondAdd = "Const(" + str(combinedConst) + ", left)"
                        initExpr += " & " + combineConstExprLeft
            else:
                if termVals[0].__contains__("x"):
                    xVal = termVals[0].split("x")
                    coef1 = termVals[1] + xVal[0]
                    initExpr = "Coef(" + coef1 + ", left)"
                    # IF SECOND TERM IS A VARIABLE
                    if termVals[1].__contains__("x"):
                        xVal = termVals[1]
                        co = xVal.split("x")
                        coef2 = "-" + co[0]
                        initExpr += " & Coef(" + coef2 + ", left)"
                        combinedCoef = int(coef1) + int(coef2)
                        # COMBINE THE VARIABLES ON LEFT SIDE
                        if (combinedCoef > 0):
                            combineVarsExprLeftPos = "CombineVarsLeftPos(" + coef1 + ", " + coef2 + ")"
                            initExpr += " & " + combineVarsExprLeftPos
                        else:
                            combineVarsExprLeftNeg = "CombineVarsLeftNeg(" + coef1 + ", " + coef2 + ")"
                            initExpr += " & " + combineVarsExprLeftNeg
                        preCondDivL = "Coef(" + str(combinedCoef) + ", left"
                    # IF SECOND TERM IS A CONSTANT
                    else:
                        const = "-" + termVals[1]
                        preCondDivL = "Coef(" + coef1 + ", left)"
                        divCond = coef1
                        preCondAdd = "Const(" + const + ", left)"
                        addCond = const
                        initExpr += " & Const(" + const + ", left)"
                    # IF FIRST TERM IS A NEG CONSTANT
                else:
                    const1 = "-" + termVals[0]
                    initExpr = "Const(" + const1 + ", left)"
                    # IF SECOND TERM IS A VARIABLE
                    if termVals[1].__contains__("x"):
                        xVal = terms[1].split("x")
                        coef = "-" + xVal[0]
                        initExpr += " & Coef(" + xVal[0] + ", left)"
                        preCondDivL = "Coef(" + xVal[0] + ", left"
                        divCond = xVal[0]
                        preCondAdd = "Const(" + const1 + ", left"
                        addCond = const1
                    # IF SECOND TERM IS ALSO A NEGATIVE CONSTANT
                    else:
                        const2 = "-" + termVals[1]
                        initExpr = " & Const(" + const2 + ", left)"
                        combineConstExprLeft = "CombineConstExprLeft(" + const1 + ", " + const2 + ")"
                        combinedConst = int(const1) + int(const2)
                        preCondAdd = "Const(" + str(combinedConst) + ", left)"
                        initExpr += " & " + combineConstExprLeft
        else:
            if len(leftSide) < 4:
                if leftSide.__contains__("x"):
                    xVal = leftSide.split("x")
                    initExpr = "Coef(" + xVal[0] + ", left) & Const(0, left)"
                    preCondDivL = "Coef(" + xVal[0] + ", left)"
                    preCondAdd = "Const(0, left)"
                    addCond = str(0)
                    divCond = str(xVal[0])
                elif leftSide == "x":
                    initExpr = "Coef(1, left)"
                else:
                    initExpr = "Const(" + leftSide + ", left)"
                    preCondAdd = "Const(" + leftSide + ", left)"
    for terms in rightSide:
        if terms == "+":
            termVals = rightSide.split("+")
            # IF FIRST VALUE IN EQUATION ON LEFT SIDE IS X
            if termVals[0].__contains__("x"):
                xVal = termVals[0]
                coef1 = xVal.split("x")
                initExprR = "Coef(" + coef1[0] + ", right)"
                # IF SECOND VALUE AFTER + ALSO CONTAINS AN X (3x+2X)
                if termVals[1].__contains__("x"):
                    xVal = termVals[1]
                    coef2 = xVal.split("x")
                    initExpr += " & Coef(" + coef2[0] + ", right)"
                    combinedCoef = int(coef1[0]) + int(coef2[0])
                    #PRECONDITION FOR COMBINING VARIABLES ON LEFT
                    if (combinedCoef > 0):
                        combineVarsExprRightPos = "CombineVarsRightPos(" + coef1[0] + ", " + coef2[0] + ")"
                        initExprR += " & " + combineVarsExprRightPos
                    else:
                        combineVarsExprRightNeg = "CombineVarsRightNeg(" + coef1[0] + ", " + coef2[0] + ")"
                        initExprR += " & " + combineVarsExprRightNeg
                    #PRECONDITION FOR DIVIDING IS THAT THERE IS A COEFFICIENT ON THE LEFT
                    preCondDivL = "Coef(" + str(combinedCoef) + ", right)"
                    divCond = combinedCoef
                # IF SECOND VALUE AFTER + IS A CONSTANT (3x+2)
                else:
                    const = termVals[1]
                    preCondDivL = "Coef(" + coef1[0] + ", right)"
                    divCond = coef1[0]
                    preCondAdd = "Const(" + const + ", right)"
                    #addCond = const
                    initExprR += " & Const(" + const + ", right)"
            #IF FIRST TERM IS A CONST
            else:
                const1 = termVals[0]
                initExprR = "Const(" + const1 + ", right)"
                #SECOND TERM IS VARIABLE -- (3+2x)
                if termVals[1].__contains__("x"):
                    coef = termVals[1].split("x")
                    preCondAdd = "Const(" + const1 + ", right)"
                    #addCond = const1
                    preCondDivL = "Coef(" + coef[0] + ", right)"
                    divCond = coef[0]
                    initExprR += " & Coef(" + coef[0] + ", right)"
                #SECOND TERM IS ALSO A CONST (3+2)
                else:
                    const2 = termVals[1]
                    initExprR += " & Const(" + const2 + ", right)"
                    #PRECONDITION FOR COMBINING CONST ON LEFT
                    combineConstExprRight = "CombineConstExprRight(" + const1 + ", " + const2 + ")"
                    combinedConst = int(const1) + int(const2)
                    preCondAdd = "Const(" + const1 + ", right)"
                    #addCond = const1
                    preCondCombAdd = "Const(" + str(combinedConst) + ", right)"
                    combineCondAdd = combinedConst
                    initExprR += " & " + combineConstExprLeft
        elif terms == "-":
            termVals = rightSide.split("-")
            # IF FIRST VALUE IN EQUATION ON LEFT SIDE IS A NEG VAR
            if termVals[0] == "":
                termVals[0] += "-"
                #IF FIRST TERM IS A NEG VARIABLE
                if termVals[1].__contains__("x"):
                    xVal = termVals[1].split("x")
                    coef1 = termVals[0] + xVal[0]
                    initExprR = "Coef(" + coef1 + ", right)"
                    #IF SECOND TERM IS A VARIABLE
                    if termVals[2].__contains__("x"):
                        xVal = termVals[2]
                        co = xVal.split("x")
                        coef2 = "-" + co[0]
                        initExprR += " & Coef(" + coef2 + ", right)"
                        combinedCoef = int(coef1) + int(coef2)
                        #COMBINE THE VARIABLES ON LEFT SIDE
                        if (combinedCoef > 0):
                            combineVarsExprRightPos = "CombineVarsRightPos(" + coef1 + ", " + coef2 + ")"
                            initExprR += " & " + combineVarsExprRightPos
                        else:
                            combineVarsExprRightNeg = "CombineVarsRightNeg(" + coef1 + ", " + coef2 + ")"
                            initExprR += " & " + combineVarsExprRightNeg
                        preCondDivL = "Coef(" + str(combinedCoef) + ", right)"
                        divCond = combinedCoef
                    # IF SECOND TERM IS A CONSTANT
                    else:
                        const = "-" + termVals[2]
                        preCondDivL = "Coef(" + coef1 + ", right)"
                        divCond = coef1
                        preCondAdd = "Const(" + const + ", right)"
                        #addCond = const
                        initExprR += " & Const(" + const + ", right)"
                # IF FIRST TERM IS A NEG CONSTANT
                else:
                    const1 = "-" + termVals[1]
                    initExprR = "Const(" + const1 + ", right)"
                    # IF SECOND TERM IS A VARIABLE
                    if termVals[2].__contains__("x"):
                        xVal = termVals[2].split("x")
                        coef = "-" + xVal[0]
                        initExprR += " & Coef(" + coef + ", right)"
                        preCondDivL = "Coef(" + coef + ", right)"
                        divCond = coef
                        preCondAdd = "Const(" + const1 + ", right)"
                        #addCond = const1
                    # IF SECOND TERM IS ALSO A NEGATIVE CONSTANT
                    else:
                        const2 = "-" + termVals[2]
                        initExprR += " & Const(" + const2 + ", right)"
                        combineConstExprRight = "CombineConstExprRight(" + const1 + ", " + const2 + ")"
                        combinedConst = int(const1) + int(const2)
                        combineCondAdd = combinedConst
                        preCondAdd = "Const(" + str(combinedConst) + ", right)"
                        initExprR += " & " + combineConstExprRight
            else:
                if termVals[0].__contains__("x"):
                    xVal = termVals[0].split("x")
                    coef1 = termVals[1] + xVal[0]
                    initExprR = "Coef(" + coef1 + ", right)"
                    # IF SECOND TERM IS A VARIABLE
                    if termVals[1].__contains__("x"):
                        xVal = termVals[1]
                        co = xVal.split("x")
                        coef2 = "-" + co[0]
                        initExprR += " & Coef(" + coef2 + ", right)"
                        combinedCoef = int(coef1) + int(coef2)
                        # COMBINE THE VARIABLES ON LEFT SIDE
                        if (combinedCoef > 0):
                            combineVarsExprRightPos = "CombineVarsRightPos(" + coef1 + ", " + coef2 + ")"
                            initExprR += " & " + combineVarsExprRightPos
                        else:
                            combineVarsExprRightNeg = "CombineVarsRightNeg(" + coef1 + ", " + coef2 + ")"
                            initExprR += " & " + combineVarsExprRightNeg
                        preCondDivL = "Coef(" + str(combinedCoef) + ", right)"
                    # IF SECOND TERM IS A CONSTANT
                    else:
                        const = "-" + termVals[1]
                        preCondDivL = "Coef(" + coef1 + ", right)"
                        divCond = coef1
                        preCondAdd = "Const(" + const + ", right)"
                        #addCond = const
                        initExprR += " & Const(" + const + ", right)"
                    # IF FIRST TERM IS A NEG CONSTANT
                else:
                    const1 = "-" + termVals[0]
                    initExprR = "Const(" + const1 + ", right)"
                    # IF SECOND TERM IS A VARIABLE
                    if termVals[1].__contains__("x"):
                        xVal = terms[1].split("x")
                        coef = "-" + xVal[0]
                        initExprR += " & Coef(" + xVal[0] + ", right)"
                        preCondDivL = "Coef(" + xVal[0] + ", right)"
                        divCond = xVal[0]
                        preCondAdd = "Const(" + const1 + ", right)"
                        #addCond = const1
                    # IF SECOND TERM IS ALSO A NEGATIVE CONSTANT
                    else:
                        const2 = "-" + termVals[1]
                        initExprR = " & Const(" + const2 + ", right)"
                        combineConstExprRight = "CombineConstExprRight(" + const1 + ", " + const2 + ")"
                        combinedConst = int(const1) + int(const2)
                        preCondAdd = "Const(" + str(combinedConst) + ", right)"
                        initExprR += " & " + combineConstExprRight
        else:
            if len(rightSide) < 3:
                if rightSide.__contains__("x"):
                    xVal = rightSide.split("x")
                    initExprR = "Coef(" + xVal[0] + ", right)"
                    preCondDivL = "Coef(" + str(xVal[0]) + ", right)"
                    divCond = str(xVal[0])
                elif rightSide == "x":
                    initExprR = "Coef(1, right)"
                else:
                    initExprR = "Const(" + rightSide + ", right)"
                    preCondAdd = "Const(" + str(rightSide) + ", right)"
                    #addCond = rightSide
                    divCond = str(1)
        addCond = str(0)
    # print(preCondAdd)
    # print(preCondDivL)
    # print(addCond)
    # print(divCond)
    initExpr += " & " + initExprR
    initExpr += " & ~Coef(1, left)"
    # print(initExpr)

    plan_prob = planning.PlanningProblem(initial=initExpr, goals='Coef(1, left)', actions=[planning.Action('Add(x)',
                                                                                                           precond=preCondAdd + " & " + preCondDivL,
                                                                                                           effect="~" + preCondAdd,
                                                                                                           domain="addCond(x)"),
                                                                                           planning.Action('AddVar(x)',
                                                                                                           precond = "Coef(3, left) & Coef(3, right)",
                                                                                                           effect= "~Coef(3, left) & ~Coef(3, right)",
                                                                                                           domain="addVarCond(x)"),
                                                                                           planning.Action('Divide(x)',
                                                                                                           precond=preCondDivL + " & ~Coef(1, left) " + " & ~" + preCondAdd,
                                                                                                           effect="~" + preCondDivL + " & Coef(1, left)",
                                                                                                           domain="divCond(x)")],
                                                                                           # planning.Action('CombineConst(x, y)',
                                                                                           #                 precond= combineConstExprLeft,
                                                                                           #                 effect= "~" + combineConstExprLeft,
                                                                                           #                 domain='combineCond(x, y)'),
                                                                                           # planning.Action('CombineLHSVars2Pos(x, y)',
                                                                                           #                 precond=combineVarsExprLeftPos,
                                                                                           #                 effect="~" + combineVarsExprLeftPos),
                                                                                           # planning.Action("CombineLHSVars2Neg(x, y)",
                                                                                           #                 precond=combineVarsExprLeftNeg,
                                                                                           #                 effect="~" + combineVarsExprLeftNeg),
                                                                                           # planning.Action("CombineRHSVars2Pos(x, y)",
                                                                                           #                 precond=combineVarsExprRightPos,
                                                                                           #                 effect="~" + combineVarsExprRightPos),
                                                                                           # planning.Action("CombineRHSVars2Neg(x, y)",
                                                                                           #                 precond=combineVarsExprRightNeg,
                                                                                           #                 effect="~" + combineVarsExprRightNeg)],

                                         domain='addCond(' + addCond +') & divCond(' + divCond + ') & addVarCond(3)')

    planning_prob = planning.ForwardPlan(plan_prob)
    # print(planning_prob.initial)
    # initial_actions = planning_prob.actions(planning_prob.initial)
    # print(initial_actions)
    # state2 = planning_prob.result(planning_prob.initial, initial_actions[0])
    # print(planning_prob.actions(state2))
    solution = search.breadth_first_graph_search(planning_prob)
    plan = []
    parentNode = solution.parent
    if combineConstExprLeft:
        plan.append("combine LHS constant terms")
    if combineVarsExprLeftNeg:
        plan.append("combine LHS variable terms to neg")
    if combineVarsExprLeftPos:
        plan.append("combine LHS variable terms to pos")
    if combineConstExprRight:
        plan.append("combine RHS constant terms")
    # if combineVarsExprRightNeg:
    #     plan.append("combine RHS variable terms to neg")
    # if combineVarsExprRightPos:
    #     plan.append("combine RHS variable terms to pos")
    while(parentNode):
        #print(solution.parent.action)
        parentNode = parentNode.parent.parent
    plan.append(str(solution.parent.action))
    plan.append(str(solution.action))
    #print(solution.action)
    #print(plan)
    return plan

""" A2 Part C

    predictSuccess is a function that takes in a list of skills students have and an equation to be solved, and returns the skills
    students need but do not currently have in order to solve the skill. For example, if students are solving the problem 3x+2=8, and have S7 and S8, 
    they would still need S4 and S5 to solve the problem.

    current_skills: A list of skills students currently have, represented by S1 through S9 (described in the assignment description)

    equation:   a String representing the equation to be solved. "x=3", "-3x=6", "3x-2=6", "4+3x=6x-7" are all possible Strings.
                For example, you could call solveEquation('x=6') or solveEquation('-3x=6')

    missing_skills: A list of skills students need to solve the problem, represented by S1 through S9.

"""
CURRENT_SKILLS = ['S8', 'S9']
EQUATION = '3x+2=8'
SAMPLE_MISSING_SKILLS = ['S4', 'S5']

def formulateProblem(equation, current_skills):
    AddPosVar = AddNegVar = AddPosConst = AddNegConst = DivPosConst = DivNegConst = CombVar2Pos = CombVar2Neg = CombConst = False
    values = equation.split("=")
    leftSide = values[0]
    rightSide = values[1]
    for terms in leftSide:
        if terms == "+":
            termVals = leftSide.split("+")
            if termVals[0].__contains__("x"):
                DivPosConst = True
                if termVals[1].__contains__("x"):
                    CombVar2Pos = True
                else:
                    AddNegConst = True
            else:
                AddNegConst = True
                if termVals[1].__contains__("x"):
                    DivPosConst = True
                else:
                    CombConst = True
        elif terms == "-":
            termVals = leftSide.split("-")
            if termVals[0].__contains__("x"):
                xVal = termVals[0]
                for num in xVal:
                    if num.isdigit():
                        coef1 = num
                        DivPosConst = True
                if termVals[1].__contains__("x"):
                    xVal2 = termVals[1]
                    for num in xVal2:
                        if num.isdigit():
                            coef2 = "-" + num
                            if (int(coef1) + int(coef2) > 0):
                                CombVar2Pos = True
                                DivPosConst = True
                            else:
                                CombVar2Neg = True
                                DivNegConst = True
                else:
                    AddPosConst = True
            else:
                AddNegConst = True
                if termVals[1].__contains__("x"):
                    DivNegConst = True
                else:
                    CombConst = True
    for terms in rightSide:
        if terms == "+":
            termVals = rightSide.split("+")
            if termVals[0].__contains__("x"):
                AddNegVar = True
                if termVals[1].__contains__("x"):
                    xVal2 = termVals[1]
                    for num in xVal2:
                        if num.isdigit():
                            CombVar2Pos = True
            else:
                if termVals[1].__contains__("x"):
                    AddNegVar = True
                else:
                    CombConst = True
        elif terms == "-":
            termVals = rightSide.split("-")
            if termVals[0].__contains__("x"):
                AddNegVar = True
                for num in xVal:
                    if num.isdigit():
                        coef1 = num
                if termVals[1].__contains__("x"):
                            coef2 = "-" + num
                            if (int(coef1) + int(coef2) > 0):
                                CombVar2Pos = True
                            else:
                                CombVar2Neg = True
            else:
                if termVals[1].__contains__("x"):
                    AddPosVar = True
                else:
                    CombConst = True

    return formulateProps(AddPosVar, AddNegVar, AddPosConst, AddNegConst, DivPosConst, DivNegConst, CombVar2Pos,
                           CombVar2Neg, CombConst)


def formulateProps(AddPosVar, AddNegVar, AddPosConst, AddNegConst, DivPosConst, DivNegConst, CombVar2Pos, CombVar2Neg, CombConst):
    skills_list = []
    if AddPosVar == True:
        skills_list.append("AddPosVar")
    if AddNegVar == True:
        skills_list.append("AddNegVar")
    if AddPosConst == True:
        skills_list.append("AddPosConst")
    if AddNegConst == True:
        skills_list.append("AddNegConst")
    if DivPosConst == True:
        skills_list.append("DivPosConst")
    if DivNegConst == True:
        skills_list.append("DivNegConst")
    if CombVar2Pos == True:
        skills_list.append("CombVar2Pos")
    if CombVar2Neg == True:
        skills_list.append("CombVar2Neg")
    if CombConst == True:
        skills_list.append("CombConst")

    return skills_list

skills_kb = logic.PropKB()
class successKB(logic.PropKB):
    AddPosVar, AddNegVar, AddPosConst, AddNegConst, DivPosConst, DivNegConst, CombVar2Pos, CombVar2Neg, CombConst, S1, S2, S3, S4, S5, S6, S7, S8, S9 = logic.expr('AddPosVar, AddNegVar, AddPosConst, AddNegConst, DivPosConst, DivNegConst, CombVar2Pos, CombVar2Neg, '
                                                                            'CombConst, S1, S2, S3, S4, S5, S6, S7, S8, S9')
    skills_kb.tell(AddPosVar | "==>" | S1)
    skills_kb.tell(AddNegVar | "==>" | S2)
    skills_kb.tell(AddPosConst | "==>" | S3)
    skills_kb.tell(AddNegConst | "==>" | S4)
    skills_kb.tell(DivPosConst | "==>" | S5)
    skills_kb.tell(DivNegConst | "==>" | S6)
    skills_kb.tell(CombVar2Pos | "==>" | S7)
    skills_kb.tell(CombVar2Neg | "==>" | S8)
    skills_kb.tell(CombConst | "==>" | S9)

def predictSuccess(current_skills, equation):
    missing_skills = []
    skillsNeeded = formulateProblem(equation, current_skills)
    for skill in skillsNeeded:
        skills_kb.tell(skill)
        if skill == "AddPosVar":
            resolution = logic.pl_resolution(skills_kb, logic.expr('S1'))
            if resolution == True:
                missing_skills.append('S1')
        if skill == "AddNegVar":
            resolution = logic.pl_resolution(skills_kb, logic.expr('S2'))
            if resolution == True:
                missing_skills.append('S2')
        if skill == "AddPosConst":
            resolution = logic.pl_resolution(skills_kb, logic.expr('S3'))
            if resolution == True:
                missing_skills.append('S3')
        if skill == 'AddNegConst':
            resolution = logic.pl_resolution(skills_kb, logic.expr('S4'))
            if resolution == True:
                missing_skills.append('S4')
        if skill == 'DivPosConst':
            resolution = logic.pl_resolution(skills_kb, logic.expr('S5'))
            if resolution == True:
                missing_skills.append('S5')
        if skill == 'DivNegConst':
            resolution = logic.pl_resolution(skills_kb, logic.expr('S6'))
            if resolution == True:
                missing_skills.append('S6')
        if skill == 'CombVar2Pos':
            resolution = logic.pl_resolution(skills_kb, logic.expr('S7'))
            if resolution == True:
                missing_skills.append('S7')
        if skill == 'CombVar2Neg':
            resolution = logic.pl_resolution(skills_kb, logic.expr('S8'))
            if resolution == True:
                missing_skills.append('S8')
        if skill == 'CombConst':
            resolution = logic.pl_resolution(skills_kb, logic.expr('S9'))
            if resolution == True:
                missing_skills.append('S9')
    for curr_skill in current_skills:
        if missing_skills.__contains__(curr_skill):
            missing_skills.remove(curr_skill)
    #print(missing_skills)
    return missing_skills


""" A2 Part D
    stepThroughProblem is a function that takes a problem, a student action, and a list of current student skills, and returns
    a list containing a feedback message to the student and their updated list of skills.

    equation: a String representing the equation to be solved. "x=3", "-3x=6", "3x-2=6", "4+3x=6x-7" are all possible Strings.

    action: an action in the task domain. For example: 'add 2', 'combine RHS constant terms', 'divide 3'

    current_skills: A list of skills students currently have, represented by S1 through S9 (described in the assignment description)

    feedback_message: A feedback message chosen correctly from M1-M9.

    updated_skills: A list of skills students have after executing the action.

"""
CURRENT_SKILLS = ['S8', 'S9']
EQUATION = '3x+2=8'
ACTION = 'add -2'
UPDATED_SKILLS = ['S8', 'S9', 'S4']


def stepThroughProblem(equation, action, current_skills):
    stepThrough = solveEquation(equation)
    skillsNeeded = predictSuccess(current_skills, equation)
    skillDone = ""
    updated_skills = []
    if action.__contains__("add"):
        values = action.split(" ")
        value = values[1]
        if stepThrough[0].__contains__("Add"):
            if value.__contains__("-"):
                skillDone = "S4"
            else:
                skillDone = "S5"
        feedback_message = giveFeedback("CorrectAnswer")
    elif action.__contains__("divide"):
        values = action.split(" ")
        value = values[1]
        if stepThrough[0].__contains__("Divide"):
            if value.__contains__("-"):
                skillDone = "S6"
            else:
                skillDone = "S5"
        feedback_message = giveFeedback("CorrectAnswer")
    elif action.__contains__("combine") and action.__contains__("positive"):
        skillDone = "S7"
    elif action.__contains__("combine") and action.__contains__("negative"):
        skillDone = "S8"
    elif action.__contains__("combine") and action.__contains__("constant"):
        skillDone = "S9"
        feedback_message = giveFeedback("CorrectAnswer")
    else:
        feedbackMessage = giveFeedback("IncorrectAnswer")

    #print(skillDone)
    current_skills.append(str(skillDone))
    updated_skills = current_skills
    #updated_skills = current_skills.append(str(skillDone))
    #print(updated_skills)
    #print(feedback_message)
    return [feedback_message, updated_skills]


if __name__ == '__main__':
    main()
