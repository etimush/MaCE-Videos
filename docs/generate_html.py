import os
import sys  # To exit script on error

# --- Configuration ---
RAW_BASE = "https://raw.githubusercontent.com/etimush/MaCE-Videos/main/docs/"
VIDEO_DIR = "Videos"
OUTPUT_HTML_FILE = "index.html"
CSS_FILE = "style.css"
MAIN_TITLE = "Sample MaCE Videos"
SUPPORTED_EXTENSIONS = ['.mp4', '.webm', '.ogg']

# --- Get Base Directory ---
script_dir = os.path.dirname(os.path.abspath(__file__))
videos_full_path = os.path.join(script_dir, VIDEO_DIR)
output_html_full_path = os.path.join(script_dir, OUTPUT_HTML_FILE)

print(f"Looking for videos in subdirectories of: {videos_full_path}")

# --- Scan Video Directory for Subdirectories and their Videos ---
sections = {}
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

# MODIFIED: Updated JavaScript for play/pause on scroll
html_end = """
    </main>

    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const lazyVideos = [].slice.call(document.querySelectorAll("video.lazy-video"));

            if ("IntersectionObserver" in window) {
                const videoObserver = new IntersectionObserver((entries, observer) => {
                    entries.forEach(entry => {
                        const video = entry.target;
                        if (entry.isIntersecting) {
                            // Video is in view
                            const firstSource = video.querySelector("source[data-src]");
                            if (firstSource) {
                                // First time: Set sources, load, and play
                                video.querySelectorAll("source[data-src]").forEach(source => {
                                    source.src = source.dataset.src;
                                    source.removeAttribute('data-src'); // Prevent re-processing
                                });
                                video.load();
                                video.play().catch(error => {
                                    console.log(`Autoplay prevented for ${video.id} on initial load:`, error);
                                    // User might need to interact if autoplay is blocked even with muted.
                                });
                            } else if (video.paused) {
                                // Video was already loaded but is paused, play it
                                video.play().catch(error => {
                                    console.log(`Autoplay prevented for ${video.id} on re-entering view:`, error);
                                });
                            }
                        } else {
                            // Video is out of view, pause it
                            if (!video.paused) {
                                video.pause();
                            }
                        }
                    });
                }, {
                    // Adjust rootMargin and threshold as needed:
                    // rootMargin: "0px 0px 200px 0px" means the "viewport" for intersection checks
                    // extends 200px below the actual viewport. Videos within this margin start loading/playing.
                    // threshold: 0.25 means 25% of the video needs to be visible within the rootMargin area
                    // for 'isIntersecting' to be true.
                    rootMargin: "0px 0px 150px 0px", // Start loading/playing when video is 150px from viewport bottom
                    threshold: 0.2 // Play when at least 20% of the video is visible in the observer's root
                });

                lazyVideos.forEach(function(lazyVideo) {
                    videoObserver.observe(lazyVideo); // Observe for continuous play/pause
                });

            } else {
                // Fallback for browsers that don't support IntersectionObserver
                // Load all videos immediately and try to play (might cause performance issues)
                console.warn("IntersectionObserver not supported. All videos will attempt to load and play at once.");
                lazyVideos.forEach(function(video) {
                    video.querySelectorAll("source[data-src]").forEach(source => {
                        source.src = source.dataset.src;
                        source.removeAttribute('data-src');
                    });
                    video.load();
                    video.play().catch(error => {
                        console.log("Video play prevented (fallback) for " + video.id + ": ", error);
                    });
                });
            }
        });
    </script>
</body>
</html>
"""

# --- Generate HTML for Each Video Section ---
video_items_html = ""
if not sections:
    video_items_html = f'            <p>No videos found in subdirectories of "{VIDEO_DIR}".</p>\n'
else:
    video_counter = 0 # For unique IDs
    for section_name, video_files_in_section in sections.items():
        video_items_html += f'            <h2 class="video-section-header">{section_name}</h2>\n'
        video_items_html += '            <div class="video-grid">\n'

        for filename in video_files_in_section:
            video_counter += 1
            video_id = f"video-{video_counter}" # Unique ID for each video
            base_name = os.path.splitext(filename)[0]
            video_path_relative = os.path.join(VIDEO_DIR, section_name, filename).replace("\\", "/")
            file_ext = os.path.splitext(filename)[1].lower()
            mime_type = ""
            if file_ext == '.mp4': mime_type = 'video/mp4'
            elif file_ext == '.webm': mime_type = 'video/webm'
            elif file_ext == '.ogg': mime_type = 'video/ogg'

            video_items_html += f"""
                <div class="video-item">
                    <video id="{video_id}" class="lazy-video" controls loop muted playsinline preload="metadata">
                        <source data-src="{RAW_BASE + video_path_relative}" type="{mime_type}">
                        Your browser does not support the video tag. ({filename})
                    </video>
                    <p class="caption">{base_name}</p>
                </div>
"""
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