#! /usr/bin/python 

import sys
import os.path
import math

#number of words in the sequence
numWords = 20
# gap opening penalty
G = -8
# gap extension penalty
E = -1
# direct match score
M = 6
# vowel/consonant mismatch penalty
X = -2
# mismatch penalty
Q = -1

##if there are no inputs tell the user to give filename
if len(sys.argv) == 1: 
	print "Please enter a file name."
	sys.exit()

##if the specified file can't be found tell the user
if not os.path.isfile(sys.argv[1]):
	print "Could not find the specified file."
	sys.exit()

##prospect data class
class PerMut:
    def __init__(self, line):
        self.line = line
        parse = line.split("\t")
        self.parsedWord = parse[1].split(",")
        self.id = parse[0]
        self.comps = [0 for i in range(32)]

def score_sentence(parsed1, parsed2):
    sent_score = 0
    for i in range(numWords):
        sent_score += gotoh_align(parsed1[i], parsed2[i], False)

    return sent_score

def gotoh_align(str1, str2, last_gap):
    if str1 == str2:
        return M*len(str1)
    elif str1 == "":
        return G + E*(len(str2) - 1)
    elif str2 == "":
        return G + E*(len(str1) - 1)

    score_match = score_letter(str1[0], str2[0]) + gotoh_align(str1[1:], str2[1:], False)
    
    if last_gap:
        score_gap1 = E + gotoh_align(str1, str2[1:], True)
        score_gap2 = E + gotoh_align(str1[1:], str2, True)
    else:
        score_gap1 = G + gotoh_align(str1, str2[1:], True)
        score_gap2 = G + gotoh_align(str1[1:], str2, True)
        last_gap = True

    return max(score_gap2, score_gap1, score_match)

def score_letter(l1, l2):
    if (l1 == l2):
        return M
    elif l1 in "AEIOU":
        if l2 in "AEIOU":
            return Q
        else:
            return X
    elif l2 in "AEIOU":
        return X
    return Q

infile = open(sys.argv[1])
outfile = open(sys.argv[1] + ".scored.txt", 'w')
list1 = []

for line in infile:
    if line[0:2] == "##":
        continue

    list1.append(PerMut(line))

for i in range(len(list1)):
    for j in range(len(list1)):
        if i == j:
	        list1[i].comps[j] = "-"
	        list1[j].comps[i] = "-"
	        continue

        if j < i:
            list1[j].comps[i] = list1[i].comps[j]
            continue

        score = score_sentence(list1[i].parsedWord, list1[j].parsedWord)
        list1[i].comps[j] = score
        list1[j].comps[i] = score
    print i

outfile.write("ID,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32\n")
for i in list1:
	out = "ID:"
	out += str(i.id)
	for s in i.comps:
		out += "," + str(s)
	outfile.write(out + "\n")
outfile.close()