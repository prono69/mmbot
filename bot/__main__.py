import logging
from bot import oppai
from pyrogram import __version__
from pyrogram.raw.all import layer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

async def start(self):
	await oppai.start()
	me = await self.get_me()
	un = '@' + me.username
	LOGGER.info(f"Pyrogram v{__version__} (Layer {layer}) started on {un}.")
	
async def stop(self, *args):
	await oppai.stop()
	LOGGER.info('Bot Stopped ! Bye..........')

	
if __name__ == "__main__":
    app = oppai
    app.run()
