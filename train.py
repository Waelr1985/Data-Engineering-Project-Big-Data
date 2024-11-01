import os
import sys
from skin.exception import SkinException
from skin.pipeline.training_pipeline import TrainPipeline

from skin.constants import *


def training():
    try:
        training_pipeline = TrainPipeline()

        training_pipeline.run_pipeline()

    except Exception as e:
        raise SkinException(e, sys) from e


if __name__ == "__main__":
    training()


