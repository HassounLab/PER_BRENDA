# 
#
#                       Extract.py
#  
#       Authors:  Thomas McNulty 
#       Date:     9/28/20
#  
#       summary
#  
#      Extract class. Capable of extracting EC numbers, categories,
#      subcategories, or fields of subcategories from the parsed JSON file.
# 	   Provided with a csv filename or compound file name additional outputs
#      to JSON may be recieved.
#
# 


import json
import pandas as pd

class extract:

	#Extraction function
	def extract(self, jsn, outfile=None, csvFile, compFile, EC, category = None, subcategory = None, fields = None):
		pd.set_option("display.max_rows", None, "display.max_columns", None)

		if type(EC) is not list:
			EC = [EC]

		if EC == []:
			for ec in jsn:
				EC.append(ec)

		copyEC = EC
		for ecR in copyEC:
			if ecR[-1] == '_':
				for ecC in jsn:
					if ecC.startswith(ecR[0:-1]):
						EC.append(ecC)
				EC.remove(ecR)			
		
		Extract = {}

		#Query specific EC numbers
		if category is None and subcategory is None and fields is None:
			for ec in EC:
				Extract[ec] = jsn[ec]

		#category extraction
		elif category and not subcategory and fields is None:
			Extract = self.categoryExtract(jsn, EC, category)	

		#subcategory extraction
		elif not category and subcategory:
			if not fields:
				for ec in EC:
					Extract[ec] = []
					for entry in jsn[ec][subcategory]:
						Extract[ec].append(entry)
			else:
				for ec in EC:
					Extract[ec] = []
					for entry in jsn[ec][subcategory]:
						values = {}
						for field in fields:
							values[field] = entry[field]
						Extract[ec].append(values)
						
		else:			
			if category and fields:
				print("Do not provide fields with category")

		if compFile and subcategory != 'SP' and subcategory != 'NSP':
			print('Can not get compounds for non SP/NSP')

		elif compFile and not category and subcategory == "SP":			
			if "PRODUCT" not in fields and "SUBSTRATE" not in fields:
				print("Please include at least 1 compound field (PRODUCT or SUBSTRATE)")
			else:
				self.makeCompFile("SUBSTRATE", "PRODUCT", Extract, compFile)
	
		elif compFile and not category and subcategory == "NSP":
			if "NATURAL PRODUCT" not in fields and "NATURAL SUBSTRATE" not in fields:
				print("Please include at least 1 compound field (NATURAL PRODUCT or NATURAL SUBSTRATE)")
			else:
				self.makeCompFile("NATURAL SUBSTRATE", "NATURAL PRODUCT", Extract, compFile)
				

		if subcategory and csvFile:
			csv = []
			for ec in Extract:
				for entry in Extract[ec]:
					clentry = entry.copy()
					clentry["EC Number"] = ec
					csv.append(clentry)

			
			pxl = pd.DataFrame(csv)
			pxl.to_csv(csvFile)

		elif csvFile:
			print("Can not make csv for non-subcategory extract")

		if outfile:
			parsed = json.dumps(Extract, indent=4, sort_keys=True)
			text_file = open(outfile, 'wt')
			text_file.write(parsed)
			text_file.close()


	# Creates compound file
	def makeCompFile(self, substrateName, productName, Extract, compFile):
		compList = set()
		for ec in Extract:
			for entry in Extract[ec]:
				if productName in entry:
					for comp in entry[productName]:
						compList.add(comp)
				if substrateName in entry:
					for comp in entry[substrateName]:
						compList.add(comp)
		text_file = open(compFile, 'wt')
		for line in compList:
			text_file.write("%s\n" % line)
		text_file.close()



	# Runs extract with JSON file input
	def templateExtract(self, infile, outfile, csv, compFile, template):
		self.extract(jsn = infile, outfile = outfile, csvFile = csv, compFile = compFile, **template)


	# Extracts based on category.
	def categoryExtract(self, jsn, EC, category):
		Extract = {}
		Enz_nom = ["SY", "RT", "RE", "SN","ID", "RN"]
		Enz_lig = ["SP","NSP","CF","ME","IN","AC"]
		Func_par = ["KM","TN","IC50","KKM","KI","PHO","PHR","TO","TR","SA","PI"]
		Enz_str = ["CR","MW","PM","SU","EN"]
		Apl = ["AP"]
		Mol_p = ["CL","EXP","GS","OS","OSS","PHS","PU","REN","SS","TS"]
		Gen_info = ["GI"]
		Org_rel = ["LO","ST","PR"]
		Refs = ["RF"]


		for ec in EC:
			Extract[ec] = {}
			if category == 'Enzyme Nomenclature':
				for sub in Enz_nom:
					Extract[ec][sub] = jsn[ec][sub]
			elif category == 'Enzyme Ligand Interactions':
				for sub in Enz_lig:
					Extract[ec][sub] = jsn[ec][sub]
			elif category == 'Functional Parameters':
				for sub in Func_par:
					Extract[ec][sub] = jsn[ec][sub]
			elif category == 'Organism Related Information':
				for sub in Org_rel:
					Extract[ec][sub] = jsn[ec][sub]
			elif category == 'General Information':
				for sub in Gen_info:
					Extract[ec][sub] = jsn[ec][sub]
			elif category == 'Enzyme Structure':
				for sub in Enz_str:
					Extract[ec][sub] = jsn[ec][sub]
			elif category == 'Molecular Properties':
				for sub in Mol_p:
					Extract[ec][sub] = jsn[ec][sub]
			elif category == 'Applications':
				for sub in Apl:
					Extract[ec][sub] = jsn[ec][sub]
			elif category == 'References':
				for sub in Refs:
					Extract[ec][sub] = jsn[ec][sub]
		return Extract
	





