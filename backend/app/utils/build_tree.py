#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Sequence

from asgiref.sync import sync_to_async

from backend.app.common.enums import BuildTreeType
from backend.app.utils.serializers import RowData, select_to_list


@sync_to_async
def get_tree_nodes(row: Sequence[RowData]) -> list[dict[str, Any]]:
    """获取所有树形结构节点"""
    tree_nodes = select_to_list(row)
    tree_nodes.sort(key=lambda x: x['sort'])
    return tree_nodes


@sync_to_async
def traversal_to_tree(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    通过遍历算法构造树形结构

    :param nodes:
    :return:
    """
    node_map = {}
    root_nodes = []

    for node in nodes:
        parent_id = node['parent_id']
        if parent_id is None:
            root_nodes.append(node)
        else:
            parent_node = node_map.get(parent_id, {})
            parent_node.setdefault('children', []).append(node)
            node_map[parent_id] = parent_node
        node_map[node['id']] = node

    return root_nodes


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
            child_node = {
                'id': node['id'],
                'parent_id': node['parent_id'],
                'children': await recursive_to_tree(nodes, parent_id=node['id']),
            }
            tree.append(child_node)
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
