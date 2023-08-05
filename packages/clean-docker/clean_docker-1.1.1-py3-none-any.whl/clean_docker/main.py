import click
import docker
from docker import DockerClient
from docker.errors import DockerException


def remove_images(client: DockerClient) -> bool:
    images = client.images.list()
    for image in images:
        click.echo(f"rm {image}")
        client.images.remove(image=image.short_id, force=True)
    return bool(images)


def remove_containers(client: DockerClient) -> bool:
    containers = client.containers.list(all=True)
    for container in containers:
        click.echo(f"rm {container}")
        container.remove(force=True)
    return bool(containers)


def remove_volumes(client: DockerClient) -> bool:
    volumes = client.volumes.list()
    for volume in volumes:
        click.echo(f"rm {volume}")
        volume.remove(force=True)
    return bool(volumes)


def remove_networks(client: DockerClient) -> bool:
    ignore_names = ["bridge", "host", "none"]
    networks = client.networks.list()
    network_names = {network.name for network in networks}

    for network in networks:
        if network.name not in ignore_names:
            click.echo(f"rm {network}")
            network.remove()
    return bool(network_names.difference(set(ignore_names)))


def main() -> int:
    try:
        client = docker.from_env()
    except DockerException as err:
        click.echo("Failed to connect to the Docker daemon", err=True)
        click.echo(err)
        return 1

    removed = False
    removed |= remove_images(client)
    removed |= remove_containers(client)
    removed |= remove_volumes(client)
    removed |= remove_networks(client)

    if not removed:
        click.echo("Nothing to remove")

    return 0
