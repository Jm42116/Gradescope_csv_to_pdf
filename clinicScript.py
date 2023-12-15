import sys
import argparse
import PyPDF2
from fpdf import FPDF
import csv
import os
import re
import os.path
import shutil

def generatePDFS(dictionary, outputPath, inputPath):
    dirname = os.path.dirname(os.path.abspath(__file__))
    outputPath = os.path.join(dirname, outputPath)
    print("OUTPUT PATH AFTER EDITING IS ")
    print(outputPath)
    # AllFiles = list(os.walk(outputPath))
    print("NEW PATH BEING CREATED IS ")
    print(os.path.join(outputPath, "clinicTeams/"))
    if not os.path.exists(os.path.join(outputPath, "clinicTeams/")):
        os.mkdir(outputPath)
        os.mkdir(os.path.join(outputPath, "clinicTeams/"))
        
    submissionIds = dictionary.keys()

    for submissionID in submissionIds:
        teamName = dictionary[submissionID]["team"]
        teamNames = dictionary[submissionID]["names"]

        teamEmails = dictionary[submissionID]["emails"]
    
        # currentDir = list(os.walk(os.path.join(outputPath, "/clinicTeams/")))

        if not os.path.exists(os.path.join(outputPath, "clinicTeams/", teamName)):
            print("NEWEST OUTPUT PATH IS ")
            print(os.path.join(outputPath, "clinicTeams/", teamName))
            os.mkdir(os.path.join(outputPath, "clinicTeams/", teamName))
        for email in teamEmails:
            if not os.path.exists(os.path.join(outputPath, "clinicTeams/", teamName, email)):
                os.mkdir(os.path.join(outputPath, "clinicTeams/", teamName, email))
        if len(teamNames) > 1:
            OutputPDF(dictionary, submissionID,os.path.join(outputPath, "clinicTeams/", teamName))
        else:
            OutputPDF(dictionary, submissionID, os.path.join(outputPath, "clinicTeams/", teamName, email))

    





def OutputPDF(dictionary, pdfSubmissionID, directory):
    pdf = FPDF()
    pdf.add_page()
    questionsList = []

    leftMargin = 0
    logoSize = 60
    iconSize = 20
    smallerIconSize = 16
    allocatedAnswerPercentage = 0.7
    
        ## Left margin by default is 10
    ## Right margin: 200

    def writeHMCLogo(width):
        pdf.set_xy(leftMargin, leftMargin)
        pdf.image("HMC.svg", w = width, h = width)
        pdf.set_xy(width + leftMargin + 10, leftMargin + 10)
        pdf.set_fill_color(0, 0, 0)
        pdf.add_font('Roboto', '', 'Roboto-Medium.ttf', uni=True)
        pdf.set_font('Roboto', size=48)

    writeHMCLogo(logoSize)

    assignmentName = dictionary[pdfSubmissionID]["displayedAssignmentName"]
    teamName = dictionary[pdfSubmissionID]['team']
    teamNames = dictionary[pdfSubmissionID]['names']
    questionsFlagged = False
    commentsLeft = False

    for key in dictionary[pdfSubmissionID]["responses"].keys():
        if dictionary[pdfSubmissionID]["responses"][key]["flagged"] == True:
            questionsFlagged = True
        if len(dictionary[pdfSubmissionID]["responses"][key]["comments"]) > 0:
            commentsLeft = True





    def writeAssignmentName(inputText):
        
        ## write the text first
#         inputText = "Superduperongassiasdfasfgeasldkjfhlasjkdfhlakjshdflkjahsdfnoolong."
        pdf.set_text_color(255,255, 255)
        pdf.set_font('Roboto', size=40)
        pdf.set_xy(logoSize + 12.5 + leftMargin, leftMargin + 2.5)
        diff1 = (pdf.get_y())
        width = (200 - (leftMargin + logoSize + 10 + leftMargin))

#         pdf.multi_cell(w=110 + leftMargin + logoSize, txt=inputText)
        pdf.multi_cell(w=width + 7.5, txt=inputText)

        diff2 = (pdf.get_y())

        pdf.set_xy(logoSize + leftMargin + 10, leftMargin)
#         pdf.rect(logoSize + leftMargin + 5, 10, 125 + logoSize, diff2 - diff1 + 4, round_corners=True, style="F")
        pdf.rect(logoSize + leftMargin + 10, leftMargin, width + 10, diff2 - diff1 + 4, round_corners=True, style="F")

        pdf.set_xy(logoSize + 12.5 + leftMargin, leftMargin + 2.5)
