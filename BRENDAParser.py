import json
import getopt, sys
import time


#Opens file and traverses over each line in the textfile, makes json
def main():

	columnValues = getJSON('Columns.json')
	brendaData = {}

	infile = ''
	outfile = ''
	errorfile = None

	#argument handleing
	try:
		optList, args = getopt.getopt(sys.argv[1:], 'lhi:o:e', ["ifile=","ofile=","efile="])
	except getopt.GetoptError:
		print('BRENDAParser.py --infile <inputfile> --ofile <outputfile>')
		sys.exit(2)
	for opt, arg in optList:

		if opt == '-h':
			print('BRENDAParser.py --infile <inputfile> --ofile <outputfile>')
			sys.exit()

		elif opt in ("-i", "--ifile"):
			infile = arg

		elif opt in ("-o", "--ofile"):
			outfile = arg

		elif opt in ("-e", "--efile"):
			errorfile = arg

	with open(infile) as brenda:
		currID, prevLine, currSubClass = [""]*3

		#processes each line by EC number and subcategory
		print("Bulk processing...")
		for line in brenda:

			brendaData, currID, prevLine, currSubClass = bulkProcess(columnValues, brendaData, line, currID, prevLine, currSubClass)

	print('Subsectioning entries...')

	#after all entries are in, each entry is broken into smaller sections
	for key in brendaData:

		for subclass in brendaData[key]:

			#parses into smaller sections
			brendaData[key][subclass] = [orderData(columnValues, key, subclass, entry)
			 for entry in brendaData[key][subclass]]

	print('Expanding...')

	brendaData = expand(brendaData)

	brendaData = addSpecialCols(brendaData, errorfile, columnValues)

	brendaData = addColumnHeaders(brendaData, columnValues)

	parsed = json.dumps(brendaData, indent=4, sort_keys=True)

	text_file = open(outfile, 'wt')
	text_file.write(parsed)
	print('Done')


#Creates two header columns for SP and NSP
def spColumns(brendaData, columnValues, ec, sub):

	for entry in brendaData[ec][sub]:

		#Title is replaced with substrate and product
		fcv = entry.pop('TITLE')
		substrateColumn = columnValues[sub]['SUBSTRATE']
		productColumn = columnValues[sub]['PRODUCT']

		#If there was title information
		if fcv != None:

			#Separate into substrate using = and +
			values = fcv.split(' = ')

			if ' + ' in values[0]:
				entry['SUBSTRATE'] = values[0].split(' + ')
			else:
				entry['SUBSTRATE'] = [values[0]]


			#Case where there are no products	
			if len(values) < 2:
				entry['PRODUCT'] = None
			else:

				#Separate into substrate using = and +
				if ' + ' in values[1]:
					entry['PRODUCT'] = values[1].split(' + ')
				else:
					entry['PRODUCT'] = [values[1]]
		

		#no title information
		else:
			entry['SUBSTRATE'] = None
			entry['PRODUCT'] = None



	return brendaData


#Changes column headers to values in Columns.json
def addColumnHeaders(brendaData, columnValues):

	#new dictionary so keys can be changed
	newCols = {}
	for ec in brendaData:

		#new sub cat
		newCols[ec] = {}
		for sub in brendaData[ec]:

			#new fields values
			newCols[ec][sub] = []
			for entry in brendaData[ec][sub]:
				newEntry = {}

				#for each old key field
				for field in columnValues[sub]:


					#if it is a field of interest
					if field in entry:
						newEntry[columnValues[sub][field]] = entry[field]
					else:
						newEntry[columnValues[sub][field]] = None


				newCols[ec][sub].append(newEntry)

	return newCols

