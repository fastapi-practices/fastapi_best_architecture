import os
import subprocess
import sys

from importlib.metadata import PackageNotFoundError, distribution

from packaging.requirements import Requirement
from starlette.concurrency import run_in_threadpool

from backend.core.conf import settings
from backend.core.path_conf import PLUGIN_DIR


class PluginInstallError(Exception):
    """插件安装错误"""


def _ensure_pip_available() -> bool:
    """确保 pip 在虚拟环境中可用"""
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            return True
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        pass

    # 尝试使用 ensurepip
    try:
        subprocess.check_call(
            [sys.executable, '-m', 'ensurepip', '--default-pip'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        pass

    # 尝试下载并安装
    try:
        import os
        import tempfile

        import httpx

        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                with httpx.Client(timeout=3) as client:
                    get_pip_url = 'https://bootstrap.pypa.io/get-pip.py'
                    response = client.get(get_pip_url)
                    response.raise_for_status()
                    f.write(response.text)
                    temp_file = f.name
        except Exception:  # noqa: ignore
            return False

        try:
            subprocess.check_call([sys.executable, temp_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            result = subprocess.run([sys.executable, '-m', 'pip', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        finally:
            try:
                os.unlink(temp_file)
            except OSError:
                pass
    except Exception:  # noqa: ignore
        pass

    return False


def get_plugins() -> list[str]:
    """
    获取插件列表

    注意：此函数从 backend.plugin.core 导入以避免循环依赖
    """
    from backend.plugin.core import get_plugins as _get_plugins

    return _get_plugins()


def install_requirements(plugin: str | None) -> None:  # noqa: C901
    """
    安装插件依赖

    :param plugin: 指定插件名，否则检查所有插件
    :return:
    """
    plugins = [plugin] if plugin else get_plugins()

    for plugin in plugins:
        requirements_file = PLUGIN_DIR / plugin / 'requirements.txt'
        missing_dependencies = False
        if os.path.exists(requirements_file):
            with open(requirements_file, encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    try:
                        req = Requirement(line)
                        dependency = req.name.lower()
                    except Exception as e:
                        raise PluginInstallError(f'插件 {plugin} 依赖 {line} 格式错误: {e!s}') from e
                    try:
                        distribution(dependency)
                    except PackageNotFoundError:
                        missing_dependencies = True

        if missing_dependencies:
            try:
                if not _ensure_pip_available():
                    raise PluginInstallError(f'pip 安装失败，无法继续安装插件 {plugin} 依赖')

                pip_install = [sys.executable, '-m', 'pip', 'install', '-r', requirements_file]
                if settings.PLUGIN_PIP_CHINA:
                    pip_install.extend(['-i', settings.PLUGIN_PIP_INDEX_URL])

                max_retries = settings.PLUGIN_PIP_MAX_RETRY
                for attempt in range(max_retries):
                    try:
                        subprocess.check_call(
                            pip_install,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                        break
                    except subprocess.TimeoutExpired:
                        if attempt == max_retries - 1:
                            raise PluginInstallError(f'插件 {plugin} 依赖安装超时')
                        continue
                    except subprocess.CalledProcessError as e:
                        if attempt == max_retries - 1:
                            raise PluginInstallError(f'插件 {plugin} 依赖安装失败：{e}') from e
                        continue
            except subprocess.CalledProcessError as e:
                raise PluginInstallError(f'插件 {plugin} 依赖安装失败：{e}') from e


def uninstall_requirements(plugin: str) -> None:
    """
    卸载插件依赖

    :param plugin: 插件名称
    :return:
    """
    requirements_file = PLUGIN_DIR / plugin / 'requirements.txt'
    if os.path.exists(requirements_file):
        try:
            pip_uninstall = [sys.executable, '-m', 'pip', 'uninstall', '-r', requirements_file, '-y']
            subprocess.check_call(pip_uninstall, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            raise PluginInstallError(f'插件 {plugin} 依赖卸载失败：{e}') from e


async def install_requirements_async(plugin: str | None = None) -> None:
    """
    异步安装插件依赖

    由于 Windows 平台限制，无法实现完美的全异步方案，详情：
    https://stackoverflow.com/questions/44633458/why-am-i-getting-notimplementederror-with-async-and-await-on-windows
    """
    await run_in_threadpool(install_requirements, plugin)


async def uninstall_requirements_async(plugin: str) -> None:
    """
    异步卸载插件依赖

    :param plugin: 插件名称
    :return:
    """
    await run_in_threadpool(uninstall_requirements, plugin)
