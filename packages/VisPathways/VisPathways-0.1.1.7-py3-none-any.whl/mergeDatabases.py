#!/usr/bin/env python
__author__ = "Tom Fu"

__version__ = "1.0"

import os
import sys
import argparse
import re
import numpy as np
import scipy.stats
import matplotlib as mpl
import pandas as pd
import glob
import datetime
import math
import time
from argparse import RawTextHelpFormatter
from argparse import Namespace

from simpleTime import SimpleTime


# import three database loading modules
import InferGoKeggToGOBP as keggLoader
import InferGoReactomeToGOBP as reactomeLoader
import InferGoSlimToGOBP as goLoader

import summarizePathwayHierarchy as summarizer


class CStruct(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class MergeDatabase:
    DEBUG_PROGRESS = True
    DEBUG_DATABASE = True

    def __init__(self, *input):
        if len(input) == 1:
            self.myArgs = input
            try:
                inferArgv = sys.argv[1: 5]
                inferArgv.extend(sys.argv[7:9])
                self.ontologyFile = inferArgv[1]
                self.xmlFile = inferArgv[3]
                self.pathwayListFileName = sys.argv[6]
                self.outputRoot = sys.argv[8]
            except:
                raise Exception("Incorrect input format.")
        elif len(input) == 4:
            try:
                self.myArgs = input
                self.ontologyFile, self.xmlFile, self.pathwayListFileName, self.outputRoot = input
            except:
                raise Exception("Incorrect input format or ordering.")
        else:
            raise Exception(
                "Number of inputs has to be either 1 (from command line) or 4 (ontologyFile, xmlFile, pathwayListFileName, outputRoot; in order).")

    @ staticmethod
    def processArguments():
        parser = argparse.ArgumentParser(description="""\
Utility %s version %s.

* Script1: MergeDatabase
    * Input 1: database specific source file
    * Input 2: xml file from gsea
    * Input 3: pathway file name
    * Input 4: output prefix

""" % (os.path.basename(sys.argv[0]), __version__), formatter_class=RawTextHelpFormatter)

        parser.add_argument(
            '-g', '--goDatabase',   help='name of the database specific source file. (.obo file for Geneontology; .txt file for Kegg and Reactome)',  required=True)
        parser.add_argument(
            '-x', '--goXml', help='XML version of the MSigDB Gene Ontology BP', required=True)
        parser.add_argument('-p', '--pathwayFileName',
                            help='name of the pathway file, recommend csv format', required=True)
        parser.add_argument('-o', '--outputRoot',
                            help='root/prefix of the output files', required=True)
        try:
            args = parser.parse_args()
        except:
            args = None
        return args

    def generateAncAndDecOnly(self):
        # get database
        databaseBool = False
        while databaseBool == False:
            print(
                "FancyTaxonomy Pathway Hierarchy Analyzer")
            print("Authors: Tom Fu, Cristian Coarfa")
            print(
                "------------------------------------------------------------------------------")
            print(
                "We currently only support csv or xls file formats for the pathway list file!")
            print(
                "------------------------------------------------------------------------------")
            print("What's the database you are using?")
            print("Enter G for Geneontology; K for Kegg; or R for Reactome.")
            val = input("Enter your value: ")
            print("The database you are using is:")
            if val in ["G", "K", "R"]:
                if val == "G":
                    print("Geneontology.")
                elif val == "K":
                    print("Kegg.")
                elif val == "R":
                    print("Reactome.")
                print("Is that correct?")
                databaseInOrNot = input("Enter Y or N: (Case-sensitive)")
                if databaseInOrNot == "Y":
                    print("What's the minimum pathway count to consider an ancestor?")
                    minNumAncestor = int(input(
                        "Enter your value (please enter a positive integer): "))
                    if minNumAncestor > 0:
                        databaseBool = True
                    else:
                        print(
                            "Please enter a positive integer for the minimum pathway count to consider an ancestor!")
            else:
                print("Invalid/unsupported database.")

        ancestorFileName = self.outputRoot + ".pathway_to_go_id_ancestors.xls"
        descendantFileName = self.outputRoot + ".term_classes_to_pathways.xls"
        if val == "G":
            databaseArgs = CStruct(
                goSlims=self.ontologyFile, goXml=self.xmlFile, outputRoot=self.outputRoot)
            bp = goLoader.InferGoSlimToGO(databaseArgs)
        elif val == "K":
            databaseArgs = CStruct(
                goKegg=self.ontologyFile, goXml=self.xmlFile, outputRoot=self.outputRoot)
            bp = keggLoader.InferGoKeggToGO(databaseArgs)
        elif val == "R":
            databaseArgs = CStruct(
                goReactomes=self.ontologyFile, goXml=self.xmlFile, outputRoot=self.outputRoot)
            bp = reactomeLoader.InferGoReactomeToGO(databaseArgs)
        bp.work()

        print("FINISHED! CHECK OUT YOUR PRODUCT FILES:")
        print(ancestorFileName + ' -> Pathway to Ancestors File.')
        print(descendantFileName + ' -> Pathway to Descendants File.')

    def generateStatsOnly(self, extraOutputName=''):
        # get database
        databaseBool = False
        while databaseBool == False:
            print(
                "FancyTaxonomy Pathway Hierarchy Analyzer")
            print("Authors: Tom Fu, Cristian Coarfa")
            print(
                "------------------------------------------------------------------------------")
            print(
                "We currently only support csv or xls file formats for the pathway list file!")
            print(
                "------------------------------------------------------------------------------")
            print("What's the database you are using?")
            print("Enter G for Geneontology; K for Kegg; or R for Reactome.")
            val = input("Enter your value: ")
            print("The database you are using is:")
            if val in ["G", "K", "R"]:
                if val == "G":
                    print("Geneontology.")
                elif val == "K":
                    print("Kegg.")
                elif val == "R":
                    print("Reactome.")
                print("Is that correct?")
                databaseInOrNot = input("Enter Y or N: (Case-sensitive)")
                if databaseInOrNot == "Y":
                    print("What's the minimum pathway count to consider an ancestor?")
                    minNumAncestor = int(input(
                        "Enter your value (please enter a positive integer): "))
                    if minNumAncestor > 0:
                        databaseBool = True
                    else:
                        print(
                            "Please enter a positive integer for the minimum pathway count to consider an ancestor!")
            else:
                print("Invalid/unsupported database.")

        ancestorFileName = self.outputRoot + ".pathway_to_go_id_ancestors.xls"
        descendantFileName = self.outputRoot + ".term_classes_to_pathways.xls"

        summarizeArgv = CStruct(pathToAncestor=ancestorFileName, ancestorToDescendant=descendantFileName,
                                pathwayList=self.pathwayListFileName, minPathwayCount=minNumAncestor, outputRoot=self.outputRoot+extraOutputName)
        bp = summarizer.SummarizePathwayHierarchy(summarizeArgv)
        bp.work()
        print("FINISHED! CHECK OUT YOUR PRODUCT FILES:")
        print(self.outputRoot+extraOutputName +
              '.pathway_count.xls -> Hierarchy Summary File.')

    def generateSummaries(self):
        # self.generateAncAndDecOnly()
        # self.generateStatsOnly()
        # get database
        databaseBool = False
        while databaseBool == False:
            print(
                "FancyTaxonomy Pathway Hierarchy Analyzer")
            print("Authors: Tom Fu, Cristian Coarfa")
            print(
                "------------------------------------------------------------------------------")
            print(
                "We currently only support csv or xls file formats for the pathway list file!")
            print(
                "------------------------------------------------------------------------------")
            print("What's the database you are using?")
            print("Enter G for Geneontology; K for Kegg; or R for Reactome.")
            val = input("Enter your value: ")
            print("The database you are using is:")
            if val in ["G", "K", "R"]:
                if val == "G":
                    print("Geneontology.")
                elif val == "K":
                    print("Kegg.")
                elif val == "R":
                    print("Reactome.")
                print("Is that correct?")
                databaseInOrNot = input("Enter Y or N: (Case-sensitive)")
                if databaseInOrNot == "Y":
                    print("What's the minimum pathway count to consider an ancestor?")
                    minNumAncestor = int(input(
                        "Enter your value (please enter a positive integer): "))
                    if minNumAncestor > 0:
                        databaseBool = True
                    else:
                        print(
                            "Please enter a positive integer for the minimum pathway count to consider an ancestor!")
            else:
                print("Invalid/unsupported database.")

        ancestorFileName = self.outputRoot + ".pathway_to_go_id_ancestors.xls"
        descendantFileName = self.outputRoot + ".term_classes_to_pathways.xls"

        summarizeArgv = CStruct(pathToAncestor=ancestorFileName, ancestorToDescendant=descendantFileName,
                                pathwayList=self.pathwayListFileName, minPathwayCount=minNumAncestor, outputRoot=self.outputRoot)
        if val == "G":
            databaseArgs = CStruct(
                goSlims=self.ontologyFile, goXml=self.xmlFile, outputRoot=self.outputRoot)
            bp = goLoader.InferGoSlimToGO(databaseArgs)
        elif val == "K":
            databaseArgs = CStruct(
                goKegg=self.ontologyFile, goXml=self.xmlFile, outputRoot=self.outputRoot)
            bp = keggLoader.InferGoKeggToGO(databaseArgs)
        elif val == "R":
            databaseArgs = CStruct(
                goReactomes=self.ontologyFile, goXml=self.xmlFile, outputRoot=self.outputRoot)
            bp = reactomeLoader.InferGoReactomeToGO(databaseArgs)
        bp.work()
        bp = summarizer.SummarizePathwayHierarchy(summarizeArgv)
        bp.work()
        print("FINISHED! CHECK OUT YOUR PRODUCT FILES:")
        print(ancestorFileName + ' -> Pathway to Ancestors File.')
        print(descendantFileName + ' -> Pathway to Descendants File.')
        print(self.outputRoot+'.pathway_count.xls -> Hierarchy Summary File.')


if __name__ == '__main__':

    ###COMMAND LINE USAGE: python3 InferGoKeggToGOBP.v-1.py -g go-basic.obo -x msigdb_v7.2.xml -o something.xls###
    ###PIP USAGE: from mergeDatabases import *; md = MergeDatabase(obo, goxml, pathwayF, 'test') after definition; md.inputDatabaseAndPathwayFileFormat()###
    try:
        sys.stderr.write("Command line %s\n" % " ".join(sys.argv))
        myArgs = MergeDatabase.processArguments()
        md = MergeDatabase(myArgs)
        if (myArgs is None):
            pass
        else:
            md.generateSummaries()
    except:
        sys.stderr.write("An unknown error occurred.\n")
        raise
