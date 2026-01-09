import os
import folder_paths
import safetensors.torch
import time


class XLoadLatent:
    @classmethod
    def INPUT_TYPES(s):
        # 获取输出目录中的所有latent文件
        latent_extensions = ['.latent', '.safetensors']
        latent_files = []
        output_dir = folder_paths.get_output_directory()
        
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() in latent_extensions:
                    rel_path = os.path.relpath(os.path.join(root, file), output_dir)
                    # Ensure path uses forward slashes
                    rel_path = rel_path.replace('\\', '/').replace('/', '/')
                    latent_files.append(rel_path)
        
        if not latent_files:
            latent_files = ["No .latent files found in output directory"]
        
        return {
            "required": {
                "filepath": (sorted(latent_files), ),
            },
            "optional": {
                "filepath_input": ("STRING", {"default": "", "label": "自定义路径和文件名(优先)"}),  # 用于接收来自XSaveLatent的路径
            }
        }


    CATEGORY = "♾️Xz3r0/Latent"

    RETURN_TYPES = ("LATENT", )
    FUNCTION = "load"
    
    @classmethod
    def _resolve_filepath(cls, filepath, filepath_input):
        """解析文件路径，优先使用filepath_input，如果不存在则尝试使用filepath作为回退"""
        output_dir = folder_paths.get_output_directory()
        output_dir = output_dir.replace('\\', '/').replace('/', '/')
        
        # 如果提供了filepath_input（来自XSaveLatent的路径），则优先使用它
        if filepath_input is not None and filepath_input and filepath_input.strip() != "":
            selected_path = filepath_input
        else:
            # 否则使用下拉菜单选择的路径
            selected_path = filepath
        
        full_path = os.path.join(output_dir, selected_path)
        full_path = os.path.normpath(full_path)
        full_path = full_path.replace('\\', '/').replace('/', '/')
        
        # 检查文件是否存在，如果不存在则尝试使用下拉菜单路径
        if not os.path.exists(full_path):
            # 如果是使用了输入连接的路径不存在，尝试回退到下拉菜单路径
            if filepath_input is not None and filepath_input and filepath_input.strip() != "":
                # 使用输入连接的路径失败，尝试使用下拉菜单路径
                fallback_full_path = os.path.join(output_dir, filepath)
                fallback_full_path = os.path.normpath(fallback_full_path)
                fallback_full_path = fallback_full_path.replace('\\', '/').replace('/', '/')
                
                if os.path.exists(fallback_full_path) and fallback_full_path.startswith(output_dir):
                    return fallback_full_path  # 返回回退路径
                else:
                    # 两个路径都无效
                    return None, f"Latent file not found: {full_path} (and fallback path also invalid)"
            else:
                # 没有使用输入连接，直接使用下拉菜单路径
                return None, f"Latent file not found: {full_path}"
        
        # 检查路径安全性
        if not full_path.startswith(output_dir):
            return None, "Invalid latent file path"
        
        return full_path, None  # 返回有效路径和无错误

    def load(self, filepath, filepath_input=""):
        # 使用辅助方法解析路径
        result_path, error_msg = self._resolve_filepath(filepath, filepath_input)
        
        if result_path is None:
            raise FileNotFoundError(error_msg)
        
        latent = safetensors.torch.load_file(result_path, device="cpu")
        multiplier = 1.0
        if "latent_format_version_0" not in latent:
            multiplier = 1.0 / 0.18215
        samples = {"samples": latent["latent_tensor"].float() * multiplier}
        return (samples, )


    @classmethod
    def IS_CHANGED(s, filepath, filepath_input=""):
        # 使用辅助方法解析路径
        result_path, error_msg = s._resolve_filepath(filepath, filepath_input)
        
        if result_path is None:
            # 如果路径无效，返回时间戳表示已更改
            return f"{time.time()}_file_not_found"
        
        return f"{os.path.getmtime(result_path) if os.path.exists(result_path) else time.time()}_{time.time()}"


    @classmethod
    def VALIDATE_INPUTS(s, filepath, filepath_input=""):
        # 使用辅助方法解析路径
        result_path, error_msg = s._resolve_filepath(filepath, filepath_input)
        
        if result_path is None:
            return error_msg  # 返回错误信息
        
        return True