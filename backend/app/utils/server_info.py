import os
import platform
import socket
import sys
from datetime import datetime, timedelta
from typing import List

import psutil


class ServerInfo:
    @staticmethod
    def get_size(data, suffix='B') -> str:
        """按照正确的格式缩放字节"""
        factor = 1024
        for unit in ['', 'K', 'M', 'G', 'T', 'P']:
            if data < factor:
                return f'{data:.2f}{unit}{suffix}'
            data /= factor

    @staticmethod
    def fmt_timedelta(td: timedelta) -> str:
        """格式化时间戳"""
        rem = td.seconds
        days, rem = rem // 86400, rem % 86400
        hours, rem = rem // 3600, rem % 3600
        minutes = rem // 60
        res = f'{minutes} 分钟'
        if hours > 0:
            res = f'{hours} 小时 {res}'
        if days > 0:
            res = f'{days} 天 {res}'
        return res

    @staticmethod
    def get_cpu_info() -> dict:
        """获取CPU信息"""
        info = dict()
        info.update({'cpu_num': psutil.cpu_count(logical=True)})
        cpu_times = psutil.cpu_times()
        total = (
            cpu_times.user
            + cpu_times.nice
            + cpu_times.system
            + cpu_times.idle
            + getattr(cpu_times, 'iowait', 0.0)
            + getattr(cpu_times, 'irq', 0.0)
            + getattr(cpu_times, 'softirq', 0.0)
            + getattr(cpu_times, 'steal', 0.0)
        )
        info.update({'total': round(total, 2)})
        info.update({'sys': round(cpu_times.system / total, 2)})
        info.update({'used': round(cpu_times.user / total, 2)})
        info.update({'wait': round(getattr(cpu_times, 'iowait', 0.0) / total, 2)})
        info.update({'free': round(cpu_times.idle / total, 2)})
        return info

    @staticmethod
    def get_mem_info() -> dict:
        """获取内存信息"""
        number = 1024**3
        return {
            'total': round(psutil.virtual_memory().total / number, 2),
            'used': round(psutil.virtual_memory().used / number, 2),
            'free': round(psutil.virtual_memory().available / number, 2),
            'usage': round(psutil.virtual_memory().percent, 2),
        }

    @staticmethod
    def get_sys_info() -> dict:
        """获取服务器信息"""
        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sk.connect(('10.0.0.0', 0))
            ip = sk.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            sk.close()
        return {'name': socket.gethostname(), 'ip': ip, 'os': platform.system(), 'arch': platform.machine()}

    @staticmethod
    def get_disk_info() -> List[dict]:
        """获取磁盘信息"""
        disk_info = []
        for disk in psutil.disk_partitions():
            usage = psutil.disk_usage(disk.mountpoint)
            disk_info.append(
                {
                    'dir': disk.mountpoint,
                    'type': disk.fstype,
                    'device': disk.device,
                    'total': ServerInfo.get_size(usage.total),
                    'free': ServerInfo.get_size(usage.free),
                    'used': ServerInfo.get_size(usage.used),
                    'usage': round(usage.percent, 2),
                }
            )
        return disk_info

    @staticmethod
    def get_service_info():
        """获取服务信息"""
        number = 1024**2
        cur_proc = psutil.Process(os.getpid())
        mem_info = cur_proc.memory_info()
        start_time = datetime.fromtimestamp(cur_proc.create_time())
        return {
            'name': 'Python3',
            'version': platform.python_version(),
            'home': sys.executable,
            'total': round(mem_info.vms / number, 2),
            'max': round(mem_info.vms / number, 2),
            'free': round((mem_info.vms - mem_info.rss) / number, 2),
            'usage': round(mem_info.rss / number, 2),
            'elapsed': ServerInfo.fmt_timedelta(datetime.now() - start_time),
            'startup': start_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
