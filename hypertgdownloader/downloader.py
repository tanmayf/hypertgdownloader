import asyncio
import os
from pathlib import Path
from math import ceil
from .clients import ClientManager
from .exceptions import HyperTGDownloadError, CancelledError
from .utils import ensure_directory_exists, get_temp_part_path

class HyperTGDownloader:
    def __init__(self, helper_bots, main_client=None, max_threads=None):
        """
        :param helper_bots: Dict[str, pyrogram.Client] - helper bots for parallel download.
        :param main_client: pyrogram.Client - your main bot (optional, for copying messages).
        :param max_threads: int - number of parallel parts. Defaults to number of helper bots.
        """
        self.client_manager = ClientManager(helper_bots)
        self.main_client = main_client
        self.max_threads = max_threads or max(8, len(helper_bots))
        self.chunk_size = 1024 * 1024  # 1MB

    async def download(self, message, download_dir="downloads", progress_callback=None):
        """
        Download a Telegram media message using helper bots.

        :param message: pyrogram.types.Message
        :param download_dir: Directory to store file
        :param progress_callback: async function(current, total)
        :return: Downloaded file path
        """
        # 1. Get media info
        media = await self._get_media(message)
        file_size = getattr(media, "file_size", 0)
        file_name = getattr(media, "file_name", None) or f"tgfile_{message.id}"
        extension = self._get_extension(media)
        full_name = file_name if file_name.endswith(extension) else f"{file_name}{extension}"
        ensure_directory_exists(download_dir)
        target_path = os.path.join(download_dir, full_name)

        # 2. Decide on parts
        if file_size < 10 * 1024 * 1024:
            num_parts = 1
        else:
            num_parts = min(self.max_threads, max(1, file_size // (10 * 1024 * 1024)))

        part_size = file_size // num_parts if num_parts > 0 else file_size
        ranges = [
            (i * part_size, min((i + 1) * part_size - 1, file_size - 1))
            for i in range(num_parts)
        ]

        # 3. Download all parts
        tasks = []
        self._processed_bytes = 0
        cancel_event = asyncio.Event()

        async def part_worker(idx, start, end):
            nonlocal self
            key = self.client_manager.get_least_loaded()
            client = self.client_manager.clients[key]
            self.client_manager.increase_load(key)
            try:
                offset = start
                local_path = get_temp_part_path(download_dir, full_name, idx)
                async with await self._aiofile_open(local_path, "wb") as f:
                    while offset <= end:
                        if cancel_event.is_set():
                            raise CancelledError("Download cancelled")
                        # Download chunk:
                        chunk = await self._download_chunk(client, message, offset, min(self.chunk_size, end - offset + 1))
                        await f.write(chunk)
                        offset += len(chunk)
                        self._processed_bytes += len(chunk)
                        if progress_callback:
                            await progress_callback(self._processed_bytes, file_size)
                return local_path
            finally:
                self.client_manager.decrease_load(key)

        for idx, (start, end) in enumerate(ranges):
            tasks.append(asyncio.create_task(part_worker(idx, start, end)))

        try:
            temp_files = await asyncio.gather(*tasks)
            # Join files
            async with await self._aiofile_open(target_path, "wb") as outf:
                for temp_file in temp_files:
                    async with await self._aiofile_open(temp_file, "rb") as inf:
                        while True:
                            chunk = await inf.read(8 * 1024 * 1024)
                            if not chunk:
                                break
                            await outf.write(chunk)
                    os.remove(temp_file)
            return target_path
        except Exception as e:
            cancel_event.set()
            raise HyperTGDownloadError(f"Download failed: {e}")

    async def _get_media(self, message):
        # Return the first downloadable media attribute.
        for attr in (
            "audio", "document", "photo", "sticker", "animation", "video", "voice", "video_note"
        ):
            media = getattr(message, attr, None)
            if media:
                return media
        raise HyperTGDownloadError("No downloadable media found in message.")

    def _get_extension(self, media):
        # Guess file extension based on media type.
        mime = getattr(media, "mime_type", None)
        if mime:
            from mimetypes import guess_extension
            ext = guess_extension(mime)
            if ext:
                return ext
        if hasattr(media, "file_name") and "." in media.file_name:
            return os.path.splitext(media.file_name)[1]
        return ".bin"

    async def _download_chunk(self, client, message, offset, length):
        # Uses Pyrogram's raw API to download a chunk. You may need to adapt this for your message types.
        # For demo, we use message.download with offset/limit if available.
        # Replace with your actual chunk logic for best performance!
        # You can adapt your original logic here.
        return await message.download(in_memory=True, offset=offset, limit=length)

    async def _aiofile_open(self, path, mode):
        # aiofiles-like async context manager stub for file IO
        import aiofiles
        return await aiofiles.open(path, mode)
