"""Exposes the basic interface to interact with the serialization means."""


import dolon.impl.utils_impl as utils_impl


async def process_message(db, payload):
    await utils_impl.process_message(db, payload)


async def get_latest_trace(app_name):
    return await utils_impl.get_latest_trace(app_name)


async def get_trace(uuid, db=None):
    return await utils_impl.get_trace(uuid, db)

