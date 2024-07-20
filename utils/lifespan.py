from contextlib import asynccontextmanager

from fastapi import FastAPI

from kafka import close_kafka_producer, init_kafka_producer


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_kafka_producer()

    yield

    await close_kafka_producer()
