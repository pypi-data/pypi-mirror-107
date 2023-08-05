from .backend import generate_tree, fold_tree, get_example_data, Options, default_options, to_graphviz, fold_and_out, fold

def viz(root_obj):
    tree = generate_tree(root_obj)
    fold_tree(tree)
    tree.show(data_property = "long")
    return tree

def quick_start():
    # # change options
    default_options.compress_level = None # compress_level is set to None to manually handle options

    default_options.id_pool = list(range(int(1e7), -1, -1)) # also tag pool. should be unique for every node.
    default_options.print_tag = True # default_options will be applied to every node.
    default_options.print_terminal_contents = True
    default_options.max_print_of_contents = 100
    default_options.max_children_search_threshold = 10
    default_options.print_max_children = {"depth_multiplier": 1, "upperbound_constant": 1, "exclude_parent_classes": [dict]}

    # # make & modify tree
    root_obj = get_example_data()

    tree = generate_tree(root_obj) # initial full tree, only with restriction of max_children_search_threshold.
    fold_tree(tree)

    fold_and_out(tree, 1181) # this folds a node and remove from tree
    fold(tree, 1179) # this folds a node, removing its children. but leaves a node in the tree.

    # # modify displayed messages
    tree.show(data_property="short") # show simple data type and size
    tree.show(data_property="long") # show keys, a little of contents too
    tree[1].data = tree[1].data._replace(long = 'foobar', short = 'barfoo', memo = "data has short, long, memo attrs to show")
    tree.show(data_property="memo")

    # graphviz
    g = to_graphviz(tree, data_property = "long", file_path = "source.gv")
    g.view()