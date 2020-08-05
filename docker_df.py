#!/usr/bin/env python2


import docker
import json
import logging
import click


def discovery_containers(data_df=None):
    """
    discover docker containers
    :data_df: docker client.df result
    :return: container list in zabbix discovery format
    """

    assert 'Containers' in data_df, 'data_df must contain "Containers" key'
    assert isinstance(data_df['Containers'], list), '"Containers" key must be list'

    data = []
    for container in data_df['Containers']:
        data.extend([{'{#DOCKER_CONTAINER}': container['Names'][0][1:]}])

    result = {'data': data}
    logging.debug(result)
    return json.dumps(result)


def get_size_images(data_df=None):
    """
    get all docker images size
    """

    assert 'Images' in data_df, 'data_df must contain "Images" key'
    assert isinstance(data_df['Images'], list), '"Images" key must be list'

    logging.debug('data_df: {}'.format(data_df['Images']))
    return sum(map(lambda x: x.get('Size', 0), data_df['Images']))


def get_size_layers(data_df=None):
    """
    get size of docker layers
    """

    assert 'LayersSize' in data_df, 'data_df must contain "LayersSize" key'
    assert isinstance(data_df['LayersSize'], int), '"LayersSize" key must be int'

    return data_df['LayersSize']


def get_docker_df():
    """
    return docker df data
    """

    try:
        client = docker.from_env()
        df = client.df()
    except Exception as e:
        logging.error(e)
        return None

    return df


def get_size_containers(data_df=None):
    """
    get all docker containers size
    """

    assert 'Containers' in data_df, 'data_df must contain "Containers" key'
    assert isinstance(data_df['Containers'], list), '"Containers" key must be list'

    logging.debug('data_df: {}'.format(data_df['Containers']))
    return sum(map(lambda x: x.get('SizeRw', 0), data_df['Containers']))


def get_size_container(container, data_df=None):
    """
    get docker container size
    """

    assert 'Containers' in data_df, 'data_df must contain "Containers" key'
    assert isinstance(data_df['Containers'], list), '"Containers" key must be list'

    logging.debug('data_df: {}'.format(data_df['Containers']))
    return filter(lambda x: x.get('Names', '')[0][1:] == container, data_df['Containers'])[0].get('SizeRw', 0)


@click.command()
@click.option('--log-level', '-l', help='Log level', default='info')
@click.option('--discovery', '-D', help='Discvoery containers', default=False, is_flag=True)
@click.option('--size-containers', '-sc', help='Get size of all containers', default=False, is_flag=True)
@click.option('--size-images', '-si', help='Get size of all images', default=False, is_flag=True)
@click.option('--size-layers', '-sl', help='Get size of all layers', default=False, is_flag=True)
@click.option('--size-container', '-c', help='Get size of container', default='')
def main(log_level, discovery, size_containers, size_images, size_layers, size_container):

    # setup logging
    try:
        level = getattr(logging, log_level.upper())
        logging.basicConfig(level=level)
    except Exception as e:
        print('ERROR: {}'.format(e))

    data_df = get_docker_df()
    #logging.debug('data_df: {}'.format(data_df))
    assert isinstance(data_df, dict), 'data_df must be dict'

    if discovery:
        data = discovery_containers(data_df)
    elif size_containers:
        data = get_size_containers(data_df)
    elif size_images:
        data = get_size_images(data_df)
    elif size_layers:
        data = get_size_layers(data_df)
    elif size_container:
        data = get_size_container(size_container, data_df)
    else:
        return 'rtfm'

    print data


if __name__ == '__main__':
    main()

