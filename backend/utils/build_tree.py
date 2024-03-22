#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Sequence

from asgiref.sync import sync_to_async

from backend.common.enums import BuildTreeType
from backend.utils.serializers import RowData, select_list_serialize


async def get_tree_nodes(row: Sequence[RowData]) -> list[dict[str, Any]]:
    """获取所有树形结构节点"""
    tree_nodes = await select_list_serialize(row)
    tree_nodes.sort(key=lambda x: x['sort'])
    return tree_nodes


@sync_to_async
def traversal_to_tree(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    通过遍历算法构造树形结构

    :param nodes:
    :return:
    """
    tree = []
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
                parent_node['children'].append(node)

    return tree


async def recursive_to_tree(nodes: list[dict[str, Any]], *, parent_id: int | None = None) -> list[dict[str, Any]]:
    """
    通过递归算法构造树形结构

    :param nodes:
    :param parent_id:
    :return:
    """
    tree = []
    for node in nodes:
        if node['parent_id'] == parent_id:
            child_node = await recursive_to_tree(nodes, parent_id=node['id'])
            if child_node:
                node['children'] = child_node
            tree.append(node)
    return tree


async def get_tree_data(
    row: Sequence[RowData], build_type: BuildTreeType = BuildTreeType.traversal, *, parent_id: int | None = None
) -> list[dict[str, Any]]:
    """
    获取树形结构数据

    :param row:
    :param build_type:
    :param parent_id:
    :return:
    """
    nodes = await get_tree_nodes(row)
    match build_type:
        case BuildTreeType.traversal:
            tree = await traversal_to_tree(nodes)
        case BuildTreeType.recursive:
            tree = await recursive_to_tree(nodes, parent_id=parent_id)
        case _:
            raise ValueError(f'无效的算法类型：{build_type}')
    return tree
