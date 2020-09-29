# PERBRENDA

**Overview**<br>
Aggregating bulk enzyme information from BRENDA Enzymes is accessible through both a SOAP interface and text file. Currently, the SOAP interface requires an extensive knowledge of the provided methods, and for bulk enzyme data applications repeated queries of the text file are costly in terms of time and efficiency.

PERBRENDA converts the provided BRENDA text file into a JSON structure which mirrors BRENDA's structure. This intuitive design allows a user to quickly and easily perform queries for desired information across various enzymes. Additionally included is the BRENDAExtract interface which allows for simple query requests from a template.

# Getting Started
`Python 3.8`

# How to parse the textfile?
`Python BRENDAParser.py --ifile brenda_download.txt --ofile parsed.json` *optionally --efile error.json*

# How to query the json?
`Python BRENDAExtract.py --ifile parsed.json --templatefile template.json --ofile query.json` *optionally --csvfile brenda.csv --compoundfile comps.txt* 


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
