import click
import logging
from aef_gw.aef_gw import aef_gw


# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aef_gw_cli")


@click.group()
def cli():
    """CLI para gestionar Aef_gw"""
    pass


@cli.command()
@click.argument("northbound_yaml", default="./northbound.yaml", type=click.Path(exists=True))
@click.argument("southbound_yaml", default="./southbound.yaml", type=click.Path(exists=True))
def start(northbound_yaml, southbound_yaml):
    """Inicia el gateway con los archivos YAML especificados."""
    logger.info(f"Starting Aef_gw with {northbound_yaml} and {southbound_yaml}")
    try:
        gw = aef_gw(northbound_yaml, southbound_yaml)
        gw.start()
        logger.info("Aef_gw started successfully.")
    except Exception as e:
        logger.error(f"Failed to start Aef_gw: {e}")


@cli.command()
@click.argument("northbound_yaml", default="./northbound.yaml", type=click.Path(exists=True))
@click.argument("southbound_yaml", default="./southbound.yaml", type=click.Path(exists=True))
def run(northbound_yaml, southbound_yaml):
    """Ejecuta el gateway sin inicializarlo."""
    logger.info(f"Running Aef_gw with {northbound_yaml} and {southbound_yaml}")
    try:
        gw = aef_gw(northbound_yaml, southbound_yaml)
        gw.run()
        logger.info("Aef_gw is running.")
    except Exception as e:
        logger.error(f"Failed to run Aef_gw: {e}")


@cli.command()
@click.argument("northbound_yaml", default="./northbound.yaml", type=click.Path(exists=True))
@click.argument("southbound_yaml", default="./southbound.yaml", type=click.Path(exists=True))
def remove(northbound_yaml, southbound_yaml):
    """Elimina todos los recursos y apaga el gateway."""
    logger.info(f"Removing Aef_gw with {northbound_yaml} and {southbound_yaml}")
    try:
        gw = aef_gw(northbound_yaml, southbound_yaml)
        gw.remove()
        logger.info("Aef_gw resources removed successfully.")
    except Exception as e:
        logger.error(f"Failed to remove Aef_gw: {e}")


def main():
    cli()
