# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

from veadk import Agent
from veadk.runner import Runner
from veadk.tools.builtin_tools.web_search import web_search
from veadk.tools.builtin_tools.image_generate import image_generate
from veadk.tools.builtin_tools.video_generate import video_generate

video_generator = Agent(
    name="video_generator",
    description="视频生成 Agent",
    instruction="你是一个原子化的 Agent，具备视频生成能力，每次执行完毕后，考虑回到主 Agent。",
    tools=[video_generate],
)

image_generator = Agent(
    name="image_generator",
    description="图像生成 Agent",
    instruction="你是一个原子化的 Agent，具备图像生成能力，每次执行完毕后，考虑回到主 Agent。",
    tools=[image_generate],
)

root_agent = Agent(
    name="eposide_generator",
    description="调用子Agents生成图片或者视频",
    instruction="""你可以根据用户输入的一段小文字来生成视频或者生成图片""",
    sub_agents=[image_generator, video_generator],
    tools=[web_search],
)
runner = Runner(agent=root_agent)


async def main(prompts: list[str]):
    session_id = uuid.uuid4().hex
    for prompt in prompts:
        response = await runner.run(
            messages=prompt,
            session_id=session_id,
        )
        print(response)


if __name__ == "__main__":
    import asyncio

    response = asyncio.run(
        main(
            [
                "请生成古文片段 落霞与孤鹜齐飞，秋水共长天一色 的首帧图片",
                "刚才的首帧图，生成视频。",
            ]
        )
    )
