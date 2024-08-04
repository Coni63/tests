import pandas as pd
from sqlalchemy import create_engine
import yaml
import click
from loguru import logger
import time

def run_transfert(source_conn_str: str, target_conn_str: str, query: str, target_table: str, mode: str) -> bool:
    try:
        source_engine = create_engine(source_conn_str)
        target_engine = create_engine(target_conn_str)
        logger.info(f"Created engine for {source_conn_str} and {target_conn_str}")
    except Exception as e:
        logger.error(f"Error while creating engine: {e}")
        return False

    try:
        logger.info("Starting transfert")
        tic = time.time()
        pd.read_sql(query, source_engine).to_sql(target_table, target_engine, if_exists=mode, index=False, method='multi')
        elapsed_time = time.time() - tic
        logger.info(f"Transfert done in {elapsed_time:.2f} seconds")
        return True
    except Exception as e:
        logger.error(f"Error while transfert: {e}")
        return False
    finally:
        logger.info(f"Closing connection {source_conn_str} and {target_conn_str}")
        source_engine.dispose()
        target_engine.dispose()


@click.argument("stage", type=str)
@click.command()
def main(stage):
    logger.info("Loading config.yaml")
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    stages = config["stages"]

    if stage not in stages:
        logger.error(f"Stage {stage} not existing in the given configuration")

    return run_transfert(**stages[stage])


if __name__ == "__main__":
    worked = main()
    if worked:
        exit(0)
    else:
        exit(1)