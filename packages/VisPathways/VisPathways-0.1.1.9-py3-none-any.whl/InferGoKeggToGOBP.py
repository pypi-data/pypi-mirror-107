#!/usr/bin/env python
__author__ = "Tom Fu, Cristian Coarfa"

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
from argparse import RawTextHelpFormatter


# from CCLabUtils.simpleTime import SimpleTime
from simpleTime import SimpleTime


class CStruct(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class InferGoKeggToGO:
    DEBUG_PROGRESS = True
    DEBUG_LOAD_GO_XML = True
    DEBUG_COMPUTE_ANCESTORS = True
    DEBUG_COMPUTE_DESCENDANTS = True
    DEBUG_OUTPUT = True

    def __init__(self, *input):
        if len(input) == 1:
            self.myArgs = input[0]
        elif len(input) == 3:
            ontologyFile, xmlFile, outputRoot = input
            self.myArgs = CStruct(
                goSlims=ontologyFile, goXml=xmlFile, outputRoot=outputRoot)
        else:
            raise Exception(
                "Number of inputs has to be either 1 (from command line) or 3 (ontologyFile, xmlFile, outputRoot; in order).")

    @staticmethod
    def processArguments():
        parser = argparse.ArgumentParser(description="""\
Utility %s version %s.

* Script1: InferGoKeggToGO
    * Input hsa0001.keg
    * Input GO_BP.xml
    * Output: go Kegg / all the GO_BP terms

""" % (os.path.basename(sys.argv[0]), __version__), formatter_class=RawTextHelpFormatter)

        parser.add_argument(
            '-g', '--goKegg',   help='kegg hsa gene ontology input file',  required=True)
        parser.add_argument(
            '-x', '--goXml', help='XML version of the MSigDB GOBP', required=True)
        parser.add_argument('-o', '--outputRoot',
                            help='root of the output files', required=True)
        try:
            args = parser.parse_args()
        except:
            args = None
        return args

    def loadGoXML(self):
        # TODO: Check - load the xml file and establish dict/hash for (id to msigdb) and (msigdb to id)
        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoKeggToGO::loadGoXML START\n" % SimpleTime.now())

        self.go_msigdb_to_go_id_hash = {}
        self.go_id_to_go_msigdb_hash = {}

        xml_reader = open(self.myArgs.goXml, "rt")

        for line in xml_reader:
            if line.find("GENESET STANDARD_NAME") == 0:
                continue
            # TODO: Debugged by Tom
            # pathway STANDARD name
            m1 = re.search(r'GENESET STANDARD_NAME="([^"]+)"', line)
            m2 = re.search(r'hsa/hsa......html',
                           line)  # Kegg HSA ID (186 in total)
            if m1 != None and m2 != None:
                go_msigdb = m1.group(1)

                go_id = m2.group(0)[4:-5]

                if (self.DEBUG_LOAD_GO_XML):
                    sys.stderr.write(
                        "Loaded GO MSIGDB %s --> KEGG HSA ID %s\n" % (go_msigdb, go_id))

                self.go_msigdb_to_go_id_hash[go_msigdb] = go_id
                self.go_id_to_go_msigdb_hash[go_id] = go_msigdb
        xml_reader.close()

        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoKeggToGO::loadGoXML STOP\n" % SimpleTime.now())

    def getAncestors(self):
        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoKeggToGO::loadOntology START\n" % SimpleTime.now())

        self.basic_ontology_ancestors = {}
        self.standard_name_match_hash = {}

        basic_ontology_ancestors = {}

        crt_id = None
        crt_ancestor_id_set = set()
        crt_ancestor_name_set = set()
        crt_name = None
        crt_pathway_id = None

        crt_A_ancestor_id = None
        crt_A_ancestor_name = None
        crt_B_ancestor_id = None
        crt_B_ancestor_name = None

        # read every small pathway line and store its ancestors into it
        kegg_reader = open(self.myArgs.goKegg, 'rt')

        # GOAL: Form a dictionary where the keys are ascension numbers (HSA ids when it has one, and if not, then the 5 digit kegg number in the kegg file)
        # Later when checking, we can see if the ids are in the msigdb dictionary, if so then it's a child (lowest level) pathway
        for ontology_line in kegg_reader:
            # check for empty line
            match_id = re.search(r'^\s*$', ontology_line)
            if (not (match_id)):
                # check for lines that are empty except the first letter being B or # (changing ancestor, no need to finalize previoius term here)
                match_id = re.search(r'^.\s*$', ontology_line)
                if (not (match_id)):
                    if ontology_line[0] == 'A':
                        # five digit id, not hsa id
                        crt_id = "ko" + ontology_line[1:6]
                        crt_name = ontology_line[7:-1]
                        crt_A_ancestor_id = crt_id
                        crt_A_ancestor_name = crt_name
                        if not crt_id in basic_ontology_ancestors:
                            term_info = {'crt_id': crt_id, 'pathway_name': crt_name,
                                         'pathway_id': None, 'ancestor_id_set': set(), 'ancestor_name_set': set()}
                            basic_ontology_ancestors[crt_id] = term_info
                        else:
                            basic_ontology_ancestors[crt_id]['ancestor_id_set'].union(
                                {crt_A_ancestor_id})
                            basic_ontology_ancestors[crt_id]['ancestor_name_set'].union(
                                {crt_A_ancestor_name})
                        if (self.DEBUG_COMPUTE_ANCESTORS):
                            sys.stderr.write("Pathway" + crt_name + "-> ancestors" +
                                             str(basic_ontology_ancestors[crt_id]['ancestor_name_set']) + "\n")
                    elif ontology_line[0] == 'B':
                        crt_id = "ko" + ontology_line[3:8]
                        crt_name = ontology_line[9:-1]
                        crt_B_ancestor_id = crt_id
                        crt_B_ancestor_name = crt_name
                        if not crt_id in basic_ontology_ancestors:
                            term_info = {'crt_id': crt_id, 'pathway_name': crt_name,
                                         'pathway_id': None, 'ancestor_id_set': {crt_A_ancestor_id}, 'ancestor_name_set': {crt_A_ancestor_name}}
                            print(crt_name)
                            basic_ontology_ancestors[crt_id] = term_info
                        else:
                            basic_ontology_ancestors[crt_id]['ancestor_id_set'].union(
                                {crt_A_ancestor_id})
                            basic_ontology_ancestors[crt_id]['ancestor_name_set'].union(
                                {crt_A_ancestor_name})
                        if (self.DEBUG_COMPUTE_ANCESTORS):
                            sys.stderr.write("Pathway" + crt_name + "-> ancestors" +
                                             str(basic_ontology_ancestors[crt_id]['ancestor_name_set']) + "\n")
                    elif ontology_line[0] == 'C':
                        crt_id = "ko" + ontology_line[5:10]
                        crt_name_and_pathway_id = ontology_line[11:].split(
                            '[')
                        if '[' in ontology_line:
                            crt_name = crt_name_and_pathway_id[0][:-1]
                            crt_pathway_id = crt_name_and_pathway_id[1][5:-2]
                            # find standard name and replace the original name
                            if crt_pathway_id in self.go_id_to_go_msigdb_hash.keys():
                                cur_standard_name = self.go_id_to_go_msigdb_hash[crt_pathway_id]
                                crt_name = cur_standard_name
                        else:
                            crt_name = crt_name_and_pathway_id[0][:-1]
                            crt_pathway_id = None
                        crt_ancestor_id_set = {
                            crt_A_ancestor_id, crt_B_ancestor_id}
                        crt_ancestor_name_set = {
                            crt_A_ancestor_name, crt_B_ancestor_name}

                        if not crt_id in basic_ontology_ancestors:
                            term_info = {'crt_id': crt_id, 'pathway_name': crt_name,
                                         'pathway_id': crt_pathway_id, 'ancestor_id_set': crt_ancestor_id_set,  'ancestor_name_set': crt_ancestor_name_set}
                            basic_ontology_ancestors[crt_id] = term_info
                        else:
                            basic_ontology_ancestors[crt_id]['ancestor_id_set'].union(
                                crt_ancestor_id_set)
                            basic_ontology_ancestors[crt_id]['ancestor_name_set'].union(
                                crt_ancestor_name_set)
                        if (self.DEBUG_COMPUTE_ANCESTORS):
                            sys.stderr.write("Pathway" + crt_name + "-> ancestors" +
                                             str(basic_ontology_ancestors[crt_id]['ancestor_name_set']) + "\n")
        self.basic_ontology_ancestors = basic_ontology_ancestors

        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoKeggToGO::loadOntology STOP\n" % SimpleTime.now())

    def getDescendants(self):

        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoSlimToGO::getDescendants START\n" % SimpleTime.now())

        basic_ontology_descendants = {}

        crt_id = None
        crt_A_id = None
        crt_B_id = None
        crt_A_descendant_id_set = set()
        crt_B_descendant_id_set = set()
        crt_A_descendant_name_set = set()
        crt_B_descendant_name_set = set()
        crt_name = None
        crt_A_name = None
        crt_B_name = None
        crt_pathway_id = None

        # read every small pathway line and store its ancestors into it
        kegg_reader = open(self.myArgs.goKegg, 'rt')

        for ontology_line in kegg_reader:
            # check for empty line
            match_id = re.search(r'^\s*$', ontology_line)
            if (not (match_id)):
                # check for lines that are empty except the first letter being B or # (changing ancestor, no need to finalize previoius term here)
                match_id = re.search(r'^.\s*$', ontology_line)
                if (match_id):
                    if ontology_line[0] == '#':
                        crt_id = crt_A_id
                        crt_name = crt_A_name
                        if not crt_id in basic_ontology_descendants:
                            term_info = {'crt_id': crt_id, 'pathway_name': crt_name,
                                         'pathway_id': None, 'descendant_id_set': crt_A_descendant_id_set, 'descendant_name_set': crt_A_descendant_name_set}
                            basic_ontology_descendants[crt_id] = term_info
                        else:
                            basic_ontology_descendants[crt_id]['descendant_id_set'].union(
                                crt_A_descendant_id_set)
                            basic_ontology_descendants[crt_id]['descendant_name_set'].union(
                                crt_A_descendant_name_set)
                        # if (self.DEBUG_COMPUTE_DESCENDANTS):
                        #     sys.stderr.write("Pathway" + crt_name + "-> descendants" +
                        #                      str(basic_ontology_descendants[crt_id]['descendant_name_set']) + "\n")
                    elif ontology_line[0] == 'B':
                        crt_id = crt_B_id
                        crt_name = crt_B_name
                        if not crt_id in basic_ontology_descendants:
                            term_info = {'crt_id': crt_id, 'pathway_name': crt_name,
                                         'pathway_id': None,  'descendant_id_set': crt_B_descendant_id_set, 'descendant_name_set': crt_B_descendant_name_set}
                            basic_ontology_descendants[crt_id] = term_info
                        else:
                            basic_ontology_descendants[crt_id]['descendant_id_set'].union(
                                crt_B_descendant_id_set)
                            basic_ontology_descendants[crt_id]['descendant_name_set'].union(
                                crt_B_descendant_name_set)
                        # if (self.DEBUG_COMPUTE_DESCENDANTS):
                        #     sys.stderr.write("Pathway" + crt_name + "-> descendants" +
                        #                      str(basic_ontology_descendants[crt_id]['descendant_name_set']) + "\n")
                else:
                    # if ontology_line[0] != 'D':
                    #     print(ontology_line)
                    if ontology_line[0] == 'A':
                        crt_A_id = "ko" + ontology_line[1:5]
                        crt_A_name = ontology_line[7:-1]
                        crt_A_descendant_id_set = set()
                        crt_A_descendant_name_set = set()
                    if ontology_line[0] == 'B':
                        crt_B_id = "ko" + ontology_line[3:8]
                        crt_B_name = ontology_line[9:-1]
                        crt_B_descendant_id_set = set()
                        crt_B_descendant_name_set = set()
                    elif ontology_line[0] == 'C':
                        crt_id = "ko" + ontology_line[5:10]
                        crt_name_and_pathway_id = ontology_line[11:].split(
                            '[')
                        if '[' in ontology_line:
                            crt_name = crt_name_and_pathway_id[0][:-1]
                            crt_pathway_id = crt_name_and_pathway_id[1][5:-2]
                            # print(crt_name)
                            # print(crt_pathway_id)
                            if crt_pathway_id in self.go_id_to_go_msigdb_hash.keys():
                                cur_standard_name = self.go_id_to_go_msigdb_hash[crt_pathway_id]
                                crt_name = cur_standard_name
                                print("standard")
                                print(crt_name)
                        else:
                            crt_name = crt_name_and_pathway_id[0][:-1]
                            crt_pathway_id = None
                        crt_A_descendant_id_set.add(crt_id)
                        crt_B_descendant_id_set.add(crt_id)
                        crt_A_descendant_name_set.add(crt_name)
                        crt_B_descendant_name_set.add(crt_name)
                        if not crt_id in basic_ontology_descendants:
                            term_info = {'crt_id': crt_id, 'pathway_name': crt_name,
                                         'pathway_id': crt_pathway_id, 'descendant_id_set': set(), 'descendant_name_set': set()}
                            basic_ontology_descendants[crt_id] = term_info
                        else:
                            basic_ontology_descendants[crt_id]['descendant_id_set'].union(
                                crt_B_descendant_id_set)
                            basic_ontology_descendants[crt_id]['descendant_name_set'].union(
                                crt_B_descendant_name_set)
                        # if (self.DEBUG_COMPUTE_DESCENDANTS):
                        #     sys.stderr.write("Pathway" + crt_name + "-> descendants" +
                        #                      str(basic_ontology_descendants[crt_id]['descendant_name_set']) + "\n")

        self.basic_ontology_descendants = basic_ontology_descendants

        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoSlimToGO::getDescendants STOP\n" % SimpleTime.now())

    def outputGoKeggToGO(self):
        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoSlimToGO::outputGoKeggToGO START\n" % SimpleTime.now())

        basic_ontology_ancestors = self.basic_ontology_ancestors
        basic_ontology_descendants = self.basic_ontology_descendants
        # pathway to ancestor file
        pathway_to_kegg_id_ancestors_file = "%s.pathway_to_go_id_ancestors.xls" % self.myArgs.outputRoot
        pathway_to_kegg_id_ancestors_file_writer = open(
            pathway_to_kegg_id_ancestors_file, "wt")
        pathway_to_kegg_id_ancestors_file_writer.write(
            "Pathway\tKegg_ID\tAncestor_count\tAncestors_Kegg_ID\tAncestors_name\n")

        for kegg_id in basic_ontology_ancestors:
            currentTerm = basic_ontology_ancestors[kegg_id]
            kegg_id = currentTerm['crt_id']
            pathway_name = currentTerm['pathway_name']
            ancestor_id_set = currentTerm['ancestor_id_set']
            ancestor_name_set = currentTerm['ancestor_name_set']
            pathway_to_kegg_id_ancestors_file_writer.write("%s\t%s\t%s\t%s\t%s\n" % (pathway_name, kegg_id, len(ancestor_id_set),
                                                                                     ";".join(list(ancestor_id_set)), ";".join(ancestor_name_set)))
        pathway_to_kegg_id_ancestors_file_writer.close()

        # pathway to descendant file
        pathway_to_kegg_id_descendants_file = "%s.term_classes_to_pathways.xls" % self.myArgs.outputRoot
        pathway_to_kegg_id_descendants_file_writer = open(
            pathway_to_kegg_id_descendants_file, "wt")
        pathway_to_kegg_id_descendants_file_writer.write(
            "Pathway\tKegg_ID\tDescendants_Count\tDescendants_Kegg_ID\tDescendants_name\n")

        for kegg_id in basic_ontology_descendants:
            currentTerm = basic_ontology_descendants[kegg_id]
            kegg_id = currentTerm['crt_id']
            pathway_name = currentTerm['pathway_name']
            descendant_id_set = currentTerm['descendant_id_set']
            descendant_name_set = currentTerm['descendant_name_set']
            pathway_to_kegg_id_descendants_file_writer.write("%s\t%s\t%s\t%s\t%s\n" % (pathway_name, kegg_id, len(descendant_id_set),
                                                                                       ";".join(list(descendant_id_set)), ";".join(descendant_name_set)))

        pathway_to_kegg_id_descendants_file_writer.close()

        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoSlimToGO::outputGoKeggToGO STOP\n" % SimpleTime.now())

    def work(self):
        mpl.rcParams['pdf.fonttype'] = 42
        self.loadGoXML()
        self.getAncestors()
        self.getDescendants()
        self.outputGoKeggToGO()

########################################################################################
# MAIN
########################################################################################

# Process command line options
# Instantiate analyzer using the program arguments
# Analyze this !


if __name__ == '__main__':

    ###USAGE: python3 InferGoKeggToGOBP.v-1.py -g go-basic.obo -x msigdb_v7.2.xml -o something.xls###
    try:
        sys.stderr.write("Command line %s\n" % " ".join(sys.argv))
        myArgs = InferGoKeggToGO.processArguments()
        if (myArgs is None):
            pass
        else:
            bp = InferGoKeggToGO(myArgs)
            bp.work()
    except:
        sys.stderr.write("An unknown error occurred.\n")
        raise
