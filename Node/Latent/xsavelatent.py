import os
import torch
import folder_paths
from comfy.cli_args import args

class XSaveLatent:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "samples": ("LATENT", ),
                "save_path": ("STRING", {"default": "Latents/ComfyUI"}),
                "number_padding": ("BOOLEAN", {"default": True, "label_on": "YES", "label_off": "NO"})
            },

        }

    RETURN_TYPES = ("LATENT", "STRING")
    RETURN_NAMES = ("Latent", "full_path")
    FUNCTION = "save"
    OUTPUT_NODE = True
    CATEGORY = "♾️Xz3r0/Latent"

    def save(self, samples, save_path="ComfyUI", number_padding=True):
        # 获取保存路径信息
        full_output_folder, filename, counter, subfolder, save_path = folder_paths.get_save_image_path(save_path, self.output_dir)
        
        # Ensure path uses forward slashes
        full_output_folder = full_output_folder.replace('\\', '/').replace('/', '/')
        
        # 准备元数据（保持空值）
        metadata = None

        # 根据开关决定是否添加序号
        if number_padding:
            # 带序号行为：防止覆盖，手动查找下一个可用的计数器
            file = self.get_filename_with_counter(full_output_folder, filename)
        else:
            # 不带序号行为：直接覆盖
            file = f"{filename}.latent"

        file_path = os.path.join(full_output_folder, file)
        # Ensure path uses forward slashes
        file_path = file_path.replace('\\', '/').replace('/', '/')

        # 计算相对于输出目录的完整路径
        rel_path = os.path.relpath(file_path, self.output_dir)
        # Ensure path uses forward slashes
        rel_path = rel_path.replace('\\', '/').replace('/', '/')

        output = {}
        output["latent_tensor"] = samples["samples"].contiguous()
        output["latent_format_version_0"] = torch.tensor([])

        # 保存文件
        import comfy.utils
        comfy.utils.save_torch_file(output, file_path, metadata=metadata)
        
        # 返回输出
        return (samples, rel_path)
    
    def get_filename_with_counter(self, full_output_folder, filename):
        # 手动查找下一个可用的计数器
        n = 0
        while True:
            file = f"{filename}_{n:05}.latent"
            # Ensure path uses forward slashes
            check_path = os.path.join(full_output_folder, file).replace('\\', '/').replace('/', '/')
            if not os.path.exists(check_path):
                return file
            n += 1


NODE_CLASS_MAPPINGS = {
    "XSaveLatent": XSaveLatent
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "XSaveLatent": "XSaveLatent"
}