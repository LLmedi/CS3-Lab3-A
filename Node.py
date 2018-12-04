class AVLNode:

	def __init__(self, name, embedding):
		self.name = str(name)
		self.embedding = embedding
		self.parent = None
		self.left = None
		self.right = None
		self.height = 0
	print
	def get_balance(self):
		#Get current height of right subtree, or -1 if None
		left_height = -1
		
		if self.left is not None:
			left_height = self.left.height
		
		#Get current height of right subtree, or -1 if None
		right_height = -1
		if self.right is not None:
			right_height = self.right.height
		
		#Calculates balance factor
		return left_height - right_height
		
	def update_height(self):
		# Get current height of left subtree, or -1 if None
		left_height = -1
		if self.left is not None:
			left_height = self.left.height
		# Get current height of right subtree, or -1 if None
		right_height = -1
		if self.right is not None:
			right_height = self.right.height
		# Assign self.height with calculated node height.
		self.height = max(left_height, right_height) + 1
		
	# Assign either the left or right data member with a new
	# child. The parameter which_child is expected to be the
	# string "left" or the string "right". Returns True if
	# the new child is successfully assigned to this node, False
	# otherwise.
	def set_child(self, which_child, child):
		# Ensure which_child is properly assigned.
		if which_child != "left" and which_child != "right":
			return False
		
		# Assign the left or right data member.
		if which_child == "left":
			self.left = child
		else:
			self.right = child
		
		# Assign the parent data member of the new child,
		# if the child is not None.
		if child is not None:
			child.parent = self
		
		# Update the node's height, since the subtree's structure
		# may have changed.
		self.update_height()
		return True
	
	# Replace a current child with a new child. Determines if
	# the current child is on the left or right, and calls
	# set_child() with the new node appropriately.
	# Returns True if the new child is assigned, False otherwise.
	def replace_child(self, current_child, new_child):
		if self.left is current_child:
			return self.set_child("left", new_child)
		elif self.right is current_child:
			return self.set_child("right", new_child)
		
		# If neither of the above cases applied, then the new child
		# could not be attached to this node.
		return False
		
	def print_all_in_node(self):
		if embeddings is None:
			print("No embeddings")
		for i in embeddings:
			print(i)
			
	def embeddingCount(self):
		print(len(embeddings))
	
	def get_balance(self):
		# Get current height of left subtree, or -1 if None
		left_height = -1
		if self.left is not None:
			left_height = self.left.height
		
		# Get current height of right subtree, or -1 if None
		right_height = -1
		if self.right is not None:
			right_height = self.right.height
		
		#Calculate the balance factor
		return left_height - right_height
		
	def get_embedding(self):
		return self.embedding
		
	def count(self):
		count = 1
		if self.left != None:
			count = count + self.left.count()
		if self.right != None:
			count = count + self.right.count()
		return count
		
class RBNode:
	def __init__(self, name, parent, embeddings, is_red = False, left = None, right = None):
		self.name = name
		self.left = left
		self.right = right
		self.parent = parent
		self.embeddings = embeddings
		
		if is_red:
			self.color = "red"
		else:
			self.color = "black"

	#Returns true if both child nodes are black. A child set to None is considered to be black
	def are_both_children_black(self):
		if self.left != None and self.left.is_red():
			return False
		if self.right != None and self.right.is_red():
			return False
		return True
		
	def count(self):
		count = 1
		if self.left != None:
			count = count + self.left.count()
		if self.right != None:
			count = count + self.right.count()
		return count
		
	# Returns the grandparent of this node
	def get_grandparent(self):
		if self.parent is None:
			return None
		return self.parent.parent
		
	#Gets this node's predecessor from the left child subtree
	#Precondition: This node's left child is not None
	def get_predecessor(self):
		node = self.left
		while node.right is not None:
			node = node.right
		return node
		
	#Returns this node's sibling, or None if this node does not have a sibling
	def get_sibling(self):
		if self.parent is not None:
			if self is self.parent.left:
				return self.parent.right
			return self.parent.left
		return None
		
	#Returns the uncle of this node
	def get_uncle(self):
		grandparent = self.get_grandparent()
		if grandparent is None:
			return None
		if grandparent.left is self.parent:
			return grandparent.right
		return grandparent.left
		
	#Returns True if this node is black, False otherwise
	def is_black(self):
		return self.color == "black"
		
	#Returns True if this node is red, False otherwise
	def is_red(self):
		return self.color == "red"
		
	#Replaces one of this node's children with a new child
	def replace_child(self, current_child, new_child):
		if self.left is current_child:
			return self.set_child("left", new_child)
		elif self.right is current_child:
			return self.set_child("right", new_child)
		return False
		
	#Sets either the left or right child of this node
	def set_child(self, which_child, child):
		if which_child != "left" and which_child != "right":
			return False
		if which_child == "left":
			self.left = child
		else:
			self.right = child
		if child != None:
			child.parent = self
		return True
		
	def get_embedding(self):
		return self.embeddings