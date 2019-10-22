#!/usr/bin/env python

from .node import Node
import logging

from Bio import Entrez
from taxadb.taxid import TaxID
import os

class Tree:
    def __init__(self, root, catalog, w):
        self._root = root
        self._catalog = catalog
        self.initialWeight = w

    def search(self, taxid):
        if taxid not in self._catalog:
            return None
        return self._catalog[taxid]

    def describe(self):
        all = self._root.findAllLeafNodes()
        line1 = "total number of nodes: {}".format(all[1]["totalNodes"])
        line2 = "total weight initially: {}".format(self.initialWeight)
        line3 = "total weight for now: {}".format(self._root.weight)
        line4 = "total number of leaf nodes: {}".format(len(all[0]))
        line5 = "the deepest node is of depth: {}".format(all[1]["deepest"])
        n = max([len(line) for line in [line1, line2, line3, line4, line5]])
        print("-" * (n + 4))
        print(line1)
        print(line2)
        print(line3)
        print(line4)
        print(line5)
        print("-" * (n + 4))

    def getWeight(self):
        return self._root.weight

    def getRoot(self):
        return self._root

    def getNode(self, taxid):
        if taxid not in self._catalog:
            return None
        return self._catalog[taxid]

    def sayGoodbye(self, node):
        # if self._catalog.get(node.taxid) is None:
        #     raise ValueError("node {} not exist in the tree".format(node.taxid))
        self._catalog.pop(node.taxid, None)
        logging.debug("node {} removed from the tree".format(node.taxid))

    def trim(self, node=None):
        if self is None or self._root is None:
            raise ValueError("the tree is empty")
        if self._root.isLeafNode():
            nd = self._root
            self._root = None
            self._catalog = {}
            return nd
        if node is None:
            p = self._root
            while len(p.childNodes) == 1:
                p = p.childNodes[0]

            id_ws = [(c.taxid, c.weight) for c in p.childNodes]
            min_nd = (sorted(id_ws, key=lambda t: t[1]))[0]
            print("node {} and its sub-nodes are to be removed ...\n".format(min_nd[0], min_nd[1]))
            nd = p.removeChildNode(self._catalog[min_nd[0]])

            nd.walk(lambda ch, d, i: self.sayGoodbye(ch))
            print("\nthe total weight is reduced by {}".format(min_nd[1]))
            print("the percentage is {0:.2f}% now\n".format((self._root.weight / self.initialWeight) * 100))
            return nd
        else:
            if self._catalog.get(node.taxid) is None:
                raise ValueError("not a child node of this tree")
            elif node.parentNode is None:
                raise ValueError("not a child node of this tree")
            else:
                if node == self._root:
                    node.walk(lambda ch, d, i: self.sayGoodbye(ch))
                    self._root = None
                    return node
                else:
                    node.walk(lambda ch, d, i: self.sayGoodbye(ch))
                    return node.parentNode.removeChildNode(node)

    def lowestCommonNode(self):
        p = self._root
        while len(p.childNodes) == 1:
            p = p.childNodes[0]

        return p

    def potentialOutlier(self):
        p = self.lowestCommonNode()
        if p.isLeafNode():
            return None

        cns = sorted(p.childNodes, key=lambda nd: nd.weight)
        return cns[0]

    def report(self, cutoff):
        score = 1
        nd = self.potentialOutlier()
        ds = nd.weight / self.initialWeight
        while score - ds >= cutoff:
            self.trim(nd)
            score = score - ds
            nd = self.potentialOutlier()
            ds = nd.weight / self.initialWeight

        res = self.lowestCommonNode()
        print("\nto meet the threshold {0:.2f}%, the lowest common node is:".format(cutoff * 100))
        print(res)
        print("the current percentage is {0:.2f}%".format(self._root.weight / self.initialWeight * 100))

    def shake(self, t=0.01):
        def tidy(node, depth, idx):
            if not node.isLeafNode():
                tmp = [cn for cn in node.childNodes if cn.weight / node.weight < t]
                for cn in tmp:
                    cn.walk(lambda ch, d, i: self.sayGoodbye(ch))
                    node.removeChildNode(cn)

        self._root.walk(tidy)

    def nearestAncestor(self, node1, node2):
        return node1.nearestAncestor(node2)

    def __str__(self):
        # lines = []
        #
        # def func(nd, depth, idx):
        #     bs = []
        #     p, q = nd, nd.parentNode
        #
        #     while q is not None: # len(q.childNodes) always >= 1
        #         bs.append(q.childNodes[-1] != p)
        #         p, q = q, q.parentNode
        #
        #     bs.append(False)
        #     bs = reversed(bs[1:])
        #     pre = "".join(["┃   " if b else "    " for b in bs])
        #
        #     if nd.parentNode is None or idx == len(nd.parentNode.childNodes) - 1:
        #         lines.append(pre + "┗━━━" + " {}[{}]".format(nd.taxid, nd.weight))
        #     else:
        #         lines.append(pre + "┣━━━" + " {}[{}]".format(nd.taxid, nd.weight))
        #
        # self._root.walk(func)
        # return "\n".join(lines)
        return self._root._show()


