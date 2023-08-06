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
import time
import pickle


# from CCLabUtils.simpleTime import SimpleTime
from simpleTime import SimpleTime


class CStruct(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class InferGoSlimToGO:
    DEBUG_PROGRESS = True
    DEBUG_LOAD_GO_XML = True
    DEBUG_LOAD_GO_SLIM = True
    DEBUG_COMPUTE_ANCESTORS = True
    DEBUG_OUTPUT = True

    def __init__(self, *input):
        if len(input) == 1:
            self.myArgs = input[0]
            time.sleep(3)
        elif len(input) == 3:
            ontologyFile, xmlFile, outputRoot = input
            self.myArgs = CStruct(
                goSlims=ontologyFile, goXml=xmlFile, outputRoot=outputRoot)

    @staticmethod
    def processArguments():
        parser = argparse.ArgumentParser(description="""\
Utility %s version %s.

* Script1: InferGoSlimToGO
    * Input go-basic.obo
    * Input GO_BP.xml
    * Output: go slim / all the GO_BP terms
    
""" % (os.path.basename(sys.argv[0]), __version__), formatter_class=RawTextHelpFormatter)

        parser.add_argument(
            '-g', '--goSlims',   help='gene ontology basic go slims',  required=True)
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
                "[%s] InferGoSlimToGO::loadGoXML START\n" % SimpleTime.now())

        self.go_msigdb_to_go_id_hash = {}
        self.go_id_to_go_msigdb_hash = {}
        print(self.myArgs)
        xml_reader = open(self.myArgs.goXml, "rt")

        for line in xml_reader:
            if line.find("GENESET STANDARD_NAME") == 0:
                continue

            # pathway STANDARD name
            m1 = re.search(r'GENESET STANDARD_NAME="([^"]+)"', line)
            m2 = re.search(r'term/(GO:[^"]+)"', line)  # GO ID
            if m1 != None and m2 != None:
                go_msigdb = m1.group(1)

                go_id = m2.group(1)

                if (self.DEBUG_LOAD_GO_XML):
                    sys.stderr.write(
                        "Loaded GO MSIGDB %s --> GO ID %s\n" % (go_msigdb, go_id))

                self.go_msigdb_to_go_id_hash[go_msigdb] = go_id
                self.go_id_to_go_msigdb_hash[go_id] = go_msigdb
        xml_reader.close()

        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoSlimToGO::loadGoXML STOP\n" % SimpleTime.now())

    def loadOntology(self):
        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoSlimToGO::loadOntology STOP\n" % SimpleTime.now())

        self.basic_ontology_ancestors = {}
        # for whole tree plotting
        self.immediate_ancestor_dict = {}

        line_id = -1
        term_count = 0

        crt_id = None
        crt_ancestor_set = None
        crt_name = None
        crt_namespace = None

        slim_reader = open(self.myArgs.goSlims, "rt")
        for ontology_line in slim_reader:
            line_id += 1

            # empty lines
            match_id = re.search(r'^\s*$', ontology_line)
            if (match_id):
                if (self.DEBUG_LOAD_GO_SLIM):
                    sys.stderr.write("[%s] found empty line \n" % line_id)
                # finalize previous term
                if (crt_id):
                    if (crt_namespace == "biological_process"):
                        # a struct involving all the ancestors?
                        term_info = CStruct(
                            goid=crt_id, go_name=crt_name, namespace=crt_namespace, ancestor_set=crt_ancestor_set)
                        self.basic_ontology_ancestors[crt_id] = term_info
                        if (self.DEBUG_LOAD_GO_SLIM):
                            sys.stderr.write("[%s] Hashing term %s %s %s \n" % (
                                line_id, crt_id, crt_name, crt_namespace))
                    crt_id = None

            if (ontology_line.find("[Term]") >= 0):
                # initialize new term
                term_count += 1
                crt_id = None
                crt_ancestor_set = None
                crt_namespace = None
                crt_name = None
                if (self.DEBUG_LOAD_GO_SLIM):
                    sys.stderr.write("[%s] New Term %s \n" %
                                     (line_id, term_count))

            # GO ID
            match_id = re.search(r'^id:\s+(GO:\d+)\s*$', ontology_line)
            if (match_id):
                go_id = match_id.group(1)
                if (self.DEBUG_LOAD_GO_SLIM):
                    sys.stderr.write("[%s] found id %s \n" % (line_id, go_id))
                crt_id = go_id
                crt_ancestor_set = set()

            # PATHWAY NAME
            match_id = re.search(r'^name:\s+(.*)\s*$', ontology_line)
            if (match_id):
                crt_name = match_id.group(1)
                if (self.DEBUG_LOAD_GO_SLIM):
                    sys.stderr.write("[%s] found name %s \n" %
                                     (line_id, crt_name))

            # NAMESPACE
            match_id = re.search(r'^namespace:\s+(.*)\s*$', ontology_line)
            if (match_id):
                crt_namespace = match_id.group(1)
                if (self.DEBUG_LOAD_GO_SLIM):
                    sys.stderr.write("[%s] found namespace %s \n" %
                                     (line_id, crt_namespace))

            # ANCESTOR (IS A)
            match_id = re.search(r'^is_a:\s+([^\s]+)\s+', ontology_line)
            if (match_id):
                ancestor = match_id.group(1)
                if (self.DEBUG_LOAD_GO_SLIM):
                    sys.stderr.write(
                        "[%s] found is_a ancestor %s \n" % (line_id, ancestor))
                crt_ancestor_set.add(ancestor)

            # ANCESTOR (PART OF)
            match_id = re.search(
                r'^relationship: part_of\s+([^\s]+)\s+', ontology_line)
            if (match_id):
                ancestor = match_id.group(1)
                if (self.DEBUG_LOAD_GO_SLIM):
                    sys.stderr.write(
                        "[%s] found part_of ancestor %s \n" % (line_id, ancestor))
                crt_ancestor_set.add(ancestor)

            # Get the dictionary representing the comprehensive graph
            if crt_id != None and (crt_ancestor_set != None and len(crt_ancestor_set) > 0):
                for ancestor in crt_ancestor_set:
                    if ancestor != None and ancestor:
                        if ancestor not in self.immediate_ancestor_dict:
                            self.immediate_ancestor_dict[ancestor] = [crt_id]
                        elif crt_id not in self.immediate_ancestor_dict[ancestor]:
                            self.immediate_ancestor_dict[ancestor].append(
                                crt_id)

        with open("%s.phylogenyGraphDict.pkl" % self.myArgs.outputRoot, 'wb') as f:
            pickle.dump(self.immediate_ancestor_dict,
                        f, pickle.HIGHEST_PROTOCOL)

        # TODO: Keeping this for future debugging
        # with open("%s.phylogenyGraphDict.txt" % self.myArgs.outputRoot, 'w') as f:
        #     f.write(str(self.immediate_ancestor_dict))

        slim_reader.close()

        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoSlimToGO::loadOntology STOP\n" % SimpleTime.now())

    # actually a loop would do, since we load the ontology first
    def recCountOntologyAncestors(self, ancestor_id, go_id_ancestors_working_set):
        # helper function that adds the ancestors of ancestors into the ancestor set of a particular pathway term
        if (self.DEBUG_PROGRESS):
            sys.stderr.write("[%s] InferGoSlimToGO::recCountOntologyAncestors START %s\n" % (
                SimpleTime.now(), ancestor_id))

        if (ancestor_id in go_id_ancestors_working_set):
            sys.stderr.write("Shortcircuit %s in %s\n" % (
                ancestor_id, ";".join(list(go_id_ancestors_working_set))))
        else:
            go_id_ancestors_working_set.add(ancestor_id)

            # check the old dictionary for info of the current standard pathway
            term_info = self.basic_ontology_ancestors[ancestor_id]
            # check every ancestor of the current pathway
            for great_ancestor_id in term_info.ancestor_set:
                self.recCountOntologyAncestors(
                    great_ancestor_id, go_id_ancestors_working_set)

    def applyBpPathwaysToOntology(self):
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
                for ancestor in term_info.ancestor_set:
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

        print("START WRITING Descendants")
        file1 = open("ontology_to_descendant_terms.txt", "w")
        file1.write(str(self.ontology_to_descendant_terms))
        file1.close()

    def loadGoSlims(self):
        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoSlimToGO::loadGoSlims START\n" % SimpleTime.now())

        self.go_slim_to_goid_hash = {}
        self.go_slim_to_go_msigdb_hash = {}

        self.loadOntology()
        self.applyBpPathwaysToOntology()

        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoSlimToGO::loadGoSlims  STOP\n" % SimpleTime.now())

    def outputGoSlimToGO(self):
        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoSlimToGO::outputGoSlimToGO START\n" % SimpleTime.now())

        # output multiple files
        # first msigdb pathways to all ancestors
        # then all ancestors to msigdb pathways

        # pathway to go_ids
        pathway_to_go_id_ancestors_file = "%s.pathway_to_go_id_ancestors.xls" % self.myArgs.outputRoot
        pathway_to_go_id_ancestors_file_writer = open(
            pathway_to_go_id_ancestors_file, "wt")
        pathway_to_go_id_ancestors_file_writer.write(
            "Pathway\tGO_ID\tAncestor_count\tAncestors_GO_ID\tAncestors_GO_name\n")

        for msigdb_id in self.go_msigdb_to_go_id_hash:
            go_id = self.go_msigdb_to_go_id_hash[msigdb_id]
            if not (go_id in self.ontology_to_ancestor_terms):
                sys.stderr.write("Eeek: %s -> %s skipped\n" %
                                 (msigdb_id, go_id))
                continue
            else:
                term_info = self.basic_ontology_ancestors[go_id]
                ancestor_set = self.ontology_to_ancestor_terms[go_id]
                ancestor_names_list = []
                for ancestor_id in ancestor_set:
                    term_info = self.basic_ontology_ancestors[ancestor_id]
                    ancestor_names_list.append(term_info.go_name)

                ancestor_names_list.sort()
                pathway_to_go_id_ancestors_file_writer.write("%s\t%s\t%s\t%s\t%s\n" % (msigdb_id, go_id, len(ancestor_set),
                                                                                       ";".join(list(ancestor_set)), ";".join(ancestor_names_list)))

        pathway_to_go_id_ancestors_file_writer.close()

        # ancestors to pathways
        term_classes_to_pathways = "%s.term_classes_to_pathways.xls" % self.myArgs.outputRoot
        term_classes_to_pathways_writer = open(term_classes_to_pathways, "wt")
        term_classes_to_pathways_writer.write(
            "Term_Class\tGO_ID\tDescendants_Count\tDescendants_GO_ID\tDescendants_MSigDB_GO_BP\n")

        for ancestor_id in self.ontology_to_descendant_terms:
            term_info = self.basic_ontology_ancestors[ancestor_id]
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

            term_classes_to_pathways_writer.write("%s\t%s\t%s\t%s\t%s\n" % (term_info.go_name, ancestor_id, len(descendant_set),
                                                                            ";".join(descendant_id_list), ";".join(descendant_name_list)))

        term_classes_to_pathways_writer.close()
        self.ontology_to_ancestor_terms = {}
        self.ontology_to_descendant_terms = {}

        # saving standard GOs for legit visualization
        with open("%s.standardDict.pkl" % self.myArgs.outputRoot, 'wb') as f:
            pickle.dump(self.go_id_to_go_msigdb_hash,
                        f, pickle.HIGHEST_PROTOCOL)

        if (self.DEBUG_PROGRESS):
            sys.stderr.write(
                "[%s] InferGoSlimToGO::outputGoSlimToGO STOP\n" % SimpleTime.now())

    def work(self):
        mpl.rcParams['pdf.fonttype'] = 42
        self.loadGoXML()
        self.loadGoSlims()
        self.outputGoSlimToGO()

########################################################################################
# MAIN
########################################################################################

# Process command line options
# Instantiate analyzer using the program arguments
# Analyze this !


if __name__ == '__main__':

    ###COMMAND LINE USAGE: python3 InferGoSlimToGOBP.v-1.py -g go-basic.obo -x msigdb_v7.2.xml -o something.xls###
    ###PIP LINE USAGE: from InferGoSlimToGOBP import *; g = InferGoSlimToGO(); g.work()###
    try:
        sys.stderr.write("Command line %s\n" % " ".join(sys.argv))
        myArgs = InferGoSlimToGO.processArguments()
        if (myArgs is None):
            pass
        else:
            bp = InferGoSlimToGO(myArgs)
            bp.work()
    except:
        sys.stderr.write("An unknown error occurred.\n")
        raise