#Adds organism and uniprot fields. If errors are found they are put into an optional error file 
def addSpecialCols(brendaData, errorfile, columnValues):

	eList = []

	for ec in brendaData:
		for sub in brendaData[ec]:

			if sub == 'SP' or sub == 'NSP':
				spColumns(brendaData, columnValues, ec, sub)
			newSub = []
			
			for entry in brendaData[ec][sub]:

				#assume no key erros
				keyError = False

				#get string values for proteins
				pro = derefPro(brendaData, ec)

				#Need to keep PR as is to serve as the index
				if sub != 'PR':

					#Some subcategories do not have this field
					if entry["Protein Numbers"]:

						#bad entry
						if entry["Protein Numbers"] not in pro:
							keyError = True
							eList.append(entry)

						#regular entry
						else:
							entry["ORGANISM"] = pro[entry["Protein Numbers"]]["TITLE"]
							entry["UNIPROT"] = pro[entry["Protein Numbers"]]["UNIPROT"]
					else:
						entry["Organism"] = None
						entry["Uniprot"] = None

					#remove original protein numbers field
					if not keyError:
						del entry["Protein Numbers"]

				#add valid entry to dictionary
				if not keyError:
					newSub.append(entry)
			brendaData[ec][sub] = newSub

		#after we can remove the protien numbebr
		for entry in brendaData[ec]['PR']:
			del entry["Protein Numbers"]

	#if there is an error file given
	if errorfile:
		e = json.dumps(eList, indent=4, sort_keys=True)
		e_file = open(errorfile, 'wt')
		e_file.write(e)

	return brendaData

#Converts protein integers into string form
def derefPro(jsn, ec):
	proteinIndex = {}
	for entry in jsn[ec]['PR']:
		proteinIndex[entry['Protein Numbers']] = entry
	return proteinIndex


#Converts citation integers into string form
def derefCits(jsn,ec):
	citIndex = {}
	for entry in jsn[ec]['RF']:
		citIndex[entry['LITERATURE']] = entry
	return citIndex

#Expands the multiprotein entry structure into separate entrties 
def expand(dc):
	for ec in dc:
		for sub in dc[ec]:
			exSub = []
			for entry in dc[ec][sub]:

				#check for null 
				if entry["Protein Numbers"]:
					for protein in entry["Protein Numbers"]:

						exEntry = entry.copy()

						#One protein for each entry
						exEntry["Protein Numbers"] = protein

						#References have commentary which is the year
						if exEntry["COMMENTARY"] and sub != "RF":
							comments  = exEntry["COMMENTARY"].split('; ')
						else:
							comments = []

						exEntry["COMMENTARY"] = []
						for comment in comments:

							#Find last #
							end = comment.rfind("#")
							#If there is a last #
							if end>0:
								header = comment[1:end]
								header = header.split(',')

								for head in header:

									if head == exEntry["Protein Numbers"]:
										exEntry["COMMENTARY"].append(comment[end+2:])
							else:
								exEntry["COMMENTARY"].append(comment)

						if exEntry["COMMENTARY"] == []:
							exEntry["COMMENTARY"] = None

						exSub.append(exEntry)
				else:
					exSub.append(entry)

			dc[ec][sub] = exSub

	return dc

#Uses columns json to fill in column values
def getJSON(jsn):
	file = open(jsn).read()
	loadJson = json.loads(file)
	return loadJson


#Creates backbone of dictionary (EC number and subdictionaries)
def bulkProcess(columnValues, brendaData, line, currID, prevLine, currSubClass):

	#Is EC#
	if line[0:2] == 'ID':
		brendaData, currID = handleID(columnValues, brendaData, line[0:-1])

	#End EC
	elif line == '///\n': 
		return brendaData, currID, prevLine, currSubClass

	#Pass over notes
	elif prevLine[0:2] == 'ID':

		#End of notes
		if line != '\n': 
			return brendaData, currID, prevLine, currSubClass
	else: 
		if line != '\n': 
			subclassIndex = line.find('\t')
			brendaData, currSubClass = appendSubDict(brendaData, line, currID, subclassIndex, currSubClass)		

	prevLine = line
	return brendaData, currID, prevLine, currSubClass


