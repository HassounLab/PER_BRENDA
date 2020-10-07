# 
#
#                       perBRENDAExtract.py
# 
#       Date:     9/28/20
#  
#      PER BRENDA: Parse and Extract tool for Machine Learning applications using the BRENDA Database 
#
# 	Gian Marco Visani1,&, Thomas McNulty1,&, and Soha Hassoun1,2,* 
#
# 	1 Department of Computer Science, Tufts University, 161 College Ave, Medford, MA, 02155, USA 
#
# 	2 Department of Chemical and Biological Engineering, Tufts University, 4 Colby St, Medford, MA, 02155, USA 
#
# 	&Equal contribution. 
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
