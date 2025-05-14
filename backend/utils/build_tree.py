#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Sequence

from backend.common.enums import BuildTreeType
from backend.utils.serializers import RowData, select_list_serialize


def get_tree_nodes(row: Sequence[RowData]) -> list[dict[str, Any]]:
    """
    Fetch all tree structure nodes

    :param row: original data line sequence
    :return:
    """
    tree_nodes = select_list_serialize(row)
    tree_nodes.sort(key=lambda x: x['sort'])
    return tree_nodes


def traversal_to_tree(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Construct tree structure through cross-calculations

    :param nodes: list of tree nodes
    :return:
    """
    tree: list[dict[str, Any]] = []
    node_dict = {node['id']: node for node in nodes}

    for node in nodes:
        parent_id = node['parent_id']
        if parent_id is None:
            tree.append(node)
        else:
            parent_node = node_dict.get(parent_id)
            if parent_node is not None:
                if 'children' not in parent_node:
                    parent_node['children'] = []
                if node not in parent_node['children']:
                    parent_node['children'].append(node)
            else:
                if node not in tree:
                    tree.append(node)

    return tree


def recursive_to_tree(nodes: list[dict[str, Any]], *, parent_id: int | None = None) -> list[dict[str, Any]]:
    """
    Construct tree structure through a recursive algorithm (higher impact)

    :param nodes: list of tree nodes
    :param parent_id: Parent ID, default None for root
    :return:
    """
    tree: list[dict[str, Any]] = []
    for node in nodes:
        if node['parent_id'] == parent_id:
            child_nodes = recursive_to_tree(nodes, parent_id=node['id'])
            if child_nodes:
                node['children'] = child_nodes
            tree.append(node)
    return tree


def get_tree_data(
    row: Sequence[RowData], build_type: BuildTreeType = BuildTreeType.traversal, *, parent_id: int | None = None
) -> list[dict[str, Any]]:
    """
    Fetch tree structure data

    :param row: original data line sequence
    :param build_type: algorithm type for building tree structures, default to traversal
    :param parent_id: Parent Node ID, used only in recursive algorithms
    :return:
    """
    nodes = get_tree_nodes(row)
    match build_type:
        case BuildTreeType.traversal:
            tree = traversal_to_tree(nodes)
        case BuildTreeType.recursive:
            tree = recursive_to_tree(nodes, parent_id=parent_id)
        case _:
            raise ValueError(f'invalid algorithm type: {build_type}')
    return tree


def get_vben5_tree_data(row: Sequence[RowData]) -> list[dict[str, Any]]:
    """
    fetch vben5 tree structure data

    :param row: original data line sequence
    :return:
    """
    # Original field to remove
    remove_keys = {'title', 'icon', 'link', 'cache', 'display', 'status'}

    vben5_nodes = [
        {
            **{k: v for k, v in node.items() if k not in remove_keys},
            'meta': {
                'title': node['title'],
                'icon': node['icon'],
                'link': node['link'],
                'keepAlive': node['cache'],
                'hideInMenu': not bool(node['display']),
                'menuVisibleWithForbidden': not bool(node['status']),
            },
        }
        for node in get_tree_nodes(row)
    ]

    return traversal_to_tree(vben5_nodes)
