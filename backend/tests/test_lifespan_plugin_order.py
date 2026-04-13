from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import pytest

from fastapi import FastAPI

from backend.common.enums import LifespanStage
from backend.common.lifespan import LifespanManager
from backend.plugin.core import _sort_plugins_by_dependency
from backend.plugin.errors import PluginConfigError
from backend.plugin.validator import validate_plugin_config


def test_lifespan_manager_orders_by_stage_and_registration_order() -> None:
    manager = LifespanManager()
    calls: list[str] = []

    @asynccontextmanager
    async def plugin_first(_: FastAPI) -> AsyncGenerator[None]:
        calls.append('plugin_first')
        yield

    @asynccontextmanager
    async def core_default(_: FastAPI) -> AsyncGenerator[None]:
        calls.append('core_default')
        yield

    @asynccontextmanager
    async def plugin_second(_: FastAPI) -> AsyncGenerator[None]:
        calls.append('plugin_second')
        yield

    manager.register(plugin_first, stage=LifespanStage.plugin)
    manager.register(core_default)
    manager.register(plugin_second, stage=LifespanStage.plugin)

    lifespan = manager.build()

    async def run() -> None:
        async with lifespan(FastAPI()):
            pass

    import anyio

    anyio.run(run)

    assert calls == ['core_default', 'plugin_first', 'plugin_second']


def test_sort_plugins_by_dependency_orders_dependencies_first(monkeypatch: pytest.MonkeyPatch) -> None:
    configs = {
        'plugin_a': {'plugin': {'depends_on': ['plugin_b']}},
        'plugin_b': {'plugin': {'depends_on': ['plugin_c']}},
        'plugin_c': {'plugin': {'depends_on': []}},
    }

    monkeypatch.setattr('backend.plugin.core.load_plugin_config', lambda plugin: configs[plugin])

    ordered = _sort_plugins_by_dependency(
        ['plugin_a', 'plugin_b', 'plugin_c'],
        {'plugin_a', 'plugin_b', 'plugin_c'},
    )

    assert ordered == ['plugin_c', 'plugin_b', 'plugin_a']


def test_sort_plugins_by_dependency_rejects_missing_plugin(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        'backend.plugin.core.load_plugin_config',
        lambda _: {'plugin': {'depends_on': ['missing_plugin']}},
    )

    with pytest.raises(PluginConfigError, match='missing_plugin.*不存在'):
        _sort_plugins_by_dependency(['plugin_a'], {'plugin_a'})


def test_sort_plugins_by_dependency_rejects_circular_dependency(monkeypatch: pytest.MonkeyPatch) -> None:
    configs = {
        'plugin_a': {'plugin': {'depends_on': ['plugin_b']}},
        'plugin_b': {'plugin': {'depends_on': ['plugin_a']}},
    }

    monkeypatch.setattr('backend.plugin.core.load_plugin_config', lambda plugin: configs[plugin])

    with pytest.raises(PluginConfigError, match='plugin_a -> plugin_b -> plugin_a'):
        _sort_plugins_by_dependency(['plugin_a', 'plugin_b'], {'plugin_a', 'plugin_b'})


def test_validate_plugin_config_rejects_self_dependency() -> None:
    config = {
        'plugin': {
            'summary': 'demo',
            'version': '1.0.0',
            'description': 'demo plugin',
            'author': 'tester',
            'tags': ['other'],
            'database': ['mysql'],
            'depends_on': ['demo_plugin'],
        },
        'app': {'router': ['router']},
    }

    with pytest.raises(PluginConfigError, match='不能依赖自身'):
        validate_plugin_config('demo_plugin', config)
