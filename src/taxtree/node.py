#!/usr/bin/env python
import os


class Node:
    def __init__(self, taxid, weight, name=None):
        self.taxid = taxid
        self.name = name
        self.weight = weight
        self.parentNode = None
        self.childNodes = []

    def isLeafNode(self):
        return len(self.childNodes) == 0

    def setParentNode(self, node):
        if not isinstance(node, Node):
            raise TypeError("not a node instance to set as parent node")
        node.addChildNode(self)

    def addChildNode(self, node):
        """
        Add a node to the child nodes list
        :param node: the node should be free node, which means its parentNode is None
        :return: None
        """
        if not isinstance(node, Node):
            raise TypeError("not a node instance to add as child node")
        if node.parentNode is not None:
            raise ValueError("the node has already had a parent node")
        for n in self.childNodes:
            if n.taxid == node.taxid:
                raise ValueError("node taxid conflicts")
        self.childNodes.append(node)
        node.parentNode = self
        if node.weight > 0:
            self.updateWeight(node.weight)

    def removeChildNode(self, node):
        """
        Remove a child node from the child nodes list
        :param node: the node must be a valid child node
        :return: the node removed
        """
        if not isinstance(node, Node):
            raise TypeError("not a node instance to remove")
        if node.parentNode != self:
            raise ValueError("not a child node")

        del self.childNodes[self.childNodes.index(node)]
        node.parentNode = None
        if node.weight > 0:
            self.updateWeight(-node.weight)
        return node

    def updateWeight(self, num):
        p = self
        while p is not None:
            p.weight += num
            p = p.parentNode

    def nearestAncestor(self, node):
        p = self
        while p is not None:
            q = node
            while q is not None:
                if p == q:
                    return p
                q = q.parentNode
            p = p.parentNode

        return None

    def walk(self, func, depth=0, index=0, afterCare=None):
        func(self, depth, index)
        if len(self.childNodes) > 0:
            for i in range(len(self.childNodes)):
                cn = self.childNodes[i]
                cn.walk(func, depth + 1, i)

        if afterCare is not None:
            afterCare(self, depth, index)


    def findAllLeafNodes(self):
        res = []
        stat = {"deepest": 0, "totalNodes": 0, "mostChildNodes": (self, len(self.childNodes))}

        def check(node, depth, idx):
            stat["totalNodes"] += 1
            if node.isLeafNode():
                res.append((node, depth))
                if depth > stat["deepest"]:
                    stat["deepest"] = depth
            else:
                if idx + 1 > stat["mostChildNodes"][1]:
                    stat["mostChildNodes"] = (node, len(node.childNodes))

        self.walk(check)
        return res, stat

    def _show(self):
        lines = []
        prefixes = {self.taxid: "    "}

        def worker(node, depth, idx):
            if node.taxid == self.taxid:
                lines.append("┗━━━{}[{}]".format(node.taxid, node.weight))
            else:
                prefix = prefixes.get(node.parentNode.taxid)
                length = len(node.parentNode.childNodes)
                if idx == length - 1:
                    prefixes[node.taxid] = prefix + "    "
                    lines.append("{}┗━━━{}[{}]".format(prefix, node.taxid, node.weight))
                else:
                    prefixes[node.taxid] = prefix + "┃   "
                    lines.append("{}┣━━━{}[{}]".format(prefix, node.taxid, node.weight))

        self.walk(worker)
        return "\n".join(lines)

    def show(self):
        print(self._show())

    def __str__(self):
        res = "| TaxId: {}\n".format(self.taxid)
        if self.name is not None:
            res += "| Name: {}\n".format(self.name)
        res += "| Weight: {}\n".format(self.weight)
        ps = []
        p = self
        while p is not None:
            ps.append(p.taxid)
            p = p.parentNode

        ps = [str(id) for id in ps]
        res += "| Path: /{}\n".format("/".join(reversed(ps)))
        cs = [n.name if n.name is not None else n.taxid for n in self.childNodes]
        cs = [str(id) for id in cs]
        res += "| Child Nodes: [{}]\n".format(", ".join(cs))
        ws = [n.weight for n in self.childNodes]
        ws = [str(w) for w in ws]
        res += "| Child Weights: [{}]\n".format(", ".join(ws))
        return res
