# @author 1995YogeshSharma
import sys
import copy
import logging

import patterns

logging.basicConfig(level=logging.DEBUG, filename='logs.log')


class Node(object):
    """A node in a tree"""
    def __init__(self, id, value, children=[], is_dummy=False, depth=0):
        super(Node, self).__init__()
        self.id = id
        self.value = value
        self.children = copy.deepcopy(children)
        self.depth = depth
        self.is_dummy = is_dummy

    def is_leaf(self):
        return len(self.children) == 0


class Tree(object):
    """Tree class to with multiple children for each node"""
    def __init__(self):
        super(Tree, self).__init__()
        self.root = None
        self.node_count = 0
        self.height = 0
        self.nodes_at_level = {}
        self.real_edges_at_level = {}
        self.fake_edges_at_level = {}
        
    def insert_nodes(self, nodes):
        """
        Make sure that all given nodes are in tree, if not
        creates them.
        """

        # if root empty insert root
        if self.root == None:
            self.height += 1
            self.node_count += 1
            self.root = Node(self.node_count, nodes[0], depth=1)

        # insert rest
        current = self.root
        for node in nodes[1:]:
            child_vals = [c.value for c in current.children]
            if node not in child_vals:
                if self.height < current.depth+1:
                    self.height = current.depth+1
                self.node_count += 1
                current.children.append(Node(self.node_count, node, depth=(current.depth+1)))

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

                if child.is_leaf():
                    print "leaf node depth ", child.depth
            if has_child:
                print '\n'
                has_child = 0
            if len(queue) >= 1:
                queue = queue[1:]

        return

    def calculate_nodes_at_each_level(self):
        logging.debug("In calculate_nodes_at_each_level")
        for i in range(0, self.height):
            self.nodes_at_level[str(i)] = 0
            self.real_edges_at_level[str(i)] = 0
            self.fake_edges_at_level[str(i)] = 0
        if self.root is None:
            return

        self.nodes_at_level[str(self.root.depth)] = 1
        queue = [self.root]
        while len(queue) > 0:
            current = queue[0]
            if current.is_leaf():
                if len(queue) >= 1:
                    queue = queue[1:]
            logging.debug("processing for node %s", current.value)

            child_cnt = 0
            real_child_cnt = 0
            fake_child_cnt = 0
            is_leaf_level = False
            for child in current.children:
                queue.append(child)
                child_cnt += 1
                if child.is_dummy:
                    fake_child_cnt += 1
                else:
                    real_child_cnt += 1
                if child.is_leaf():
                    is_leaf_level = True
            if not is_leaf_level:
                self.nodes_at_level[str(current.depth+1)] += child_cnt
            self.real_edges_at_level[str(current.depth)] += real_child_cnt
            self.fake_edges_at_level[str(current.depth)] += fake_child_cnt

            if len(queue) >= 1:
                queue = queue[1:]
        return 

    def convert_to_balanced(self, current):

        print "Processing for node ",
        print current.value
        # check if any children of current is leaf
        for child_num in range(0, len(current.children)):
            # if leaf, extend
            if current.children[child_num].is_leaf():
                # extend
                if current.children[child_num].depth == self.height:
                    continue
                child_copy = copy.deepcopy(current.children[child_num])
                
                self.node_count += 1
                current.children[child_num] = Node(
                    self.node_count, "dummy", is_dummy=True, depth=(current.depth + 1))
                new_current = current.children[child_num]
                while new_current.depth < self.height - 1:
                    new_current.children.append(
                        Node(self.node_count, "dummy", is_dummy=True, depth=(current.depth + 1)))
                    new_current = new_current.children[0]
                child_copy.depth = new_current.depth + 1
                new_current.children.append(child_copy)
                    
            else:
                self.convert_to_balanced(current.children[child_num])

            # self.calculate_nodes_at_each_level()
        return

    def get_level_factor(self, depth):
        """Returns level factor for a given depth"""
        return (2 * (self.height - depth)) / (self.height * (self.height - 1))

    def get_merge_factor(self, depth):
        """ MF = (Num nodes at level `depth` - 1) / (Num nodes at level `depth + 1` -1)"""
        if len(self.nodes_at_level) == 0:
            self.calculate_nodes_at_each_level()

        if self.nodes_at_level[str(depth)] - 1 == 0:
            return 0
        if self.nodes_at_level[str(depth+1)] - 1 == 0:
            raise ValueError
        return (self.nodes_at_level[str(depth)] - 1) / (self.nodes_at_level[str(depth+1)] - 1)

    def get_adjustment_factor(self, depth):
        return self.real_edges_at_level[str(depth)] / (
            self.real_edges_at_level[str(depth)] + self.fake_edges_at_level[str(depth)])


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

    item_path_dict = {}
    is_item = True
    cur_item = ''
    path = []
    for line in fin.readlines():
        path = []
        if line.strip() == '':
            continue

        if is_item:
            # line is item
            item = line.strip()
            cur_item = item
            is_item = 0
        else:
            # line is path
            path = line.strip().split(' ')
            item_path_dict[cur_item] = path
            is_item = 1
    
    # threshold randomly decided
    freq_patterns = patterns.extract_frequent_patterns(fpat, 4)
    print "Frequent pattern read. "

     # CH.print_tree()
    return (item_path_dict, freq_patterns)


def main():
    (item_path_dict, freq_patterns) = read_input()

    # drank for a pattern
    dranks = []
    idx = 0
    for pattern in freq_patterns:
        logging.info("processing pattern %s", ' '.join(pattern))
        CH = Tree()
        for item in pattern:
            CH.insert_nodes(item_path_dict[item])
        logging.info("projection is created")
        CH.convert_to_balanced(CH.root)
    #     logging.info("converted to balanced CH")
    #     CH.print_tree()
    #     # calculating drank
    #     drank = 0
    #     for level in range(1, CH.height-1):
    #         logging.debug('nodes info at level ' + str(level))
    #         logging.debug(CH.nodes_at_level[str(level)])
    #         logging.debug(CH.real_edges_at_level[str(level)])
    #         logging.debug(CH.fake_edges_at_level[str(level)])
    #         level_factor = CH.get_level_factor(level)
    #         merge_factor = CH.get_merge_factor(level)
    #         adjustment_factor = CH.get_adjustment_factor(level)

    #         drank += merge_factor * adjustment_factor * level_factor
    #         logging.debug("drank till level " + str(level) + " is " + str(drank))
    #     dranks[idx] = drank
    #     idx += 1

    # # Now we have drank for evey frequent pattern.
    # for i in range(0, len(freq_patterns)):
    #     print "pattern - ",
    #     print freq_patterns[i]
    #     print "drank - "
    #     print dranks[i]
    #     print '\n'


if __name__ == '__main__':
    main()
