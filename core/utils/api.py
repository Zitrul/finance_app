import aiohttp


async def post_image_async(url, file_path, values):
    async with aiohttp.ClientSession() as session:
        with open(file_path, 'rb') as file:
            data = aiohttp.FormData()
            data.add_field('uploaded_file', file, filename='bill.png')

            # 将整个values字典转换为字符串键值对
            for key, value in values.items():
                data.add_field(str(key), str(value))

            async with session.post(url, data=data) as response:
                response_text = await response.text()
                return response_text
