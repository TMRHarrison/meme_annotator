#!/usr/bin/env python3 
# 
# .gff specialization
# Fields must be tab-separated. Also, all but the final field in each feature line must contain a value; "empty" columns should be denoted with a '.'
#    seqname - name of the chromosome or scaffold; chromosome names can be given with or without the 'chr' prefix. Important note: the seqname must be one used within Ensembl, i.e. a standard chromosome name or an Ensembl identifier such as a scaffold ID, without any additional content such as species or assembly. See the example GFF output below.
#    source - name of the program that generated this feature, or the data source (database or project name)
#    feature - feature type name, e.g. Gene, Variation, Similarity
#    start - Start position of the feature, with sequence numbering starting at 1.
#    end - End position of the feature, with sequence numbering starting at 1.
#    score - A floating point value.
#    strand - defined as + (forward) or - (reverse).
#    frame - One of '0', '1' or '2'. '0' indicates that the first base of the feature is the first base of a codon, '1' that the second base is the first base of a codon, and so on..
#    attribute - A semicolon-separated list of tag-value pairs, providing additional information about each feature.
# 
# [sequence 1 name]	MEME Suite	nucleotide_motif	[position]	[position + motif-length]	.	[strand]	.	ID=[ID];Name=[motifName]
# 
# 


## Is it bad?
## Yes

## Does it do what I want it to?
## Also yes


import argparse
import re

def getParams():
	parser = argparse.ArgumentParser()
	parser.add_argument("--motifs", help = "The file to be worked on")

	return parser.parse_args()

class Tag:
	def __init__(self,t,f):
		self.start = re.compile("<"+t+".*>")
		self.end = "</"+t+">"
		self.flag = False
		self.func = f

class Seq: #sequence
	def __init__(self, n, l):
		self.name = n
		self.length = l


class Mot: #motif
	def __init__(self, n, a, l):
		self.name = n
		self.altn = a
		self.length = l

def main():

	## Tag-specific search functions
	# These get passed as arguments sometimes because if it allows this kind of weirdness, I'm down.
	# putting them in here is easier than passing around all the variables as arguments

	# if it's a <sequence/> line, parse it into a seq object
	def training_set(line):
		if (sequence_tag.search(line)):
			# Find everything enclosed by quotes in the line
			vals = quotePattern.findall(line)
			# make a seq value with the ID as the key and add the name and length
			seqs[vals[0]] = Seq(vals[1], int(vals[2]))

	def motifs(line):
		if (motif_tag.search(line)):
			vals = quotePattern.findall(line)
			mot[len(mot)] = Mot(vals[1], vals[2], int(vals[3]))

	def contributing_sites(line):
		if (contributing_site_tag.search(line)):
			vals = quotePattern.findall(line)
			# [sequence 1 name]	MEME Suite	nucleotide_motif
			# [position]	[position + motif-length]	.	
			# [strand]	.	ID=[ID];Name=[motifName]

			ann[len(ann)] = (seqs[vals[0]].name+
				"\tMEME Suite"+
				"\tnucleotide_motif\t"+
				str(int(vals[1])+1)+"\t"+
				str(int(vals[1])+mot[len(mot)-1].length)+
				"\t."+
				"\t+"+
				"\t."+
				"\tNote=p-value:"+vals[3]+";Name="+mot[len(mot)-1].altn+" "+mot[len(mot)-1].name)


	args = getParams()

	motif_file = open(args.motifs)

	seqs = {} # sequences
	mot = {}  # motifs
	tags = {} # XML tags to search within
	ann = {}  # annotations

	# construct patterns etc. for encasing tags
	tags[len(tags)] = Tag("training_set",training_set)
	tags[len(tags)] = Tag("motifs",motifs)
	tags[len(tags)] = Tag("contributing_sites",contributing_sites)

	quotePattern = re.compile(r'"([^"]*)"')

	# this is for inner tags that need data pulled from them
	sequence_tag = re.compile(r'<sequence .*>')
	motif_tag = re.compile(r'<motif .*>')
	contributing_site_tag = re.compile(r'<contributing_site .*>')

	for i in motif_file:
		line = i[:-1] # clip the newline off

		# start/stop parsing sections
		findTags(line,tags)

		# Do the whatever on the sections
		parseTags(line,tags)


	print("##gff-version 3")
	for i in seqs:
		print("##sequence-region "+seqs[i].name+" 1 "+str(seqs[i].length))
	for i in ann:
		print(ann[i])

	motif_file.close()

# If this line is the start of a line, start parsing it, or stop if it's the end
def findTags(line, tags):
	for n in range(0, len(tags)):
		# if the tag starts on this line start the search
		if (tags[n].start.search(line)):
			tags[n].flag = True
		# if the tag ends here, stop searching
		elif (tags[n].end == line):
			tags[n].flag = False

# If you're parsing a tag, run the function associated with it
def parseTags(line,tags):
	for n in range(0, len(tags)):
		if (tags[n].flag):
			tags[n].func(line)





# import-safety
if __name__ == '__main__':
	main()