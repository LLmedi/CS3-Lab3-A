from Node import *

class RBTree(object):
	root = None
	
	def __init__(self):
		self.root = None
		
	def __len__(self):
		if self.root is None:
			return 0
		return self.root.count()

	def insert(self, name, embeddings):
		new_node = RBNode(name, None, embeddings, True, None, None)
		self.insert_node(new_node)
		
	def insert_node(self, node):
		if self.root is None:
			self.root = node
		else:
			curr = self.root
			#Traverse
			while curr is not None:
				#Traverse left
				if node.name < curr.name:
					if curr.left is None:
						curr.set_child("left", node)
						break
					else:
						curr = curr.left
				#Traverse right
				else:
					if curr.right is None:
						curr.set_child("right", node)
						break
					else:
						curr = curr.right
		node.color = "red"
			
		self.insertion_balance(node)
	
	def insertion_balance(self, node):
		 # If node is the tree's root, then color node black and return
		if node.parent is None:
			node.color = "black"
			return
		
		# If parent is black, then return without any alterations
		if node.parent.is_black():
			return
		
		# References to parent, grandparent, and uncle are needed for remaining operations
		parent = node.parent
		grandparent = node.get_grandparent()
		uncle = node.get_uncle()
		
		# If parent and uncle are both red, then color parent and uncle black, color grandparent
		# red, recursively balance  grandparent, then return
		if uncle is not None and uncle.is_red():
			parent.color = uncle.color = "black"
			grandparent.color = "red"
			self.insertion_balance(grandparent)
			return
			
		# If node is parent's right child and parent is grandparent's left child, then rotate left
		# at parent, update node and parent to point to parent and grandparent, respectively
		if node is parent.right and parent is grandparent.left:
			self.rotate_left(parent)
			node = parent
			parent = node.parent
		# Else if node is parent's left child and parent is grandparent's right child, then rotate
		# right at parent, update node and parent to point to parent and grandparent, respectively
		elif node is parent.left and parent is grandparent.right:
			self.rotate_right(parent)
			node = parent
			parent = node.parent
			
		#Color parent black and grandparent red
		parent.color = "black"
		grandparent.color = "red"
		
		#If node is parent's left child, then rotate right at grandparent, otherwise rotate left
		#at grandparent
		if node is parent.left:
			self.rotate_right(grandparent)
		else:
			self.rotate_left(grandparent)
		
	def rotate_left(self, node):
		right_left_child = node.right.left
		if node.parent != None:
			node.parent.replace_child(node, node.right)
		else:#Node is root
			self.root = node.right
			self.root.parent = None
		node.right.set_child("left", node)
		node.set_child("right", right_left_child)
		
	def rotate_right(self, node):
		left_right_child = node.left.right
		if node.parent != None:
			node.parent.replace_child (node, node.left)
		else:
			self.root = node.left
			self.root.parent = None
		node.left.set_child("right", node)
		node.set_child("left", left_right_child)
		
	def _bst_remove(self, name):
		node = self.search(name)
		self._bst_remove_node(node)
	
	def _bst_remove_node(self, node):
		if node is None:
			return
		
		#Case 1: Internal node with 2 children
		if node.left is not None and node.right is not None:
			#Find successor
			successor_node = node.right
			while successor_node.left is not None:
				successor_node = successor_node.left
			
			#Copy successor's name
			successor_name = successor_node.name
			
			#Recursively remove successor
			self._bst_remove_node(successor_node)
			
			#Set node's name to copied successor name
			node.name = successor_name
			
		#Case 2: Root node (with 1 or 0 children)
		elif node is self.root:
			if node.left is not None:
				self.root = node.left
			else:
				self.root = node.right
			
			#Make sure the new root, if not None, has parent set to None
			if self.root is not None:
				self.root.parent = None
		
		#Case 3: Internal with left child only
		elif node.left is not None:
			node.parent.replace_child(node, node.left)
		
		#Case 4: Internal with right child OR leaf
		else:
			node.parent.replace_child(node, node.right)
			
	def is_not_none_and_red(self, node):
		if node is None:
			return False
		return node.is_red()
		
	def prepare_for_removal(self, node):
		if self.try_casel(node):
			return
			
		sibling = node.get_sibling()
		if self.try_case2(node, sibling):
			sibling = node.get_sibling()
		if self.try_case3(node, sibling):
			return
		if self.try_case4(node, sibling):
			return
		if self.try_case5(node, sibling):
			sibling = node.get_sibling()
		if self.try_case6(node, sibling):
			sibling = node.get_sibling()
			
		sibling.color = node.parent.color
		node.parent.color = "black"
		if node is node.parent.left:
			sibling.right.color = "black"
			self.rotate_left(node.parent)
		else:
			sibling.left.color = "black"
			self.rotate_right(node.parent)
			
	def remove(self, name):
		node = self.search(name)
		if node is not None:
			self.remove_node(node)
			return True
		return False
		
	def remove_node(self, node):
		if node.left is not None and node.right is not None:
			predecessor_node = node.get_predecessor()
			predecessor_name = predecessor_node.name
			self.remove_node(predecessor_node)
			node.name = predecessor_name
			return
		
		if node.is_black():
			self.prepare_for_removal(node)
		self._bst_remove(node.name)
		
		#One special case if the root was changed to red
		if self.root is not None and self.root.is_red():
			self.root.color = "black"
			
	def search(self, name):
		current_node = self.root
		while current_node is not None:
			#Return the node if the name matches.
			if current_node.name == name:
				return current_node
			
			#Navigate to the left is the search name is less than the node's key
			elif name < current_node.name:
				current_node = current_node.left
			
			#Navigate to the right if search name is larger
			else:
				current_node = current_node.right
				
		#The key was not found 
		return None
		
	def try_case1(self, node):
		if node.is_red() or node.parent is None:
			return True
		return False #node case 1
		
	def try_case2(self, node, sibling):
		if sibling.is_red():
			node.parent.color = "red"
			sibling.color = "black"
			if node is node.parent.left:
				self.rotate_left(node.parent)
			else:
				self.rotate_right(node.parent)
			return True
		return False #not case 2
		
	def try_case3(self, node, sibling):
		if node.parent.is_black() and sibling.are_both_children_black():
			sibling.color = "red"
			self.prepare_for_removal(node.parent)
			return True
		return False # not case 3
		
	def try_case4(self, node, sibling):
		if node.parent.is_red() and sibling.are_both_children_black():
			node.parent.color = "black"
			sibling.color = "red"
			return True
		return False # not case 4
		
	def try_case5(self, node, sibling):
		if self.is_not_none_and_red(sibling.left):
			if self.is_none_or_black(sibling.right):
				if node is node.parent.left:
					seibling.color = "red"
					sibling.left.color = "black"
					self.rotate_right(sibling)
					return True
		return False # not case 5
		
	def try_case6(self, node, sibling):
		if self.is_none_or_black(sibling.left):
			if self.is_not_none_and_red(sibling.right):
				if node is node.parent.right:
					sibling.color = "red"
					sibling.right.color = "black"
					self.rotate_left(sibling)
					return True
		return False # not case 6
		
	def print_nodes_to(self, n):
		curr = self.root
		if n == curr.name:
			print(curr.name)
			return
		while curr.name != n and curr is not None:
			print(curr.name)
			if n < curr.name:
				curr = curr.left
			else:
				curr = curr.right
	def print_root(self):
		print(self.root.name)
		
	#Returns the height of passed node
	def height(self, node):

		if node is None:
			return -1
		else:
			left_depth = self.height(node.left)
			right_depth = self.height(node.right)
			
			return 1 + max(left_depth, right_depth)
			
	#Returns the number of nodes in the tree
	def node_count(self):
		return len(self)
	
	def print_all(self, node = None):
		
		if node is None:
			node = self.root
			
		print(node.name)
		
		if node.left is not None:
			self.print_all(node.left)
		if node.right is not None:
			self.print_all(node.right)
			
	#Returns ordered list of nodes
	def return_in_order(self, node = None, list = []):
		if node is None:
			node = self.root
		if node.left is not None:
			self.return_in_order(node.left, list)
		
		list.append(node.name)
		
		if node.right is not None:
			self.return_in_order(node.right, list)
		return list

	def nodes_in_depth(self, d, node = None, list = []):
		if node is None:
			node = self.root
		if d == 0:
			list.append(node.name)
		else:
			if node.left is not None:
				self.nodes_in_depth(d-1, node.left, list)
			if node.right is not None:
				self.nodes_in_depth(d-1, node.right, list)
		return list
		
