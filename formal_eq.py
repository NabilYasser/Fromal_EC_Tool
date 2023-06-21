import graphviz
class BDDNode:
    def __init__(self, Low , High ,Name , Expression):
        self.__low  = Low
        self.__high = High
        self.__name  = Name
        self.__expression = Expression 
    
    def GetLow(self):
        return self.__low
    
    def GetHigh(self):
        return self.__high

    def GetExpression(self):
        return self.__expression
    
    def GetName(self):
        return self.__name
    
    def SetLow(self,LowChild):
        self.__low = LowChild
    
    def SetHigh(self,HighChild):
        self.__high = HighChild
    
    def SetValue(self,Name):
        self.__name = Name    
        
    def SetExpression(self,Expression):
        self.__expression = Expression        
    
    def __repr__(self):
        return f"BDD Node ( Name {self.GetName()} \n, Low Child {self.GetLow()} \n , High Child {self.GetHigh()} \n, Expression {self.GetExpression()} \n)"
       
    @staticmethod
    def ConstructBDD(ParseTree,Order):
        index=0
        
        start=BDDNode(None, None, Order[index], ParseTree)
        Dic=CreateDic(Order,index)
        start ,index=BDDNode.BDD(start,ParseTree,Order,index,Dic)
        return start , index
        
    @staticmethod
    def BDD(Node,ParseTree,Order,index,Data):
        
        Data_re=Data.copy()       
        Data_re.update({Order[index]: 0})
        #print(Data)
        #print(Data_re)
        #print(ParseTree.evaluate(Data))
        if ParseTree.evaluate(Data_re) == 1:
            Node.SetLow(BDDNodeOne)
            #print(f"@ {Order[index]} == 0 ,{ParseTree.evaluate(Data_re)} ")
        elif ParseTree.evaluate(Data_re) == 0:
            Node.SetLow(BDDNodeZero)
            #print(f"@ {Order[index]} == 0 ,{ParseTree.evaluate(Data_re)} ")
        else :
            #print(f"@ {Order[index]} == 0 ,{ParseTree.evaluate(Data_re)} ")
            LowNode=BDDNode(None,None,Order[index+1],ParseTree.evaluate(Data_re))
            Node.SetLow(LowNode)
            BDDNode.BDD(LowNode,ParseTree.evaluate(Data_re),Order,index+1,Data)
            
        Data_re=Data.copy() 
        Data_re.update({Order[index]: 1})
        #print(Data)
        #print(Data_re)
        #print(index)
        #print(ParseTree.evaluate(Data))
        if ParseTree.evaluate(Data_re) == 1:
            Node.SetHigh(BDDNodeOne)
            #print(f"@ {Order[index]} == 1 ,{ParseTree.evaluate(Data_re)} ")
        elif ParseTree.evaluate(Data_re) == 0:
            Node.SetHigh(BDDNodeZero)
            #print(f"@ {Order[index]} == 1 ,{ParseTree.evaluate(Data_re)} ")
        else :
            #print(f"@ {Order[index]} == 1 ,{ParseTree.evaluate(Data_re)} ")
            HighNode=BDDNode(None,None,Order[index+1],ParseTree.evaluate(Data_re))
            Node.SetHigh(HighNode)
            BDDNode.BDD(HighNode,ParseTree.evaluate(Data_re),Order,index+1,Data)
            
        return Node  ,index  
    
    @staticmethod
    def BDDRed(start):
        if (start != None):
            if  (start.GetLow().GetLow() !=None ) | (start.GetLow().GetHigh() !=None ):
                if start.GetLow().GetLow().GetExpression() == start.GetLow().GetHigh().GetExpression() :
                    print(start.GetLow().GetName())
                    print(start.GetLow().GetName())
                    start.SetLow(start.GetLow().GetLow()) 
                BDDNode.BDDRed(start.GetLow())
                
        if (start != None):
            if  (start.GetHigh().GetLow() !=None ) | (start.GetHigh().GetHigh() !=None ):
                if start.GetHigh().GetLow().GetExpression() == start.GetHigh().GetHigh().GetExpression() :
                    print(start.GetHigh().GetName())
                    print(start.GetHigh().GetName())
                    start.SetHigh(start.GetHigh().GetLow()) 
                BDDNode.BDDRed(start.GetHigh())
        return start
            
    @staticmethod
    def check_Eq(BDD_Root_1,BDD_Root_2):
        if BDD_Root_1.GetName() != BDD_Root_2.GetName():
            print("No match")
            return 0
        if (BDD_Root_1.GetLow() != None) | (BDD_Root_2.GetLow() != None) :
            returnVlaue=BDDNode.check_Eq(BDD_Root_1.GetLow(),BDD_Root_2.GetLow())
            if returnVlaue == 0:
                return 0
        if (BDD_Root_1.GetHigh() != None) | (BDD_Root_2.GetHigh() != None) :
            returnVlaue=BDDNode.check_Eq(BDD_Root_1.GetHigh(),BDD_Root_2.GetHigh())
            if returnVlaue == 0:
                return 0
        return 1
            
    
    @staticmethod
    def display_BDD(BDD_Root, bdd):
        
        if (BDD_Root.GetLow() != None):
         if ((BDD_Root.GetLow().GetName() == '1' ) or ( BDD_Root.GetLow().GetName() == '0')):
             bdd.node(str(BDD_Root.GetLow() ), label = str(BDD_Root.GetLow().GetName()) , shape="square")
             bdd.edge(str(BDD_Root), str(BDD_Root.GetLow()), label="0", style= "dashed" )  
             print(BDD_Root.GetLow().GetName())# Connect the left node with the Root
         else:
             bdd.node(str(BDD_Root.GetLow()), label = BDD_Root.GetLow().GetName(), shape="circle" )
             bdd.edge(str(BDD_Root),str(BDD_Root.GetLow()), label="0", style= "dashed" )   # Connect the left node with the Root

         BDDNode.display_BDD(BDD_Root.GetLow(),bdd)    # Consider the left node as the root of the lower tree and recurse

        # Create right and left instances
        if (BDD_Root.GetHigh() != None):
         if ( (BDD_Root.GetHigh().GetName() == '1') or (BDD_Root.GetHigh().GetName() == '0') ):     # note the name of the leaf nodes is integer
             bdd.node(str(BDD_Root.GetHigh()), label = str(BDD_Root.GetHigh().GetName()) ,shape="square")
             bdd.edge(str(BDD_Root), str(BDD_Root.GetHigh()), label="1" )    # Connect the right node with the Root
         else:
             bdd.node(str(BDD_Root.GetHigh()), label = BDD_Root.GetHigh().GetName(), shape="circle")
             bdd.edge(str(BDD_Root), str(BDD_Root.GetHigh()), label="1" )    # Connect the right node with the Root

         BDDNode.display_BDD(BDD_Root.GetHigh(),bdd)     # Consider the right node as the root of the lower tree and recurse

        return bdd

