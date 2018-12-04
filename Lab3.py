from Node import *
from Trees import *
import math

def main():
	tree = file_to_tree_("glove.6B.50d.txt")
	
	#Word similarities
	print("Word similarities:")
	with open("test_pairs.txt", encoding = "utf8") as f:
		for line in f:
			current_line = line.split()
			
			#Serach for words in file
			word0 = tree.search(current_line[0])
			word1 = tree.search(current_line[1])

			if word0 is None:
				print(word0, "0 not found.")
				continue
			if word1 is None:
				print(word1, "1 not found.")
				continue
			s = similarity(word0, word1)
			print(word0.name, word1.name, s)
	#Prints the number of nodes
	print("Node count:", tree.node_count())
	
	#Prints the height of the tree
	print("Tree height", tree.height(tree.root))
	
	#Writes words to file in order
	ordered_words = tree.return_in_order()
	write_to_file(ordered_words, "ordered_words.txt")
	
	#Writes nodes of depth d to file
	print("Wrote nodes of depth d to file.")
	node_list = sorted(tree.nodes_in_depth(1))
	write_to_file(node_list, "nodes_in_depth.txt")

#Creates a tree from a formatted file
def file_to_tree_(doc):	
	#Prompts user input
	treeChoice = user_input()
	
	#Choice = Red Black
	if treeChoice == 1:
		#Create tree
		tree = RBTree()
		#Read file
		with open(doc, encoding = "utf8") as f:
			for line in f:
				current_line = line.split()
				embedding = [float(i) for i in current_line[1:]]
				#Ignore commas and periods
				if current_line[0][0] >= "A" and current_line[0][0] <= "Z" or current_line[0][0] >= "a" and current_line[0][0] <= "z":
					tree.insert(current_line[0], embedding)

	#Choice = AVL
	elif treeChoice == 2:
		#Create tree
		tree = AVLTree()
		#Read file
		with open(doc, encoding = "utf8") as f:
			for line in f:
				current_line = line.split()
				embedding = [float(i) for i in current_line[1:]]
				
				#Ignore commas and periods
				if current_line[0][0] >= "A" and current_line[0][0] <= "Z" or current_line[0][0] >= "a" and current_line[0][0] <= "z":
					new_node = AVLNode(current_line[0], embedding)
					tree.insert(new_node)
	return tree	

#Reads user input
def user_input():
	
	validChoice = False
	while not validChoice:
		treeChoice = input("Please select a BST type to use by entering a number: \n1) Red-Black Tree\n2)AVL Tree\n")
		if treeChoice == "1":
			return int(1)
		if treeChoice == "2":
			return int(2)
			
#Finds the similarity of two words
def similarity(word0, word1):
	
	#get embeddings
	e0 = word0.get_embedding()
	e1 = word1.get_embedding()
	product = 0
	magnitude = 0
	
	#Finds dot product and magnitude
	for (i, item) in enumerate(e0):
		product += e0[i] * e1[i]
		magnitude += math.sqrt(pow(e0[i], 2) + pow(e1[i], 2))
	
	return product/magnitude
	
def write_to_file(list, name):
	with open(name, 'w', encoding = "utf8") as new_file:
		for word in list:
			new_file.write(word + "\n")
	new_file.close()
main()