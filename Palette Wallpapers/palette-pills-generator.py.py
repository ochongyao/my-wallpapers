from PIL import Image, ImageDraw
import time
import os

# --- 1. CONFIGURATION & PALETTES ---

PALETTES = {
    # --- The Classics ---
    "Crimson_Slate": [
        "#F42E1D", "#E86C5E", "#97524C", "#AFB1B5", 
        "#84898D", "#606469", "#363E48", "#1C1D22"
    ],
    "Retro_Sunset": [
        "#D62828", "#B53139", "#822F35", "#521B29", 
        "#291528", "#D67D34", "#F79D40", "#F7E1B5"
    ],
    "Warm_Industrial": [
        "#F23022", "#F27138", "#F59E4C", "#FADC38", 
        "#AAB0B6", "#787C81", "#4B4E53", "#222327"
    ],
    "Ocean_Depths": [
        "#0D3B66", "#2678B2", "#3590D6", "#64C5EB", 
        "#B2DDE8", "#1C374D", "#15222E", "#0B1116"
    ],
    "Monolith": [
        "#FFFFFF", "#D6D6D6", "#9E9E9E", "#757575", 
        "#545454", "#363636", "#1C1C1C", "#080808"
    ],
    "Cyberpunk_Neon": [
        "#FF0055", "#FF00AA", "#BC00DD", "#7700E6", 
        "#3300FF", "#0055FF", "#00AAFF", "#00FFFF"
    ],
    "Forest_Canopy": [
        "#386641", "#6A994E", "#A7C957", "#F2E8CF", 
        "#BC4749", "#7F4F24", "#582F0E", "#281105"
    ],
    "Cotton_Candy": [
        "#FFC8DD", "#FFAFCC", "#BDE0FE", "#A2D2FF",
        "#CDB4DB", "#FFC8DD", "#FFAFCC", "#A2D2FF"
    ],
    "Matcha_Latte": [
        "#3F4238", "#5F6F52", "#A9B388", "#FEFAE0",
        "#F9EBC7", "#B99470", "#FEFAE0", "#A9B388"
    ],

    # --- Aesthetic & Trendy ---
    "Deep_Sea": [
        "#001219", "#005F73", "#0A9396", "#94D2BD", 
        "#E9D8A6", "#EE9B00", "#CA6702", "#9B2226"
    ],
    "Vaporwave_Sunset": [
        "#240046", "#3C096C", "#5A189A", "#7B2CBF", 
        "#9D4EDD", "#C77DFF", "#E0AAFF", "#FF9E00"
    ],
    "Lofi_Beats": [
        "#2B2D42", "#8D99AE", "#EDF2F4", "#EF233C", 
        "#D90429", "#540D6E", "#EE4266", "#FFD23F"
    ],
    "Molten_Lava": [
        "#050505", "#2A2A2A", "#4A0E0E", "#8B0000", 
        "#CD3700", "#FF4500", "#FFA500", "#FFD700"
    ],
    "Dried_Lavender": [
        "#231942", "#4A3B69", "#6B5077", "#8D6B8D", 
        "#B08BA3", "#D4ACB6", "#E9DCEB", "#F8F1F5"
    ],
    "Acid_Matrix": [
        "#000000", "#0F290F", "#1B4D1B", "#286E28", 
        "#3D8C3D", "#56AC56", "#74CC74", "#00FF41"
    ],
    "Cold_Brew": [
        "#3E2723", "#4E342E", "#5D4037", "#6D4C41", 
        "#795548", "#8D6E63", "#A1887F", "#D7CCC8"
    ],
    "Neon_Tokyo": [
        "#050510", "#121226", "#222240", "#2D2D55", 
        "#00F0FF", "#FF003C", "#FDFDFD", "#7000FF"
    ],
    "Swamp_Witch": [
        "#1A2F1A", "#2D472D", "#3F5E3F", "#4F764F", 
        "#5C8D5C", "#6B9E6B", "#8DA88D", "#C2B280"
    ],
    "Peach_Fuzz": [
        "#603813", "#855E42", "#A67C52", "#C9A66B", 
        "#EBC9A5", "#FFE8D6", "#FFF5EE", "#FFFFFF"
    ]
}

# --- 2. GENERATION ENGINE ---

def generate_design(target_width, target_height, colors, bg_color, super_sample=2):
    # Setup dimensions with SSAA
    render_width = target_width * super_sample
    render_height = target_height * super_sample
    
    # Reference Proportions
    REF_WIDTH = 800
    REF_HEIGHT = 400
    BASE_BAR_WIDTH = 70
    BASE_BAR_HEIGHT = 280
    BASE_SPACING = 42

    # Math
    scale = min(render_width / REF_WIDTH, render_height / REF_HEIGHT)
    bar_width = BASE_BAR_WIDTH * scale
    bar_height = BASE_BAR_HEIGHT * scale
    spacing = BASE_SPACING * scale
    radius = bar_width / 2

    # Centering
    total_group_width = (spacing * (len(colors) - 1)) + bar_width
    start_x = (render_width - total_group_width) / 2
    start_y = (render_height - bar_height) / 2

    # Draw
    img = Image.new("RGB", (render_width, render_height), bg_color)
    draw = ImageDraw.Draw(img)

    for i, color in enumerate(colors):
        x = start_x + (i * spacing)
        y = start_y
        bounds = [x, y, x + bar_width, y + bar_height]
        draw.rounded_rectangle(bounds, radius=radius, fill=color)

    # Downsample (Anti-Aliasing)
    if super_sample > 1:
        img = img.resize((target_width, target_height), resample=Image.Resampling.LANCZOS)

    return img

def main():
    print("--- Theme Generator (OLED & Solarized Light) ---")
    
    # Input
    w_str = input("Enter Width (default 10080): ")
    h_str = input("Enter Height (default 4320): ")
    w = int(w_str) if w_str.strip() else 10080
    h = int(h_str) if h_str.strip() else 4320
    
    output_dir = "generated_wallpapers"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"\nTarget Resolution: {w}x{h}")
    print(f"Palettes: {len(PALETTES)} | Variations: 2 (Dark_OLED/Light)")
    print("-" * 50)

    # Define Modes
    modes = [
        {"name": "Dark_OLED",  "bg": "#000000"}, # OLED Black
        {"name": "Light", "bg": "#FDF6E3"}  # Solarized Paper White
    ]

    for mode in modes:
        mode_name = mode["name"]
        bg = mode["bg"]
        print(f"\n>>> Generating {mode_name} Mode ({bg})...")

        for name, palette in PALETTES.items():

            try:
                # Generate
                img = generate_design(w, h, palette, bg, super_sample=2)
                
                # Save
                filename = f"{output_dir}/{name}_{mode_name}_{w}x{h}.png"
                img.save(filename, compress_level=1)
                print(f"    Saved: {filename}")
                
            except MemoryError:
                print("    ERROR: Out of Memory. Try super_sample=1.")

    print("-" * 50)
    print(f"Done! Check the '{output_dir}' folder.")

if __name__ == "__main__":
    main()