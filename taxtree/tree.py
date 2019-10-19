#!/usr/bin/env python

from .node import Node


class Tree:
    def __init__(self, root, catalog, w):
        self.root = root
        self.catalog = catalog
        self.initialWeight = w

    def search(self, taxid):
        if taxid not in self.catalog:
            return None
        return self.catalog[taxid]

    def sayGoodbye(self, node):
        # if self.catalog.get(node.taxid) is None:
        #     raise ValueError("node {} not exist in the tree".format(node.taxid))
        self.catalog.pop(node.taxid, None)
        print("node {} removed from the tree".format(node.taxid))

    def trim(self, node=None):
        if self is None or self.root is None:
            raise ValueError("the tree is empty")
        if self.root.isLeafNode():
            nd = self.root
            self.root = None
            self.catalog = {}
            return nd
        if node is None:
            p = self.root
            while len(p.childNodes) == 1:
                p = p.childNodes[0]

            id_ws = [(c.taxid, c.weight) for c in p.childNodes]
            min_nd = (sorted(id_ws, key=lambda t: t[1]))[0]
            print("node {} and its sub-nodes are to be removed ...\n".format(min_nd[0], min_nd[1]))
            nd = p.removeChildNode(self.catalog[min_nd[0]])

            nd.walk(lambda ch, d, i: self.sayGoodbye(ch))
            print("\nthe total weight is reduced by {}".format(min_nd[1]))
            print("the percentage is {0:.2f}% now\n".format((self.root.weight / self.initialWeight) * 100))
            return nd
        else:
            if self.catalog.get(node.taxid) is None:
                raise ValueError("not a child node of this tree")
            elif node.parentNode is None:
                raise ValueError("not a child node of this tree")
            else:
                if node == self.root:
                    node.walk(lambda ch, d, i: self.sayGoodbye(ch))
                    self.root = None
                    return node
                else:
                    node.walk(lambda ch, d, i: self.sayGoodbye(ch))
                    return node.parentNode.removeChildNode(node)

    def lowestCommonNode(self):
        p = self.root
        while len(p.childNodes) == 1:
            p = p.childNodes[0]

        return p

    def possibleOutlier(self):
        p = self.lowestCommonNode()
        if p.isLeafNode():
            return None

        cns = sorted(p.childNodes, key=lambda nd: nd.weight)
        return cns[0]

    def report(self, cutoff):
        score = 1
        nd = self.possibleOutlier()
        ds = nd.weight / self.initialWeight
        while score - ds >= cutoff:
            self.trim(nd)
            score = score - ds
            nd = self.possibleOutlier()
            ds = nd.weight / self.initialWeight

        res = self.lowestCommonNode()
        print("\nto meet this threshold, the lowest common node is:")
        print(res)

    def shake(self, t=0.01):
        def tidy(node, depth, idx):
            if not node.isLeafNode():
                tmp = [cn for cn in node.childNodes if cn.weight / node.weight < t]
                for cn in tmp:
                    cn.walk(lambda ch, d, i: self.sayGoodbye(ch))
                    node.removeChildNode(cn)

        self.root.walk(tidy)

    def __str__(self):
        lines = []

        def func(nd, depth, idx):
            bs = []
            p = nd
            q = p.parentNode

            while q is not None:
                if len(q.childNodes) > 1 and q.childNodes[-1] != p:
                    bs.append(True)
                else:
                    bs.append(False)
                p = q
                q = p.parentNode

            bs.append(False)
            bs = reversed(bs[1:])
            pre = "".join(["┃   " if b else "    " for b in bs])

            v = 1
            if nd.parentNode is not None and len(nd.parentNode.childNodes) > 1:
                v = len(nd.parentNode.childNodes) - 1

            if idx == 0:
                if nd.parentNode is not None and len(nd.parentNode.childNodes) > 1:
                    lines.append(pre + "┣━━━" + " {}[{}]".format(nd.taxid, nd.weight))
                else:
                    lines.append(pre + "┗━━━" + " {}[{}]".format(nd.taxid, nd.weight))
            elif idx == v:
                lines.append(pre + "┗━━━" + " {}[{}]".format(nd.taxid, nd.weight))
            else:
                lines.append(pre + "┣━━━" + " {}[{}]".format(nd.taxid, nd.weight))

        self.root.walk(func)
        return "\n".join(lines)


def createTree(arr):
    """
    Create a tree using the provided list of tuples. In the tree, a node may contains multiple
    child nodes, but it can only have one parent node.
    :param arr: list of tuples (taxid, weight, lineage), where lineage is a list of taxid
    :return: Tree instance
    """
    root = Node(0, 0)
    catalog = {}
    for bucket in arr:
        leaf = Node(bucket[0], bucket[1])
        iter = root
        for i in range(len(bucket[2])):
            lin = bucket[2][i]
            if catalog.get(lin) is None:
                node = Node(lin, 0)
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