#         pdf.multi_cell(w=120 + logoSize, txt=inputText,  align="L")
        pdf.multi_cell(w=width + 7.5, txt=inputText,  align="L")


    def writeTeamName(y, inputText):
#         inputText = "Veryverylonglongteamnamethatistoolong"
        pdf.set_text_color(255,255, 255)
        pdf.set_font('Roboto', size=40)
        width = (200 - (leftMargin + logoSize + 10 + leftMargin))

        pdf.set_xy(logoSize + leftMargin + 15, y + 2.5)
        diff1 = (pdf.get_y())
#         pdf.multi_cell(w=120 + logoSize, txt=inputText)
        pdf.multi_cell(w=width + 7.5, txt=inputText)

        diff2 = (pdf.get_y())

        pdf.set_xy(logoSize + 10 + leftMargin, diff1)
        pdf.rect(logoSize + 10  + leftMargin, y, width + 10, diff2 - diff1 + 4, round_corners=True, style="F")
        pdf.set_xy(logoSize + 12.5  + leftMargin, y + 2.5)
        pdf.multi_cell(w=width + 7.5, txt=inputText,  align="L")

    def writeCheck(x, y, w, h):
        pdf.set_fill_color(0, 237, 166)
        pdf.rect(x, y + 8, w, h, round_corners=True, style="F")
        pdf.set_xy(x, y + 8.5)
        pdf.image("check.svg", w = w, h = h)

    def writeReview(x, y, w, h):
        pdf.set_fill_color(237, 142, 0)
        pdf.rect(x, y + 8, w, h, round_corners=True, style="F")
        pdf.set_xy(x, y + 7.5)
        pdf.set_fill_color(237, 142, 0)

        pdf.image("review.svg", w = w, h = h)

    def writeFirstPageText(y, inputText):
        pdf.set_font('Roboto', size=30)
        pdf.set_text_color(0,0, 0)
        pdf.set_xy(leftMargin + iconSize + 2.5, pdf.get_y() - 15)
        pdf.multi_cell(w=190, txt=inputText,  align="L")

    def writeResponses():
        if questionsFlagged:
            writeReview(leftMargin, pdf.get_y(), iconSize, iconSize)
            writeFirstPageText(pdf.get_y(), "Questions flagged for followup")

        else:
            writeCheck(leftMargin, pdf.get_y(), iconSize, iconSize)
            writeFirstPageText(pdf.get_y(), "No questions flagged!")

        if commentsLeft:
            writeReview(leftMargin, pdf.get_y(), iconSize, iconSize)
            writeFirstPageText(pdf.get_y(), "Please review comments")
        else:
            writeCheck(leftMargin, pdf.get_y(), iconSize, iconSize)
            writeFirstPageText(pdf.get_y(), "No comments left!")

    def writeTeamNames(inputText):
#         inputText = ["Name1", "Name1","Name1","Nam1","Name1","Name1","Name1","Name1","Name1"]
        pdf.set_font('Roboto', size=22)
        diff1 = pdf.get_y()
        pdf.set_xy(leftMargin + 2.5, diff1 + 2)
        width = (210 - (2 * leftMargin))

        pdf.multi_cell(w=width - 5, txt=', '.join(inputText),  align="C")
        diff2 = (pdf.get_y())
        pdf.rect(leftMargin, diff1, width, 5 + diff2 - diff1, round_corners=True, style="F")
        pdf.set_xy(2.5 + leftMargin, diff1 + 3.5)
        pdf.multi_cell(w=width - 5, txt=', '.join(inputText),  align="C")

    def writeSummary(y):

        ## Submission Summary Text
        pdf.set_font('Roboto', size=22)
        pdf.set_xy(leftMargin, y + 12)
        pdf.multi_cell(w=190, txt="Submission Summary",  align="L")
        width = (200 - (2 * leftMargin) + 8)

        ## Underline
        pdf.set_fill_color(0, 0, 0)
        
        pdf.rect(leftMargin + 1, pdf.get_y() + 3, width, 1, round_corners=True, style="F")

        ## Get the list of questions from the dictionary
