import asyncio


class Dispatcher:
    def __init__(self, eventQueue):
        self.handlers = set()
        self.eventQueue = eventQueue

    def add_handler(self, event, callback):
        self.handlers.add((event, callback))

    def on(self, event):
        def decorator(func):
            self.add_handler(event, func)
            return func

        return decorator

    async def listen(self):
        print("Start listening")
        while True:
            if not self.eventQueue.empty():
                event = await self.eventQueue.get()
                for _event, callback in self.handlers:
                    if isinstance(event, _event):
                        await callback(event)

            await asyncio.sleep(5)
