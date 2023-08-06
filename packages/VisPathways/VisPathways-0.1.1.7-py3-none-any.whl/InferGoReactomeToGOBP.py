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
import time

# from CCLabUtils.simpleTime import SimpleTime
from simpleTime import SimpleTime


class CStruct(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class InferGoReactomeToGO:
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

* Script1: InferGoReactomeToGO
    * Input ReactomePathwaysRelation.txt
    * Input GO_BP.xml
    * Output: go Reactome / all the GO_BP terms

""" % (os.path.basename(sys.argv[0]), __version__), formatter_class=RawTextHelpFormatter)

        parser.add_argument(
            '-g', '--goReactomes',   help='Reactome gene ontology hiearchy input file',  required=True)
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
                "[%s] InferGoReactomeToGO::loadGoXML START\n" % SimpleTime.now())

        self.go_msigdb_to_go_id_hash = {}
        self.go_id_to_go_msigdb_hash = {}

        xml_reader = open(self.myArgs.goXml, "rt")

        for line in xml_reader:
            if line.find("GENESET STANDARD_NAME") == 0:
                continue
            # TODO: Debugged by Tom
            # pathway STANDARD name
            m1 = re.search(r'GENESET STANDARD_NAME="([^"]+)"', line)
            # Reactome HSA ID (186 in total)
            m3 = re.search(r'EXACT_SOURCE="R-([^"]+)', line)
            m2 = re.search(r'detail/([^"]+)', line)
            if m1 != None and (m2 != None or m3 != None):
                go_msigdb = m1.group(1)

                if m2 == None:
                    go_id = m3.group(0)[14:].split("|")[0]
                else:
                    go_id = m2.group(0)[7:].split("|")[0]

                if (self.DEBUG_LOAD_GO_XML):
                    sys.stderr.write(
                        "Loaded GO MSIGDB %s --> REACTOME ID %s\n" % (go_msigdb, go_id))

                self.go_msigdb_to_go_id_hash[go_msigdb] = go_id
                self.go_id_to_go_msigdb_hash[go_id] = go_msigdb
        xml_reader.close()

        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoReactomeToGO::loadGoXML STOP\n" % SimpleTime.now())

    def getAncestors(self):
        """Get basic ancestors"""
        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoReactomeToGO::getAncestors START\n" % SimpleTime.now())

        self.basic_ontology_ancestors = {}

        line_id = -1
        crt_id = None
        crt_name = None

        Reactome_reader = open(self.myArgs.goReactomes, "rt")
        for ontology_line in Reactome_reader:
            line_id += 1

            # empty lines
            match_id = re.search(r'^\s*$', ontology_line)
            if (match_id):
                if (self.DEBUG_COMPUTE_ANCESTORS):
                    sys.stderr.write("[%s] found empty line \n" % line_id)
            else:
                crt_line_info_list = ontology_line.split("	")
                crt_ancestor_id = crt_line_info_list[0]
                crt_id = crt_line_info_list[1][:-1]

                if (crt_id in self.go_id_to_go_msigdb_hash.keys()) and (crt_ancestor_id in self.go_id_to_go_msigdb_hash.keys()):
                    crt_name = self.go_id_to_go_msigdb_hash[crt_id]

                    if crt_id not in self.basic_ontology_ancestors.keys():
                        term_info = {'crt_id': crt_id, 'pathway_name': crt_name, 'ancestor_id_set': {
                            crt_ancestor_id}}
                        self.basic_ontology_ancestors[crt_id] = term_info
                    else:
                        # already existing, append ancestors
                        self.basic_ontology_ancestors[crt_id]['ancestor_id_set'].update({
                                                                                        crt_ancestor_id})

                    if (self.DEBUG_COMPUTE_ANCESTORS):
                        sys.stderr.write("Pathway" + crt_name +
                                         "-> getting initial ancestors" + "\n")

        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoReactomeToGO::getAncestors STOP\n" % SimpleTime.now())

    # actually a loop would do, since we load the ontology first
    def recCountOntologyAncestors(self, ancestor_id, go_id_ancestors_working_set):
        """helper function that adds the ancestors of ancestors into the ancestor set of a particular pathway term"""
        if (self.DEBUG_PROGRESS):
            sys.stderr.write("[%s] InferGoSlimToGO::recCountOntologyAncestors START %s\n" % (
                SimpleTime.now(), ancestor_id))

        if (ancestor_id in go_id_ancestors_working_set):
            sys.stderr.write("Shortcircuit %s in %s\n" % (
                ancestor_id, ";".join(list(go_id_ancestors_working_set))))
        else:
            go_id_ancestors_working_set.add(ancestor_id)

            # check the old dictionary for info of the current standard pathway
            if ancestor_id in self.basic_ontology_ancestors.keys():
                term_info = self.basic_ontology_ancestors[ancestor_id]
                # check every ancestor of the current pathway
                for great_ancestor_id in term_info['ancestor_id_set']:
                    self.recCountOntologyAncestors(
                        great_ancestor_id, go_id_ancestors_working_set)

    def applyBpPathwaysToOntology(self):
        """Get all the ancestors for each node, i.e. gett ancestors of ancestors of a current node into
        this node's ancestor id set"""
        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoSlimToGO::applyBpPathwaysToOntology START\n" % SimpleTime.now())

        self.ontology_to_ancestor_terms = {}

        # for every standard pathway, get ancestors of its ancestors into its ancestor set
        for msigdb_go_name in self.go_msigdb_to_go_id_hash:
            go_id = self.go_msigdb_to_go_id_hash[msigdb_go_name]
            if (self.DEBUG_COMPUTE_ANCESTORS):
                sys.stderr.write("StartPathway %s -> %s\n" %
                                 (msigdb_go_name, go_id))

            go_id_ancestors_working_set = set()

            if (go_id in self.basic_ontology_ancestors):
                term_info = self.basic_ontology_ancestors[go_id]
                for ancestor in term_info['ancestor_id_set']:
                    self.recCountOntologyAncestors(
                        ancestor, go_id_ancestors_working_set)

                self.ontology_to_ancestor_terms[go_id] = go_id_ancestors_working_set
                if (self.DEBUG_COMPUTE_ANCESTORS):
                    sys.stderr.write("Pathway %s -> %s: %s ancestors %s\n" % (msigdb_go_name, go_id, len(
                        go_id_ancestors_working_set), ";".join(list(go_id_ancestors_working_set))))
            else:
                sys.stderr.write(
                    "NotFoundPathway %s %s in ontology\n" % (msigdb_go_name, go_id))

        # now setup the reverse lookup hash: eg node to all descendants
        self.ontology_to_descendant_terms = {}
        for go_id in self.ontology_to_ancestor_terms:
            go_id_ancestors_set = self.ontology_to_ancestor_terms[go_id]

            for ancestor_id in go_id_ancestors_set:
                if not (ancestor_id in self.ontology_to_descendant_terms):
                    self.ontology_to_descendant_terms[ancestor_id] = set()
                self.ontology_to_descendant_terms[ancestor_id].add(go_id)

        if (self.DEBUG_COMPUTE_ANCESTORS):
            for ancestor_id in self.ontology_to_descendant_terms:
                descendant_set = self.ontology_to_descendant_terms[ancestor_id]
                sys.stderr.write("ancestor %s has %s descendants \n" %
                                 (ancestor_id, len(descendant_set)))

        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoSlimToGO::applyBpPathwaysToOntology STOP\n" % SimpleTime.now())

    def outputGoReactomeToGO(self):
        """output multiple files
        # first msigdb pathways to all ancestors
        # then all ancestors to msigdb pathways
        [Revised from Cristian's code]"""

        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoSlimToGO::outputGoSlimToGO START\n" % SimpleTime.now())

        # FILE1: pathway to go_ids
        pathway_to_go_id_ancestors_file = "%s.pathway_to_go_id_ancestors.xls" % self.myArgs.outputRoot
        pathway_to_go_id_ancestors_file_writer = open(
            pathway_to_go_id_ancestors_file, "wt")
        pathway_to_go_id_ancestors_file_writer.write(
            "Pathway\tReactome_ID\tAncestor_count\tAncestors_Reactome_ID\tAncestors_name\n")

        for msigdb_id in self.go_msigdb_to_go_id_hash:
            go_id = self.go_msigdb_to_go_id_hash[msigdb_id]
            if not (go_id in self.ontology_to_ancestor_terms):
                sys.stderr.write("Eeek: %s -> %s skipped\n" %
                                 (msigdb_id, go_id))
                continue
            else:
                ancestor_set = self.ontology_to_ancestor_terms[go_id]
                ancestor_names_list = []
                for ancestor_id in ancestor_set:
                    go_name = self.go_id_to_go_msigdb_hash[ancestor_id]
                    ancestor_names_list.append(go_name)

                ancestor_names_list.sort()
                pathway_to_go_id_ancestors_file_writer.write("%s\t%s\t%s\t%s\t%s\n" % (msigdb_id, go_id, len(ancestor_set),
                                                                                       ";".join(list(ancestor_set)), ";".join(ancestor_names_list)))

        pathway_to_go_id_ancestors_file_writer.close()

        # FILE2: ancestors to pathways
        term_classes_to_pathways = "%s.term_classes_to_pathways.xls" % self.myArgs.outputRoot
        term_classes_to_pathways_writer = open(term_classes_to_pathways, "wt")
        term_classes_to_pathways_writer.write(
            "Pathway\tReactome_ID\tDescendants_Count\tDescendants_Reactome_ID\tDescendants_MSigDB_name\n")

        for ancestor_id in self.ontology_to_descendant_terms:
            go_name = self.go_id_to_go_msigdb_hash[ancestor_id]
            descendant_set = self.ontology_to_descendant_terms[ancestor_id]
            descendant_name_list = []
            for descendant_id in descendant_set:
                if (descendant_id in self.go_id_to_go_msigdb_hash):
                    descendant_name = self.go_id_to_go_msigdb_hash[descendant_id]
                    descendant_name_list.append(descendant_name)

                if (self.DEBUG_OUTPUT):
                    sys.stderr.write("ancestor id %s w/ %s descendants ; descendant_id %s descendant_pathway %s\n" % (
                        ancestor_id, len(descendant_set), descendant_id, descendant_name))

            descendant_name_list.sort()

            descendant_id_list = list(descendant_set)
            if (len(descendant_set) > 100):
                descendant_id_list = descendant_id_list[0:100]
                descendant_name_list = descendant_name_list[0:100]

            term_classes_to_pathways_writer.write("%s\t%s\t%s\t%s\t%s\n" % (go_name, ancestor_id, len(descendant_set),
                                                                            ";".join(descendant_id_list), ";".join(descendant_name_list)))

        term_classes_to_pathways_writer.close()

        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoSlimToGO::outputGoSlimToGO STOP\n" % SimpleTime.now())

    def work(self):
        mpl.rcParams['pdf.fonttype'] = 42
        self.loadGoXML()
        self.getAncestors()
        self.applyBpPathwaysToOntology()
        self.outputGoReactomeToGO()

########################################################################################
# MAIN
########################################################################################

# Process command line options
# Instantiate analyzer using the program arguments
# Analyze this !


if __name__ == '__main__':

    ###USAGE: python3 InferGoReactomeToGOBP.v-2.py -g ReactomePathwaysRelation.txt -x msigdb_v7.2.xml -o test###
    try:
        sys.stderr.write("Command line %s\n" % " ".join(sys.argv))
        myArgs = InferGoReactomeToGO.processArguments()
        if (myArgs is None):
            pass
        else:
            bp = InferGoReactomeToGO(myArgs)
            bp.work()
    except:
        sys.stderr.write("An unknown error occurred.\n")
        raise
