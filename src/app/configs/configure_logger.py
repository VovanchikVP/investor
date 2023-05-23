import logging

from fastapi import FastAPI


def configure_logger(app: FastAPI):
    """Setting up logger"""
    logger_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
