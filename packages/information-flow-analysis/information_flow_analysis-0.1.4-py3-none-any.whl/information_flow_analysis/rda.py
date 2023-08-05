import angr
from angrutils import *
import matplotlib.pyplot as plt
import angr.analyses.reaching_definitions.dep_graph as dep_graph
import networkx as nx
from information_flow_analysis import information

class DefinitionDecorator(angr.knowledge_plugins.key_definitions.definition.Definition):
    def __init__(self, atom, codeloc, data, dummy, tags):
        angr.knowledge_plugins.key_definitions.definition.Definition.__init__(self, atom, codeloc, data, dummy, tags)
        self.given_sec_class = 0 #Explicitly defined sec class, from subj/high_addrs
        self.explicit_sec_class = 0 #Derived or given explicit sec class
        self.explicit_source = None #Derived source of explicit sec class
        self.implicit_sec_class = 0 #Derived implicit sec class
        self.implicit_source = None #Derived source of implicit sec class
        self.branching_sec_class = 0 #If a branching node, the current sec class of the implicit context

    @property
    def sec_class(self):
        return max(self.explicit_sec_class, self.implicit_sec_class)

    @property
    def sec_class_source(self):
        return self.implicit_source if self.implicit_sec_class > self.explicit_sec_class and self.implicit_source else self.explicit_source

    def __repr__(self):
        return "{Atom: " + str(self.atom) + ", Codeloc: " + str(self.codeloc) + ", Exp: " + str(self.explicit_sec_class) +\
            (", Imp: " + str(self.implicit_sec_class) if self.implicit_sec_class != 0 else "") +\
            (", Sat: " + str(self.given_sec_class) if self.given_sec_class != 0 else "") + "}"

#Get intermediate nodes from source
def get_intermediates(source_node):
    inters = []
    source = source_node
    while(source.sec_class_source and source.sec_class_source != source):
        inters.append(source)
        source = source.sec_class_source
    return source, inters

def elevate_explicit(rda_graph, node, given_sec_class):
    node.given_sec_class = given_sec_class
    if node.explicit_sec_class < given_sec_class:
        node.explicit_sec_class = given_sec_class
        node.explicit_source = node
        descendants = networkx.descendants(rda_graph, node)
        for des in descendants:
            if des.explicit_sec_class < given_sec_class:
                des.explicit_sec_class = given_sec_class
                des.explicit_source = node

def elevate_implicit(rda_graph, node, branch_node):
    if node.explicit_sec_class < branch_node.sec_class:
        node.implicit_sec_class = branch_node.sec_class
        node.implicit_source = branch_node
        descendants = networkx.descendants(rda_graph, node)
        for des in descendants:
            if des.explicit_sec_class < branch_node.sec_class:
                des.implicit_sec_class = branch_node.sec_class
                des.implicit_source = branch_node

def wrap_rda(rda):
    g = networkx.DiGraph()
    map = {}
    for n in rda.graph.nodes:
        decorator = DefinitionDecorator(n.atom, n.codeloc, n.data, n.dummy, n.tags)
        map[n] = decorator
        g.add_node(decorator)
    for e in rda.graph.edges:
        g.add_edge(map[e[0]],map[e[1]],type=0) #Explicit
    g.enriched_class_addrs = {0:[],1:[],2:[]}
    return g

#Create rda foreach function
#Create new super graph containing all rda graphs
def get_super_dep_graph_with_linking(proj, cfg, start_node, func_addrs=None):
    if not func_addrs:
        func_addrs = information.get_unique_reachable_function_addresses(cfg, start_node)
    rda_graph = wrap_rda(get_super_rda(proj, func_addrs))
    link_externals_to_earliest_definition(rda_graph, cfg, [start_node])
    return rda_graph

def get_super_rda(proj, function_addrs):
    cfg = proj.analyses.CFGFast() #adds info to kb
    rda_dep_graph = dep_graph.DepGraph()
    for func_addr in function_addrs:
        func = proj.kb.functions.function(addr=func_addr)
        if func == None:
            print('Warning: ' + str(hex(func_addr)) + ' did not map to any function through kb!')
            continue
        rda = proj.analyses.ReachingDefinitions(
            subject = func,
            cc = func.calling_convention if func.calling_convention else None,
            dep_graph = rda_dep_graph,
            observe_all=True
        )
        rda_dep_graph = rda.dep_graph
    return rda_dep_graph

def find_rda_graph_nodes(rda_graph, ins_addrs):
    if not isinstance(ins_addrs, list):
        ins_addrs = [ins_addrs]
    for n in rda_graph.nodes():
        if n.codeloc and n.codeloc.ins_addr in ins_addrs:
            yield n

def __find_rda_graph_node__(rda_graph, ins_addr):
    for n in rda_graph.nodes():
            if n.codeloc and n.codeloc.ins_addr == ins_addr:
                return n
    return None   

def link_externals_to_earliest_definition(rda_graph, cfg, cfg_end_nodes):
    leafs = get_leafs(rda_graph)
    externals = get_externals(rda_graph)
    for external in externals:
        for nn in list(nx.all_neighbors(rda_graph, external)):
            cfg_node = information.find_cfg_node(cfg, nn.codeloc.block_addr)
            if not cfg_node:
                continue
            matches = find_earliest_matching_definition(external, nn, leafs, cfg_end_nodes, cfg_node)
            for match in matches:
                rda_graph.add_edge(match, nn, type=0) #Explicit

#external is the target external node from which the target is child
#the target is the node to which we want to link, we need to know it's block_addr
#leafs are the end-nodes of the super_dep_graph
#the cdg_node is currently inspected node
def find_earliest_matching_definition(external, target, leafs, cfg_end_nodes, cfg_node):
    if cfg_node.block and target.codeloc.block_addr != cfg_node.block.addr:
        for leaf in leafs:
            if leaf.codeloc and leaf.codeloc.block_addr == cfg_node.block.addr:
                if leaf.atom == external.atom:
                    return [leaf]
    if cfg_node in cfg_end_nodes:
        return []
    caller_blocks = cfg_node.predecessors
    matches = []
    for caller_block in caller_blocks:
        matches += find_earliest_matching_definition(external, target, leafs, cfg_end_nodes, caller_block)
    return matches

def get_leafs(graph):
    leaf_nodes = [node for node in graph.nodes() if graph.in_degree(node)!=0 and graph.out_degree(node)==0]
    return leaf_nodes

def get_externals(rda_graph):
    for n in rda_graph.nodes:
        if isinstance(n.codeloc, angr.analyses.reaching_definitions.external_codeloc.ExternalCodeLocation):
            yield n

def check_explicit_flow(rda_graph, source, target):
    paths = nx.all_simple_edge_paths(rda_graph, source=source, target=target)
    for path in paths:
        valid = True
        for edge in path:
            if rda_graph.get_edge_data(edge[0],edge[1])['type'] == 1:
                valid = False
                break
        if valid:
            return path
    return None

def print_edge_flow(edge_flow):
    print(edge_flow[0][0].codeloc)
    for edge in edge_flow:
        print(edge[1].codeloc)

def get_edge_flow_rda(rda_graph, edge_flow):
    rda_graph = rda_graph.copy()
    node_whitelist = []
    node_whitelist.append(edge_flow[0][0])
    for edge in edge_flow:
        node_whitelist.append(edge[1])
    remove = [node for node in rda_graph.nodes if not node in node_whitelist]
    rda_graph.remove_nodes_from(remove)
    remove = [edge for edge in rda_graph.edges if not edge in edge_flow]
    rda_graph.remove_edges_from(remove)
    return rda_graph