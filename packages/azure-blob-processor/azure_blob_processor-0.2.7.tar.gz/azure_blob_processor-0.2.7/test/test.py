import asyncio
from pathlib import Path
from aiofile import async_open
from azure_blob_processor import Decompressor

# constants
CONTAINER_NAME = "dhub"
COMPANY_NAME = "att"
CONNECT_STR = "DefaultEndpointsProtocol=https;AccountName=mndhubdl;AccountKey=tBI5ZQyJO14m4JpqjBmaeullZCsuPTRyu2Uq/UqAHK1yxX4eisGoFfgNl/DOYHsUgOcV0omLuPMFyM16G1yzpA==;EndpointSuffix=core.windows.net"

async def main():
    local_temp_dir = "{}/{}".format(".", COMPANY_NAME) 
    decompressor = Decompressor(CONNECT_STR)
    await decompressor.process_blob_files("dhub", "raw", "curated", local_temp_dir)

if __name__ == '__main__':
    asyncio.run(main())