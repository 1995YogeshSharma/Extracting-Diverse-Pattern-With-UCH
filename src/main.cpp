// author - @22PoojaGaur

#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

class Node {
public:
	int id;
	string value;
	vector<Node> children;

	Node(int _id, string _value) : id(_id), value(_value) {}
};

class Tree {
public:
	Node root;
	int node_count;

	Tree() {
		root = NULL;
		node_count = 1;
	}

	void add_node(string category, vector<string> &path_till_now) {
		if (root == NULL) {
			root = Node(node_count, category);
			node_count++;
		}

	}
};

Tree read_input(ifstream &infile) {
	Tree ch = Tree();

	string item, category;
	vector <string> path_till_now;

	while (!infile.eof()){
		path_till_now.clear();

		// scanning item
		infile >> item;

		// scanning path
		infile >> category;
		while (category != item) {
			ch.add_node(category, path_till_now);
		}
		ch.add_node(item, path_till_now);
		cout << item << endl;
	}

	return ch;
}

int main(int argc, char **argv) {
	if (argc < 2) {
		cout << "Enter file name as command line argument \n";
		return 0;
	}

	string inp_filename = (string) argv[1];

	ifstream infile(inp_filename);

	Tree CH = read_input(infile);

	return 0;
}
