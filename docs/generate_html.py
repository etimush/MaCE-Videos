import os
import sys # To exit script on error

# --- Configuration ---
VIDEO_DIR = "Videos"
OUTPUT_HTML_FILE = "index.html"
CSS_FILE = "style.css"
MAIN_TITLE = "Samples of MaCELenia Worlds"
SUPPORTED_EXTENSIONS = ['.mp4', '.webm', '.ogg'] # Ensure your converted files match these

# --- Get Base Directory ---
script_dir = os.path.dirname(os.path.abspath(__file__))
videos_full_path = os.path.join(script_dir, VIDEO_DIR)
output_html_full_path = os.path.join(script_dir, OUTPUT_HTML_FILE)

print(f"Looking for videos in: {videos_full_path}")

# --- Scan Video Directory ---
video_files = []
try:
    all_files = os.listdir(videos_full_path)
    for filename in all_files:
        if os.path.splitext(filename)[1].lower() in SUPPORTED_EXTENSIONS:
            video_files.append(filename)
    video_files.sort()
    print(f"Found {len(video_files)} video files.")

except FileNotFoundError:
    print(f"Error: Directory not found - '{videos_full_path}'")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred while reading the video directory: {e}")
    sys.exit(1)

# --- HTML Template Parts ---
html_start = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Gallery</title>
    <link rel="stylesheet" href="{CSS_FILE}">
</head>
<body>

    <header>
        <h1 id="main-title">{MAIN_TITLE}</h1>
    </header>

    <main>
        <div class="video-grid">
"""

html_end = """
        </div> <!-- end .video-grid -->
    </main>

</body>
</html>
"""

# --- Generate HTML for Each Video ---
video_items_html = ""
if not video_files:
    video_items_html = '            <p>No videos found in the "Videos" directory.</p>\n'
else:
    for filename in video_files:
        # --- Get filename without extension ---
        base_name = os.path.splitext(filename)[0]
        # --- End of change ---

        video_path = os.path.join(VIDEO_DIR, filename).replace("\\", "/")
        file_ext = os.path.splitext(filename)[1].lower()
        mime_type = ""
        if file_ext == '.mp4':
            mime_type = 'video/mp4'
        elif file_ext == '.webm':
            mime_type = 'video/webm'
        elif file_ext == '.ogg':
            mime_type = 'video/ogg'

        # --- Modify generated HTML to include caption ---
        video_items_html += f"""
            <div class="video-item">
                <video controls autoplay loop muted playsinline preload="metadata">
                    <source src="{video_path}" type="{mime_type}">
                    Your browser does not support the video tag. ({filename})
                </video>
                <p class="caption">{base_name}</p> {""}
            </div>
"""
        # --- End of change ---


# --- Combine and Write HTML File ---
final_html = html_start + video_items_html + html_end

try:
    with open(output_html_full_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"Successfully generated '{OUTPUT_HTML_FILE}' with {len(video_files)} videos.")
    print(f"\n-> Open the generated '{OUTPUT_HTML_FILE}' file in your web browser.")
except Exception as e:
    print(f"Error writing HTML file '{output_html_full_path}': {e}")
    sys.exit(1)