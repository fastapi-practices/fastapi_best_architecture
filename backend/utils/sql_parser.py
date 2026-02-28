import anyio

from anyio import open_file
from sqlparse import split

from backend.common.exception import errors


async def parse_sql_script(filepath: str) -> list[str]:
    """
    解析 SQL 脚本

    :param filepath: 脚本文件路径
    :return:
    """
    path = anyio.Path(filepath)
    if not await path.exists():
        raise errors.NotFoundError(msg='SQL 脚本文件不存在')

    async with await open_file(filepath, encoding='utf-8') as f:
        contents = await f.read(1024)
        while additional_contents := await f.read(1024):
            contents += additional_contents

    statements = [stmt for stmt in split(contents) if stmt.strip()]
    allowed_prefixes = ['select', 'insert', 'set', 'do']
    for statement in statements:
        if not any(statement.strip().lower().startswith(prefix) for prefix in allowed_prefixes):
            raise errors.RequestError(
                msg=f'SQL 脚本 {filepath} 存在非法操作，仅允许：{", ".join(item.upper() for item in allowed_prefixes)}'
            )

    return statements
