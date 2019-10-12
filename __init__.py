
from queue import LinkedQueue

#树基类
class Tree:

  class Position:
    def element(self):
      raise NotImplementedError('must be implemented by subclass')

    def __eq__(self, other):
      raise NotImplementedError('must be implemented by subclass')
    
    def __ne__(self, other):
      return not (self == other)

  def root(self):
    raise NotImplementedError('must be implemented by subclass')

  def parent(self, pos):
    raise NotImplementedError('must be implemented by subclass')

  def num_children (self, pos):
    raise NotImplementedError('must be implemented by subclass')
  
  def __len__(self):
    raise NotImplementedError('must be implemented by subclass')
  
  def __iter__(self):
    return self.positions()

  def is_root(self, pos):
    return self.root() == pos

  def is_leaf(self, pos):
    return self.num_children(pos) == 0

  def is_empty(self):
    return len(self) == 0

  def depth(self, pos):
    if self.is_root(pos):
      return 0
    return 1 + self.depth(self.parent(pos))
  
  def _height(self, pos):
    if (self.is_leaf(pos)):
      return 0
    return 1 + max(self._height(child) for child in self.children(pos))
  
  def height(self, pos = None):
    pos = pos or self.root()
    return self._height(pos)

  def _subtree_preorder(self, pos):
    yield pos
    for child in self.children(pos):
      for other in self._subtree_preorder(child):
        yield other
  
  def preorder(self):
    if self.is_empty():
      return
    for pos in self._subtree_preorder(self.root()):
      yield pos

  def _subtree_postorder(self, pos):
    for child in self.children(pos):
      for other in self._subtree_postorder(child):
        yield other
    yield pos

  def postorder(self):
    if not self.is_empty():
      for pos in self._subtree_postorder(self.root()):
        yield pos

  def positions(self):
    return self.preorder()
  
  def breadthfirst(self):
    if self.is_empty():
      return
    queue = LinkedQueue()
    queue.enqueue(self.root())
    while not queue.is_empty():
      pos = queue.dequeue
      yield pos
      for child in this.children(pos):
        queue.enqueue(child)
# 二叉树
class BinaryTree(Tree):

  def left(self, pos):
    raise NotImplementedError('must be implemented by subclass')
  
  def right(self, pos):
    raise NotImplementedError('must be implemented by subclass')
  
  def sibling (self, pos):
    parent = self.parent(pos)
    if not parent:
      return None
    left = self.left(parent)
    return self.right(pos) if pos == left else left

  def children (self, pos):
    left = self.left(pos)
    right = self.right(pos)
    if left:
      yield left
    if right:
      yield right
  
  def inorder(self):
    pass
  
#链式二叉树
class LinkedBinaryTree(BinaryTree):

  class _Node:
    __slots__ = '_element', '_parent', '_left', '_right'

    def __init__(self, element, parent = None, left = None, right = None):
      self._element = element
      self._parent = parent
      self._left = left
      self._right = right
    
  class Position(BinaryTree.Position):

    def __init__(self, container, node):
      self._container = container
      self._node = node
    
    def element(self):
      return self._node._element
    
    def __eq__(self, other):
      return type(self)  is type(other) and other._node is self._node
    
  def _validate(self, pos):
    if not isinstance(pos, self.Position):
      raise TypeError('pos must be proper Position type')
    if pos._container is not self:
      raise ValueError('pos does not belong to this container')
    if pos._node._parent is pos._node:
      raise ValueError('pos is no longer valid')
    return pos._node
  
  def _make_position(self, node):
    return self.Position(self, node) if node is not None else None

  def _add_root(self, element):
    if self._root:
      raise ValueError('Root exists')
    self._size = 1
    self._root = self._Node(element)
    return self._make_position(self._root)
  
  def _add_left(self, pos, element):
    node = self._validate(pos)
    if node._left:
      raise ValueError('Left child exists')
    self._size += 1
    node._left = self._Node(element, node)
    return self._make_position(node._left)
  
  def _add_right(self, pos, element):
    node = self._validate(pos)
    if node._right:
      raise ValueError('Left child exists')
    self._size += 1
    node._right = self._Node(element, node)
    return self._make_position(node._right)

  def _replace(self, pos, element):
    node = self._validate(pos)
    old = node._element
    node._element =element
    return old
  
  def _delete(self, pos):
    node = self._validate(pos)
    if self.num_children(pos) == 2:
      raise ValueError('pos has two children')
    child = node._left if node._left else node._right
    if child:
      child._parent = node._parent
    if node is self._root:
      self._root = child
    else:
      parent = node._parent
      if node is parent._left:
        parent._left = child
      else:
        parent._right = child
    self._size -= 1
    node._parent = node
    return node._element

  def _attach(self, pos, left_tree, right_tree):
    node = self._validate(pos)
    if not self.is_leaf(pos):
      raise ValueError('pos must be leaf')
    if not type(self) is type(left_tree) is type(right_tree):
      raise TypeError('Tree type must match')
    self._size += len(left_tree) + len(right_tree)
    if not left_tree.is_empty():
      left_tree._root._parent = node
      node._left = left_tree._root
      left_tree._root = None
      left_tree._size = 0
    if not right_tree.is_empty():
      right_tree._root._parent = node
      node._right = right_tree._root
      right_tree._root = None
      right_tree._size = 0

  def __init__(self):
    self._root = None
    self._size = 0
  
  def __len__(self):
    return self._size
  
  def root(self):
    return self._make_position(self._root)

  def parent(self, pos):
    node = self._validate(pos)
    return self._make_position(node._parent)
  
  def left(self, pos):
    node = self._validate(pos)
    return self._make_position(node._left)

  def right(self, pos):
    node = self._validate(pos)
    return self._make_position(node._right)
  
  def num_children(self, pos):
    node = self._validate(pos)
    count = 0
    if node._left:
      count += 1
    if node._right:
      count += 1
    return count

def test():
  tree = LinkedBinaryTree()
  root = tree._add_root(1)
  tree._add_left(root, 2)
  tree._add_right(root, 3)
  for pos in tree:
    print(pos.element())

test()