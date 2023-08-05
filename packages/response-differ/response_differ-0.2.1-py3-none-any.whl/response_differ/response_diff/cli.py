import click
import yaml
from click import pass_context

from ..Config_store import Serialize
from ..cheks import check_diff_responses
from ..exceptions import get_grouped_exception
from ..play import replay, Replayed


def bold(message):
    return click.style(message, bold=True)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option()
def differ():
    """Command line tool for testing your web application"""
    #if custom_serializer:
    #    DDDDDD = custom_serializer
    #    Serialize.custom_serializer_path.append(custom_serializer)


#@click.pass_context
@differ.command()
#@click.option("cassette_path", type=click.Path(exists=True))
@click.argument("cassette_path", type=str)
@click.option("--uri", help="A regexp that filters interactions by their request URI.", required=False, type=str)
@click.option("--host", help="HOST.", required=False, type=str, default='')
@click.option("--protocol", help="protocol", required=False, type=str)
@click.option("--diff", '-d',  help="Comparing new response with the old", required=False, type=bool)
@click.option("--status", '-s',  help="Status code", required=False, type=int)
@click.option("--ignore_body", '-ib',  help="ignore body", required=False, type=str)
@click.option("--config", '-c',  help="Comparing new response with the old", required=False, type=click.Path())
@click.option("--custom_serializer", '-cs',  help="Custom serializer", required=False, type=click.Path())
def run(cassette_path, status=None, host='', diff=False, config=None, custom_serializer=None, ignore_body=None, protocol='http'):
    click.secho(f"{bold('Replaying cassette')}: {cassette_path}")
    if custom_serializer:
        Serialize.custom_serializer_path.append(custom_serializer)

    #click.secho(f"{bold('Total interactions')}: {len(cassette['interactions'])}\n")
    for replayed in replay(cassette_path=cassette_path, ignore_body=ignore_body, host=host, status=status, protocol=protocol, diff=diff):

        pass
        click.secho(f"  {bold('ID')}              | {replayed.id}")
        click.secho(f"  {bold('URI')}             | {replayed.request.uri}")
        if hasattr(replayed, 'response'):
            click.secho(f"  {bold('Old status code')} | {replayed.cass_response['status']['code']}")
        if hasattr(replayed, 'response'):
            click.secho(f"  {bold('New status code')} | {replayed.response.status_code}")
        #click.secho(f"  {bold('Old request')}     | {replayed.interaction['request']}")
        #if hasattr(replayed, 'response'):
        #    click.secho(f"  {bold('New request')}     | {replayed.response.request.body}\n")
        if diff:
            with open(config) as fd2:
                Replayed.config = yaml.load(fd2, Loader=yaml.SafeLoader)
            check_diff_responses(replayed)
    if Replayed.errors:
        for error in Replayed.errors:
            click.secho(error)
        raise AssertionError
    #if diff:
    #    with open(config) as fd2:
    #        Replayed.config =yaml.load(fd2, Loader=yaml.SafeLoader)
    #    check_diff_responses()
