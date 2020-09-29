# 
#
#                       BRENDAExtract.py
#  
#       Authors:  Thomas McNulty 
#       Date:     9/28/20
#  
#       summary
#  
#      Extract runner file. Extracts information from JSON based
#      on provided command line arguments.  
#  
#  


from Extract import extract
import getopt, sys
import json

def main():
	infile = ''
	template = ''
	outfile = ''
	csvFile = False
	compFile = False

	#argument handleing
	try:
		optList, args = getopt.getopt(sys.argv[1:], 'hi:t:ovc', ["ifile=","templatefile=","ofile=", "csvfile=", "compoundfile="])
	except getopt.GetoptError:
		print('Usage: BRENDAExtract.py --ifile <inputfile> --templatefile <templatefile> --ofile <outputfile>')
		sys.exit(2)
	for opt, arg in optList:

		if opt == '-h':
			print('Usage: BRENDAExtract.py --ifile <inputfile> --templatefile <templatefile> --ofile <outputfile>')
			sys.exit()

		elif opt in ("-i", "--ifile"):
			infile = arg

		elif opt in ("-t", "--templatefile"):
			template = arg

		elif opt in ("-o", "--ofile"):
			outfile = arg

		elif opt in ("-v","--csvfile"):
			csvFile = arg

		elif opt in ("-c","--compoundfile"):
			compFile = arg

	q = extract()

	input_file = open(infile).read()
	input_json = json.loads(input_file)

	template_file = open(template).read()
	template_json = json.loads(template_file)

	q.templateExtract(input_json, outfile, csvFile, compFile, template_json)



main()