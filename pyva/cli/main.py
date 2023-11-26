import typer

app = typer.Typer()


@app.callback()
def main():
    """
    PyVa CLI Tool.

    This tool helps you to initialize and manage your PyVa projects.
    """
    typer.echo("Welcome to PyVa CLI!")


@app.command()
def create_project(name: str):
    """
    创建一个PyVa项目
    """

    typer.echo(f"Creating project: {name}")


@app.command()
def create_module(name: str):
    """
    创建一个PyVa模块
    """
    typer.echo(f"Creating module: {name}")


@app.command()
def create_api(name: str):
    """
    创建一个PyVa接口类
    """
    typer.echo(f"Creating api: {name}")


@app.command()
def create_client(name: str):
    """
    创建一个PyVa客户类
    """
    typer.echo(f"Creating client: {name}")


@app.command()
def create_config(name: str):
    """
    创建一个PyVa配置类
    """
    typer.echo(f"Creating config: {name}")


@app.command()
def create_dao(name: str):
    """
    创建一个PyVa数据操作类
    """
    typer.echo(f"Creating dao: {name}")


@app.command()
def create_dto(name: str):
    """
    创建一个PyVa数据转换类
    """
    typer.echo(f"Creating dto: {name}")


@app.command()
def create_entity(name: str):
    """
    创建一个PyVa实体类
    """
    typer.echo(f"Creating entity: {name}")


@app.command()
def create_service(name: str):
    """
    创建一个PyVa服务类
    """
    typer.echo(f"Creating service: {name}")


if __name__ == "__main__":
    app()
