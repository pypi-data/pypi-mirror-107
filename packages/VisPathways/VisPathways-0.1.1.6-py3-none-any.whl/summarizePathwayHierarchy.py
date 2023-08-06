#!/usr/bin/env python
__author__ = "Cristian Coarfa"

__version__ = "3.0"

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
from argparse import RawTextHelpFormatter
import scipy.stats
import pickle

# from CCLabUtils.simpleTime import SimpleTime
from simpleTime import SimpleTime


class CStruct(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class SummarizePathwayHierarchy:
    DEBUG_PROGRESS = True
    DEBUG_LOAD_PATHWAY_LIST = True
    DEBUG_LOAD_DISTILLED_ONTOLOGY = True
    DEBUG_OUTPUT = True

    def __init__(self, *input):
        if len(input) == 1:
            self.myArgs = input[0]
        elif len(input) == 5:
            ancestorFileName, descendantFileName, pathwayListFileName, minNumAncestor, outputRoot = input
            self.myArgs = CStruct(pathToAncestor=ancestorFileName, ancestorToDescendant=descendantFileName,
                                  pathwayList=pathwayListFileName, minPathwayCount=minNumAncestor, outputRoot=outputRoot)
        else:
            raise Exception(
                "Number of inputs has to be either 1 (from command line) or 5 (ancestorFileName, descendantFileName, pathwayListFileName, minNumAncestor, outputRoot; in order).")

    @staticmethod
    def processArguments():
        parser = argparse.ArgumentParser(description="""\
Utility %s version %s.

* Script1: SummarizePathwayHierarchy
    * Input pathway description
    * Input nodes to descendants
    * Output: per node total/count/odds-ratio/p-value
    
""" % (os.path.basename(sys.argv[0]), __version__), formatter_class=RawTextHelpFormatter)

        parser.add_argument('-a', '--pathToAncestor',
                            help='path to ancestors',  required=True)
        parser.add_argument('-d', '--ancestorToDescendant',
                            help='node to descendant', required=True)
        parser.add_argument('-p', '--pathwayList',
                            help='pathway list file', required=True)
        parser.add_argument('-m', '--minPathwayCount',
                            help='minimum pathway count to consider an ancestor', required=False, default=100)
        parser.add_argument('-o', '--outputRoot',
                            help='root of the output files', required=True)
        try:
            args = parser.parse_args()
        except:
            args = None
        return args

    def loadDistilledOntology(self):
        """Check: 
        (1) For each pathway, find all of its ancestors and save into a set, which is in term 
        saved into pathway_info. This is saved into a hashset for pathways.
        (2) For each ancestor, find all of its descendants and save into a set, which is in term 
        saved into ancestor_info. This is saved into a hashset for ancestors."""
        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] SummarizePathwayHierarchy::loadDistilledOntology START\n" % SimpleTime.now())

        self.pathway_info_hash = {}
        self.pathway_id_hash = {}

        pathway_info_reader = open(self.myArgs.pathToAncestor, "rt")
        line_idx = -1

        for line in pathway_info_reader:
            line_idx += 1
            if (line_idx == 0):
                continue

            ff = line.strip().split('\t')
            pathway_name = ff[0]
            pathway_id = ff[1]
            pathway_ancestor_count = int(ff[2])

            if (self.DEBUG_LOAD_DISTILLED_ONTOLOGY):
                sys.stderr.write("Loading pathway info for %s %s %s ancestors\n" % (
                    pathway_name, pathway_id, pathway_ancestor_count))

            pathway_ancestor_set = set()
            if (pathway_ancestor_count > 0):
                ancestor_list = ff[3].split(';')
                for ancestor in ancestor_list:
                    pathway_ancestor_set.add(ancestor)

            pathway_info = CStruct(pathway_name=pathway_name, pathway_id=pathway_id,
                                   pathway_ancestor_count=pathway_ancestor_count, pathway_ancestor_set=pathway_ancestor_set)
            self.pathway_info_hash[pathway_name] = pathway_info
            self.pathway_id_hash[pathway_name] = pathway_id

        pathway_info_reader.close()

        self.ancestor_info_hash = {}
        ancestor_info_reader = open(self.myArgs.ancestorToDescendant, "rt")
        self.minPathwayCount = int(self.myArgs.minPathwayCount)
        line_idx = -1

        for line in ancestor_info_reader:
            line_idx += 1
            if (line_idx == 0):
                continue

            ff = line.strip().split('\t')
            ancestor_name = ff[0]
            ancestor_id = ff[1]
            descendants_count = int(ff[2])
            if (descendants_count < self.minPathwayCount):
                continue

            ancestor_info = CStruct(ancestor_name=ancestor_name, ancestor_id=ancestor_id, descendants_count=descendants_count,
                                    descendants_set=set(), ancestor_representation=0, ancestor_odds_ratio=0, ancestor_pvalue=1)
            self.ancestor_info_hash[ancestor_id] = ancestor_info

        ancestor_info_reader.close()

        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] SummarizePathwayHierarchy::loadDistilledOntology STOP\n" % SimpleTime.now())

    def loadEnrichedPathwaysList(self):
        """Use the input pathway list (a list of enriched pathways for a particular clinical condition?). For each enriched pathway, find all the ancestors.
        TODO: Line 163-171: save the ones that are high count - so-called "observed" nodes?? What does it mean """
        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] SummarizePathwayHierarchy::loadEnrichedPathwaysList START\n" % SimpleTime.now())

        self.pathway_set = set()

        pathway_list_reader = open(self.myArgs.pathwayList, "rt")
        line_idx = 0

        for line in pathway_list_reader:
            line_idx += 1
            if (line_idx == 0):
                continue

            if self.myArgs.pathwayList[-3:] == 'csv':
                ff = line.strip().split(',')
            elif self.myArgs.pathwayList[-3:] == 'xls':
                ff = line.strip().split(';')[0].split('	')
            pathway_name = ff[0]
            if (pathway_name in self.pathway_info_hash):
                self.pathway_set.add(pathway_name)
                # propagate to all ancestors
                pathway_info = self.pathway_info_hash[pathway_name]

                if (self.DEBUG_LOAD_PATHWAY_LIST):
                    sys.stderr.write("Found known pathway %s %s %s\n" % (
                        pathway_name, pathway_info.pathway_id, pathway_info.pathway_ancestor_count))

                for ancestor_id in pathway_info.pathway_ancestor_set:
                    if (ancestor_id in self.ancestor_info_hash):  # we remove low count ancestors
                        ancestor_info = self.ancestor_info_hash[ancestor_id]
                        ancestor_info.descendants_set.add(
                            pathway_info.pathway_id)

                        if (self.DEBUG_LOAD_PATHWAY_LIST):
                            sys.stderr.write("%s found ancestor %s %s %s -> %s pathways \n" % (pathway_info.pathway_id, ancestor_id,
                                                                                               ancestor_info.ancestor_name, ancestor_info.descendants_count, len(ancestor_info.descendants_set)))
        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] SummarizePathwayHierarchy::loadEnrichedPathwaysList STOP\n" % SimpleTime.now())

    def outputAnnotatedPathways(self):
        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] SummarizePathwayHierarchy::outputAnnotatedPathways START\n" % SimpleTime.now())

        output_file = "%s.pathway_count.xls" % self.myArgs.outputRoot

        # save standard enriched pathways for each subtree root
        with open("%s.infoForSubtree.pkl" % self.myArgs.outputRoot, 'wb') as f:
            pickle.dump(self.ancestor_info_hash, f)

        output_file_writer = open(output_file, "wt")
        header = ["Ontology_Node", "GO_ID", "Node Total Pathways", "Node Observed Pathway",
                  "Node Observed Pathways (%)", "Total pathways", "Enriched Pathways count", "Enriched pathways in term", "Enriched pathways in term (%)", "Odds-ratio", "p-value"]
        output_file_writer.write("%s\n" % "\t".join(header))

        total_pathways = len(self.pathway_info_hash)
        enriched_pathways = len(self.pathway_set)

        for ancestor_id in self.ancestor_info_hash:
            ancestor_info = self.ancestor_info_hash[ancestor_id]

            # set up the Fisher's exact test
            # overall pathways
            # pathways in this term
            # pathway list size
            # pathway list in this term

            pathways_in_term = ancestor_info.descendants_count
            pathways_not_in_term = len(
                self.pathway_info_hash) - ancestor_info.descendants_count
            pathways_in_ancestor = len(ancestor_info.descendants_set)
            pathways_not_in_ancestor = enriched_pathways-pathways_in_ancestor
            if (self.DEBUG_OUTPUT):
                sys.stderr.write("Enriched pathways in ancestor %s enriched pathways not in ancestor %s Pathways in term %s Pathways not in term %s\n" % (
                    pathways_in_ancestor, pathways_not_in_ancestor, pathways_in_term, pathways_not_in_term))

            oddsRatio, pValue = scipy.stats.fisher_exact([[pathways_in_ancestor, pathways_not_in_ancestor],
                                                          [pathways_in_term, pathways_not_in_term]])
            observed_pathways_in_ancestor_ratio = float(
                pathways_in_ancestor)/float(ancestor_info.descendants_count)
            if enriched_pathways != 0:
                observed_pathways_in_enriched_pathways_ratio = float(
                    pathways_in_ancestor)/float(enriched_pathways)
                ancestor_buffer = [ancestor_info.ancestor_name, ancestor_info.ancestor_id, ancestor_info.descendants_count, pathways_in_ancestor,
                                   observed_pathways_in_ancestor_ratio, total_pathways, enriched_pathways, pathways_in_ancestor, observed_pathways_in_enriched_pathways_ratio, oddsRatio, pValue]
                output_file_writer.write("%s\n" % "\t".join(
                    [str(x) for x in ancestor_buffer]))
            else:
                print(ancestor_info.ancestor_name)
        output_file_writer.close()

        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] SummarizePathwayHierarchy::loadDistilledHierarchy STOP\n" % SimpleTime.now())

    def work(self):
        mpl.rcParams['pdf.fonttype'] = 42
        self.loadDistilledOntology()
        self.loadEnrichedPathwaysList()
        self.outputAnnotatedPathways()

########################################################################################
# MAIN
########################################################################################

# Process command line options
# Instantiate analyzer using the program arguments
# Analyze this !


###PIP USAGE: sum = SummarizePathwayHierarchy(ancestorF, desF, pathwayF, 10, 'test0418'); sum.work()###
if __name__ == '__main__':
    try:
        sys.stderr.write("Command line %s\n" % " ".join(sys.argv))
        myArgs = SummarizePathwayHierarchy.processArguments()
        if (myArgs is None):
            pass
        else:
            bp = SummarizePathwayHierarchy(myArgs)
            bp.work()
    except:
        sys.stderr.write("An unknown error occurred.\n")
        raise
