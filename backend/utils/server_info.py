#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import socket
import sys

from datetime import datetime, timedelta
from datetime import timezone as tz

import psutil

from backend.utils.timezone import timezone


class ServerInfo:
    @staticmethod
    def format_bytes(size: int | float) -> str:
        """
        格式化字节大小

        :param size: 字节大小
        :return:
        """
        factor = 1024
        for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(size) < factor:
                return f'{size:.2f} {unit}B'
            size /= factor
        return f'{size:.2f} YB'

    @staticmethod
    def fmt_seconds(seconds: int) -> str:
        """
        格式化秒数为可读的时间字符串

        :param seconds: 秒数
        :return:
        """
        days, rem = divmod(int(seconds), 86400)
        hours, rem = divmod(rem, 3600)
        minutes, seconds = divmod(rem, 60)

        parts = []
        if days:
            parts.append(f'{days} 天')
        if hours:
            parts.append(f'{hours} 小时')
        if minutes:
            parts.append(f'{minutes} 分钟')
        if seconds:
            parts.append(f'{seconds} 秒')

        return ' '.join(parts) if parts else '0 秒'

    @staticmethod
    def fmt_timedelta(td: timedelta) -> str:
        """
        格式化时间差

        :param td: 时间差对象
        :return:
        """
        return ServerInfo.fmt_seconds(round(td.total_seconds()))

    @staticmethod
    def get_cpu_info() -> dict[str, float | int]:
        """获取 CPU 信息"""
        cpu_info = {
            'usage': round(psutil.cpu_percent(interval=0.1), 2),  # %
            'logical_num': psutil.cpu_count(logical=True) or 0,
            'physical_num': psutil.cpu_count(logical=False) or 0,
            'max_freq': 0.0,
            'min_freq': 0.0,
            'current_freq': 0.0,
        }

        try:
            if hasattr(psutil, 'cpu_freq'):
                cpu_freq = psutil.cpu_freq()
                if cpu_freq:  # Some systems return None
                    cpu_info.update({
                        'max_freq': round(cpu_freq.max, 2),
                        'min_freq': round(cpu_freq.min, 2),
                        'current_freq': round(cpu_freq.current, 2),
                    })
        except Exception:
            pass

        return cpu_info

    @staticmethod
    def get_mem_info() -> dict[str, float]:
        """获取内存信息"""
        mem = psutil.virtual_memory()
        gb_factor = 1024**3
        return {
            'total': round(mem.total / gb_factor, 2),
            'used': round(mem.used / gb_factor, 2),
            'free': round(mem.available / gb_factor, 2),
            'usage': round(mem.percent, 2),
        }

    @staticmethod
    def get_sys_info() -> dict[str, str]:
        """获取服务器信息"""
        hostname = socket.gethostname()
        ip = '127.0.0.1'

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(0.5)
                s.connect(('8.8.8.8', 80))
                ip = s.getsockname()[0]
        except (socket.gaierror, socket.timeout, OSError):
            pass

        return {
            'name': hostname,
            'ip': ip,
            'os': platform.system(),
            'arch': platform.machine(),
        }

    @staticmethod
    def get_disk_info() -> list[dict[str, str]]:
        """获取磁盘信息"""
        disk_info = []
        for partition in psutil.disk_partitions(all=False):
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    'dir': partition.mountpoint,
                    'type': partition.fstype,
                    'device': partition.device,
                    'total': ServerInfo.format_bytes(usage.total),
                    'free': ServerInfo.format_bytes(usage.free),
                    'used': ServerInfo.format_bytes(usage.used),
                    'usage': f'{usage.percent:.2f}%',
                })
            except (PermissionError, psutil.AccessDenied):
                continue
        return disk_info

    @staticmethod
    def get_service_info() -> dict[str, str | datetime]:
        """获取服务信息"""
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()

        try:
            create_time = datetime.fromtimestamp(process.create_time(), tz=tz.utc)
            start_time = timezone.f_datetime(create_time)
        except (psutil.NoSuchProcess, OSError):
            start_time = timezone.now()

        elapsed = ServerInfo.fmt_timedelta(timezone.now() - start_time)

        return {
            'name': 'Python3',
            'version': platform.python_version(),
            'home': sys.executable,
            'cpu_usage': f'{process.cpu_percent(interval=0.1):.2f}%',
            'mem_vms': ServerInfo.format_bytes(mem_info.vms),
            'mem_rss': ServerInfo.format_bytes(mem_info.rss),
            'mem_free': ServerInfo.format_bytes(mem_info.vms - mem_info.rss),
            'startup': timezone.t_str(start_time),
            'elapsed': elapsed,
        }


server_info: ServerInfo = ServerInfo()
