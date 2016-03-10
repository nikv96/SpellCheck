#This program is designed to get an inputword and suggest a correction 
import time
#This function reads big.txt
def readbig():
        Start_time=time.time()
        global list_of_words #database of words
        list_of_words = []
        with open('big.txt','r') as myFile:
                tempword = ''#Temporary word to make changes to before uploading in the database
                for line in myFile:
                        line = line.lower()
                        for char in line:
                                if char.isalpha() or char == '-' or char == "'":#Only alphabets,- or ' is acceptable
                                        tempword += char
                                elif tempword !='':
                                        if "'" in tempword:
                                                length = len(tempword)
                                                i=0
                                                while i<length:#to check if "'" is in inappropriate position and edit tempword
                                                        if (tempword[i] == "'" and (i != length-3) and (i != length-2)):
                                                                tempword = tempword[:i]+tempword[i+1:]
                                                                length -=1
                                                        i+=1
                                        list_of_words.append(tempword)
                                        tempword = ''

        templist = set(list_of_words)  #to remove all duplicates in corpus
        list_of_words = list(templist)
        print ("\nElapsed time for creating database=", time.time()-Start_time)

#this function reads wordlist.txt
def readwordlist():
        Start_time=time.time()
        global list_of_words
        with open('word_list(2).txt','r') as myFile:
                tempword = ''
                for line in myFile:
                        line = line.lower()
                        for char in line:
                                if char.isalpha() or char == '-' or char == "'":
                                        tempword += char
                                elif tempword !='':
                                        if "'" in tempword:
                                                length = len(tempword)
                                                i=0
                                                while i<length:
                                                        if (tempword[i] == "'" and (i != length-3) and (i != length-2)):
                                                                tempword = tempword[:i]+tempword[i+1:]
                                                                length -=1
                                                        i+=1
                                        list_of_words.append(tempword)
                                        tempword = ''

        templist = set(list_of_words)  
        list_of_words = list(templist)
        print ("\nElapsed time for creating database=", time.time()-Start_time)

#this function computes word distance of two words and returns the value
def worddist(inputword,word):

        if len(word)<len(inputword):#toassign a small word and large word
                smallword = word
                bigword = inputword
        else:
                smallword = inputword
                bigword = word

        if abs(len(inputword)-len(word))>2: #length diff <2 is dealt with in the following cases. These statements execute for any worddist>2
                word_dist1=word_dist2=0#word_dist1 keeps check of the length diff and word_dist2 keeps check of the char difference
                word_dist1 = len(bigword)-len(smallword)
                for i in range (len(smallword)):#this loop directly compares the letters of the word and counts any mismatch
                        if smallword[i] != bigword[i]:
                                word_dist2 +=1
                if word_dist2 == 0:#this condition is to further check if there are char mismatches
                        for i in bigword:
                                if i not in smallword:
                                        word_dist2 +=1
                return word_dist2+word_dist1 #the sum of the length and char diff is returned to account for entire worddist
                
                
                
        elif len(smallword)!=len(bigword) :#these statements check for worddist 1 or 2 when the lengths don't match
                flag = 0 
                tempword = '' #tempword is created to modify the existing word
                for i in range (len(bigword)):#this for loop basically removes one char at a time from the bigword and check if smallword is present in the tempstring
                        tempword = ' '+bigword[:i] + bigword[(i+1):]
                        if tempword in smallword or smallword in tempword and abs(len(word)-len(inputword))<2:
                                flag =1
                                break
                if flag ==1:
                        return 1 #any mismatch in the above statements implies a worddist of 1. 
                flag = 0

                for i in range (len(bigword)):#this for loop checks worddist of 2 by removing two chars at a time
                        for j in range (0,len(bigword)):
                                if j <= i:
                                       tempword = ' '+bigword[:j] + bigword[(j+1):i] + bigword[i+1:]
                                else:
                                        tempword = ' '+bigword[:i] + bigword[(i+1):j] + bigword[j+1:]
                                if  tempword in smallword or smallword in tempword:
                                        flag+= 1
                                        break
                if flag !=0:
                       return 2
                

        else:#these statements are executed if worddist<=2 and lengths don't match
                flag = 0
                tempword1=tempword2 = ''#tempword1 and 2 are to store modifications of the words
                for i in range( len(smallword)):#this loop test the case when the worddist is 1 with just a single char replacement
                        tempword1 = (smallword[:i]+smallword[i+1:])#one char is removed from the word and stored in tempword
                        tempword2 = (bigword[:i]+bigword[i+1:])
                        if tempword1 == tempword2:
                                flag =1
                                break
                if flag ==1:
                        return 1

                flag = 0

                for i in range (len(smallword)):#this loop test the case when the worddist is 2 with 2 chars replacement
                        for j in range (len(bigword)):
                                if j <= i:
                                       tempword2 = (bigword[:j] + bigword[(j+1):i] + bigword[i+1:])#2 chars are removed at a time and result stored in temp word
                                       tempword1 = (smallword[:j] + smallword[(j+1):i] + smallword[i+1:])
                                else:
                                        tempword2 = (bigword[:i] + bigword[(i+1):j] + bigword[j+1:])
                                        tempword1 = (smallword[:i] + smallword[(i+1):j] + smallword[j+1:])
                                if  tempword1 == tempword2:
                                        flag+= 1
                                        break
                if flag != 0:
                        return 2

        if len(bigword)-len(smallword) == 0 and smallword[0] == bigword[0]:#this case test when the above cases have not been executed and length diff is zero
                error = 0 #counts the mismatches directly
                for i in range(len(smallword)):
                        if smallword[i]!=bigword[i]:
                                error+=1
                return error
        
        return 100 #if all the above cases have not been executed then the words are completely unrelated. 100 is a large no. and hence set as default.\
                        #purpose of setting 100 is because the words are sorted according to word dist later and min worddist words are displayed
                        #100 is improbable to be the minimum

