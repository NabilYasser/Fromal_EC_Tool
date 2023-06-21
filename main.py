from formal_eq import *
if __name__ == "__main__":
    #input_str = " ( ( ! a & ( ! b & ! c ) ) | ( a & b ) )  | ( b & c ) \n"
    input_str = " a & ( b & c ) \n"
    input_str_2 = " a  & ( b | c ) \n" # another function to test the eq checking
   
    
    Order=('a','b','c') # you should extracted the var from the input string or ask the user to enter the order he/she wants
    index=0
    input_tokens = input_str.split()
    input_tokens=search_for_one_zero(input_tokens)
    parsetree, index = parse(input_tokens)
    print(parsetree)
    start,index=BDDNode.ConstructBDD(parsetree,Order)
    start=BDDNode.BDDRed(start)
    
    index=0
    input_tokens = input_str_2.split()
    input_tokens=search_for_one_zero(input_tokens)
    parsetree_2, index = parse(input_tokens)
    print(parsetree_2)
    start_2,index=BDDNode.ConstructBDD(parsetree_2,Order)
    start_2=BDDNode.BDDRed(start_2)
    print(parsetree)
    print(parsetree_2)
    
    if BDDNode.check_Eq(start,start_2):
        print("The two circuits are equivalent")
    else:
        print("The two circuits are NOT equivalent")
 
    bdd = graphviz.Digraph()
    bdd.node(str(start), label = start.GetName(), shape="circle")
    bdd = BDDNode.display_BDD(start,bdd)
    bdd.render("Circuit 1", format="png")
    
    bdd = graphviz.Digraph()
    bdd.node(str(start_2), label = start_2.GetName(), shape="circle")
    bdd = BDDNode.display_BDD(start_2,bdd)
    bdd.render("Circuit 2", format="png")

