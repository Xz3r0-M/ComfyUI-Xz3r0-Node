import os
import subprocess
import sys
import time
import tempfile
from datetime import datetime
import numpy as np
import folder_paths
from PIL import Image
from comfy_api.latest import ComfyExtension, io, ui, Input, InputImpl, Types
from comfy.cli_args import args
from typing_extensions import override


class XVideoSave(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="XVideoSave",
            display_name="X Video Save",
            category="♾️Xz3r0/Video",
            description="Saves the input images as a video file with preview.",
            inputs=[
                io.Image.Input("images", tooltip="The images to save as video."),
                io.String.Input("filename_prefix", default="ComfyUI_Video", tooltip="The prefix for the video file name."),
                io.Int.Input("fps", default=30, min=1, max=240, step=1, tooltip="Frames per second for the output video."),
                io.Boolean.Input("use_custom_folder", default=False, label_on="YES", label_off="NO", tooltip="Whether to save in a custom folder."),
                io.String.Input("folder", default="", multiline=False, placeholder="Enter folder name or leave empty to use default", optional=True, tooltip="Custom folder name for saving video."),
            ],
            hidden=[io.Hidden.prompt, io.Hidden.extra_pnginfo],
            outputs=[
                io.String.Output(display_name="Saved Path"),
            ],
            is_output_node=True,
        )

    @classmethod
    def execute(cls, images, filename_prefix="ComfyUI_Video", fps=30, use_custom_folder=False, folder=None, prompt=None, extra_pnginfo=None):
        # Process filename prefix with tokens
        filename_prefix = cls.replace_tokens(filename_prefix, prompt)
        
        output_dir = folder_paths.get_output_directory()
        type = "output"
        
        # Determine save directory
        if use_custom_folder and folder and folder.strip():
            # Use folder as subfolder within output directory for security
            subfolder_path = folder.strip().replace('\\', '/').replace('/', '/').rstrip('/')
            save_dir = os.path.join(output_dir, subfolder_path)
                    
            try:
                # Ensure path uses OS-appropriate separators
                save_dir = os.path.normpath(save_dir)
                os.makedirs(save_dir, exist_ok=True)
            except Exception as e:
                print(f"Warning: Could not create or access subdirectory {subfolder_path}, using default: {e}")
                save_dir = output_dir
        else:
            save_dir = output_dir
        
        # Create temporary directory for image sequence
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save images as sequence in temp directory
            for i, image in enumerate(images):
                i_tensor = 255. * image.cpu().numpy()
                img = Image.fromarray(np.clip(i_tensor, 0, 255).astype(np.uint8))
                
                # Save image as PNG in temporary directory
                temp_filename = f"frame_{i+1:05d}.png"  # Start from 1 instead of 0
                temp_path = os.path.join(temp_dir, temp_filename)
                img.save(temp_path)
            
            final_filename = f"{filename_prefix}.mkv"
            video_path = os.path.join(save_dir, final_filename)
            
            # Ensure path uses OS-appropriate separators
            video_path = os.path.normpath(video_path)
            
            # Use FFmpeg to create lossless video
            success = cls.create_video_with_ffmpeg_v3(
                temp_dir, 
                video_path, 
                fps
            )
            
            if not success:
                raise Exception("Failed to create video with FFmpeg")
        
        # Calculate relative path from output directory
        base_output_dir = folder_paths.get_output_directory()
        relative_path = os.path.relpath(os.path.dirname(video_path), base_output_dir)
        
        # Format path with forward slashes
        if relative_path != '.':
            output_path = f"{os.path.basename(base_output_dir)}/{relative_path}/{os.path.basename(video_path)}"
        else:
            output_path = f"{os.path.basename(base_output_dir)}/{os.path.basename(video_path)}"
        
        output_path = output_path.replace('\\', '/').replace('/', '/')
        
        # Prepare video preview information
        subfolder = os.path.dirname(video_path)[len(output_dir):].strip(os.sep)
        
        # Format the video URL for preview
        video_info = ui.SavedResult(
            os.path.basename(video_path),
            subfolder,
            io.FolderType.output
        )
        
        return io.NodeOutput(
            output_path,
            ui=ui.PreviewVideo([video_info])
        )

    @classmethod
    def replace_tokens(cls, text, prompt=None):
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

    @classmethod
    def create_video_with_ffmpeg_v3(cls, input_dir, output_path, fps):
        """Create video using FFmpeg with lossless settings"""
        # First try to use system FFmpeg
        ffmpeg_cmd = cls.get_ffmpeg_command_v3()
        if not ffmpeg_cmd:
            # If system FFmpeg not found, try using imageio-ffmpeg
            try:
                import imageio_ffmpeg
                ffmpeg_cmd = imageio_ffmpeg.get_ffmpeg_exe()
            except ImportError:
                # If imageio-ffmpeg not available, try with python-ffmpeg
                try:
                    import ffmpeg
                    # For python-ffmpeg, we'll build the command differently
                    return cls.create_video_with_python_ffmpeg_v3(input_dir, output_path, fps)
                except ImportError:
                    raise Exception("Neither system FFmpeg nor imageio-ffmpeg is available. Please install either FFmpeg or imageio-ffmpeg.")
        
        # Build FFmpeg command for system/imageio-ffmpeg
        cmd = [
            ffmpeg_cmd,
            '-y',  # Overwrite output file if it exists
            '-r', str(fps),  # Input framerate
            '-f', 'image2',  # Input format
            '-i', os.path.join(input_dir, 'frame_%05d.png'),  # Input pattern
            '-c:v', 'libx265',  # Video codec (H.265/HEVC)
            '-crf', '0',  # Lossless compression
            '-preset', 'fast',  # Encoding speed preset
            '-pix_fmt', 'yuv444p10le',  # Pixel format
            '-vtag', 'hvc1',  # For compatibility
            output_path  # Output file
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"FFmpeg error: {result.stderr}")
                return False
            return True
        except Exception as e:
            print(f"Error running FFmpeg: {e}")
            return False

    @classmethod
    def get_ffmpeg_command_v3(cls):
        """Check if system FFmpeg is available"""
        try:
            # Try to run FFmpeg to check if it's in PATH
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            if result.returncode == 0:
                return 'ffmpeg'
        except FileNotFoundError:
            pass
        
        # On Windows, FFmpeg might be installed in a different location
        if sys.platform.startswith('win'):
            # Try common Windows FFmpeg locations
            possible_paths = [
                'ffmpeg.exe',
                os.path.expanduser('~/ffmpeg/bin/ffmpeg.exe'),
                'C:/ffmpeg/bin/ffmpeg.exe'
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    try:
                        result = subprocess.run([path, '-version'], capture_output=True, text=True)
                        if result.returncode == 0:
                            return path
                    except:
                        continue
        
        return None

    @classmethod
    def create_video_with_python_ffmpeg_v3(cls, input_dir, output_path, fps):
        """Create video using python-ffmpeg as fallback"""
        try:
            import ffmpeg
            
            # Build the FFmpeg command using python-ffmpeg
            stream = ffmpeg.input(
                os.path.join(input_dir, 'frame_%05d.png'),
                framerate=fps,
                f='image2'
            )
            stream = ffmpeg.output(
                stream,
                output_path,
                vcodec='libx265',
                crf=0,  # Lossless
                preset='fast',
                pix_fmt='yuv444p10le',
                vtag='hvc1'
            )
            
            # Run the command
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            return True
        except Exception as e:
            print(f"Error with python-ffmpeg: {e}")
            return False


class VideoExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            XVideoSave,
        ]


async def comfy_entrypoint() -> VideoExtension:
    return VideoExtension()