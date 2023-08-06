import os
import angr
import angr.analyses.reaching_definitions.dep_graph as dep_graph
from angrutils import *
import matplotlib.pyplot as plt
import networkx as nx
import pydot
import random
from information_flow_analysis import explicit, rda
from networkx.drawing.nx_pydot import graphviz_layout

def cfgs(proj, simgr, state):
    if not os.path.isdir("out"):
        os.mkdir("out")
    cfg_emul = None
    try:
        print("--CFGEmulated--")
        cfg = proj.analyses.CFGEmulated(keep_state=True, normalize=True, starts=[simgr.active[0].addr], initial_state=state, context_sensitivity_level=5, resolve_indirect_jumps=True)
        plot_cfg(cfg, "out/cfg_emul", "pdf", asminst=True, remove_imports=True, remove_path_terminator=True)
        print("Plotted to cfg_emul.pdf")
        cfg_emul = cfg
    except Exception as e:
        print(e)
    try:
        print("--CFGFast--")
        cfg_fast = proj.analyses.CFGFast()
        plot_cfg(cfg_fast, "out/cfg_fast", "pdf", asminst=True, remove_imports=True, remove_path_terminator=True)  
        print("Plotted to cfg_fast.pdf")
    except Exception as e:
        print(e)
    return cfg_emul

def transform_cfg_reachable(cfg, start_addr):
    start_node = None
    for n in cfg.graph.nodes:
        if n.addr == start_addr:
            start_node = n
            break
    if not start_node:
        raise Exception("Failed to find start node!")
    reachable_nodes = networkx.descendants(cfg.graph, start_node)
    excluded_nodes = []
    for n in cfg.graph.nodes:
        if (not n in reachable_nodes) and (not n == start_node):
            excluded_nodes.append(n)
    cfg.graph.remove_nodes_from(excluded_nodes)
    return cfg

def draw_everything(proj, simgr, state, start_node=None):
    cfg = cfgs(proj, simgr, state)

    draw_cfg_dependent_graphs(cfg)

    if start_node:
        print("--PDG--")
        pdg = rda.get_super_dep_graph_with_linking(proj, cfg, cdg, start_node)
        draw_pdg(proj, pdg)
        print("Plotted to pdg.pdf")

def draw_cfg_dependent_graphs(cfg):
    print("--CDG--")
    cdg = proj.analyses.CDG(cfg = cfg)
    plot_cdg(cfg, cdg, "out/cdg", format="pdf")
    print("Plotted to cdg.pdf")

    print("--POST_DOM--")
    postdom = cdg.get_post_dominators()
    draw_tree(postdom, fname="out/postdom.pdf")
    print("Plotted to postdom.pdf")

def draw_pdg(proj, pdg, fname="out/pdg.pdf"):
    if not os.path.isdir("out"):
        os.mkdir("out")

    fig = plt.figure(figsize=(100,100))
    color_map = {0: 0.5, 1: 0.25, 2: 0}
    colors = [color_map[node.sec_class] for node in pdg.nodes()]
    pos = nx.spring_layout(pdg)
    nx.draw_networkx_nodes(pdg, cmap=plt.cm.Set1, node_color=colors, pos=pos)
    nx.draw_networkx_labels(pdg, pos)
    edge_labels = {edge: ("implicit" if pdg.get_edge_data(edge[0],edge[1])['type'] == 1 else "explicit") for edge in pdg.edges}
    explicit_edges = list(filter(lambda edge: pdg.get_edge_data(edge[0],edge[1])['type'] == 0, pdg.edges))
    implicit_edges = list(filter(lambda edge: pdg.get_edge_data(edge[0],edge[1])['type'] == 1, pdg.edges))
    nx.draw_networkx_edges(pdg, style="solid", edgelist=explicit_edges, pos=pos, width=2.5)
    nx.draw_networkx_edges(pdg, style="dotted", edgelist=implicit_edges, pos=pos, width=2.5, alpha=0.5)
    nx.draw_networkx_edge_labels(pdg, pos=pos, edge_labels=edge_labels)
    fig.savefig(fname, dpi=5)

