import os
import json
import numpy as np
from datetime import datetime
import folder_paths
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import time


class XImageSave:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                "use_custom_path": ("BOOLEAN", {"default": False}),
                "folder": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Enter folder name or leave empty to use default"
                }),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "Xz3r0/Image"

    def save_images(self, images, filename_prefix="ComfyUI", use_custom_path=False, folder="", prompt=None, extra_pnginfo=None):
        # Process filename prefix with tokens
        filename_prefix = self.replace_tokens(filename_prefix, prompt)
        
        # Determine save directory
        if use_custom_path and folder and folder.strip():
            # Use folder as subfolder within output directory for security
            # ComfyUI restricts saving to subdirectories of the output folder
            subfolder_path = folder.strip().replace('\\', '/').rstrip('/')
            save_dir = os.path.join(self.output_dir, subfolder_path)
            try:
                # Ensure path uses OS-appropriate separators
                save_dir = os.path.normpath(save_dir)
                os.makedirs(save_dir, exist_ok=True)
                
                # Process images with the custom folder path
                # Get the basic save parameters without subfolder to ensure correct path handling
                full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
                    filename_prefix, save_dir, images[0].shape[1], images[0].shape[0]
                )
            except Exception as e:
                print(f"Warning: Could not create or access subdirectory {subfolder_path}, using default: {e}")
                full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
                    filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0]
                )
        else:
            # Use default path
            full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
                filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0]
            )
        
        results = list()
        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            # Prepare metadata
            metadata = PngInfo()
            if prompt is not None:
                metadata.add_text("prompt", json.dumps(prompt))
            if extra_pnginfo is not None:
                for x in extra_pnginfo:
                    metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            # Generate filename with timestamp and counter
            file = f"{filename}_{counter:05}_.png"
            file_path = os.path.join(full_output_folder, file)

            # Save directly to target location
            try:
                img.save(file_path, compress_level=self.compress_level, pnginfo=metadata)
                print(f"Saved image to: {file_path}")
                results.append({
                    "filename": file,
                    "subfolder": subfolder_path if use_custom_path and folder and folder.strip() else subfolder,
                    "type": self.type
                })
            except Exception as e:
                print(f"Error saving image to {file_path}: {e}")
            
            counter += 1

        return {"ui": {"images": results}}
    
    def replace_tokens(self, text, prompt=None):
        """Replace tokens in the text with actual values"""
        # Replace date tokens (YYYY-MM-DD format)
        now = datetime.now()
        text = text.replace("%date%", now.strftime("%Y-%m-%d"))
        text = text.replace("%Y%", str(now.year))
        text = text.replace("%m%", now.strftime("%m"))
        text = text.replace("%d%", now.strftime("%d"))
        
        # Replace time tokens
        text = text.replace("%time%", now.strftime("%H-%M-%S"))
        text = text.replace("%H%", now.strftime("%H"))
        text = text.replace("%M%", now.strftime("%M"))
        text = text.replace("%S%", now.strftime("%S"))
        
        # Replace timestamp
        text = text.replace("%timestamp%", str(int(time.time())))
        
        # Extract seed from prompt if available
        if prompt and isinstance(prompt, dict):
            # Look for common node types that might contain seed information
            for node_id, node_info in prompt.items():
                if isinstance(node_info, dict) and 'inputs' in node_info:
                    inputs = node_info['inputs']
                    # Common seed parameter names
                    for seed_param in ['seed', 'noise_seed', 'start_seed', 'seed_value', 'initial_seed']:
                        if seed_param in inputs:
                            text = text.replace("%seed%", str(inputs[seed_param]))
                            break  # Only replace once
                    
                    # Look for special sampler nodes that may contain seeds
                    if node_info.get('class_type', '').lower().find('sampler') != -1:
                        for seed_param in ['seed', 'noise_seed']:
                            if seed_param in inputs:
                                text = text.replace("%seed%", str(inputs[seed_param]))
                                break
        
        return text


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "XImageSave": XImageSave
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "XImageSave": "X Image Save"
}