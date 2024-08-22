from typing import Callable, Dict

import fire
import logging
import logging.config

from model.training import train


tasks: Dict[str, Callable] = {
    "training_model": train,
}


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",
        level=logging.DEBUG,
    )

    fire.Fire(tasks)