BDDNodeOne=BDDNode(None,None,'1',1)
BDDNodeZero=BDDNode(None,None,'0',0)

def CreateDic(Order,index):
    Data={
    }
    for x in Order:
       Data.update({ Order[index]: Node(Order[index])}) 
       index +=1
    return Data                
         
    
class Node:
    def evaluate(self, context):
        pass

class Node(Node):
    NUM_OF_VARS=0
    def __init__(self, name):
        self.name = name
        Node.NUM_OF_VARS+=1

    def evaluate(self, context):
        return context[self.name]

    def __repr__(self):
        return f"{self.name}"

class AndNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context):
    
        if  isinstance(self.left, int):
            # SELF.LEFT IS INTEGR
            if self.left == 0:
                return 0
            elif isinstance(self.right, int):
                return self.left & self.right
            elif isinstance(self.right.evaluate(context), int):
                return self.left & self.right.evaluate(context)
            else:
                return self.right.evaluate(context)
            
        elif isinstance(self.left.evaluate(context), int):
            # SELF.LEFT.EV IS INTEGR
            if self.left.evaluate(context) == 0:
                return 0
            elif isinstance(self.right, int):
                return self.left.evaluate(context) & self.right
            elif isinstance(self.right.evaluate(context), int):
                return self.left.evaluate(context) & self.right.evaluate(context)
            else:
                return self.right.evaluate(context)
        else:
    
            if isinstance(self.right, int):
                if self.right==0:
                    return 0
                else:
                    return self.left.evaluate(context)
            elif isinstance(self.right.evaluate(context), int) :
                if (self.right.evaluate(context)==0):
                    return 0
                else:
                    return self.left.evaluate(context)
                
            else :
                if self.left.evaluate(context) == self.right.evaluate(context) :
                    return self.left.evaluate(context) 
                else :
                    return AndNode(self.left.evaluate(context), self.right.evaluate(context))      
                
            
    
       

    def __repr__(self):
        return f"AND ({self.left}, {self.right})"

class OrNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context):
        if  isinstance(self.left, int):
            if self.left == 1:
                return 1
            elif isinstance(self.right, int):
                return self.left | self.right
            elif isinstance(self.right.evaluate(context), int):
                return self.left | self.right.evaluate(context)
            else:
                return self.right.evaluate(context)
        elif isinstance(self.left.evaluate(context), int):
            if self.left.evaluate(context) == 1:
                return 1
            elif isinstance(self.right, int):
                return self.left.evaluate(context) | self.right
            elif isinstance(self.right.evaluate(context), int):
                return self.left.evaluate(context) | self.right.evaluate(context)
            else:
                return self.right.evaluate(context)
        else:
    
            if isinstance(self.right, int):
                if self.right==1:
                    return 1
                else:
                    return self.left.evaluate(context)
            elif isinstance(self.right.evaluate(context), int) :
                if (self.right.evaluate(context)==1):
                    return 1
                else:
                    return self.left.evaluate(context)
                
            else :
                if self.left.evaluate(context) == self.right.evaluate(context) :
                    return self.left.evaluate(context) 
                else :
                    return OrNode(self.left.evaluate(context), self.right.evaluate(context))    

    def __repr__(self):
        return f"OR ({self.left}, {self.right})"

class NotNode(Node):
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, context):
        if isinstance(self.expr.evaluate(context), int):
            return int (not self.expr.evaluate(context))
        else :
            return NotNode(self.expr.evaluate(context))

            

    def __str__(self):
        return( f" Not({self.expr})")

class XorNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context):
        if  isinstance(self.left, int):
            if isinstance(self.right, int):
                return self.left ^ self.right
            elif isinstance(self.right.evaluate(context), int):
                return self.left ^ self.right.evaluate(context)
            else:
                return XorNode( self.left ,self.right.evaluate(context))
            
        elif isinstance(self.left.evaluate(context), int):
            if isinstance(self.right, int):
                return self.left.evaluate(context) ^ self.right
            elif isinstance(self.right.evaluate(context), int):
                return self.left.evaluate(context) ^ self.right.evaluate(context)
            else:
                return XorNode( self.left.evaluate(context) ,self.right.evaluate(context))
        else:
    
            if isinstance(self.right, int):
                   return XorNode( self.left.evaluate(context), self.right) 
            elif isinstance(self.right.evaluate(context), int) :
                    return XorNode( self.left.evaluate(context), self.right.evaluate(context)) 
                
            else :
                if self.left.evaluate(context) == self.right.evaluate(context) :
                    return 0
                else :
                    return XorNode(self.left.evaluate(context), self.right.evaluate(context))    
                
    def __repr__(self):
        return f"Xor({self.left}, {self.right})"

def search_for_one_zero(input_tokens):
    index=0
    for x in input_tokens :
        
        if ( x == '1' ):
            input_tokens[index] = 1
        elif ( x == '0' ):
            input_tokens[index] = 0
        index +=1
    return input_tokens         
            
def parse(tokens):
    index = 0
    node = parse_exp(tokens, index)
    return node

def parse_exp(tokens, index):
    left_exp ,index = parse_subexp(tokens, index)
    if index >= len(tokens): # last token => Rule 2
        return left_exp

    token = tokens[index]
    if token == "&":
        index += 1
        right_exp ,index = parse_subexp(tokens, index)
        return AndNode(left_exp, right_exp) ,index
    elif token == "|":
        index += 1
        right_exp ,index = parse_subexp(tokens, index)
        return OrNode(left_exp, right_exp) ,index
    elif token == "^":
        index += 1
        right_exp ,index = parse_subexp(tokens, index)
        return XorNode(left_exp, right_exp) ,index
    else:
        raise Exception("Expected 'and' or 'or' or 'xor' or EOF")

def parse_subexp(tokens, index):
    token = tokens[index]
    if token == "(":
        index += 1
        node ,index = parse_exp(tokens, index)
        if tokens[index] != ")":
            raise Exception("Expected ')'")
        index += 1
        return node ,index
    elif token == "!":
        index += 1
        node ,index = parse_subexp(tokens, index)
        return NotNode(node) ,index
    elif token == 1:
        index += 1
        return 1,index
    
    elif token == 0:
        index += 1
        return 0,index
    
    else:
        index += 1
        return Node(token) ,index
