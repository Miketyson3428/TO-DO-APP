import os
import sys
from typing import Literal, Dict, Optional

import fire


sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from utils.wrapper import StreamDiffusionWrapper

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class MakeImageInfo():
    def __init__(self,
                 output: str = os.path.join(CURRENT_DIR, "..", "..", "images", "outputs", "output.png"),  # 画像を保存する出力画像ファイル
                 model_id_or_path: str = "KBlueLeaf/kohaku-v2.1",  # 画像生成に使用するモデルの名前
                 lora_dict: Optional[Dict[str, float]] = None,  # ロードするlora_dict。デフォルトはNone。キーはLoRAの名前、値はLoRAのスケール
                 prompt: str = "1girl cat",  # 画像を生成するためのプロンプト
                 width: int = 512,  # 画像の幅。デフォルトは512
                 height: int = 512,  # 画像の高さ。デフォルトは512
                 acceleration: Literal["none", "xformers", "tensorrt"] = "xformers",  # 画像生成に使用する加速のタイプ
                 use_denoising_batch: bool = False,  # デノイジングバッチを使用するかどうか。デフォルトはFalse
                 seed: int = 2):  # シード。デフォルトは2
        self.output = output
        self.model_id_or_path = model_id_or_path
        self.lora_dict = lora_dict
        self.prompt = prompt
        self.width = width
        self.height = height
        self.acceleration = acceleration
        self.use_denoising_batch = use_denoising_batch
        self.seed = seed
    

def main(
    image_info: MakeImageInfo
):
    
    """
    Process for generating images based on a prompt using a specified model.

    Parameters
    ----------
    image_info : MakeImageInfo
        The information needed to generate the image.
    """

    stream = StreamDiffusionWrapper(
        model_id_or_path=image_info.model_id_or_path,
        lora_dict=image_info.lora_dict,
        t_index_list=[0, 16, 32, 45],
        frame_buffer_size=1,
        width=image_info.width,
        height=image_info.height,
        warmup=10,
        acceleration=image_info.acceleration,
        mode="txt2img",
        use_denoising_batch=image_info.use_denoising_batch,
        cfg_type="none",
        seed=image_info.seed,
    )

    stream.prepare(
        prompt=image_info.prompt,
        num_inference_steps=50,
    )

    for _ in range(stream.batch_size - 1):
        stream()

    output_image = stream()
    output_image.save(image_info.output)
    return image_info.output

def make_img_fire(*args, **kwargs):
    fire.Fire(main(*args, **kwargs))

if __name__ == "__main__":
    fire.Fire(main)
