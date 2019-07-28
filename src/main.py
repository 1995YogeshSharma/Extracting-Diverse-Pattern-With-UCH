# @author 1995YogeshSharma
import sys
import copy

import patterns

class Node(object):
    """A node in a tree"""
    def __init__(self, id, value, children=[]):
        super(Node, self).__init__()
        self.id = id
        self.value = value
        self.children = copy.deepcopy(children)


class Tree(object):
    """Tree class to with multiple children for each node"""
    def __init__(self):
        super(Tree, self).__init__()
        self.root = None
        self.node_count = 0
        
    def insert_nodes(self, nodes):
        """
        Make sure that all given nodes are in tree, if not
        creates them.
        """

        # if root empty insert root
        if self.root == None:
            self.node_count += 1
            self.root = Node(self.node_count, nodes[0])

        # insert rest
        current = self.root
        for node in nodes[1:]:
            child_vals = [c.value for c in current.children]
            if node not in child_vals:
                self.node_count += 1
                current.children.append(Node(self.node_count, node))

            child_vals = [c.value for c in current.children]
            
            for cnum in range(0, len(current.children)):
                if current.children[cnum].value == node:
                    current = current.children[cnum]
                    break

        return

    def print_tree(self):
        """Prints tree in level order."""

        if self.root is None:
            print "Tree is not built"
            return

        print self.root.value + '\n'
        queue = [self.root]
        while len(queue) > 0:
            current = queue[0]

            has_child = 0
            for child in current.children:
                print child.value + " - ",
                queue.append(child)
                has_child = 1
            if has_child:
                print '\n'
                has_child = 0
            if len(queue) >= 1:
                queue = queue[1:]

        return


def read_input():
    if len(sys.argv) < 3:
        print "program expects name of input file and pattern file"
        sys.exit(1)

    try:
        in_filname = sys.argv[1]
        pat_filename = sys.argv[2]
        fin = open(in_filname, 'r')
        fpat = open(pat_filename, 'r')
    except:
        print "file not found"
        sys.exit(1)

    # threshold randomly decided
    freq_patterns = patterns.extract_frequent_patterns(fpat, 4)
    is_item = 1
    item = ''
    path = []
    CH = Tree()
    for line in fin.readlines():
        path = []
        if line.strip() == '':
            continue

        if is_item:
            # line is item
            item = line.strip()
            is_item = 0
        else:
            # line is path
            path = line.strip().split(' ')
            CH.insert_nodes(path)
            is_item = 1

     # CH.print_tree()
    return CH


def main():
    CH = read_input()
    CH.print_tree()

if __name__ == '__main__':
    main()
