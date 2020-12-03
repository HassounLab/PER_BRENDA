# 
#
#                       Extract.py
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

import json
import pandas as pd
import sys

class extract:

	#main extraction function
	def extract(self, jsn, outfile, csvFile, compFile, EC, category = None, subcategory = None, fields = None):
		pd.set_option("display.max_rows", None, "display.max_columns", None)

		#makes list from EC if not list
		if type(EC) is not list:
			EC = [EC]

		#get all EC numbers
		if EC == []:
			for ec in jsn:
				EC.append(ec)

		copyEC = EC
		
		#EC number tree
		for ecR in copyEC:
			if ecR[-1] == '.':
				for ecC in jsn:
					if ecC.startswith(ecR[0:-1]):
						EC.append(ecC)
				EC.remove(ecR)			
		
		Extract = {}

		#Extract specific EC numbers
		if category is None and subcategory is None and fields is None:
			for ec in EC:
				Extract[ec] = jsn[ec]

		else:

			#Warnings and exits
			if category == None and subcategory == None:
				sys.exit("Please provide a category and or subcategory")

			if type(subcategory) == str:
				subcategory = [subcategory]
			elif not subcategory:
				subcategory = []

			if type(fields) == str:
				fields = [fields]				

			if category:
				if type(category) == str:
					category = [category]
				for cat in category:
					subcategory = subcategory + self.categoryExtract(cat)

			if len(subcategory) > 1 and fields:
				print("Warning: Fields do not work with category or more than 1 subcategory")

			if len(subcategory)>1 and csvFile:
				print("Warning: csv only for 1 subcategory")

			if len(subcategory)>1 and compFile:
				print("Warning: compoundFile only for 1 subcategory")

			#One subcategory extractions
			if len(subcategory) == 1:
				if fields:
					for ec in EC:
						Extract[ec] = []
						for entry in jsn[ec][subcategory[0]]:
							values = {}
							for field in fields:
								values[field] = entry[field]
							Extract[ec].append(values)
				else:
					for ec in EC:
						Extract[ec] = []
						for entry in jsn[ec][subcategory[0]]:
							Extract[ec].append(entry)
						

				if compFile and subcategory[0] != 'SP' and subcategory[0] != 'NSP':
					print('Can not get compounds for non SP/NSP')

				elif compFile and not category and subcategory[0] == "SP":			
					if fields != None and ("PRODUCT" not in fields and "SUBSTRATE" not in fields):
						print("Failed: Please include at least 1 compound field (PRODUCT or SUBSTRATE)")
					else:
						self.makeCompFile("SUBSTRATE", "PRODUCT", Extract, compFile)
			
				elif compFile and not category and subcategory[0] == "NSP":
					if fields != None and ("NATURAL PRODUCT" not in fields and "NATURAL SUBSTRATE" not in fields):
						print("Failed: Please include at least 1 compound field (NATURAL PRODUCT or NATURAL SUBSTRATE)")
					else:
						self.makeCompFile("NATURAL SUBSTRATE", "NATURAL PRODUCT", Extract, compFile)

				if csvFile:
					csv = []
					for ec in Extract:
						for entry in Extract[ec]:
							clentry = entry.copy()
							clentry["EC Number"] = ec
							csv.append(clentry)

					
					pxl = pd.DataFrame(csv)
					pxl.to_csv(csvFile)

			else:
				for ec in EC:
					Extract[ec] = {}
					for sub in subcategory:
						Extract[ec][sub] = jsn[ec][sub]
				

			

		parsed = json.dumps(Extract, indent=4, sort_keys=True)
		text_file = open(outfile, 'wt')
		text_file.write(parsed)
		text_file.close()



	def makeCompFile(self, substrateName, productName, Extract, compFile):
		compList = set()
		for ec in Extract:
			for entry in Extract[ec]:
				if productName in entry:
					if entry[productName]:
						for comp in entry[productName]:
							units = comp.split(" ",1)
							if units[0].isnumeric() and len(units)>1:
								comp = units[1]
							compList.add(comp)
				if substrateName in entry:
					if entry[substrateName]:
						for comp in entry[substrateName]:
							units = comp.split(" ",1)
							if units[0].isnumeric() and len(units)>1:
								comp = units[1]
							compList.add(comp)
		text_file = open(compFile, 'wt')
		for line in compList:
			text_file.write("%s\n" % line)
		text_file.close()



	# Runs extract with JSON file input
	def templateExtract(self, infile, outfile, csv, compFile, template):
		self.extract(jsn = infile, outfile = outfile, csvFile = csv, compFile = compFile, **template)


	# Queries based on category.
	def categoryExtract(self, category):
		Sub = []
		Enz_nom = ["SY", "RT", "RE", "SN", "RN"]
		Enz_lig = ["SP","NSP","CF","ME","IN","AC"]
		Func_par = ["KM","TN","IC50","KKM","KI","PHO","PHR","TO","TR","SA","PI"]
		Enz_str = ["CR","MW","PM","SU","EN"]
		Apl = ["AP"]
		Mol_p = ["CL","EXP","GS","OS","OSS","PHS","PU","REN","SS","TS"]
		Gen_info = ["GI"]
		Org_rel = ["LO","ST","PR"]
		Refs = ["RF"]

		if category == 'Enzyme Nomenclature':
			Sub = Enz_nom
		elif category == 'Enzyme Ligand Interactions':
			Sub = Enz_lig
		elif category == 'Functional Parameters':
			Sub = Func_par
		elif category == 'Organism Related Information':
			Sub = Org_rel
		elif category == 'General Information':
			Sub = Gen_info
		elif category == 'Enzyme Structure':
			Sub = Enz_str
		elif category == 'Molecular Properties':
			Sub = Mol_p
		elif category == 'Applications':
			Sub = Apl
		elif category == 'References':
			Sub = Refs
		else:
			sys.exit("Invalid category")

		return Sub
	