class AVLTree:
	
	# Constructor to create an empty AVLTree. There is only
	# one data member, the tree's root Node, and it starts
	# out as None.
	def __init__(self):
		self.root = None
	
	def __len__(self):
		if self.root is None:
			return 0
		return self.root.count()
	
	# Performs a left rotation at the given node. Returns the
	# new root of the subtree.
	def rotate_left(self, node):
		# Define a convenience pointer to the right child of the 
		# left child.
		right_left_child = node.right.left
		
		# Step 1 - the right child moves up to the node's position.
		# This detaches node from the tree, but it will be reattached
		# later.
		if node.parent is not None:
			node.parent.replace_child(node, node.right)
		else: #node is root
			self.root = node.right
			self.root.parent = None
			
		# Step 2 - the node becomes the left child of what used
		# to be its right child, but is now its parent. This will
		# detach right_left_child from the tree.
		node.right.set_child("left", node)
		
		# Step 3 - reattach right_left_child as the right child of node.
		node.set_child("right", right_left_child)
		return node.parent
	
	# Performs a right rotation at the given node. Returns the
	# subtree's new root.
	def rotate_right(self, node):
		# Define a convenience pointer to the left child of the 
		# right child.
		left_right_child = node.left.right
		
		# Step 1 - the left child moves up to the node's position.
		# This detaches node from the tree, but it will be reattached
		# later.
		if node.parent is not None:
			node.parent.replace_child(node, node.left)
		else: # node is root
			self.root = node.left
			self.root.parent = None
		# Step 2 - the node becomes the right child of what used
		# to be its left child, but is now its parent. This will
		# detach left_right_child from the tree.
		node.left.set_child("right", node)
		
		# Step 3 - reattach left_right_child as the left child of node.
		node.set_child("left", left_right_child)
		
		return node.parent
	# Updates the given node's height and rebalances the subtree if
	# the balancing factor is now -2 or +2. Rebalancing is done by
	# performing a rotation. Returns the subtree's new root if
	# a rotation occurred, or the node if no rebalancing was required.
	def rebalance(self, node):
		# First update the height of this node.
		node.update_height()
		
		# Check for an imbalance.
		if node.get_balance() == -2:
		
			# The subtree is too big to the right.
			if node.right.get_balance()== 1:
				#Double rotation case
				self.rotate_right(node.right)
				
			 # A left rotation will now make the subtree balanced.
			return self.rotate_left(node)
		
		elif node.get_balance() == 2:
			
			# The subtree is too big to the left
			if node.left.get_balance() == -1:
				#Double rotation case
				self.rotate_left(node.left)
				
			# A right rotation will now make the subtree balanced.
			return self.rotate_right(node)
		# No imbalance, so just return the original node.
		return node

	def insert(self, node):
		#if tree is empty, new node = root
		if self.root is None:
			self.root = node
			node.parent = None

		else:
			# Step 1 - do a regular binary search tree insert.
			current_node = self.root
			while current_node is not None:
				# Choose to go left or right
				if node.name < current_node.name:
				# Go left. If left child is None, insert the new
				# node here.
					if current_node.left is None:
						current_node.left = node
						node.parent = current_node
						current_node = None
					else:
						# Go left and do the loop again.
						current_node = current_node.left
				else:
					# Go right. If the right child is None, insert the
					# new node here.
					if current_node.right is None:
						current_node.right = node
						node.parent = current_node
						current_node = None
					else:
						# Go right and do the loop again.
						current_node = current_node.right
			# Step 2 - Rebalance along a path from the new node's parent up
			# to the root.
			node = node.parent
			while node is not None:
				self.rebalance(node)
				node = node.parent

	def remove_node(self, node):
		#Base case:
		if node is None:
			return False
		
		#Parent needed for rebalancing.
		parent = node.parent
		
		#Case 1: Internal node with 2 children
		if node.left is not None and node.right is not None:
			#Find successor
			successor_node = node.right
			while successor_node.left != None:
				successor_node = successor_node.left
			
			#Copy the value from the node
			node.name = successor_node.name
			
			#Recursibely remove successor
			self.remove_node(successor_node)
			
			#Nothing left to do since the recursive call will have rebalance
			return True
		
		#Case 2: Root node (with 1 or 0 children)
		elif node is self.root:
			if node.left is not None:
				self.root = node.left
			else:
				self.root = node.right
			if self.root is not None:
				self.root.parent = None
			return True
		
		# Case 3: Internal with left child only
		elif node.left is not None:
			parent.replace_child(node, node.left)
			
		# Case 4: Internal with right child only OR leaf
		else:
			parent.replace_child(node, node.right)
			
		# node is gone. Anything that was below node that has persisted is already correctly
		# balanced, but ancestors of node may need rebalancing.
		node = parent
		while node is not None:
			self.rebalance(node)
			node = node.parent
		return True
		
	# Searches for a node with a matching key. Does a regular
	# binary search tree search operation. Returns the node with the
	# matching key if it exists in the tree, or None if there is no
	# matching key in the tree.
	def search(self, name):
		current_node = self.root
		while current_node is not None:
			# Compare the current node's key with the target key.
			# If it is a match, return the current key; otherwise go
			# either to the left or right, depending on whether the 
			# current node's key is smaller or larger than the target key.
			if current_node.name == name: return current_node
			elif current_node.name < name: current_node = current_node.right
			else: current_node = current_node.left
			
	# Attempts to remove a node with a matching key. If no node has a matching key
	# then nothing is done and False is returned; otherwise the node is removed and
	# True is returned.
	def remove_key(self, name):
		node = self.search(name)
		if node is None:
			return False
		else:
			return self.remove_node(node)
			
	#Returns the height of passed node
	def height(self, node):
		if node is None:
			return -1
		else:
			left_depth = self.height(node.left)
			right_depth = self.height(node.right)
			
			return 1 + max(left_depth, right_depth)
	
	#Returns the number of nodes in the tree
	def node_count(self):
		return len(self)
		
	#Returns ordered list of nodes
	def return_in_order(self, node = None, list = []):
		if node is None:
			node = self.root
		if node.left is not None:
			self.return_in_order(node.left, list)
		
		list.append(node.name)
		
		if node.right is not None:
			self.return_in_order(node.right, list)
		return list
		
	def nodes_in_depth(self, d, node = None, list = []):
		if node is None:
			node = self.root
		if d == 0:
			list.append(node.name)
		else:
			if node.left is not None:
				self.nodes_in_depth(d-1, node.left, list)
			if node.right is not None:
				self.nodes_in_depth(d-1, node.right, list)
		return list