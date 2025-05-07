import os
import sys  # To exit script on error

# --- Configuration ---
VIDEO_DIR = "Videos"
OUTPUT_HTML_FILE = "index.html"
CSS_FILE = "style.css"
MAIN_TITLE = "Samples of MaCELenia Worlds"
SUPPORTED_EXTENSIONS = ['.mp4', '.webm', '.ogg']  # Ensure your converted files match these

# --- Get Base Directory ---
script_dir = os.path.dirname(os.path.abspath(__file__))
videos_full_path = os.path.join(script_dir, VIDEO_DIR)
output_html_full_path = os.path.join(script_dir, OUTPUT_HTML_FILE)

print(f"Looking for videos in subdirectories of: {videos_full_path}")

# --- Scan Video Directory for Subdirectories and their Videos ---
sections = {}  # Key: subdir_name, Value: list of video filenames in it

try:
    if not os.path.isdir(videos_full_path):
        print(f"Error: Directory not found - '{videos_full_path}'")
        sys.exit(1)

    for item_name in sorted(os.listdir(videos_full_path)):
        item_full_path = os.path.join(videos_full_path, item_name)

        if os.path.isdir(item_full_path):
            subdir_name = item_name
            videos_in_subdir = []
            try:
                for filename in sorted(os.listdir(item_full_path)):
                    file_path_in_subdir = os.path.join(item_full_path, filename)
                    if os.path.isfile(file_path_in_subdir) and \
                            os.path.splitext(filename)[1].lower() in SUPPORTED_EXTENSIONS:
                        videos_in_subdir.append(filename)
            except Exception as e:
                print(f"Warning: Could not fully read subdirectory '{item_full_path}': {e}")

            if videos_in_subdir:
                sections[subdir_name] = videos_in_subdir

    if not sections:
        print(f"No subdirectories with supported video files found in '{videos_full_path}'.")
    else:
        print(f"Found {len(sections)} section(s) with videos:")
        for section_name, videos_list in sections.items():
            print(f"  - Section '{section_name}': {len(videos_list)} video(s)")

except FileNotFoundError:
    print(f"Error: Directory not found - '{videos_full_path}'")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred while reading the video directory: {e}")
    sys.exit(1)

total_videos_processed = sum(len(v_list) for v_list in sections.values())

# --- HTML Template Parts ---
# MODIFIED: Removed the main <div class="video-grid"> from html_start
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
"""

# MODIFIED: Removed the closing </div> for the main video-grid from html_end
html_end = """
    </main>

</body>
</html>
"""

# --- Generate HTML for Each Video Section ---
video_items_html = ""
if not sections:
    # This message will now be directly inside <main> if no sections are found
    video_items_html = f'            <p>No videos found in subdirectories of "{VIDEO_DIR}".</p>\n'
else:
    for section_name, video_files_in_section in sections.items():
        # Add section header (still useful to have a class for styling the H2 itself)
        video_items_html += f'            <h2 class="video-section-header">{section_name}</h2>\n'

        # Start a new video-grid for this section
        video_items_html += '            <div class="video-grid">\n'

        for filename in video_files_in_section:
            base_name = os.path.splitext(filename)[0]
            video_path = os.path.join(VIDEO_DIR, section_name, filename).replace("\\", "/")
            file_ext = os.path.splitext(filename)[1].lower()
            mime_type = ""
            if file_ext == '.mp4':
                mime_type = 'video/mp4'
            elif file_ext == '.webm':
                mime_type = 'video/webm'
            elif file_ext == '.ogg':
                mime_type = 'video/ogg'

            video_items_html += f"""
                <div class="video-item">
                    <video controls autoplay loop muted playsinline preload="metadata">
                        <source src="{video_path}" type="{mime_type}">
                        Your browser does not support the video tag. ({filename})
                    </video>
                    <p class="caption">{base_name}</p> {""}
                </div>
"""
        # Close the video-grid for this section
        video_items_html += '            </div> <!-- end .video-grid for section -->\n'

# --- Combine and Write HTML File ---
final_html = html_start + video_items_html + html_end

try:
    with open(output_html_full_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    if total_videos_processed > 0:
        plural_section = "s" if len(sections) != 1 else ""
        plural_video = "s" if total_videos_processed != 1 else ""
        print(
            f"Successfully generated '{OUTPUT_HTML_FILE}' with {total_videos_processed} video{plural_video} from {len(sections)} section{plural_section}.")
    elif sections:
        print(f"Successfully generated '{OUTPUT_HTML_FILE}'. No videos found in the identified sections.")
    else:
        print(f"Successfully generated '{OUTPUT_HTML_FILE}'. No videos were found to include.")

    print(f"\n-> Open the generated '{OUTPUT_HTML_FILE}' file in your web browser.")
except Exception as e:
    print(f"Error writing HTML file '{output_html_full_path}': {e}")
    sys.exit(1)