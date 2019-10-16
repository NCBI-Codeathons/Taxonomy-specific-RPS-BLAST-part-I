class Node:
    def __init__(self, taxid, weight):
        self.taxid = taxid
        self.weight = weight
        self.parentNode = None
        self.childNodes = []

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
            p = self
            while p is not None:
                p.weight += node.weight

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
        for i in range(len(self.childNodes)):
            if self.childNodes[i].taxid == node.taxid:
                self.childNodes = self.childNodes[:i].extend(self.childNodes[i + 1:])
                node.parentNode = None
                if node.weight > 0:
                    p = self
                    while p is not None:
                        p.weight -= node.weight
                return node

    def mergeNewNode(self, node):
        """
        Merge a free node with the same taxid to the one that has been present in a tree
        :param node: a free node means no parent node and no child nodes
        :return: None
        """
        if not isinstance(node, Node):
            raise TypeError("not a node instance to merge")
        if self.taxid != node.taxid:
            raise ValueError("taxid not match")
        if node.parentNode is not None:
            raise ValueError("only free node can be merged")
        if len(node.childNodes) != 0:
            raise ValueError("only free node can be merged")
        if node.weight > 0:
            p = self
            while p is not None:
                p.weight += node.weight
