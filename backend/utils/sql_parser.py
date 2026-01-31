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

    statements = split(contents)
    for statement in statements:
        if not any(statement.lower().startswith(_) for _ in ['select', 'insert']):
            raise errors.RequestError(msg='SQL 脚本文件中存在非法操作，仅允许 SELECT 和 INSERT')

    return statements
