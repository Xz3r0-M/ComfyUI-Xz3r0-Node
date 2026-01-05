import os
import folder_paths
import safetensors.torch


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
                "filepath_input": ("STRING", {"default": "", "label": "手动输入路径(优先)"}),  # 用于接收来自XSaveLatent的路径
            }
        }


    CATEGORY = "♾️Xz3r0/Latent"

    RETURN_TYPES = ("LATENT", )
    FUNCTION = "load"

    def load(self, filepath, filepath_input=""):
        # 如果提供了filepath_input（来自XSaveLatent的路径），则优先使用它
        if filepath_input and filepath_input.strip() != "":
            # 使用传入的路径
            selected_path = filepath_input
        else:
            # 否则使用下拉菜单选择的路径
            selected_path = filepath
        
        # 确保路径安全（防止路径遍历攻击）
        output_dir = folder_paths.get_output_directory()
        # Ensure output_dir uses forward slashes for comparison
        output_dir = output_dir.replace('\\', '/').replace('/', '/')
        full_path = os.path.join(output_dir, selected_path)
        full_path = os.path.normpath(full_path)
        
        # Ensure path uses forward slashes
        full_path = full_path.replace('\\', '/').replace('/', '/')
        
        if not full_path.startswith(output_dir):
            raise ValueError("Invalid latent file path")
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Latent file not found: {full_path}")
        
        latent = safetensors.torch.load_file(full_path, device="cpu")
        multiplier = 1.0
        if "latent_format_version_0" not in latent:
            multiplier = 1.0 / 0.18215
        samples = {"samples": latent["latent_tensor"].float() * multiplier}
        return (samples, )


    @classmethod
    def IS_CHANGED(s, filepath, filepath_input=""):
        # 如果提供了filepath_input（来自XSaveLatent的路径），则优先使用它
        if filepath_input and filepath_input.strip() != "":
            selected_path = filepath_input
        else:
            selected_path = filepath
        
        output_dir = folder_paths.get_output_directory()
        # Ensure output_dir uses forward slashes for comparison
        output_dir = output_dir.replace('\\', '/').replace('/', '/')
        full_path = os.path.join(output_dir, selected_path)
        
        # 确保路径安全
        full_path = os.path.normpath(full_path)
        # Ensure path uses forward slashes
        full_path = full_path.replace('\\', '/').replace('/', '/')
        if not full_path.startswith(output_dir):
            raise ValueError("Invalid latent file path")
        
        import time
        return f"{os.path.getmtime(full_path) if os.path.exists(full_path) else time.time()}_{time.time()}"


    @classmethod
    def VALIDATE_INPUTS(s, filepath, filepath_input=""):
        # 如果提供了filepath_input（来自XSaveLatent的路径），则优先使用它
        if filepath_input and filepath_input.strip() != "":
            selected_path = filepath_input
        else:
            selected_path = filepath
        
        output_dir = folder_paths.get_output_directory()
        # Ensure output_dir uses forward slashes for comparison
        output_dir = output_dir.replace('\\', '/').replace('/', '/')
        full_path = os.path.join(output_dir, selected_path)
        
        # 确保路径安全
        full_path = os.path.normpath(full_path)
        # Ensure path uses forward slashes
        full_path = full_path.replace('\\', '/').replace('/', '/')
        if not full_path.startswith(output_dir):
            return "Invalid latent file path"
        
        if not os.path.exists(full_path):
            return f"Invalid latent file: {selected_path}"
        return True