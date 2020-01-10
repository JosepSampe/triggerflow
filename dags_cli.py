#!/usr/bin/env python3
import click
import json
import dags.client as client


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command('make')
@click.argument('dag_def', type=click.File('r'))
@click.option('--output', '-o', help='Resulting dag in json format', type=str)
def cli_make(dag_def, output):
    dag_json = client.make(dag_def.read())
    if output is None:
        print(dag_json)
    else:
        with open(output, 'w') as dagf:
            dagf.write(dag_json)


@cli.command('put')
@click.argument('dag_json', type=click.File('r'))
def cli_put(dag_json):
    status_code, res = client.put(dag_json)
    if status_code == 200:
        pass
    else:
        print('{}: {}'.format(status_code, res))


@cli.command('deploy')
@click.argument('dag_id', type=click.File('r'))
def cli_deploy(dag_id):
    dagrun_id = client.deploy(dag_id)
    if dagrun_id:
        print('dagrun_id: {}'.format(dagrun_id))


@cli.command('run')
@click.argument('dagrun_id', type=str)
def cli_run(dagrun_id):
    status_code, res = client.run(dag_id)
    print('{} {}'.format(status_code, res))


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
