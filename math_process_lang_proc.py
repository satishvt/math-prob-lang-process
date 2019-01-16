import re
import sys
import subprocess
import os

## Function to identify the sentence-break and print the necessary results.

def sentence_break():

### Checks if the sentence s a question? 
    if is_question in question:
        for k in res2:
            if k==subj:
                if res2[subj][0]==question_obj:
                    if res2[subj][1] >= 0:
                        print('Answer to the Math Query is:')
                        print(res2[subj][1])
                    else:
                        print('Problem with Query, check the Para again')

### Checks if the sentence is a assignining a value ot the subject
    else:
        if actions[action] == 'hold':
            res2[subj]={}
            res2[subj] = [obj,int(count)]

### Checks if the sentence is a subtraction action
        elif actions[action] == 'sub':
            for k in res2:
                if k==subj:
                    if res2[subj][0]==obj:
                        res2[subj][1] = res2[subj][1] - int(count)

### Checks if the sentence is a addition action
        else:
            for k in res2:
                if k==subj:
                    if res2[subj][0]==obj:
                        res2[subj][1] = res2[subj][1] + int(count)


## Start of Main


### Checks if the file consisting of the Math Query is passed as an input
if(len(sys.argv)<>2):
    sys.exit('Input the file with the Math Query (Give full path)')

### Checks if the input file exists
if os.path.isfile(sys.argv[1])==False:
    sys.exit('Problem reading the input file. Please ensure you give file path as input')

### Executes the lex parser code, and passes the output to parse.
f = subprocess.Popen(
    ("C:\\Users\\satish.vengla\\Downloads\\stanford-parser-full-2017-06-09\\stanford-parser-full-2017-06-09\\lexparser1.bat",sys.argv[1]), shell=True,
    stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout 
    
res2={}
res3={}
subj=''
obj=''
action=''
is_question=''
question_obj=''
nsubj_pri=''
count=0
nsubj=0
dobj=0
nummod=0
hold_1=0
hold_num=0
computed_value =0
numbers={'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9, 'ten':10, 'eleven':11, 'twelve':12, 'thirteen':13, 'fourteen':14, 'fifteen':15, 'sixteen':16, 'seventeen':17, 'eighteen':18, 'nineteen':19, 'twenty':20, 'thirty':30, 'forty':40, 'fifty':50, 'sixty':60, 'seventy':70, 'eighty':80, 'ninety':90 }
multipliers = {'hundred':100, 'thousand':1000, 'lakh':100000, 'million':1000000, 'crore':10000000}
actions={'has':'hold','have':'hold','had':'hold','gave':'sub','given':'sub','lost':'sub','found':'add','added':'add', 'ate':'sub', 'bought':'add', 'bring ':'add', 'brought':'add', 'buy':'add', 'draw':'add', 'drawn':'add', 'eaten':'sub', 'eats':'sub', 'fall':'sub', 'falls':'sub', 'fell':'sub', 'finds':'add', 'founds':'add', 'get ':'add', 'give':'sub', 'gives':'sub', 'got':'add', 'include':'add', 'included':'add', 'includes':'add', 'leaves':'sub', 'left':'sub', 'lose':'sub', 'move':'sub', 'moved':'sub', 'moves':'sub', 'offer':'sub', 'offered':'sub', 'offers':'sub', 'pass':'sub', 'passed':'sub', 'receive':'add', 'received':'add', 'receives':'add', 'return':'sub', 'returned':'sub', 'returns':'sub', 'sell':'sub', 'serve':'sub', 'served':'sub', 'serves':'sub', 'sold':'sub', 'spend':'sub', 'spent':'sub', 'take':'add', 'taken':'add', 'took':'add', 'win':'add', 'won':'add' }
question=['How']


#### Reads the para sentence by sentence
for line in f:   

    hold_name=''

## Reading the sentences and identifying the actions


#### Ignore unnecessary lines & comments
    if (line.startswith('SLF4J')) or (line.startswith('Parsing file:')) or (line.startswith('Parsing [sent. 1')):
        pass
    else:
        
#### Checks if the sentence is breaking, to identify the semantic meaning of the sentence
        if (line.startswith('Parsing')) or (line.startswith('Parsed')):
            if hold_1 ==1:      
                computed_value = computed_value + hold_num
            if nummod < 1:
                count = computed_value
            #print('count:')
            #print(count)
            sentence_break()
            subj=''
            obj=''
            action=''
            is_question=''
            question_obj=''
            nsubj_pri=''
            question_obj=''
            nsubj_pri=''
            hold_1=1
            hold_num=0
            computed_value =0
            nummod=0

### Exit the code, if all the sentences are parsed.
        if (line.startswith('Parsed')):
            sys.exit()                                            
                                                    
### Extract the subject
        if line.startswith('nsubj('):
            res=re.findall(r"\w\((\w+)\W\w+[,][ ](\w+)\W\w+\)",line)
            for match in res:
                subj=match[1]
            nsubj=1

### Extract the value of the number of objects (if it sia numerical)
        if line.startswith('nummod'):
            res=re.findall(r"\w\((\w+)\W\w+[,][ ](\w+)\W\w+\)",line)
            for match in res:
                obj=match[0]
                count=match[1]
            if count.isdigit():
                nummod=1

### Extract the value of the number of objects (if it sia numerical)
        if line.startswith('root'):        
            res=re.findall(r"\w\((\w+)\W\w+[,][ ](\w+)\W\w+\)",line)
            for match in res:
                action=match[1]

### Checks if the sentence is a question
        if line.startswith('advmod'):        
            res=re.findall(r"\w\((\w+)\W\w+[,][ ](\w+)\W\w+\)",line)
            for match in res:
                is_question=match[1]
    
#### Extracts the object details, in question
        if line.startswith('amod'):        
            res=re.findall(r"\w\((\w+)\W\w+[,][ ](\w+)\W\w+\)",line)
            for match in res:
                question_obj=match[0]
                obj=match[0]
            if match[1].isdigit():
                count=match[1]
                nummod=1            

#### Extracts the subject in question
        if line.startswith('nmod:with'):        
            res=re.findall(r"\w\((\w+)\W\w+[,][ ](\w+)\W\w+\)",line)
            for match in res:
                subj=match[1]
    
#### Changes the textual number into a number.    
        res3=re.findall(r"\w\((\w+)\W\w+[,][ ](\w+)\W\w+\)",line)
        for match2 in res3:
            if (match2[1] in numbers.keys()) & (hold_1==1):
                computed_value = computed_value + hold_num
                hold_num = numbers[match2[1]]
                hold_1 = 1
    
            elif (match2[1] in numbers.keys()):
                hold_num = numbers[match2[1]]
                hold_1 = 1 
            
            elif (match2[1] in multipliers.keys()) & (hold_1==1):
                computed_value = computed_value +  (hold_num * multipliers[match2[1]])
                hold_1 = 0
                hold_num = 1       
                            
