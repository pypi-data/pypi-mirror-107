# @author       Jiawei Lu (jiaweil9@asu.edu)
# @time         2021/5/17 13:49
# @desc         [script description]



def filterNet(net, link_types=('motorway', 'trunk', 'primary'), number_of_POIs=None, minimum_POI_size=None):
    if isinstance(link_types, str):
        link_types_ = (link_types,)
    else:
        link_types_ = link_types

    links_to_be_removed = []     # id

    for link_id, link in net.link_dict.items():
        if link.link_type_name not in link_types_:
            links_to_be_removed.append(link_id)

    for link_id in links_to_be_removed:
        link = net.link_dict[link_id]
        link.from_node.outgoing_link_list.remove(link)
        link.to_node.incoming_link_list.remove(link)
        del net.link_dict[link_id]

    nodes_to_be_removed = []        # id
    for node_id, node in net.node_dict.items():
        if len(node.incoming_link_list) == 0 and len(node.outgoing_link_list) == 0:
            nodes_to_be_removed.append(node_id)

    for node_id in nodes_to_be_removed:
        del net.node_dict[node_id]