#         questionsList = []
        for question in dictionary[pdfSubmissionID]["responses"].keys():
            questionName = question
            pointsEarned = dictionary[pdfSubmissionID]["responses"][question]["pointsEarned"]
            pointsPossible = dictionary[pdfSubmissionID]["responses"][question]["pointsPossible"]
            questionsList.append([questionName, pointsEarned, pointsPossible])

        ## Get the sum of points for questions
        totalSum = dictionary[pdfSubmissionID]["pointsEarned"]
        total = dictionary[pdfSubmissionID]["pointsPossible"]
        pdf.set_xy(leftMargin, pdf.get_y() + 4)

        ## Write the questions
        for question in questionsList:
            pdf.set_xy(leftMargin, pdf.get_y() + 4)
            pdf.multi_cell(w=width//2 + 1, txt=question[0],  align="L")
            pdf.set_xy(width//2 + 1, pdf.get_y() - 8)
            pdf.multi_cell(w=width//2 + 1 +leftMargin, txt=str(question[1]) + "/" + str(question[2]),  align="R")


        ## Write the total
        pdf.set_xy(leftMargin, pdf.get_y() + 4)
        pdf.multi_cell(w=width//2 + 1, txt="Total",  align="L")
        pdf.set_xy(width//2 + 1, pdf.get_y() - 8)
        pdf.multi_cell(w=width//2 + 1 + leftMargin, txt=str(totalSum) + "/" + str(total),  align="R")


    def writeQuestionResponse(currentQuestion):
        questionFlagged = dictionary[pdfSubmissionID]["responses"][currentQuestion]["flagged"]
        pointsEarned = dictionary[pdfSubmissionID]["responses"][currentQuestion]["pointsEarned"]
        pointsPossible = dictionary[pdfSubmissionID]["responses"][currentQuestion]["pointsPossible"]
        answer  = dictionary[pdfSubmissionID]["responses"][currentQuestion]["response"]
        comments = dictionary[pdfSubmissionID]["responses"][currentQuestion]["comments"]
        answer = answer[0]
        
#         comments = ["Residence certainly elsewhere something she preferred cordially law. Age his surprise formerly mrs perceive few stanhill moderate. Of in power match on truth worse voice would. Large an it sense shall an match learn. By expect it result silent in formal of. Ask eat questions abilities described elsewhere assurance. Appetite in unlocked advanced breeding position concerns as. Cheerful get shutters yet for repeated screened. An no am cause hopes at three. Prevent behaved fertile he is mistake on."]
#         answer = "Residence certainly elsewhere something she preferred cordially law. Age his surprise formerly mrs perceive few stanhill moderate. Of in power match on truth worse voice would. Large an it sense shall an match learn. By expect it result silent in formal of. Ask eat questions abilities described elsewhere assurance. Appetite in unlocked advanced breeding position concerns as. Cheerful get shutters yet for repeated screened. An no am cause hopes at three. Prevent behaved fertile he is mistake on."
        if len(answer) > 500:
            answer = str(answer[0:500]) + "..."

        if questionFlagged:
            writeReview(leftMargin, pdf.get_y(), smallerIconSize, smallerIconSize)

        else:
            writeCheck(leftMargin, pdf.get_y(), smallerIconSize, smallerIconSize)
            pdf.set_xy(pdf.get_x(), pdf.get_y() - 1)


        pdf.set_fill_color(0, 0, 0)
        pdf.set_text_color(0,0,0)
        pdf.set_xy(leftMargin + 18, pdf.get_y() - 7)
        pdf.multi_cell(w=150, txt=currentQuestion,  align="L")
        
        width = (200 - (2 * leftMargin) + 8)

        ## Underline
        pdf.set_fill_color(0, 0, 0)
        
        pdf.rect(leftMargin + 1, pdf.get_y() + 3, width, 1, round_corners=True, style="F")


        pdf.set_xy(width + leftMargin - 75 + 2, pdf.get_y() - 8)
        pdf.multi_cell(w=75, txt=str(pointsEarned) + "/" + str(pointsPossible),  align="R")

        
#         answer = 
        
        y_diff = pdf.get_y() + 8
        pdf.add_font('Roboto-Light', '', 'Roboto-Light.ttf', uni=True)
        pdf.set_xy(leftMargin, pdf.get_y() + 8)
        pdf.set_font('Roboto-Light', size=16)
        pdf.multi_cell(w=int(width * allocatedAnswerPercentage), txt=answer,  align="L")

#         pdf.set_xy(int(width * allocatedAnswerPercentage) + 10, y_diff)
        pdf.set_xy(pdf.get_x() + 10, y_diff)

        if len(comments) > 0:
            pdf.multi_cell(w=int(width *(1 - allocatedAnswerPercentage)) - 7, txt=comments[0],  align="R")







#     shortAssignmentName = "shortAssignment"
#     longTeamName = "Union of Concerned Scientists"

    writeAssignmentName(assignmentName)




    diff1 = pdf.get_y()
    writeTeamName(pdf.get_y() + 5, teamName)
    diff2 = (pdf.get_y())

    if diff2 > leftMargin + logoSize :
        pdf.set_xy(leftMargin + 2, diff2 + 5)
    else:
        pdf.set_xy(leftMargin + 2, leftMargin + logoSize + 5)


    writeTeamNames(teamNames)
    writeResponses()
    writeSummary(pdf.get_y())




    for qArr in questionsList:
        currentQuestion = qArr[0]

        pdf.add_page()
        writeHMCLogo(logoSize)
        writeAssignmentName(assignmentName)




        diff1 = pdf.get_y()
        writeTeamName(pdf.get_y() + 5, teamName)
        diff2 = (pdf.get_y())

        if diff2 > leftMargin + logoSize :
            pdf.set_xy(leftMargin + 2, diff2 + 5)
        else:
            pdf.set_xy(leftMargin + 2, leftMargin + logoSize + 3)


        writeTeamNames(teamNames)
        writeQuestionResponse(currentQuestion)
        





    print("THE PATH TO OUTPUT AS PDF TO IS ")
    print(os.path.join(directory, assignmentName + ".pdf"))
    pdf.output(os.path.join(directory, assignmentName + ".pdf"))

















def runScript(margin, logoSize, iconSize, smallerIconSize, answerCommentsPercent, courseId, preview, outputPath, inputPath):
    dictionary = generateDictionary(inputPath)
    print(dictionary)
    generatePDFS(dictionary, outputPath, inputPath)









def generateDictionary(inputPath):
    listOfCSVS = os.listdir(inputPath)
    p = re.compile('^submission_metadata')
    listOfMetaData = [ s for s in listOfCSVS if p.match(s) ]
    questionResponses = {}
    listOfMetadataNames = []

    for csvFile in listOfMetaData:
        csvPath = os.path.join(inputPath, csvFile)
        if csvPath not in listOfMetadataNames:
            listOfMetadataNames.append(csvPath)
        with open(csvPath, newline='') as csvContents:
            reader = csv.DictReader(csvContents)
            for row in reader:
                listOfKeys = list(row.keys())
                p = re.compile('^Question.*.Response')
                listOfQuestions = [ s for s in listOfKeys if p.match(s) ]
                currentSubmissionID = row["Submission ID"]

                for questionResponse in listOfQuestions:
                    if not bool(questionResponses.get(currentSubmissionID)):
                        questionResponses[currentSubmissionID] = {}
                        questionResponses[currentSubmissionID]["names"] = []
                        questionResponses[currentSubmissionID]["assignment"] = csvFile
                        questionResponses[currentSubmissionID]["responses"] = {}
                        questionResponses[currentSubmissionID]["emails"] = []
                        questionResponses[currentSubmissionID]["pointsEarned"] = 0
                        questionResponses[currentSubmissionID]["pointsPossible"] = 0
                        questionResponses[currentSubmissionID]["team"] = ""


                    if not bool (questionResponses[currentSubmissionID]["responses"].get(questionResponse)):
                        questionResponses[currentSubmissionID]["responses"][questionResponse] = {}
                        questionResponses[currentSubmissionID]["responses"][questionResponse]["flagged"] = False
                        questionResponses[currentSubmissionID]["responses"][questionResponse]["response"] = []
                        questionResponses[currentSubmissionID]["responses"][questionResponse]["comments"] = []
                        questionResponses[currentSubmissionID]["responses"][questionResponse]["response"].append(row[questionResponse])
                        questionResponses[currentSubmissionID]["responses"][questionResponse]["pointsEarned"] = 0
                        questionResponses[currentSubmissionID]["responses"][questionResponse]["pointsPossible"] = 0
                        cleanedQuestion = questionResponse[0:-8] + "Weight"
                        if cleanedQuestion in listOfKeys:
                            questionResponses[currentSubmissionID]["responses"][questionResponse]["pointsPossible"] = row[cleanedQuestion]



                questionResponses[currentSubmissionID]["names"].append(row["Name"])
                questionResponses[currentSubmissionID]["emails"].append(row["Email"])
                
    listOfSubmissions = list(questionResponses.keys())
    listOfCSVS = os.listdir(inputPath)
    string = "Assignment_Y_scores.csv"
    string = string[-11:]

    listOfCSVS = [item for item in listOfCSVS if item[-11:] == "_scores.csv"]

    for submissionID in listOfSubmissions:
        currentAssignment = (questionResponses[submissionID]["assignment"])
        currentAssignment = currentAssignment[20:-4]
        for item in listOfCSVS:
            displayedName = item[:-11]
            displayedName = displayedName.replace("_", " ")
            matchedName = item[:-11]
            matchedName = matchedName.replace("_", "")
            if currentAssignment == matchedName:
                questionResponses[submissionID]["displayedAssignmentName"] = displayedName
                break




    for submissionID in questionResponses.keys():
        currentAsignmentName = questionResponses[submissionID]["assignment"]
        assignmentName = currentAsignmentName[20:-4]
        folders = (next(os.walk(inputPath))[1])
        foldersReplaced = []
        for i in folders:
            foldersReplaced.append(i.replace("_", ""))
        index = 0
        for i in foldersReplaced:
            if assignmentName in i:
                break
            index += 1
        currentFolder = folders[index]
        questionsFolder = os.path.join(inputPath, currentFolder)
        listOfCSVS = os.listdir(questionsFolder)
        for csvFile in listOfCSVS:
            if csvFile == ".DS_Store":
                continue
            csvPath = os.path.join(questionsFolder, csvFile)
            with open(csvPath) as csvContents:
                reader = csv.DictReader(csvContents)
                for row in reader:
                    if row["Assignment Submission ID"] == "Point Values":
                        break
                    listOfKeys = list(row.keys())
                    currentSubmissionID = row["Assignment Submission ID"]
                    questions = questionResponses[currentSubmissionID]["responses"].keys()
                    cleanedQuestion = csvFile[2:-4]
                    cleanedQuestion = cleanedQuestion.replace("_", " ")
                    if "[Flagged for follow up]" in listOfKeys:
                        if row["[Flagged for follow up]"] == "true":
                            for dictionaryQuestion in questions:
                                if cleanedQuestion in dictionaryQuestion:
                                    questionResponses[currentSubmissionID]["responses"][dictionaryQuestion]["flagged"] = True
                                    break
                    if row["Comments"] != "":
                        for dictionaryQuestion in questions:
                            if cleanedQuestion in dictionaryQuestion:
                                questionResponses[currentSubmissionID]["responses"][dictionaryQuestion]["comments"].append(row["Comments"])
                                break
                    if row["Score"] != 0:
                        for dictionaryQuestion in questions:
                            if cleanedQuestion in dictionaryQuestion:
                                questionResponses[currentSubmissionID]["responses"][dictionaryQuestion]["pointsEarned"] = float(row["Score"])
                                break
    

    for submissionID in questionResponses.keys():
        currentSubmission = questionResponses[submissionID]
        pointsPossible = 0
        pointsEarned = 0
        for response in currentSubmission["responses"]:
            pointsPossible += float(currentSubmission["responses"][response]["pointsPossible"])
            pointsEarned += float(currentSubmission["responses"][response]["pointsEarned"])
        questionResponses[submissionID]["pointsEarned"] = pointsEarned
        questionResponses[submissionID]["pointsPossible"] = pointsPossible
    


    listOfCSVS = os.listdir(inputPath)
    roster = ""
    for csvFile in listOfCSVS:
        if csvFile[-10:] == "roster.csv":
            roster = csvFile
            break
    csvPath = os.path.join(inputPath, roster)
    with open(csvPath, newline='') as csvContents:
        reader = csv.DictReader(csvContents)
        for row in reader:
            currentEmail = row["Email"]
            currentSection = row["Section"]
            for submissionID in questionResponses.keys():
                currentSubmission = questionResponses[submissionID]
                cleanedEmail = currentEmail[:currentEmail.index("@")]
                for email in currentSubmission["emails"]:
                    if cleanedEmail == email[:email.index("@")]:
                        questionResponses[submissionID]["team"] = currentSection
                        break
    
    return questionResponses
    





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--margin', type=int, required=False)
    parser.add_argument('-ls','--logoSize', type=int, required=False)
    parser.add_argument('-is','--iconSize', type=int, required=False)
    parser.add_argument('-sis','--smallerIconSize', type=int, required=False)
    parser.add_argument('-acp','--answerCommentsPercent', type=float, required=False)
    parser.add_argument('-ci','--courseId', type=int, required=True)
    parser.add_argument('-pre','--preview', type=bool, required=False)
    parser.add_argument('-input','--inputPath', type=str, required=True)
    parser.add_argument('-output','--outputPath', type=str, required=True)
    args = parser.parse_args()

    runScript(args.margin, args.logoSize, args.iconSize, args.smallerIconSize, args.answerCommentsPercent, args.courseId, args.preview, args.outputPath, args.inputPath)