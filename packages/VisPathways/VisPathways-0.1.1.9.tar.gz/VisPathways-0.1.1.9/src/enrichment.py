import pandas as pd
import summarizePathwayHierarchy as summarizer
from mergeDatabases import MergeDatabase
import os


class EnrichmentPreprocess:
    def __init__(self, outputRoot):
        self.outputRoot = outputRoot
        self.enrichmentFileNameL = []
        self.enrichmentsL = [[]]

    def splitFilesAndRunSummary(self, source, ontologyFile, xmlFile, runAncAndDes=False, deleteTempCSV=True):
        '''Method for splitting one file containing multiple columns to form multiple pandas dfs to be run the summary on each one'''
        if runAncAndDes == False:
            # Assumes that the two files exist
            ancestorFileName = self.outputRoot + ".pathway_to_go_id_ancestors.xls"
            descendantFileName = self.outputRoot + ".term_classes_to_pathways.xls"
        else:
            md = MergeDatabase(ontologyFile, xmlFile,
                               'enrichmentPlaceholder', self.outputRoot)
            md.generateAncAndDecOnly()
        # start splitting
        # df = self.versatileSingleFileProcess(source)
        if source[-3:] == 'txt':
            df = pd.read_csv(source, sep="\t")
        elif source[-3:] == 'csv':
            df = pd.read_csv(source)
        else:
            raise Exception(
                "Multiple enrichment formatted unsupported: we currently only support txt or csv format.")
        colNames = list(df.columns)
        allPathwaysL = list(df[colNames[0]])
        colNames = colNames[1:]
        dfL = [list(df[colName]) for colName in colNames]
        for ind, dfSubL in enumerate(dfL):
            print("Currently printing summary stats for", colNames[ind])
            # for each column, extract useful pathways (value != 0)
            dfSubLPathways = [allPathwaysL[subInd]
                              for subInd, num in enumerate(dfSubL) if num != 0]
            df = pd.DataFrame(dfSubLPathways, columns=[colNames[ind]])
            df.to_csv(self.outputRoot+colNames[ind]+'temp.csv', index=False)
            md = MergeDatabase(ontologyFile, xmlFile,
                               self.outputRoot+colNames[ind]+'temp.csv', self.outputRoot)
            md.generateStatsOnly(extraOutputName=colNames[ind])
            if deleteTempCSV:
                os.remove(self.outputRoot+colNames[ind]+'temp.csv')
        return

    def versatileSingleFileProcess(self, source):
        '''Handles csv, xlsx, xls, txt file types for single enrichment file input'''
        fileName = source.split('/')[-1]
        fileFormat = fileName.split('.')[-1]
        df = pd.DataFrame()
        if fileFormat == 'xlsx':
            df = pd.read_excel(source)
        elif fileFormat == 'xls':
            df = pd.read_table(source)
        elif fileFormat == 'csv':
            df = pd.read_csv(source)
        elif fileFormat == 'txt':
            df = pd.read_csv(source, sep=" ")
        self.enrichmentFileNameL.append(source)
        return df

    def runSummary(self, source):
        '''run summarization for one enrichment file'''
        print("What's the minimum pathway count to consider an ancestor?")
        minNumAncestor = int(input(
            "Enter your value (please enter a positive integer): "))
        while minNumAncestor <= 0:
            print(
                "Please enter a positive integer for the minimum pathway count to consider an ancestor!")
        print("Your minimum pathway count to consider an ancestor is:", minNumAncestor)
        ancestorFileName = self.outputRoot + ".pathway_to_go_id_ancestors.xls"
        descendantFileName = self.outputRoot + ".term_classes_to_pathways.xls"
        pathwayListFileName = source
        summarizeArgv = summarizer.CStruct(pathToAncestor=ancestorFileName, ancestorToDescendant=descendantFileName,
                                           pathwayList=pathwayListFileName, minPathwayCount=minNumAncestor, outputRoot=self.outputRoot)
        bp = summarizer.SummarizePathwayHierarchy(summarizeArgv)
        bp.work()
        print("FINISHED! CHECK OUT YOUR PRODUCT FILES:")
        print(ancestorFileName + ' -> Pathway to Ancestors File.')
        print(descendantFileName + ' -> Pathway to Descendants File.')
        print(self.outputRoot +
              '.pathway_count.xls -> Hierarchy Summary File.')

    def oneEnrichmentProcess(self, source):
        '''Produce list of enriched pathways from a file, supporting csv, xlsx, xls, txt file types'''
        df = self.versatileSingleFileProcess(source)
        currentEnrichedPathways = df.iloc[:, [0]].T.values.tolist()[0]
        return currentEnrichedPathways

    def multipleEnrichmentFileProcess(self, sourceL):
        '''Handles a list of enrichment files, supporting csv, xlsx, xls, txt file types
        for each file in the list'''
        GONameToGOIDDict = {}
        pathwayNameL = []
        indivPathwayNameL = []
        allEnrichmentsL = []
        pathway_to_go_id_ancestors_file_name = "%s.pathway_to_go_id_ancestors.xls" % self.outputRoot
        # getting all enrichment names
        print("Getting enriched pathways' names")
        for source in sourceL:
            currentEnrichedPathways = self.oneEnrichmentProcess(source)
            indivPathwayNameL.append(currentEnrichedPathways)
            pathwayNameL.extend(
                pathway for pathway in currentEnrichedPathways if pathway not in pathwayNameL)
        # get all enrichments' names to their goids dict
        pathway_to_go_id_ancestors_file = open(
            pathway_to_go_id_ancestors_file_name, "r")
        print("Getting enrichment GOIDs")
        while(True):
            line = pathway_to_go_id_ancestors_file.readline()
            lineContent = line.split('\t')
            if lineContent[0] == "":
                break
            if lineContent[0] != 'Pathway' and lineContent[0] in pathwayNameL:
                GONameToGOIDDict.update(
                    {lineContent[0]: lineContent[1][3:]})

        # get each individual enrichment's goids
        for enrichment in range(1, len(sourceL)+1):
            print("finding the GO IDs for enrichment", sourceL[enrichment-1])
            currentEnrichedPathways = indivPathwayNameL[enrichment-1]
            currentEnrichedPathwaysGO = [
                GONameToGOIDDict[pathway] for pathway in currentEnrichedPathways if pathway in GONameToGOIDDict]
            allEnrichmentsL.append(currentEnrichedPathwaysGO)

        extendedAdditionalEnrichments = [
            item for sublist in allEnrichmentsL for item in sublist]
        return allEnrichmentsL, extendedAdditionalEnrichments

    def multipleEnrichmentProcess(self, source):
        '''Handles single file of csv, xlsx, xls, txt file types that contains
        multiple information, with an example 1mthNMR_MM_Human_UVresponse_GSEA.xlsx'''
        # initialize
        df = self.versatileSingleFileProcess(source)
        GONameToGOIDDict = {}
        allEnrichmentsL = []
        extendedAdditionalEnrichments = []
        pathway_to_go_id_ancestors_file_name = "%s.pathway_to_go_id_ancestors.xls" % self.outputRoot
        # a list of all pathway names
        pathwayNameL = df.iloc[:, [0]].T.values.tolist()[0]
        # number of enrichments (variables) listed
        enrichmentVars = list(df)[1:]
        numOfEnrichments = len(enrichmentVars)
        # get all enrichments' names to their goids dict
        pathway_to_go_id_ancestors_file = open(
            pathway_to_go_id_ancestors_file_name, "r")
        print("Getting enrichment GOIDs")
        while(True):
            line = pathway_to_go_id_ancestors_file.readline()
            lineContent = line.split('\t')
            if lineContent[0] == "":
                break
            if lineContent[0] != 'Pathway' and lineContent[0] in pathwayNameL:
                GONameToGOIDDict.update(
                    {lineContent[0]: lineContent[1][3:]})
        # get each individual enrichment's goids
        for enrichment in range(1, numOfEnrichments+1):
            print("finding the GO IDs for enrichment",
                  enrichmentVars[enrichment-1])
            currentEnrichedPathways = df.iloc[:, [0, enrichment]].dropna().iloc[:, [
                0]].T.values.tolist()[0]
            currentEnrichedPathwaysGO = [
                GONameToGOIDDict[pathway] for pathway in currentEnrichedPathways if pathway in GONameToGOIDDict]
            allEnrichmentsL.append(currentEnrichedPathwaysGO)
            extendedAdditionalEnrichments.append(
                [pathway for pathway in currentEnrichedPathwaysGO if pathway not in extendedAdditionalEnrichments])
        return allEnrichmentsL, extendedAdditionalEnrichments