def draw_everything_with_data(proj, cfg_emul, cfg_fast, cdg, postdom, pdg):
    if not os.path.isdir("out"):
        os.mkdir("out")
    
    print("--CFGEmulated--")
    plot_cfg(cfg_emul, "out/cfg_emul", "pdf", asminst=True, remove_imports=True, remove_path_terminator=True)
    print("Plotted to cfg_emul.pdf")

    print("--CFGFast--")
    plot_cfg(cfg_fast, "out/cfg_fast", "pdf", asminst=True, remove_imports=True, remove_path_terminator=True)  
    print("Plotted to cfg_fast.pdf")

    print("--CDG--")
    plot_cdg(cfg_emul, cdg, "out/cdg", format="pdf")
    print("Plotted to cdg.pdf")

    print("--POST_DOM--")
    draw_tree(postdom, fname="out/postdom.pdf")
    print("Plotted to postdom.pdf")

    print("--PDG--")
    draw_pdg(proj, pdg)
    print("Plotted to pdg.pdf")

def write_stashes(simgr, filename="stash_summary.txt", args=[], input_write_stashes=[], verbose=True):
    file = open(filename,"w+") 
    if verbose:
        print('--stashes--')
    for key in simgr.stashes:
        string = str(key) + ": " + str(len(simgr.stashes[key]))
        if verbose:
            print(string)
        writeline(file, string)
    if verbose:
        print('writing...')
    for key in simgr.stashes:
        writeline(file, "===" + str(key) + ": " + str(len(simgr.stashes[key])) + "===")
        for c in range(len(simgr.stashes[key])):
            stash = simgr.stashes[key][c]
            writeline(file, "no: " + str(c))
            writeline(file, str(hex(stash.addr)))
            for d in range(3):
                try:
                    writeline(file, "dump["+str(d)+"]: " + str(stash.posix.dumps(d)))
                except Exception as e:
                    if verbose:
                        print("dump["+str(d)+"]: eval failure")
                    pass
            for i in range(len(args)):
                writeline(file, "arg" + str(i) + " " + get_str_from_arg(stash, args[i]))
                if(key in input_write_stashes):
                    inputfile = open(key + str(c) + "_input" + str(i),"wb+")
                    sol = stash.solver.eval(args[i], cast_to=bytes)
                    inputfile.write(sol)
                    inputfile.close()
            writeline(file, "-----")
    if verbose:
        print('written to ' + filename)
    file.close()

def get_str_from_arg(state, arg, no=5, newline=True):
    str = ""
    solutions = gather_evals(state, arg, no)
    first = True
    for bs in solutions:
        try:
            decoded_sol = bs.decode('UTF-8')
            str += ("" if first else ("\n" if newline else "|")) + decoded_sol
        except:
            str +=  ("" if first else ("\n" if newline else "|")) + "no utf-8 "
        first = False
    return str

def gather_evals(state, arg, max):
    solutions = []
    try:
        for i in range(max):
            solutions = state.solver.eval_upto(arg, i, cast_to=bytes)
    except:
        pass
    return solutions

def writeline(file, string):
    file.write(string + "\n")

def writefile(string, filename):
    file = open(filename,"w+") 
    file.write(string)
    file.close()

def draw_ddg(ddg):
    draw_graph(ddg.graph, "ddg.pdf")
    
def draw_graph(graph, fname="out/graph.pdf"):
    if not os.path.isdir("out"):
        os.mkdir("out")
    fig = plt.figure(figsize=(100,100))
    nx.draw(graph, with_labels=True)
    fig.savefig(fname, dpi=5)

def draw_tree(tree, fname="out/tree.pdf"):
    if not os.path.isdir("out"):
        os.mkdir("out")
    fig = plt.figure(figsize=(100,100))
    pos = graphviz_layout(tree, prog="dot")
    nx.draw(tree, pos,with_labels=True)
    fig.savefig(fname, dpi=5)

def hexlist(seq):
    return list(map(lambda x: hex(x), seq))
