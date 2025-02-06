import os
import random
from datetime import datetime
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

VIDEO_DIR = "/app/video_templates"
OUTPUT_DIR = "/app/output"
FONTS_DIR = "/usr/local/share/fonts/custom"

def ensure_output_dir():
    """Ensure output directory exists"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_output_filename():
    """Generate unique filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(OUTPUT_DIR, f"quote_video_{timestamp}.mp4")

def get_random_font():
    """Get a random font from the fonts directory"""
    fonts = [f for f in os.listdir(FONTS_DIR) if f.endswith(('.ttf', '.otf'))]
    if not fonts:
        raise ValueError("No fonts found in fonts directory")
    selected_font = os.path.join(FONTS_DIR, random.choice(fonts))
    print(f"Selected font: {os.path.basename(selected_font)}")
    return selected_font

def add_text_to_video(input_video, output_video, text):
    try:
        # Create video clip from file
        clip = VideoFileClip(input_video)
        print(f"Loaded video: duration={clip.duration}s, size={clip.size}")
        
        # Get random font
        font_path = get_random_font()
        
        # Calculate maximum dimensions (use 80% of video dimensions)
        max_width = int(clip.w * 0.8)
        max_height = int(clip.h * 0.8)
        
        # Start with a reasonable font size
        fontsize = int(clip.w * 0.08)
        
        # Binary search to find the optimal font size
        min_size = 20
        max_size = fontsize
        optimal_size = min_size
        
        while min_size <= max_size:
            test_size = (min_size + max_size) // 2
            try:
                test_clip = TextClip(
                    text,
                    fontsize=test_size,
                    color='white',
                    font=font_path,
                    stroke_color='black',
                    stroke_width=2,
                    kerning=-1,
                    interline=-25,
                    size=(max_width, None),
                    method='caption',
                    align='center'
                )
                
                if test_clip.h <= max_height:
                    optimal_size = test_size
                    min_size = test_size + 1
                else:
                    max_size = test_size - 1
                
                test_clip.close()
            except:
                max_size = test_size - 1
        
        print(f"Found optimal font size: {optimal_size}")
        
        txt_clip = (TextClip(
            text,
            fontsize=optimal_size,
            color='white',
            font=font_path,
            stroke_color='black',
            stroke_width=2,
            kerning=-1,
            interline=-25,
            size=(max_width, None),
            method='caption',
            align='center'
        )
        .set_position(('center', 'center'))
        .set_duration(clip.duration))
        
        final_clip = CompositeVideoClip([clip, txt_clip])
        ensure_output_dir()
        
        print(f"Writing output video to {output_video}...")
        final_clip.write_videofile(output_video, codec="libx264", fps=24)
        print("Video processing completed successfully")
        
    except Exception as e:
        print(f"Error in video processing: {str(e)}")
        raise
    
    finally:
        try:
            if 'clip' in locals(): clip.close()
            if 'txt_clip' in locals(): txt_clip.close()
            if 'final_clip' in locals(): final_clip.close()
        except:
            pass

def process_video(text):
    """ Selects a random video and overlays text """
    video_files = [os.path.join(VIDEO_DIR, f) for f in os.listdir(VIDEO_DIR) if f.endswith((".mp4", ".mov"))]
    
    if not video_files:
        print("No videos found in directory!")
        return None

    selected_video = random.choice(video_files)
    print(f"Selected video template: {os.path.basename(selected_video)}")
    
    output_video = get_output_filename()
    add_text_to_video(selected_video, output_video, text)
    return output_video