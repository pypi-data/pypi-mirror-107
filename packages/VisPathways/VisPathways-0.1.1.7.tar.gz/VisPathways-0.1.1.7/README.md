# VisPathways Documentation

**VisPathways** is a python library that allows for user-friendly pathway ontology summarization and visualization. The library supports usage from the python environment. Some of functionalities can also be achieved by calling certain files from the command-line.

## Content

1. [Table of Content](#Content)
2. [Installation](#Installation)
3. [Dependencies](#Dependencies)
4. [Functions](#Functions)
5. [Tutorials](#Tutorials)
6. [Acknowledgement](#Acknowledgement)

## Installation

You can install the package with [pip](https://pypi.org/project/pip/) using the command below:

```
pip install -i https://test.pypi.org/simple/ VisPathways==0.1.0.7
```

If you would like the development version of this package, check out our [Github page](https://github.com/tommyfuu/FancyTaxonomies).

## Dependencies

The dependencies should be automatically installed along with VisPathways when you install VisPathway using pip. If you would like to use the development version and install dependencies manually, in addition to the default libraries that come with python, you need:

- the ete3 module. (Install by [pip](https://pypi.org/project/ete3/) or [conda](http://etetoolkit.org/download/))
- [scipy](https://scipy.org/install.html) version 1.6.3
- [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
- [PyQt5](https://pypi.org/project/PyQt5/)

## Functions

Since **VisPathways** is a python library, the users will get the most out of this library by calling the classes and methods from the python environment. The functions of the VisPathways package can easily called within the VisPathways Master Class, which has several subclasses:

- VisPathways
  - [MergeDatabase](#MergeDatabase) (streamlined summarization for GeneOntology, Reactome, and Kegg).
    - [InferGoSlimToGO](#InferGoSlimToGO) (Finding all available pathway hierarchies for GeneOntology database)
    - [InferGoKeggToGO](#InferGoKeggToGO) (Finding all available pathway hierarchies for Kegg database)
    - [InferGoReactomeToGO](#InferGoReactomeToGo) (Finding all available pathway hierarchies for Reactome database)
    - [SummarizePathwayHierarchy](#SummarizePathwayHierarchy) (Generate summary table for a given set of enrichment data)
  - [EnrichmentPreprocess](#EnrichmentPreprocess) (Format and clean enrichment data; conduct scaled summary stats generation)
  - [GOTrees](#GOTrees) (Pathway ontology and enrichment visualization for GeneOntology)

Here we present some of our core methods of each of these classes.

_**IMPORTANT NOTE:** Make sure that `outputRoot` is consistent throughout running the whole workflow from summarization to visualization._

### Inputs for the whole Summarization + Visualization workflow

- You will need a `.obo` file from the GeneOntology database including the pathway hierarchy information. For example, you can use [`go-basic.obo`](http://geneontology.org/docs/download-ontology/), which is the file we use for writing our algorithm if you prefer to use that. There are also other options on that page for downloads. Similar file is required for Kegg (e.g. [`hsa00001.keg`](https://www.kegg.jp/kegg-bin/download_htext?htext=hsa00001.keg&format=htext&filedir=)) and Reactome (e.g.[ `ReactomePathwaysRelation.txt`](https://reactome.org/download/current/ReactomePathwaysRelation.txt)).
- You will need a `.xml` file including all the pathway signatures. We have one (`msigdb_v7.2.xml`) by default in this directory if you prefer to use that.
- You will need at least one pathway enrichment file in `.csv` format. For examples of this file, see `H_24hUV_over_30minUV_Enrichment.csv` or `gsea.FCG_GObp_8.27.20.csv` in the `test` directory. We are working on supporting more file formats. Additionally, you can have more relevant enrichment files in the same format for visualization. Note that this csv file should only contain one single column, with a column name that is NOT pathway name, and the file should NOT contain indices. There is also an option for inputting multiple enrichments at once to generate multiple summary statistics. For that, check out the `multipleEnrichmentFileProcess` method under the `EnrichmentPreprocess` class for more information.

### MergeDatabase

#### _Function_ MergeDatabase.generateSummaries

```
MergeDatabase.generateSummaries()
```

Asks user to input and confirm database used (G for GeneOntology; R for Reactome; K for Kegg).

Generate three files:

- _OutputRoot_.term_classes_to_pathways.xls (summarizing each standard pathway and its descendants)
- _OutputRoot_.pathway_to_go_id_ancestors.xls (summarizing each standard pathway and its ancestors)
- _OutputRoot_.pathway_count.xls (summarizing each enriched pathway's summary data)

**_Example Usage_**

```
#  After specifying ontologyFile (path), xmlFile (path), enrichmentFile (path), outputRoot (string)
from VisPathways import MergeDatabase
md = MergeDatabase(ontologyFile, xmlFile, enrichmentFile, outputRoot)
md.generateSummaries()
```

### InferGoSlimToGO

#### _Function_ InferGoSlimToGO.work

```
InferGoSlimToGO.work()
```

Generate two files:

- _OutputRoot_.term_classes_to_pathways.xls (summarizing each standard pathway and its descendants)
- _OutputRoot_.pathway_to_go_id_ancestors.xls (summarizing each standard pathway and its ancestors)

(Along with some artifact files necessary for tree visualization, don't delete!)

**_Example Usage_**

```
#  After specifying ontologyFile (path), xmlFile (path),outputRoot (string)
from VisPathways import InferGoSlimToGO
in = InferGoSlimToGO(ontologyFile, xmlFile, outputRoot)
in.work()
```

### InferGoKeggToGO

#### _Function_ InferGoKeggToGO.work

```
InferGoKeggToGO.work()
```

Generate two files:

- _OutputRoot_.term_classes_to_pathways.xls (summarizing each standard pathway and its descendants)
- _OutputRoot_.pathway_to_go_id_ancestors.xls (summarizing each standard pathway and its ancestors)

**_Example Usage_**

```
#  After specifying ontologyFile (path), xmlFile (path),outputRoot (string)
from VisPathways import InferGoKeggToGO
in = InferGoKeggToGO(ontologyFile, xmlFile, outputRoot)
in.work()
```

### InferGoReactomeToGO

#### _Function_ InferGoReactomeToGO.work

```
InferGoReactomeToGO.work()
```

Generate two files:

- _OutputRoot_.term_classes_to_pathways.xls (summarizing each standard pathway and its descendants)
- _OutputRoot_.pathway_to_go_id_ancestors.xls (summarizing each standard pathway and its ancestors)

**_Example Usage_**

```
#  After specifying ontologyFile (path), xmlFile (path),outputRoot (string)
from VisPathways import InferGoReactomeToGO
in = InferGoReactomeToGO(ontologyFile, xmlFile, outputRoot)
in.work()
```

### SummarizePathwayHierarchy

#### _Function_ SummarizePathwayHierarchy.work

```
SummarizePathwayHierarchy.work()
```

Given outputs of any of the three functions above, generate:

- _OutputRoot_.pathway_count.xls (summarizing each enriched pathway's summary data)

_Note that because of the limited ontology information in Kegg and Reactome databases, it is generally recommended to use this method for GeneOntology rather than the other two databases._

**_Example Usage_**

```
#  After specifying term_classes_to_pathways_path (path), pathway_to_go_id_ancestors (path), outputRoot (string)
from VisPathways import SummarizePathwayHierarchy
md = SummarizePathwayHierarchy(term_classes_to_pathways_path, pathway_to_go_id_ancestors, outputRoot)
md.generateSummaries()
```

### GOTrees

#### _Function_ GOTrees.graphTreeWrapper

```
GOTrees.graphTreeWrapper(select='all', enrichment=1, firstEnrichmentName='enrichment 1', enrichVis='pie', outputFormat='png', numOfBackgroundEnrichments=0)
```

_Arguments:_

- **select** (string): **'all'** (visualize tree for all descendants of a selected node in the GeneOntology database) or **'legit'** (visualize tree for standard descendants of a selected node specified in the xml file in the GeneOntology database)
- **enrichment** (int): **1**, **2**, or **3**. Number of enrichment files displayed in one single tree graph. The current package supports up to 3 enrichments (1 default enrichment from summarization + 0-2 additional enrichment files). Note that the function will ask users to specify the path to additional enrichment files if applicable.
- **firstEnrichmentName** (string): default value **'enrichment 1'**. The name of the default enrichment from summarization displayed on the trees. Note that the function will ask users to specify the names of the other enrichment files if applicable.
- **enrichVis** (string): **'pie'** or **'sphere'**, default value **'pie'**, the two different ways to visualize enrichment annotations on ontology trees.
- **outputFormat** (string): **'png'**, **'pdf'**, or **'svg'**, default value **'png'**, three supported output formats of ontology visualizations.
- **numOfBackgroundEnrichments** (int): default value **0**. Background enrichments are those enrichments who will show up at the tips but not as part of the pie chart or sphere representation.

Generate:

- _OutputRoot_.treeGraph*index*._outputFormat_ (tree visualizations of pathway ontology and enrichments, e.g. _test.treeGraph.1.svg_. The function can generate multiple tree graphs at a time.)

_Note that the function can also request users to input the following_

- The paths to additional enrichments (if applicable).
- The names of additional enrichments (if applicable).
- Segment Coloring (if _select = **'all**_, you can choose to color certain parts of the tree).

**_Example Usage_**

```
#  After outputRoot (string)
from VisPathways import GOTrees
tr = GOTrees(outputRoot)
tree.graphTreeWrapper(select = 'legit', enrichment = 3, firstEnrichmentName='MM1m_24h_over_NoUV', outputFormat='pdf')
```

### EnrichmentPreprocess

#### _Function_ EnrichmentPreprocess.splitFilesAndRunSummary

```
EnrichmentPreprocess.splitFilesAndRunSummary(source, ontologyFile, xmlFile, runAncAndDes=False, deleteTempCSV=True)
```

_Arguments:_

- **source** (string): path to the enrichment file that contains multiple columns. The first column contains all the pathway names while the rest of the columns each contains the enrichment data. The method assumes a non-zero value in a cell as the pathway being enriched in that corresponding column. An example of such file would be the `namsed-pathwaysuper-sig-bp.txt` file in the `test` directory.
- **ontologyFile** (string): path to the ontology file such as `go-basic.obo`.
- **xmlFile** (string): path to the gsea xml file, such as `msigdb_v7.2.xml`.
- **runAncAndDes** (boolean): whether or not to run the part of the workflow that generates the `pathway_to_ancestor` and `pathway_to_descendant` files. If _False_ (by default), then the function assumes that you have the `pathway_to_ancestor` and `pathway_to_descendant` files in the current directory.
- **deleteTempCSV** (boolean): the function generates artifact csv files that are essentially the csv files needed to run one single enrichment summary with the **SummarizePathwayHierarchy** class. If you wish to keep these files, set this argument to False, otherwise, set it to True.

Generate:

A series of _OutputRoot_**columnName**.pathway_count.xls (the number of files in this series will be the number of columns in the input file)

If **runAncAndDes** is set to True, the method also generates:

- _OutputRoot_.term_classes_to_pathways.xls (summarizing each standard pathway and its descendants)
- _OutputRoot_.pathway_to_go_id_ancestors.xls (summarizing each standard pathway and its ancestors)

If **deleteTempCSV** is set to False, the method also generates a series of files that look like _outputRoot_**colNames**.temp.csv, each of which is a single enrichment file.

_Note that because of the limited ontology information in Kegg and Reactome databases, it is generally recommended to use this method for GeneOntology rather than the other two databases._

**_Example Usage_**

```
#  After defining outputRoot (string), ontologyFile (string), xmlFile (string)
from VisPathways import EnrichmentPreprocess
en = EnrichmentPreprocess(outputRoot)
en.splitFilesAndRunSummary(source, ontologyFile, xmlFile, runAncAndDes=True)
```

## Tutorials

Here are two tutorials for using the whole summarization + visualization workflow. Note that you will need to do everything here in the Python environment! (You can do it by simply typing `python` or `python3` in your terminal and then return)

### 1. Single enrichment summarization + canonical tree visualization

```
from VisPathways import *
ontologyFile = 'go-basic.obo'
xmlFile = 'msigdb_v7.2.xml'
enrichmentFile = 'H_24hUV_over_30minUV_Enrichment.csv'
outputRoot = 'test'
# summarization
md = MergeDatabase(ontologyFile, xmlFile, enrichmentFile, outputRoot)
md.generateSummaries()
# visualization
gr = GOTrees(outputRoot)
gr.graphTreeWrapper(select = 'legit', enrichment = 3, firstEnrichmentName='Moorthy_all', outputFormat='pdf')
## upon function request, select the third tree to plot (select top 3 enrichments, and select N to the first two tree and Y for the third tree), then input two additional enrichment files and their names (here we assign as 'enrichment 1' and 'yeehaw'), and we are done!
```

Here is the link to the result tree plot:
[plot](https://github.com/tommyfuu/FancyTaxonomies/blob/main/stableUsage/src/test.treeGraph.1.pdf)

### 2. Multiple enrichment summarization + canonical tree visualization

```
from VisPathways import *
ontologyFile = '/Users/chenlianfu/Documents/Github/FancyTaxonomies/stableUsage/test/testSourceData/go-basic.obo'
xmlFile = '/Users/chenlianfu/Documents/Github/FancyTaxonomies/stableUsage/test/testSourceData/msigdb_v7.2.xml'
multiEnrichmentFile = '/Users/chenlianfu/Documents/Github/FancyTaxonomies/stableUsage/test/testSourceData/namsed-pathwaysuper-sig-bp.txt'
outputRoot = 'hoa'
# summarization
md = MergeDatabase(ontologyFile, xmlFile, 'enrichmentPlaceholder', outputRoot)
md.generateAncAndDecOnly()
en = EnrichmentPreprocess(outputRoot)
en.splitFilesAndRunSummary(multiEnrichmentFile, ontologyFile, xmlFile, runAncAndDes=True)
# visualization
gr = GOTrees(outputRoot)
gr.graphTreeWrapper(select = 'legit', enrichment = 3, firstEnrichmentName='', outputFormat='pdf', numOfBackgroundEnrichments = 3)
## upon function request, select the third tree to plot (select top 3 enrichments, and select N to the first two tree and Y for the third tree), then input two additional enrichment files and their names (here we assign as 'enrichment 1' and 'yeehaw'), and we are done!
```

## Acknowledgement

**author**: Chenlian (Tom) Fu, Dr. Cristian Coarfa\
**affiliation**: Coarfa Lab, Baylor College of Medicine\
**support**: Dr. Cristian Coarfa, Dr. Sandy Grimm, Dr. Tajhal Patel

Cheers,\
TF\
04/20/2021
