
#!/usr/bin/env python
__author__ = "Tom Fu"

__version__ = "1.0"


import pickle
from ete3 import Tree, TreeStyle, Tree, TextFace, add_face_to_node, NodeStyle, faces, AttrFace, CircleFace, PieChartFace
import re
import random
import pandas as pd
import math
import numpy as np
import time

# from CCLabUtils.simpleTime import SimpleTime
from simpleTime import SimpleTime
from enrichment import *

NUML = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

ENRICHMENTPERCENTS = {"1": [100], "2": [100], "3": [100],
                      "1-2": [50, 50], "1-3": [50, 50], "2-3": [50, 50], "1-2-3": [33.3, 33.3, 33.4]}

ENRICHCOLOR1 = "Red"
ENRICHCOLOR2 = "Green"
ENRICHCOLOR3 = "Blue"

# ENRICHMENTCOLORS = {"1": ["Red"], "2": ["Green"], "3": ["Blue"],
#                     "1-2": ["Red", "Green"], "1-3": ["Red", "Blue"], "2-3": ["Blue", "Green"], "1-2-3": ["Red", "Blue", "Green"]}

SUPPORTEDFORMATS = ['png', 'pdf', 'svg']


class GOTrees():
    def __init__(self, outputRoot, canonicalEnrichment='', displayedEnrichmentColors=[ENRICHCOLOR1, ENRICHCOLOR2, ENRICHCOLOR3]):
        self.outputRoot = outputRoot
        self.canonicalEnrichment = canonicalEnrichment
        self.ENRICHMENTCOLORS = {"1": [displayedEnrichmentColors[0]], "2": [displayedEnrichmentColors[1]], "3": [displayedEnrichmentColors[2]],
                                 "1-2": [displayedEnrichmentColors[0], displayedEnrichmentColors[1]], "1-3": [displayedEnrichmentColors[0], displayedEnrichmentColors[2]], "2-3": [displayedEnrichmentColors[1], displayedEnrichmentColors[2]], "1-2-3": [displayedEnrichmentColors[0], displayedEnrichmentColors[1], displayedEnrichmentColors[2]]}

        self.enrichmentsL = []

    def selectSubTrees(self):
        """Following outputs from merger to allow users to select trees to be plotted"""
        currentSummaryFile = self.outputRoot + \
            self.canonicalEnrichment + '.pathway_count.xls'
        topPathwayReader = open(currentSummaryFile, "r")
        summaryDict = {}
        counter = 0
        for line in topPathwayReader:
            currentLineContent = line.split('	')
            if currentLineContent[0] != 'Ontology_Node':
                counter += 1
                currentAncestor = currentLineContent[0]
                currentAncestorID = currentLineContent[1]
                currentTotalPathways = currentLineContent[2]
                currentEnrichedPercent = currentLineContent[4]
                currentPVal = currentLineContent[10]
                summaryDict.update({currentPVal: (currentAncestor, currentAncestorID,
                                                  currentTotalPathways, currentEnrichedPercent)})
        print(
            "------------------------------------------------------------------------------")
        print("You have " + str(counter) + " summarised ontologies.")
        print(
            "Enter the number of top pathway ontologies you would like to build trees with.")
        val = input("Enter your value: (A positive integer)")
        print(
            "------------------------------------------------------------------------------")
        print("Now you can select and visualize trees starting from a pathway as the root:")
        print("Due to the limitation of file size, our library currently stably supports \"all\" trees with default number of enrichments <100")
        print("Our library currently stably supports bigger \"legit\" trees with default number of enrichments < 800")
        print("The top pathways you selected have below info, please choose now:")
        selectedRootsDict = {}
        for num in range(int(val)):
            min_pval = min(summaryDict.keys())
            currentInfo = summaryDict[min_pval]
            print("name: " + currentInfo[0] + ", ID: "+currentInfo[1] +
                  ", total number of pathways: "+currentInfo[2]+", Enriched percentage: "+currentInfo[3]+", pVal: "+min_pval[:-2])
            saveBool = input("Enter Y or N: (Case-sensitive)")
            if saveBool == "Y":
                currentID = currentInfo[1]
                selectedRootsDict.update({currentID: {
                    "name": currentInfo[0], "totalPathways": currentInfo[2], "EnrichedPercent": currentInfo[3], "pVal": min_pval[:-2]}})
            del summaryDict[min_pval]

        return selectedRootsDict

    def formSubtree(self, currentRoot, graphDict):
        '''Recursive helper function'''
        # recursively getting sons of currentRoot (latest uniterated node) and attach that to currentTree
        # has not reached leaf yet: recursive case
        if currentRoot in graphDict.keys():
            currentDescendants = graphDict[currentRoot]
            currentTree = [tuple([self.formSubtree(descendant, graphDict)
                                  for descendant in currentDescendants])]
            currentTree.append(currentRoot)
            print("tree in the work...")
            return tuple(currentTree)
        else:
            return (currentRoot)

    def legitFormSubtree(self, currentRoot, graphDict, currentLegitDesL):
        '''Recursive helper function for the legit case, removing non-standard nodes while
        maintaining its children'''
        if currentRoot in currentLegitDesL:
            if currentRoot in graphDict.keys():
                currentDescendants = graphDict[currentRoot]
                currentTree = [tuple([self.legitFormSubtree(descendant, graphDict, currentLegitDesL)
                                      for descendant in currentDescendants])]
                currentTree.append(currentRoot)
                print("legit tree in the work...")
                return tuple(currentTree)
            else:
                return (currentRoot)
        else:
            if currentRoot in graphDict.keys():
                currentDescendants = graphDict[currentRoot]
                currentTree = [tuple([self.legitFormSubtree(descendant, graphDict, currentLegitDesL)
                                      for descendant in currentDescendants])]
                currentTree.append("DELETE")
                print("legit tree in the work...")
                return tuple(currentTree)
            else:
                return ("DELETE")

    def filterLegitTree(self, rawTreeRoot, currentLegitDesL):
        """if it is a legit tree, filter out non-GSEA pathways"""
        currentChildren = rawTreeRoot.children
        outputRaw = ()
        for child in currentChildren:
            outputRaw += self.filterLegitTree(child, currentLegitDesL)
        if "GO:"+str(rawTreeRoot.name) in currentLegitDesL:
            return (outputRaw, rawTreeRoot.name)
        else:
            return outputRaw

    def getAllNumberSubstrings(self, finalTreeText, NUML):
        '''Get all numbers non-repeated from the finalTreeText'''
        length = len(finalTreeText)

        def checkInt(substring):
            for el in substring:
                if el not in NUML:
                    return False
            return True
        rawAllElements = [finalTreeText[i:i+7]
                          for i in range(length) if (i+7 <= length) and checkInt(finalTreeText[i:i+7])]
        return np.unique(np.array(rawAllElements))

    def readTermToPathways(self):
        '''helper function that gets the list of legit descendants for checking'''
        desFileName = self.outputRoot + '.term_classes_to_pathways.xls'
        descendantDFRaw = pd.read_table(desFileName)
        descendantDF = descendantDFRaw[['GO_ID', 'Descendants_GO_ID']]
        outDictRaw = descendantDF.set_index('GO_ID').T.to_dict('list')
        for item in outDictRaw.items():
            current_key = item[0]
            current_val = item[1]
            updated_val = current_val[0].split(';')
            outDictRaw[current_key] = updated_val
        return outDictRaw

    def segmentColoring(self, tree, segmentColorDict):
        """for all tree, enable to option of segment coloring"""
        subrootColoringL = segmentColorDict.keys()
        for n in tree.traverse():
            if str(n.name) in subrootColoringL:
                currentColor = segmentColorDict[str(n.name)]
                nst1 = NodeStyle()
                nst1["bgcolor"] = currentColor
                n.set_style(nst1)
        return tree

    def getTreeFromNodeHelper(self, rootOfSubtree, selectedRootsDict, treeNum, select):
        # get subtree annotation
        currentAnnotation = selectedRootsDict[rootOfSubtree]
        rootName = currentAnnotation["name"]
        totalNumPathways = currentAnnotation["totalPathways"]
        enrichedPercent = currentAnnotation["EnrichedPercent"]
        pVal = currentAnnotation["pVal"]
        # get current enriched nodes
        currentSubtreeInfoName = self.outputRoot + \
            self.canonicalEnrichment + '.infoForSubtree.pkl'
        with open(currentSubtreeInfoName, "rb") as input_file:
            allubtreeInfoDict = pickle.load(input_file)
        currentSubtreeInfoDict = allubtreeInfoDict[rootOfSubtree]
        # get all legit descendants:
        currentLegitDesL = self.readTermToPathways()[
            rootOfSubtree]
        # load the graph Dict
        graphPickleName = self.outputRoot + '.phylogenyGraphDict.pkl'
        if select == "all":
            with open(graphPickleName, "rb") as input_file:
                graphDict = pickle.load(input_file)
            finalTree = self.formSubtree(rootOfSubtree, graphDict)
        elif select == "legit":
            with open(graphPickleName, "rb") as input_file:
                graphDict = pickle.load(input_file)
            finalTree = self.formSubtree(rootOfSubtree, graphDict)

        # get tree
        finalTreeText = str(finalTree) + ";"
        finalTreeText = finalTreeText.replace(",)", ")")
        finalTreeText = finalTreeText.replace("), ", ")")
        finalTreeText = finalTreeText.replace("'", "")
        finalTreeText = finalTreeText.replace(")(", "),(")
        finalTreeText = finalTreeText.replace("GO:", "")

        tree = Tree(finalTreeText, format=1)
        return finalTreeText, tree, currentLegitDesL, currentSubtreeInfoDict, rootName, totalNumPathways, enrichedPercent, pVal

    def getTreeFromNode(self, rootOfSubtree, selectedRootsDict, treeNum, select, enrichment, enrichmentFileL, enrichmentNameL, enrichVis, segmentColorDict={}, outputFormat='png', backgroundAdditionalEnrichmentsL=[]):
        '''form tree given selected roots dict information and output root
        two cases: either the whole tree or legit tree depending on the input select'''
        # error cases
        if select not in ['all', 'legit']:
            raise Exception("Only \'all\' and \'legit\' trees are allowed.")
        if not isinstance(enrichment, int):
            raise Exception(
                "The argument \'enrichment\' has to be an integer between 1 and 3.")
        if enrichment > 3:
            raise Exception(
                "Currently only supporting 1-3 enrichments on one single tree graph.")
        if enrichVis not in ['pie', 'sphere']:
            raise Exception(
                "Currently only two types of enrichment visualizations: \'pie\', \'sphere\'.")
        if outputFormat not in SUPPORTEDFORMATS:
            raise Exception(
                "Output format not supported. Currently only supporting pdf, svg, and png.")
        # get basic tree
        finalTreeText, tree, currentLegitDesL, currentSubtreeInfoDict, rootName, totalNumPathways, enrichedPercent, pVal = self.getTreeFromNodeHelper(
            rootOfSubtree, selectedRootsDict, treeNum, select)

        # nodestyle
        nstyle = NodeStyle()
        nstyle["shape"] = "sphere"
        nstyle["size"] = 0
        nodeCounter = 0

        # clean and annotate tree
        for n in tree.traverse():
            n.set_style(nstyle)
            nodeCounter += 1

        if select == "legit":
            tree = self.filterLegitTree(tree, currentLegitDesL)
            finalTreeText = str(tree)+";"
            finalTreeText = finalTreeText.replace("(),", "")
            finalTreeText = finalTreeText.replace("\'", "")

            tree = Tree(finalTreeText, format=1)

        # Now deal with enrichment
        # first deal with enrichments that will be plotted in the pie charts
        extendedAdditionalEnrichments = []
        additionalEnrichments = []
        if enrichment > 1:
            en = EnrichmentPreprocess(self.outputRoot)
            additionalEnrichments, extendedAdditionalEnrichments = en.multipleEnrichmentFileProcess(
                enrichmentFileL)

        # then deal with background enrichments
        bGAdditionalEnrichments, extendedBGAdditionalEnrichments = en.multipleEnrichmentFileProcess(
            backgroundAdditionalEnrichmentsL)

        # extendedAdditionalEnrichments = [item for sublist in additionalEnrichments for item in sublist]
        origEnrichments = []
        for n in tree.traverse():
            # if it's enriched
            if ("GO:"+str(n.name) in currentSubtreeInfoDict.descendants_set) or (str(n.name) in extendedAdditionalEnrichments):
                origEnrichments.append(n.name)
                n.add_features(weight=math.log(int(nodeCounter), 3)*1.5)
            if str(n.name) == "DELETE":
                n.delete(prevent_nondicotomic=False,
                         preserve_branch_length=False)
            if str(n.name) == "" and len(n.children) == 1:
                n.delete(prevent_nondicotomic=False,
                         preserve_branch_length=False)

        # segment coloring
        if segmentColorDict != {} and select == "all":
            tree = self.segmentColoring(tree, segmentColorDict)

        ts = TreeStyle()
        ts.show_leaf_name = False
        # visualization

        def makePieChartFace(faces, node, colors, percents):
            # Creates a sphere face whose size is proportional to node's
            # feature "weight" - default enrichment
            # C = CircleFace(radius=node.weight, color=newColor,
            #                style="sphere")
            C = PieChartFace(
                width=node.weight*2.3, height=node.weight*2.3, colors=colors, percents=percents)
            # Let's make the sphere transparent
            # And place as a float face over the tree
            faces.add_face_to_node(C, node, 0, position="float")
        # tree node display styles

        def makeCircularFace(faces, node, color):
            # Creates a sphere face whose size is proportional to node's
            # feature "weight" - default enrichment
            C = CircleFace(radius=node.weight, color=color, style="sphere")
            # Let's make the sphere transparent
            C.opacity = 0.8
            # And place as a float face over the tree
            faces.add_face_to_node(C, node, 0, position="branch-top")

        def internalNode_display_layout(node):
            F = TextFace(node.name, tight_text=True)
            add_face_to_node(F, node, column=0, position="branch-right")
            if "weight" in node.features:
                if len(additionalEnrichments) == 0:
                    if str(node.name) in origEnrichments:
                        # makeCircularFace(faces, node, "Red")
                        if enrichVis == "pie":
                            makePieChartFace(
                                faces, node, colors=self.ENRICHMENTCOLORS["1"], percents=ENRICHMENTPERCENTS["1"])
                        elif enrichVis == "sphere":
                            makeCircularFace(faces, node, "Red")
                if len(additionalEnrichments) == 1:
                    if str(node.name) in additionalEnrichments[0] and str(node.name) in origEnrichments:
                        if enrichVis == "pie":
                            makePieChartFace(
                                faces, node, colors=self.ENRICHMENTCOLORS["1-2"], percents=ENRICHMENTPERCENTS["1-2"])
                        elif enrichVis == "sphere":
                            makeCircularFace(faces, node, "Red")
                            makeCircularFace(faces, node, "Green")
                    elif str(node.name) in origEnrichments:
                        if enrichVis == "pie":
                            makePieChartFace(
                                faces, node, colors=self.ENRICHMENTCOLORS["1"], percents=ENRICHMENTPERCENTS["1"])
                        elif enrichVis == "sphere":
                            makeCircularFace(faces, node, "Red")
                    elif str(node.name) in additionalEnrichments[0]:
                        # makeCircularFace(faces, node, ENRICHMENTCOLORS["2"])
                        if enrichVis == "pie":
                            makePieChartFace(
                                faces, node, colors=self.ENRICHMENTCOLORS["2"], percents=ENRICHMENTPERCENTS["2"])
                        elif enrichVis == "sphere":
                            makeCircularFace(faces, node, "Green")

                if len(additionalEnrichments) == 2:
                    if str(node.name) in origEnrichments:
                        if (str(node.name) in additionalEnrichments[0]) and (str(node.name) in additionalEnrichments[1]):
                            if enrichVis == "pie":
                                makePieChartFace(
                                    faces, node, colors=self.ENRICHMENTCOLORS["1-2-3"], percents=ENRICHMENTPERCENTS["1-2-3"])
                            elif enrichVis == "sphere":
                                makeCircularFace(faces, node, "Red")
                                makeCircularFace(faces, node, "Green")
                                makeCircularFace(faces, node, "Blue")
                        elif str(node.name) in additionalEnrichments[0]:
                            if enrichVis == "pie":
                                makePieChartFace(
                                    faces, node, colors=self.ENRICHMENTCOLORS["1-2"], percents=ENRICHMENTPERCENTS["1-2"])
                            elif enrichVis == "sphere":
                                makeCircularFace(faces, node, "Red")
                                makeCircularFace(faces, node, "Green")
                        elif str(node.name) in additionalEnrichments[1]:
                            if enrichVis == "pie":
                                makePieChartFace(
                                    faces, node, colors=self.ENRICHMENTCOLORS["1-3"], percents=ENRICHMENTPERCENTS["1-3"])
                            elif enrichVis == "sphere":
                                makeCircularFace(faces, node, "Red")
                                makeCircularFace(faces, node, "Blue")
                    elif str(node.name) in additionalEnrichments[0]:
                        if str(node.name) in additionalEnrichments[1]:
                            if enrichVis == "pie":
                                makePieChartFace(
                                    faces, node, colors=self.ENRICHMENTCOLORS["2-3"], percents=ENRICHMENTPERCENTS["2-3"])
                            elif enrichVis == "sphere":
                                makeCircularFace(faces, node, "Blue")
                                makeCircularFace(faces, node, "Green")
                        else:
                            if enrichVis == "pie":
                                makePieChartFace(
                                    faces, node, colors=self.ENRICHMENTCOLORS["2"], percents=ENRICHMENTPERCENTS["2"])
                            elif enrichVis == "sphere":
                                makeCircularFace(faces, node, "Green")
                    else:
                        if enrichVis == "pie":
                            makePieChartFace(
                                faces, node, colors=self.ENRICHMENTCOLORS["3"], percents=ENRICHMENTPERCENTS["3"])
                        elif enrichVis == "sphere":
                            makeCircularFace(faces, node, "Blue")
            if "GO:"+str(node.name) in currentLegitDesL:
                if len(additionalEnrichments) == 0:
                    if str(node.name) in origEnrichments:
                        name_face = TextFace("▓▓▓▓▓", fgcolor="blue",
                                             fsize=math.sqrt(int(nodeCounter))*0.001)
                        node.add_face(name_face, column=0,
                                      position='branch-right')
                    else:
                        name_face = TextFace("▓▓▓▓▓", fgcolor="Gray",
                                             fsize=math.sqrt(int(nodeCounter))*0.001)
                        node.add_face(name_face, column=0,
                                      position='branch-right')
                else:
                    if str(node.name) in additionalEnrichments[0] or str(node.name) in additionalEnrichments[1] or str(node.name) in origEnrichments or str(node.name) in extendedBGAdditionalEnrichments:
                        name_face = TextFace("▓▓▓▓▓", fgcolor="Purple",
                                             fsize=math.sqrt(int(nodeCounter))*0.001)
                        node.add_face(name_face, column=0,
                                      position='branch-right')
                    else:
                        name_face = TextFace("▓▓▓▓▓", fgcolor="Gray",
                                             fsize=math.sqrt(int(nodeCounter))*0.001)
                        node.add_face(name_face, column=0,
                                      position='branch-right')
        ts.layout_fn = internalNode_display_layout
        # circular tree
        ts.mode = "c"
        ts.arc_start = -180  # 0 degrees = 3 o'clock

        # annotate legend
        titleText = "Pathway Subtree with Root " + \
            rootName + " ("+rootOfSubtree+")"
        legendText = "Total number of pathways: " + \
            str(totalNumPathways) + "\n" + "Enriched percentage: " + \
            enrichedPercent + "\n" + "p-value: " + pVal

        ts.title.add_face(
            TextFace(titleText, fsize=int(totalNumPathways)*1.5), column=0)
        ts.legend.add_face(
            TextFace(legendText, fsize=int(totalNumPathways)), column=0)
        ts.legend.add_face(
            TextFace("●: "+enrichmentNameL[0], fsize=int(totalNumPathways), fgcolor=self.ENRICHMENTCOLORS["1"][0]), column=0)
        if enrichment >= 2:
            ts.legend.add_face(TextFace("●: "+enrichmentNameL[1], fsize=int(
                totalNumPathways), fgcolor=self.ENRICHMENTCOLORS["2"][0]), column=0)
        if enrichment == 3:
            ts.legend.add_face(TextFace("●: "+enrichmentNameL[2], fsize=int(
                totalNumPathways), fgcolor=self.ENRICHMENTCOLORS["3"][0]), column=0)
        ts.legend_position = 4

        # output
        outputTreeGraphText = self.outputRoot + self.canonicalEnrichment + \
            ".treeGraph." + str(treeNum)+"."+outputFormat
        tree.render(outputTreeGraphText, tree_style=ts)
        return outputTreeGraphText

    def graphTreeWrapper(self, select='all', enrichment=1, firstEnrichmentName='enrichment 1', enrichVis='pie', outputFormat='png', numOfBackgroundEnrichments=0):
        '''wrapper function for tree visualization
        select: either 'all' or 'legit'
        enrichment: either 'single' or numbers (2 or 3)
        enrichVis: either 'pie' or 'sphere'''
        treeNum = 0
        # error cases
        if select not in ['all', 'legit']:
            raise Exception("Only \'all\' and \'legit\' trees are allowed.")
        if not isinstance(enrichment, int):
            raise Exception(
                "The argument \'enrichment\' has to be an integer between 1 and 3.")
        if enrichment > 3:
            raise Exception(
                "Currently only supporting 1-3 enrichments on one single tree graph.")
        if enrichVis not in ['pie', 'sphere']:
            raise Exception(
                "Currently only two types of enrichment visualizations: \'pie\', \'sphere\'.")
        if outputFormat not in SUPPORTEDFORMATS:
            raise Exception(
                "Output format not supported. Currently only supporting pdf, svg, and png.")

        def getSingleEnrichmentFile(index, enrichmentFileL, enrichmentNameL, bg=False):
            """Get single enrichment file, recurse until success"""
            print(
                "------------------------------------------------------------------------------")
            print("Input your additional enrichment file", i+1)
            fileName = input("Enter your filename, include format:")
            if bg == False:
                curEnrichmentName = input(
                    "Enter name for current enrichment:")
                if curEnrichmentName == '':
                    curEnrichmentName = "enrichment " + str(index+2)
            print(
                "Your current file name (address) is as following, please check:")
            print(fileName)
            if bg == False:
                print(
                    "This enrichment is named as following, please check:")
                print(curEnrichmentName)
            enterFileName = input(
                "Enter Y (Case-sensitive) if the above information is correct:")
            if enterFileName == "Y":
                enrichmentFileL.append(fileName)
                if bg == False:
                    enrichmentNameL.append(curEnrichmentName)
                return enrichmentFileL, enrichmentNameL
            else:
                print("enterFileName", enterFileName)
                print("Please input your enrichment file address again")
                return getSingleEnrichmentFile(index, enrichmentFileL, enrichmentNameL)

        selectedRootsDict = self.selectSubTrees()

        # get enrichment info and background enrichment info
        # for enrichment
        enrichmentFileL = []
        enrichmentNameL = [firstEnrichmentName]
        if enrichment != 1:
            for i in range(enrichment-1):
                enrichmentFileL, enrichmentNameL = getSingleEnrichmentFile(
                    i, enrichmentFileL, enrichmentNameL)
                print(enrichmentFileL)
            if len(enrichmentFileL) != enrichment-1:
                raise Exception(
                    "Number of inputted enrichment files does not match the number of enrichment inputted as the argument:", enrichment)
        # for background enrichment
        print(
            "------------------------------------------------------------------------------")
        print("Now start to input background enrichments")
        bgenrichmentFileL = []
        bgenrichmentNameL = []
        if numOfBackgroundEnrichments != 0:
            for i in range(numOfBackgroundEnrichments):
                bgenrichmentFileL, bgenrichmentNameL = getSingleEnrichmentFile(
                    i, bgenrichmentFileL, bgenrichmentNameL, bg=True)
            if len(bgenrichmentFileL) != numOfBackgroundEnrichments:
                raise Exception(
                    "Number of inputted enrichment files does not match the number of enrichment inputted as the argument:", enrichment)

        # for general visualization
        for currentSubtreeRoot in selectedRootsDict.keys():
            print(
                "------------------------------------------------------------------------------")
            print("Preparing to draw subtree with root "+currentSubtreeRoot+".")

            # for segment coloring
            segmentColorDict = {}
            if select == "all":
                segmentContinue = True
                while(segmentContinue):
                    print(
                        "------------------------------------------------------------------------------")
                    print("Currently you are coloring",
                          len(segmentColorDict), "subroots")
                    print("They are", list(segmentColorDict.keys()))
                    print("Would you like to add segment colors?")
                    segmentTempBool = input(
                        "Enter Y (Case-sensitive) if you would like to add more segment color:")
                    if segmentTempBool == "Y":
                        print(
                            "What node (subroot) would you like your segment coloring to start at?")
                        inputSubroot = input(
                            "Enter a node number: (e.g. enter 0032350 for GO:0032350), uncorrectly formatted node number will not be displayed ")
                        print("What color would you like to add?")
                        print(
                            "Check this link for color reference: http://etetoolkit.org/docs/latest/reference/reference_treeview.html?highlight=color#color-names")
                        inputColor = input("Enter a color:")
                        segmentColorDict.update({inputSubroot: inputColor})
                    else:
                        print("Segment Coloring finished.")
                        time.sleep(3)
                        segmentContinue = False
            print(
                "------------------------------------------------------------------------------")
            print("Subtree with root "+currentSubtreeRoot+" generating.")
            treeNum += 1
            outputTreeGraphText = self.getTreeFromNode(
                currentSubtreeRoot, selectedRootsDict, treeNum, select, enrichment, enrichmentFileL, enrichmentNameL, enrichVis, segmentColorDict, outputFormat, bgenrichmentFileL)
            print("Subtree with root "+currentSubtreeRoot +
                  " printing finished, check out file " + outputTreeGraphText)
        print("Everything is done!")
        return