#Creates EC key in dictionary and initialezes subclasses to empty
def handleID(columnValues, brendaData, line):

	#Strips EC number
	line = line.strip('ID\t')
	brendaData[line] = {}

	for subclass in columnValues:

		brendaData[line][subclass] = []

	return brendaData, line


#Appends to subclasses of ECs
def appendSubDict(brendaData, line, currID, subclassIndex, currSubClass):

	#Has header
	if subclassIndex > 0:
		currSubClass = line[0:subclassIndex]
		brendaData[currID][currSubClass].append(line[subclassIndex+1:-1])

	#Is extra information
	elif subclassIndex == 0: 
		last_elt = brendaData[currID][currSubClass].pop()
		last_elt = last_elt+line[0:-1]
		brendaData[currID][currSubClass].append(last_elt)

	return brendaData, currSubClass


#Orders each entry into a TITLE, commentary, special, and Literature sections
def orderData(columnValues, key, subclass, entry):
	returnDict = {}

	#remove header
	header, entry = proteinHeader(entry)
	returnDict["Protein Numbers"] = header

	#remove tabs
	entry = entry.replace('\t',' ')

	#If this subclass contains a special field
	if 'SPECIAL' in columnValues[subclass]:

		#removes special field
		entry, special = specialFields(entry)
		returnDict["SPECIAL"] = special

	#Unique subs with COMMENTARY (PRODUCT)
	if subclass == "SP" or subclass == "NSP":
		entry, prodComment = formatSP(entry, returnDict)

	#Standard breakdown
	returnDict["COMMENTARY"], returnDict["TITLE"], returnDict["LITERATURE"] = parseRemains(entry)

	if subclass == "PR":
		TITLE = returnDict["TITLE"].split(' ')
		returnDict, TITLE = formatProtein(TITLE, returnDict)

	if subclass == "RF":
		returnDict["LITERATURE"] = (returnDict["TITLE"].split(' ')[0])[1:-1]
		returnDict["TITLE"] = returnDict["TITLE"].replace("<"+returnDict["LITERATURE"]+"> ", "")


	#Uses None instead of ""
	if returnDict["COMMENTARY"] == "":
		returnDict["COMMENTARY"] = None

	if returnDict["TITLE"] == "":
		returnDict["TITLE"] = None

	if returnDict["LITERATURE"] == "":
		returnDict["LITERATURE"] = None

	return returnDict

#Creates COMMENTARY (PRODUCT) sections for NSP and SP
def formatSP(entry, returnDict):
	prodComment = None

	#Find all indicies of "|"
	prod_indicies = [i for i in range(len(entry)) if entry[i] == "|"]

	#If we dont have a prodComment
	if len(prod_indicies) > 1:

		#COMMENTARY (PRODUCT) is assumed to be the first and second indicies
		prodComment = entry[prod_indicies[0]:prod_indicies[1]+1]

		#Remove the product comment
		entry = entry.replace(prodComment, "")

		#Strip the two |
		prodComment = prodComment[1:-1]

	returnDict["COMMENTARY (Product)"] = [prodComment]
	return entry, returnDict


#Adds uniprot and swissprot fields for protein section
def formatProtein(TITLE, returnDict):

	#create sections as null
	returnDict["DATABASE"] = None
	returnDict["UNIPROT"] = None

	#if last substring is uniprot
	if TITLE[-1].lower() == 'uniprot':

		#Uniprot is second to last
		returnDict["UNIPROT"] = TITLE[-2]
		returnDict["DATABASE"] = 'UniProt'

		#without accession or database
		TITLE = TITLE[:-2]
		returnDict["TITLE"] = ' '.join(TITLE)

	#if last substring is swissprot
	elif TITLE[-1].lower() == 'swissprot':

		#Uniprot is second to last
		returnDict["UNIPROT"] = TITLE[-2]
		returnDict["DATABASE"] = 'SwissProt'

		#without accession or database
		TITLE = TITLE[:-2]
		returnDict["TITLE"] = ' '.join(TITLE)

	#if last is genbank
	elif TITLE[-1].lower() == 'genbank':

		#Uniprot is second to last
		returnDict["UNIPROT"] = TITLE[-2]
		returnDict["DATABASE"] = 'GenBank'

		#without accession or database
		TITLE = TITLE[:-2]
		returnDict["TITLE"] = ' '.join(TITLE)

	return returnDict, TITLE