def _get_name_for_taxid(target_taxid, taxadb):
    """
    Returns the name for a given taxonomy ID
    """
    retval = None
    if target_taxid == 0:
        return "root"

    if "GET_NAMES_FROM_ENTREZ" in os.environ: # pardon the hack!
        handle = Entrez.efetch(db="Taxonomy", id=str(target_taxid), retmode="xml")
        records = Entrez.read(handle)
        if len(records) == 1:
            retval = records[0]["ScientificName"]
    else:
        retval = taxadb.sci_name(target_taxid)

    return retval

def createTree(arr):
    """
    Create a tree using the provided list of tuples. In the tree, a node may contains multiple
    child nodes, but it can only have one parent node.
    :param arr: list of tuples (taxid, weight, lineage), where lineage is a list of taxid
    :return: Tree instance
    """
    taxadb = TaxID()
    if "GET_NAMES_FROM_ENTREZ" in os.environ: # pardon the hack!
        import getpass
        Entrez.email = "{}@ncbi.nlm.nih.gov".format(getpass.getuser())

    root = Node(0, 0, _get_name_for_taxid(0, taxadb))
    catalog = {}
    for bucket in arr:
        taxid = int(bucket[0])
        name = _get_name_for_taxid(taxid, taxadb)

        leaf = Node(taxid, bucket[1], name)
        iter = root
        for i in range(len(bucket[2])):
            lin = bucket[2][i]
            if catalog.get(lin) is None:
                node = Node(lin, 0, _get_name_for_taxid(lin, taxadb))
                iter.addChildNode(node)
                catalog[lin] = node
                iter = node
            else:
                # below we check the compatibility of the data
                # each node can only have one parent node
                eid = catalog[lin].parentNode.taxid
                if i == 0:
                    if eid != root.taxid:
                        m = "node #{} got two parent nodes #{} and #{}".format(lin, eid, root.taxid)
                        raise ValueError(m)
                else:
                    if eid != bucket[2][i - 1]:
                        m = "node #{} got two parent nodes #{} and #{}".format(lin, eid, bucket[2][i - 1])
                        raise ValueError(m)

                iter = catalog[lin]

        if catalog.get(leaf.taxid) is None:
            iter.addChildNode(leaf)
            catalog[leaf.taxid] = leaf
        else:
            eid = catalog[bucket[0]].parentNode.taxid
            if eid != bucket[2][-1]:
                m = "node #{} got two parent nodes #{} and #{}".format(lin, eid, bucket[2][-1])
                raise ValueError(m)
            iter = catalog[bucket[0]]
            iter.updateWeight(leaf.weight)

    return Tree(root, catalog, root.weight)
