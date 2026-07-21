class node:
    def __init__(self,name="",cut_type=None):
        self.name=name
        self.cut_type=cut_type

        self.width=0
        self.height=0

        self.right=None
        self.left=None
        self.parent=None

class slicingfloorplan:
    def __init__(self):
        self.root=None
    
    def create(self,rectangle_name):
        self.root=node(rectangle_name)

    def search(self,node,rectangle_name):
        if node is None:
            return None

        print("checkin:",node.name,node.cut_type)
        if node.cut_type is None and node.name==rectangle_name:
            return node

        left=self.search(node.left,rectangle_name)

        if left:
            return left
        return self.search(node.right,rectangle_name)

    def horizontal_cut(self,rectangle,top_rect,bottom_rect):
        leaf=self.search(self.root,rectangle)
        if leaf is None:
            print("rectangle not found")
            return
        leaf.cut_type='H'
        leaf.name=""
        leaf.left=node(top_rect)
        leaf.right=node(bottom_rect)

        leaf.left.parent=leaf
        leaf.right.parent=leaf
    
    def vertical_cut(self,rectangle,left_rect,right_rect):
        leaf=self.search(self.root,rectangle)
        if leaf is None:
            print("rectangle not found")
            return
        
        leaf.cut_type='v'
        leaf.name=""
        leaf.left=node(left_rect)
        leaf.right=node(right_rect)

        leaf.left.parent=leaf
        leaf.right.parent=leaf


    def assign_dimensions(self,rectangle,width,height):
        leaf=self.search(self.root,rectangle)
        if leaf is None:
            print("rectangle not found")
            return
        leaf.width=width
        leaf.height=height

    def compact(self,node):
        if node is None:
            return
        if node.cut_type is None:
            return
        self.compact(node.left)
        self.compact(node.right)

        if node.cut_type=='H':
            node.width=max(node.left.width,node.right.width)
            node.height=node.left.height+node.right.height
        elif node.cut_type=='v':
            node.width=node.left.width+node.right.width
            node.height=max(node.left.height,node.right.height)

    def display(self,node,level=0):
        if node is None:
            return
        print(" "*level,end="")

        if node.cut_type is None:
            print(f"{node.name}({node.width},{node.height})")
        else:
            print(f"{node.cut_type}({node.width},{node.height})")
        self.display(node.left,level+1)
        self.display(node.right,level+1)

    def inorder(self,node):
        if node is None:
            return
        self.inorder(node.left)
        if node.cut_type:
            print(node.cut_type,end=" ")
        else:
            print(node.name,end=" ")
        self.inorder(node.right)

fp=slicingfloorplan()
fp.create("root")

fp.horizontal_cut("root","left","right")
fp.vertical_cut("left","a","x")

fp.horizontal_cut("x","b","y")
fp.vertical_cut("y","c","d")

fp.vertical_cut("right","e","f")

fp.assign_dimensions("a",4,8)
fp.assign_dimensions("b",5,3)
fp.assign_dimensions("c",4,6)
fp.assign_dimensions("d",3,5)
fp.assign_dimensions("e",2,2)
fp.assign_dimensions("f",5,2)

fp.compact(fp.root)

print("\nslicing tree\n")
fp.display(fp.root)

print("\n inorder traversal\n")
fp.inorder(fp.root)

print("overall width:",fp.root.width)
print("overall height:",fp.root.height)