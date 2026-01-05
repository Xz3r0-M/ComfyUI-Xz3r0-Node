class XSize:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {
                    "default": 1024,
                    "min": 64,
                    "max": 8192,
                    "step": 8,
                    "display": "number"
                }),
                "height": ("INT", {
                    "default": 768,
                    "min": 64,
                    "max": 8192,
                    "step": 8,
                    "display": "number"
                }),
                "swap_dimensions": ("BOOLEAN", {"default": False, "label_on": "YES", "label_off": "NO"})
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("Width", "Height")
    FUNCTION = "execute"
    CATEGORY = "♾️Xz3r0/Resolution"

    def execute(self, width, height, swap_dimensions):
        result_width = width
        result_height = height

        # 如果需要交换宽高，则交换它们
        if swap_dimensions:
            result_width, result_height = result_height, result_width
        
        return (result_width, result_height)