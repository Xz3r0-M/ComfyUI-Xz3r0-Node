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
                    latent_files.append(rel_path)
        
        if not latent_files:
            latent_files = ["No .latent files found in output directory"]
        
        return {
            "required": {
                "filepath": (sorted(latent_files), ),
            },
        }



    CATEGORY = "Xz3r0/Latent"

    RETURN_TYPES = ("LATENT", )
    FUNCTION = "load"

    def load(self, filepath):
        # 确保路径安全（防止路径遍历攻击）
        output_dir = folder_paths.get_output_directory()
        full_path = os.path.join(output_dir, filepath)
        full_path = os.path.normpath(full_path)
        
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
    def IS_CHANGED(s, filepath):
        output_dir = folder_paths.get_output_directory()
        full_path = os.path.join(output_dir, filepath)
        
        # 确保路径安全
        full_path = os.path.normpath(full_path)
        if not full_path.startswith(output_dir):
            raise ValueError("Invalid latent file path")
        
        import time
        return f"{os.path.getmtime(full_path) if os.path.exists(full_path) else time.time()}_{time.time()}"


    @classmethod
    def VALIDATE_INPUTS(s, filepath):
        output_dir = folder_paths.get_output_directory()
        full_path = os.path.join(output_dir, filepath)
        
        # 确保路径安全
        full_path = os.path.normpath(full_path)
        if not full_path.startswith(output_dir):
            return "Invalid latent file path"
        
        if not os.path.exists(full_path):
            return f"Invalid latent file: {filepath}"
        return True