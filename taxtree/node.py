#!/usr/bin/env python

class Node:
    def __init__(self, taxid, weight):
        self.taxid = taxid
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

    def walk(self, func, depth=0, index=0):
        if self.isLeafNode():
            func(self, depth, index)
            return
        else:
            func(self, depth, index)
            for i in range(len(self.childNodes)):
                cn = self.childNodes[i]
                cn.walk(func, depth + 1, i)

    def __str__(self):
        res = "| TaxId: {}\n".format(self.taxid)
        res += "| Weight: {}\n".format(self.weight)
        ps = []
        p = self
        while p is not None:
            ps.append(p.taxid)
            p = p.parentNode

        ps = [str(id) for id in ps]
        res += "| Path: /{}\n".format("/".join(reversed(ps)))
        cs = ["{}TaxId: {}, Weight: {}{}".format("{", n.taxid, n.weight, "}") for n in self.childNodes]
        res += "| Child Nodes: [{}]\n".format(", ".join(cs))
        return res
