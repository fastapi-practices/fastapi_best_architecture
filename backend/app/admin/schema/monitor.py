from pydantic import Field

from backend.common.schema import SchemaBase


class CpuInfo(SchemaBase):
    """CPU 信息"""

    physical_num: int = Field(description='物理核心数')
    logical_num: int = Field(description='逻辑核心数')
    max_freq: float = Field(description='最大频率（MHz）')
    min_freq: float = Field(description='最小频率（MHz）')
    current_freq: float = Field(description='当前频率（MHz）')
    usage: float = Field(description='使用率（%）')


class MemInfo(SchemaBase):
    """内存信息"""

    total: float = Field(description='总容量（GB）')
    used: float = Field(description='已使用（GB）')
    free: float = Field(description='可用（GB）')
    usage: float = Field(description='使用率（%）')


class SysInfo(SchemaBase):
    """系统信息"""

    name: str = Field(description='主机名')
    os: str = Field(description='操作系统')
    ip: str = Field(description='IP 地址')
    arch: str = Field(description='系统架构')


class DiskInfo(SchemaBase):
    """磁盘信息"""

    dir: str = Field(description='挂载点')
    device: str = Field(description='设备名称')
    type: str = Field(description='文件系统类型')
    total: str = Field(description='总容量')
    used: str = Field(description='已使用')
    free: str = Field(description='可用')
    usage: str = Field(description='使用率（%）')


class ServiceInfo(SchemaBase):
    """服务进程信息"""

    name: str = Field(description='服务名称')
    version: str = Field(description='版本')
    home: str = Field(description='安装路径')
    startup: str = Field(description='启动时间')
    elapsed: str = Field(description='运行时长')
    cpu_usage: str = Field(description='CPU 使用率')
    mem_vms: str = Field(description='虚拟内存')
    mem_rss: str = Field(description='物理内存')
    mem_free: str = Field(description='可用内存')


class ServerMonitorInfo(SchemaBase):
    """服务器监控信息"""

    cpu: CpuInfo = Field(description='CPU 信息')
    mem: MemInfo = Field(description='内存信息')
    sys: SysInfo = Field(description='系统信息')
    disk: list[DiskInfo] = Field(description='磁盘信息')
    service: ServiceInfo = Field(description='服务信息')


class RedisServerInfo(SchemaBase):
    """Redis 服务器信息"""

    redis_version: str = Field(description='版本号')
    redis_mode: str = Field(description='运行模式')
    role: str = Field(description='节点角色')
    tcp_port: str = Field(description='监听端口')
    uptime: str = Field(description='运行时长')
    connected_clients: str = Field(description='已连接客户端数')
    blocked_clients: str = Field(description='阻塞客户端数')
    used_memory_human: str = Field(description='已使用内存')
    used_memory_rss_human: str = Field(description='RSS 内存')
    maxmemory_human: str = Field(description='最大内存限制')
    mem_fragmentation_ratio: str = Field(description='内存碎片率')
    instantaneous_ops_per_sec: str = Field(description='每秒操作数')
    total_commands_processed: str = Field(description='命令处理总数')
    rejected_connections: str = Field(description='拒绝连接数')
    keys_num: str = Field(description='键总数')


class RedisCommandStat(SchemaBase):
    """Redis 命令统计"""

    name: str = Field(description='命令名称')
    value: str = Field(description='调用次数')


class RedisMonitorInfo(SchemaBase):
    """Redis 监控信息"""

    info: RedisServerInfo = Field(description='服务器信息')
    stats: list[RedisCommandStat] = Field(description='命令统计')
