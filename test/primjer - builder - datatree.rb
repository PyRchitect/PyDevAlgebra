# frozen_string_literal: true

module BuilderTech
  module Builder
    module DataTree #:nodoc:all
      class TreeNode #:nodoc:all
        include Enumerable
        include Comparable

        attr_accessor :parent, :type, :count, :link
        protected :parent=, :type=, :count=

        # attributes:
        # @parent - node from which self stems, can be only one
        # @children - array of nodes which stem from self, multiple
        # @type - node type, has to be provided + count = unique
        # @count - local (to parent) node ID, counts same type nodes
        # @link - node link to DB, optional, can be nil, non-unique

        def initialize(type, link = nil)
          @type = type
          @count = 0
          @link = link
          @children = []
          @parent = nil # effectively sets initializing node as root
        end

        # tree attributes

        def root?
          @parent.nil? # node is root if it has no parent
        end

        def root
          fetch_root = self
          fetch_root = fetch_root.parent until fetch_root.root?
          fetch_root
        end

        def root!
          self.parent = nil
        end

        # protected :root!

        def leaf?
          @children.empty?
        end

        def leaves(&_block)
          if block_given?
            each { |node| yield(node) if node.leaf? }
            self
          else
            self.select(&:leaf?)
          end
        end

        def parents
          return nil if root?

          parents_list = []
          current = @parent

          loop do
            parents_list << current
            break if current.root?

            current = current.parent
          end

          parents_list
        end

        def parents?
          !parents.nil? # if no parents it means the node is root
        end

        def parents_relative(to_parent)
          return nil if root?

          parents_list = []
          current = @parent

          loop do
            parents_list << current
            break if current.parent == to_parent # excluding

            current = current.parent
          end

          parents_list
        end

        def node_level
          parents ? parents.size : 0
        end

        def get_level(relative_level)
          tree_root = root
          level_number = node_level + relative_level
          return nil if level_number.negative?

          level_array = []

          tree_root.level_each do |el|
            next if el.first.node_level < level_number
            break if el.first.node_level > level_number

            if el.first.node_level == level_number
              el.each { |node| level_array << node }
            end
          end

          level_array
        end

        def subtree_size
          counter = 0
          each { |_el| counter += 1 }
          counter
        end

        def children?
          @children.any? # return whether the node has children
        end

        def children
          if block_given?
            @children.each { |child| yield child } # each child
          else
            @children.clone # if no block, returns instance copy!
          end
        end

        def first_child
          @children.first
        end

        def first_child?
          root? ? true : self == @parent.children.first
        end

        def last_child
          @children.last
        end

        def last_child?
          root? ? true : self == @parent.children.last
        end

        def which_child?
          root? ? 0 : @parent.children.index(self)
        end

        def only_child?
          root? ? true : parent.children.size == 1
        end

        def siblings
          return [] if root?

          if block_given?
            parent.children.each { |sibling| yield sibling if sibling != self }
          else
            sibling_array = []
            parent.children do |my_sibling|
              sibling_array << my_sibling if my_sibling != self
            end
            sibling_array
          end
        end

        def next_sibling
          return nil if root?

          return nil if last_child?

          index = parent.children.index(self)
          parent.children.at(index + 1)
        end

        def previous_sibling
          return nil if root?

          return nil if first_child?

          index = parent.children.index(self)
          parent.children.at(index - 1)
        end

        def first_sibling
          root? ? self : parent.children.first
        end

        def first_sibling?
          first_sibling == self
        end

        def last_sibling
          root? ? self : parent.children.last
        end

        def last_sibling?
          last_sibling == self
        end

        def link?
          @link.nil? # return whether the node holds link
        end

        def <=>(other)
          if other.nil? || other.class != DataTree::TreeNode ||
               @type != other.type
            return nil
          end

          @count <=> other.count
        end

        # tree operations

        def available_count
          return 0 unless @parent.children?

          existing = []

          @parent.children.each do |node|
            next unless node.type == @type

            id = node.count
            pos = existing.empty? ? 0 : existing.find_index { |el| el > id }
            pos ? existing.insert(pos, id) : existing << id
          end

          available_position = 0

          existing.each_with_index do |el, index|
            el != index ? (return index) : (available_position += 1)
          end

          available_position
        end

        def add_child(child, check_count = true)
          child.parent = self
          child.count = child.available_count if check_count
          @children << child

          nil
        end

        def retype_node(new_type)
          return nil if root?

          test_node = TreeNode.new(new_type)
          test_node.parent = @parent
          pos = test_node.available_count

          @type = new_type
          @count = pos

          test_node.root!
        end

        def remove_child!(child)
          @children.delete(child)
          child.parent = nil
        end

        def remove_from_parent!
          @parent.remove_child!(self) unless root?
        end

        def remove_children!
          @children.clear
        end

        def replace_child!(old_child, new_child)
          remove_child!(old_child)
          add_child(new_child)
        end

        def replace_node!(new_node)
          @parent.replace_child!(self, new_node)
        end

        def move(new_parent)
          return nil if root?

          remove_from_parent!
          new_parent.add_child(self)
        end

        def copy(new_parent)
          # node = self # assign self to variable to keep track?
          return nil if root? && self != new_parent

          unless root?
            node_parent = @parent # save the pointer to orig parent node for later
            remove_from_parent!
            root! # make the head of the newly split subtree the root node
          end

          current_node = self # initialize node visitor > preserves pointer to orig node
          copy_head = nil # initialize rep. root pointer (needs to exist outside block)

          orig_prev_level = {} # data reuse: arrays of saved orig levels, node_depth as key
          copy_prev_level = {} # data reuse: arrays of saved copy levels, node_depth as key

          current_node.breadth_each do |el|
            node_copy = TreeNode.new(el.type, el.link.clone) # transfer data to new node
            node_copy.count = el.count # count is same as on orig node, no need to check

            if el == self # if current node is root after split initialize rep. root
              # node_copy.type = type # new head has to be labeled correctly (consistency)
              copy_head = node_copy # copy node attributes to rep. root placeholder
              copy_head.root! # make the newly created node the root of the rep. tree
            elsif el.node_level == 1 # if current node is on the first row (root child)
              copy_head.add_child(node_copy, false) # you know parent on rep. tree, simply add
            else
              # all other rows - problem: you don't have pointer to parent on rep. tree
              orig_depth = el.node_level # see how far down you are from temp. root

              unless orig_prev_level.key?(orig_depth - 1) # collect all in prev level
                orig_prev_level[orig_depth - 1] = get_level(orig_depth - 1)
              end

              orig_parent_index =
                orig_prev_level[orig_depth - 1].index(el.parent) # how far?

              unless copy_prev_level.key?(orig_depth - 1) # as much down in rep. tree
                copy_prev_level[orig_depth - 1] =
                  copy_head.get_level(orig_depth - 1)
              end

              copy_parent = copy_prev_level[orig_depth - 1][orig_parent_index] # mirror pos.

              copy_parent.add_child(node_copy, false) # found parrent on rep. tree, add child copy
            end
          end

          orig_prev_level = copy_prev_level = {} # clear hashes immediately to free memory
          node_parent&.add_child(self, false) # add back original node head to original parent
          new_parent.add_child(copy_head) # add newly rep. subtree to specified parent, check count

          # note, speed-up: check_count disabled for all nodes except copy_head (unchanged !)
        end

        # tree traversal

        def [](node_type, node_count)
          # returns the requested node from set of children
          @children.detect do |child|
            child.type == node_type && child.count == node_count
          end
        end

        def each(&_block)
          return to_enum unless block_given?

          node_stack = [self] # start with self

          until node_stack.empty?
            current = node_stack.shift
            if current
              yield current
              node_stack = current.children.concat(node_stack)
            end
          end
        end

        def progressive_each(&_block)
          return to_enum(:progressive_each) unless block_given?

          marked_node = Struct.new(:node, :marked)
          node_stack = [marked_node.new(self, false)] # start with self

          until node_stack.empty?
            current = node_stack.first
            next unless current

            if current.node.children? && !current.marked
              current.marked = true
              marked_children =
                current.node.children.map do |node|
                  marked_node.new(node, false)
                end
              node_stack = marked_children.concat(node_stack)
            else
              yield current.node
              node_stack.shift
            end
          end
        end

        def preordered_each(&block)
          each(&block)
        end

        def postordered_each(&block)
          progressive_each(&block)
        end

        def breadth_each(&_block)
          return to_enum(:breadth_each) unless block_given?

          node_stack = [self]

          until node_stack.empty?
            current = node_stack.shift
            yield current
            current.children { |child| node_stack.push(child) }
          end
        end

        def level_each(&_block)
          if block_given?
            level = [self]

            until level.empty?
              yield level
              level = level.map(&:children).flatten
            end
          else
            each
          end
        end

        def to_s
          "#{@type}: #{@count}"
        end

        def print_tree
          each do |el|
            prefix = '> '
            prefix *= el.node_level
            puts prefix + el.type.to_s + ': ' + el.count.to_s
          end
        end
      end
    end
  end
