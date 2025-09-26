import json

def load_config_from_json(filename):
    """Load configuration from a JSON file."""
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filename}'.")
        return None

def color_name_to_rgb(color_name):
    """Convert color name to RGB tuple."""
    color_map = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'purple': (128, 0, 128),
        'orange': (255, 165, 0),
        'pink': (255, 192, 203),
        'brown': (165, 42, 42),
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'gray': (128, 128, 128),
        'grey': (128, 128, 128),
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255),
        'lime': (0, 255, 0),
        'navy': (0, 0, 128),
        'maroon': (128, 0, 0),
        'olive': (128, 128, 0),
        'teal': (0, 128, 128),
        'silver': (192, 192, 192)
    }
    
    color_name = color_name.lower().strip()
    return color_map.get(color_name)

def get_label_color(config):
    """Get label color from config and return RGB tuple for graphics.Color()."""
    if 'label_color' in config:
        return color_name_to_rgb(config['label_color'])
    return None

def get_time_color(config):
    """Get time color from config and return RGB tuple for graphics.Color()."""
    if 'time_color' in config:
        return color_name_to_rgb(config['time_color'])
    return None

def get_all_colors(config):
    """Get all colors from config."""
    colors = {}
    
    label_rgb = get_label_color(config)
    if label_rgb:
        colors['label_color'] = label_rgb
    
    time_rgb = get_time_color(config)
    if time_rgb:
        colors['time_color'] = time_rgb
    
    return colors

def main():
    # Specify the JSON filename
    json_filename = 't0.json'  # Change this to your file name
    
    # Load configuration from JSON file
    config = load_config_from_json(json_filename)
    
    if config is None:
        return
    
    print("Configuration loaded:")
    print(f"t0: {config.get('t0', 'Not specified')}")
    print("-" * 40)
    
    # Get colors
    label_rgb = get_label_color(config)
    time_rgb = get_time_color(config)
    
    print("Color conversions:")
    if label_rgb:
        print(f"label_color = graphics.Color({label_rgb[0]}, {label_rgb[1]}, {label_rgb[2]})")
    else:
        print("label_color: Not found or unknown color")
    
    if time_rgb:
        print(f"time_color = graphics.Color({time_rgb[0]}, {time_rgb[1]}, {time_rgb[2]})")
    else:
        print("time_color: Not found or unknown color")

# Utility functions for direct use in your code
def load_colors(filename):
    """Load and return all colors from JSON config file."""
    config = load_config_from_json(filename)
    if config:
        return get_all_colors(config)
    return {}

def create_graphics_colors(filename):
    """Create graphics.Color objects from JSON config."""
    config = load_config_from_json(filename)
    if not config:
        return None, None
    
    label_rgb = get_label_color(config)
    time_rgb = get_time_color(config)
    
    return label_rgb, time_rgb

if __name__ == "__main__":
    main()
    
    # Example usage for your specific case
    print("\nExample usage in your code:")
    print("# Load colors from JSON")
    print("label_rgb, time_rgb = create_graphics_colors('config.json')")
    print("if label_rgb:")
    print("    label_color = graphics.Color(*label_rgb)")
    print("if time_rgb:")
    print("    time_color = graphics.Color(*time_rgb)")
    
    # Demonstrate with your actual data
    config = {
        "t0": "2025-10-31T00:00:00.000000",
        "label_color": "purple",
        "time_color": "orange"
    }
    
    print("\nWith your JSON data:")
    label_rgb = get_label_color(config)
    time_rgb = get_time_color(config)
    print(f"Purple (label): {label_rgb} -> graphics.Color({label_rgb[0]}, {label_rgb[1]}, {label_rgb[2]})")
    print(f"Orange (time): {time_rgb} -> graphics.Color({time_rgb[0]}, {time_rgb[1]}, {time_rgb[2]})")
