
import typer
import uvicorn
from fastapi_migrations.cli import MigrationsCli
from services_reviews.platform_data_aggregator.main import platform_data_aggregator
from services_reviews.sending_message_service.main import sending_message_service
# pylint: disable=unused-import
from services_reviews.common_api.Api import CommonApi, conf_common_api

common_cli: typer.Typer = typer.Typer()


common_cli.add_typer(MigrationsCli())


@common_cli.command()
def runserver() -> None:
    uvicorn.run('services_reviews.common_cli:CommonApi', host=conf_common_api.get('fastapi', 'HOST'), port=int(conf_common_api.get('fastapi', 'PORT')), reload=True)


@common_cli.command()
def aggregator() -> None:
    platform_data_aggregator()


@common_cli.command()
def message_sender() -> None:
    sending_message_service()
