import torch


class XMath:
    """
    A node for mathematical calculations supporting both integers and floats
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "operation": (["add (+)", "subtract (-)", "multiply (×)", "divide (÷)", "power (^)", "modulo (%)", "floor_divide", "percentage (%)", "min", "max"], {"default": "add (+)"}),
                "a": ("FLOAT", {"default": 0.0, "min": -2147483648.0, "max": 2147483647.0, "step": 0.01, "display": "number"}),
                "b": ("FLOAT", {"default": 0.0, "min": -2147483648.0, "max": 2147483647.0, "step": 0.01, "display": "number"}),
            },
        }

    RETURN_TYPES = ("FLOAT", "INT")
    RETURN_NAMES = ("FLOAT", "INT")
    FUNCTION = "execute"
    CATEGORY = "♾️Xz3r0/Math"

    def execute(self, operation, a, b):
        # Validate inputs are numeric before conversion
        try:
            a_val = float(a)
        except (ValueError, TypeError):
            raise ValueError(f"Parameter A must be a number, got {type(a).__name__}: {a}")
            
        try:
            b_val = float(b)
        except (ValueError, TypeError):
            raise ValueError(f"Parameter B must be a number, got {type(b).__name__}: {b}")
        
        result = 0.0
        if operation == "add (+)":
            result = a_val + b_val
        elif operation == "subtract (-)":
            result = a_val - b_val
        elif operation == "multiply (×)":
            result = a_val * b_val
        elif operation == "divide (÷)":
            if b_val != 0:
                result = a_val / b_val
            else:
                result = float('inf')  # Return infinity if dividing by zero
        elif operation == "power (^)":
            result = a_val ** b_val
        elif operation == "modulo (%)":
            if b_val != 0:
                result = a_val % b_val
            else:
                result = float('nan')  # Return NaN if modulo by zero
        elif operation == "floor_divide":
            if b_val != 0:
                result = a_val // b_val
            else:
                result = float('inf')
        elif operation == "percentage (%)":
            result = (a_val * b_val) / 100.0
        elif operation == "min":
            result = min(a_val, b_val)
        elif operation == "max":
            result = max(a_val, b_val)
        
        # Return both the original result (as float) and the integer version
        return (result, int(result))


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "XMath": XMath
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "XMath": "XMath"
}