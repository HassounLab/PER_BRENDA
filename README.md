# PER BRENDA

**Overview**<br>
Enzyme information from the BRENDA database is accessible through both a SOAP interface. Currently, the SOAP interface requires an extensive knowledge of the provided methods. Repeated queries of the text file, which are costly in terms of time and efficiency, are needed to gather enzymatic information for machine learning applications. 

PER BRENDA converts the provided BRENDA text file into a JSON which mirrors BRENDA's structural organization. This intuitive design allows a user to quickly and easily perform queries for desired information across various enzymes. The parsed output JSON can then be traversed for EC numbers, categories, subcategories, and fields of the JSON. an Aptional parameter allows for extracting the file in a comma sepa-rated textfile. 

Feel free to use this code!  But if you do, please provide reference to the following publciation:
TBA 


# Dependencies
`Python 3.8` <br>
`pandas`

# How to parse the textfile?
`Python perBRENDAParser.py --ifile brenda_download.txt --ofile parsed.json` *optionally --efile error.json*


# How to extract from the json?
`Python perBRENDAExtract.py --ifile parsed.json --templatefile template.json --ofile extract.json`<br> *optionally --csvfile brenda.csv --compoundfile comps.txt* <br>

Extractions may be executed provided with a parsed JSON file name, output file name, and extraction parameters. These parameters include EC numbers, subcategories, and fields of interest. For command line extractions, a templatefile should be included to extract these parameters, an example template may be found in entryTemplate.json and categoryTemplate.json.

For the extraction of a single subcategory, a csvfile may be provided for a csv output of the subcategory. For extractions with Substrate/Product and Natural Substrates a compoundfile which will contain a list of all the compound names in the extraction result without duplicates. The file may be processed on MetaboAnalyst for KEGG, PubChem, and other database ID numbers.

Category: Labels shown in BRENDA sidebar (example Enzyme-Ligand Interactions)

Subcategory: Labels shown under each category (example Activating Compounds)

Fields: Columns in each subcategory (example (under Activating Compounds) ACTIVATING COMPOUND, UNIPROT, or COMMENTARY) 

To extract multiple EC numbers under the same branch, use `'.'` at the end of the stem (example '1.1.') 


Avaliable fields are as follows:

 	Activating Compound (AC): COMMENTARY, LITERATURE, ORGANISM, ACTIVATING COMPOUND, UNIPROT

	Applications (AP): COMMENTARY, LITERATURE, ORGANISM, APPLICATION, UNIPROT

	Cofactors (CF): COMMENTARY, LITERATURE, ORGANISM, COFACTOR, UNIPROT

	Cloned (CL): CLONED (Commentary), LITERATURE, ORGANISM, UNIPROT

	Crystallization (CR): CRYSTALLIZATION (Commentary), LITERATURE, ORGANISM, UNIPROT

	Protein Variants (EN): COMMENTARY, LITERATURE, ORGANISM, PROTEIN VARIANTS, UNIPROT

	Expression (EXP): LITERATURE, ORGANISM, EXPRESSION, COMMENTARY, UNIPROT

	General Information (GI): COMMENTARY, LITERATURE, ORGANISM, GENERAL INFORMATION, UNIPROT

	General Stability (GS): GENERAL STABILITY, LITERATURE, ORGANISM, UNIPROT

	IC50 Values (IC50): COMMENTARY, LITERATURE, ORGANISM, INHIBITOR, IC50 VALUE, UNIPROT

	Inhibitors (IN): COMMENTARY, LITERATURE, ORGANISM, INHIBITOR, UNIPROT

	Ki Values (KI): COMMENTARY, LITERATURE, ORGANISM, INHIBITOR, Ki VALUE, UNIPROT

	kcat/KM Values (KKM): COMMENTARY, LITERATURE, ORGANISM, SUBSTRATE, kcat/KM VALUE, UNIPROT

	KM Values (KM): COMMENTARY, LITERATURE, ORGANISM, SUBSTRATE, KM VALUE, UNIPROT

	Localizations (LO): COMMENTARY, LITERATURE, ORGANISM, LOCALIZATION, UNIPROT

	Metals and Ions (ME): COMMENTARY, LITERATURE, ORGANISM, METALS and IONS, UNIPROT

	Molecular Weight (MW): COMMENTARY, LITERATURE, ORGANISM, MOLECULAR WEIGHT, UNIPROT

	Natural Substrates (NSP): COMMENTARY (Substrate), COMMENTARY (Product), LITERATURE, ORGANISM, NATURAL PRODUCT, REVERSIBILITY, NATURAL SUBSTRATE, UNIPROT

	Oxidation Stability (OS): OXIDATION STABILITY, LITERATURE, ORGANISM, UNIPROT

	Organic Solvent Stability (OSS): COMMENTARY, LITERATURE, ORGANISM, ORGANIC SOLVENT, UNIPROT

	pH Optima (PHO): COMMENTARY, LITERATURE, ORGANISM, pH OPTIMUM, UNIPROT

	pH Range (PHR): COMMENTARY, LITERATURE, ORGANISM, pH RANGE, UNIPROT

	pH Stability (PHS): COMMENTARY, LITERATURE, ORGANISM, pH STABILITY, UNIPROT

	pI Values (PI): COMMENTARY, LITERATURE, ORGANISM, pI VALUE, UNIPROT

	Posttranslational Modification (PM): COMMENTARY, LITERATURE, ORGANISM, POSTTRANSLATIONAL MODIFICATION, UNIPROT

	Organisms (PR): COMMENTARY, SEQUENCE DB, LITERATURE, ORGANISM, ORGANISM, UNIPROT

	Purification (PU): PURIFICATION (Commentary), LITERATURE, ORGANISM, UNIPROT

	Reactions (RE): COMMENTARY, LITERATURE, ORGANISM, REACTION, UNIPROT **bad**

	Renatured (REN): RENATURED/Commentary, LITERATURE, ORGANISM, UNIPROT

	References (RF): COMMENTARY, LITERATURE, REFERENCES

	IUPAC Name (RN): ACCEPTED NAME (IUPAC)

	Reaction Types (RT): REACTION TYPE

	Specific Activity (SA): COMMENTARY, LITERATURE, ORGANISM, SPECIFIC ACTIVITY, UNIPROT

	Systematic Name (SN): SYSTEMATIC NAME

	Substrates/Products (SP): COMMENTARY (Substrate), COMMENTARY (Product), LITERATURE, ORGANISM, PRODUCT, REVERSIBILITY, SUBSTRATE, UNIPROT

	Storage Stability (SS): STORAGE STABILITY, LITERATURE, ORGANISM, UNIPROT

	Source Tissues (ST): COMMENTARY, LITERATURE, ORGANISM, SOURCE TISSUE, UNIPROT

	Subunits (SU): COMMENTARY, LITERATURE, ORGANISM, SUBUNIT, UNIPROT

	Synonyms (SY): COMMENTARY, LITERATURE, ORGANISM, SYNONYM, UNIPROT

	Turnover Numbers (TN): COMMENTARY, LITERATURE, ORGANISM, SUBSTRATE, TURNOVER NUMBER, UNIPROT

	Temperature Optima (TO): COMMENTARY, LITERATURE, ORGANISM, TEMPERATURE OPTIMUM, UNIPROT

	Temperature Range (TR): COMMENTARY, LITERATURE, ORGANISM, TEMPERATURE RANGE, UNIPROT

	Temperature Stability (TS): COMMENTARY, LITERATURE, ORGANISM, TEMPERATURE STABILITY, UNIPROT