#Parses protein section information
def proteinHeader(entry):

	#If entry is nothing
	if entry == "":
		return None, entry

	#If protein header
	if entry[0] == '#':
		for i in range(1,len(entry)):

			#end of protein header
			if entry[i] == '#':

				#header without #
				header = entry[1:i]

				#entry without header
				entry = entry[i+1:]

				#replaces tabs with commas
				header = header.replace('\t', ',')

				#split by commas
				header = header.split(',')

				return header, entry

	return  None, entry



#Initializes fields, calls functions to pull Literature, comments, and extras
def parseRemains(entry):
	TITLE, Comments, Literature = [None]*3

	#Removes Literature from the entry
	entry, Literature = parseLiterature(entry)

	#Removes tabs from the entry
	entry = entry.replace('\t', ' ')
	#Finds all ") " and makes array of their indicies
	end_indicies = [i for i in range(len(entry)) if entry.startswith(") ", i)]

	if end_indicies: 
		#Removes comments from entry
		entry, Comments = commentStack(entry, end_indicies[-1])

	#TITLE is the remaining after this process
	TITLE = entry

	#Remove possible blank space
	TITLE = TITLE.strip()

	return Comments, TITLE, Literature



#Parses Literature section within <...>
def parseLiterature(entry):

	#Adds an extra space so ending parenthesis is interprited 
	entry = entry + ' '
	tempEntry = entry

	#Finds last closing citation parenthesis
	end_citation = [i for i in range(len(tempEntry)) if tempEntry.startswith('> ', i)]
	if not end_citation:
		return entry, None

	#Finds last opening special parenthesis 
	start_citation = [i for i in range(len(tempEntry)) if tempEntry.startswith(' <', i)]
	if not start_citation:
		return entry, None

	#Literature are last indicies of find
	refs = tempEntry[start_citation[-1]+2:end_citation[-1]]

	#replace spaces with commas
	refs = refs.replace(' ', ',')

	#list by commas
	refs = refs.split(',')

	return entry[0:start_citation[-1]+1], refs


#Parses special fields contained in {...}
def specialFields(entry):

	#Adds an extra space so ending parenthesis is interprited 
	entry = entry + ' '
	tempEntry = entry

	#Finds last closing special parenthesis
	end_special = [i for i in range(len(tempEntry)) if tempEntry.startswith('} ', i)]
	if not end_special:
		return entry, None

	#Finds last opening special parenthesis 
	start_special = [i for i in range(len(tempEntry)) if tempEntry.startswith(' {', i)]
	if not start_special:
		return entry, None

	#special is last indicies of find 
	special = tempEntry[start_special[-1]+2:end_special[-1]]

	#remove special
	entry = entry.replace("{" + special + "}", "")

	return entry, special



#Stack for parsing the comment section, looks for closing parenthesis
def commentStack(entry, startIndex):

	#Before last parenthesis found
	index = startIndex-1
	comment = ""
	stack = 1

	while index !=0 and stack>0:

		#new nested comment
		if entry[index] == ")":
			stack+=1

		#close nested comment
		if entry[index] == "(":
			stack-=1

		index = index-1

	#comment includes parenthesis  	
	comment = entry[index+1:startIndex+1]

	#remove comment
	entry = entry.replace(comment, "")

	#remove spaces
	entry = entry.strip()

	#remove parenthesis
	comment = comment[1:-1]

	return entry, comment


#run
start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))