#this function returns the most likely word
def favouredword(solwordlist, maxwordcount):
        
        dict_of_wordcount = {}#to store the # of occurence with the word
        with open('big.txt','r') as myFile:
                for checkingword in solwordlist:#checkingword is in the list of words with min worddist 
                        count = 0
                        for line in myFile:
                                wordlist = []#this wordlist is temporary storage to store the words in the lines in a list
                                line = line.lower()
                                for char in line:#to modify the string
                                        if not(char.isalpha() or char == '-' or char == "'" or char =='.' or char == ' '):#alphabets,'-','.',"'",' ' are allowed in a line
                                                line.replace(char,'')
                                wordlist = line.split()
                                for checkword in wordlist:
                                        if "'" in checkword:#this piece of code is to filter out wrong "'" in the word
                                                length = len(checkword)
                                                i=0
                                                while i<length:
                                                        if checkword[i] == "'" and (i != len(checkword)-3) and (i != len(checkword)-2):
                                                                checkword = checkword[:i]+checkword[i+1:]
                                                                length -=1
                                                        i+=1
                                        if checkingword in checkword:#checking occurence
                                                count+=1
                        dict_of_wordcount[count] = checkingword
        if maxwordcount < max(dict_of_wordcount.keys()):#this condition checks if the maxwordcount is same as previous result.(while displaying more suggestions
                maxwordcount = max(dict_of_wordcount.keys())#returns max of the occurences
                print("\nThe most likely word is: {}".format(dict_of_wordcount[maxwordcount]))
        else:
                print("\nThe most likely is same as previous result")

        return maxwordcount#this number is to be used in case the function is called again
        
#this function performs main autocorrect task and calls worddist
def autocorrect(inputword):
    Start_time=time.time()
    worddist_list = {}
    if ' ' in inputword:#error if sentence is provided
            print("\nError! More than one word")
            
    else:
            length = len(inputword)
            i=0
            while i<length:#this replaces the unknown chars in the inputword
                    if inputword[i].isalpha()==False and inputword[i] !='-' and not(inputword[i]=="'"):
                            inputword.replace(inputword[i],'')
                    if inputword[i] == "'" and i != len(inputword)-1 and i != len(inputword)-2:
                            inputword = inputword[:i]+inputword[i+1:]
                            length -=1
                    i+=1    
                            
            if inputword in list_of_words:#checks if word already exists
                print( "\nWord exists in dictionary" )
                print ("\nElapsed time to run autocorrect=", time.time()-Start_time)
            else:
                for word in list_of_words:#this for loop creates a dictionary with worddist as keys and a list of words as values
                        if (worddist(inputword,word) not in worddist_list.keys()):
                                worddist_list[worddist(inputword,word)]=[word]
                        else:
                                worddist_list[worddist(inputword,word)].append(word)
                minworddist = min(worddist_list.keys())#words with min word dist are only printed
                ch = 'y'
                i=0
                maxwordcount = 0 #this variable keeps track of the best suggestion
                while ch=='y':
                        print("\nDid you mean: ", worddist_list[minworddist+i])
                        if i ==0:
                                print ("\nElapsed time to run autocorrect=", time.time()-Start_time)
                        choice = input ("\nDo you want the best suggestion?Y/N")#best suggestion is made optional
                        if choice == 'Y' or choice =='y':
                                start_time = time.time()
                                maxwordcount = favouredword(worddist_list[minworddist+i],maxwordcount)
                                print("\nEstimated time to calculate most likely word:", time.time()-start_time)
                        ch = input ("\nDo you want to see more suggestions?Y/N")
                        i+=1
                ch1 = input("\nDo you want to add {} to the corpus?Y/N".format(inputword))
                if ( ch1=='Y' or ch1 =='y'):#to add the unknown word to the dictionary
                        list_of_words.append(inputword)
       
#this function provides the top menu
def menu():
        ch=0
        readbig()
        choice=input("Big.txt has been read. Do you want to read wordlist.txt too? Y/N")#reading wordlist is made optional
        if choice=='Y' or choice == 'y':
                readwordlist()
        while ch!=4:
                print("\nTOP MENU\n")
                print("1.Execute Spell Check")
                print("2.Enter a word into the corpus")
                print("3.Exit from program")
                ch=int(input("Enter your choice:"))
                if ch==1:
                    inputword = input("\nPlease input a word: ")
                    autocorrect(inputword)      
                elif ch==2:
                    list_of_words.append(input("\nEnter the word you want to add:"))
                    print("\nWord has been added")
                elif ch==3:
                        exit()
                else:
                        print("\n\nEnter correct choice")
                                              
menu()        
    
                    
    
    
                    
    