end

# load 'C:/Users/Marin/SketchUp Extensions/src/Builder/data_tree.rb'
# TREE_NODE_CLASS = BuilderTech::Builder::DataTree::TreeNode

# tree_root = TREE_NODE_CLASS.new('type-G')

# c01 = TREE_NODE_CLASS.new('type-G')
# tree_root.add_child(c01)
# c02 = TREE_NODE_CLASS.new('type-G')
# tree_root.add_child(c02)

# c01g01 = TREE_NODE_CLASS.new('type-P')
# c01.add_child(c01g01)
# c01g02 = TREE_NODE_CLASS.new('type-P')
# c01.add_child(c01g02)
# c01g03 = TREE_NODE_CLASS.new('type-P')
# c01.add_child(c01g03)

# c02g01 = TREE_NODE_CLASS.new('type-G')
# c02.add_child(c02g01)
# c02g02 = TREE_NODE_CLASS.new('type-P')
# c02.add_child(c02g02)

# c02g02gg01 = TREE_NODE_CLASS.new('type-P')
# c02g01.add_child(c02g02gg01)
# c02g02gg02 = TREE_NODE_CLASS.new('type-P')
# c02g01.add_child(c02g02gg02)
# c02g02gg03 = TREE_NODE_CLASS.new('type-P')
# c02g01.add_child(c02g02gg03)
# c02g02gg04 = TREE_NODE_CLASS.new('type-P')
# c02g01.add_child(c02g02gg04)

# tree_root.print_tree
