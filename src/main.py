# from scraper import get_random_quote
# from video_editor import process_video
# from uploader import upload_to_youtube

# if __name__ == "__main__":
#     # Fetch quote
#     author, quote = get_random_quote()
#     if not quote:
#         print("No quote retrieved. Exiting.")
#         exit()

#     print(f"Using quote: {quote} - {author}")

#     # Process video
#     output_video = process_video(f"{quote}\n- {author}")
#     if not output_video:
#         print("No video processed. Exiting.")
#         exit()

#     # Upload to YouTube
#     upload_to_youtube(
#         video_file=output_video,
#         title=f"🔥 {author} - Life-Changing Wisdom #Shorts",
#         description=f"{quote} - {author} | #motivation #quotes #shorts",
#         tags=["motivation", "quotes", "shorts", author.replace(" ", "_")],
#         privacy="public"
#     )

import time
from scraper import get_random_quote
from video_editor import process_video
from uploader import upload_to_youtube
from notification import send_slack_alert

TOTAL_VIDEOS = 5
INTERVAL = 21600  # Time in seconds - upload every 4 hours

def main():
    try:
        for i in range(TOTAL_VIDEOS):
            print(f"Starting upload {i + 1}/{TOTAL_VIDEOS}...")
            send_slack_alert(f"Starting upload {i + 1}/{TOTAL_VIDEOS}...")

            # Fetch quote
            author, quote = get_random_quote()
            if not quote:
                error_msg = f"No quote retrieved for video {i + 1}. Skipping."
                print(error_msg)
                send_slack_alert(error_msg, is_error=True)
                continue

            print(f"Using quote: {quote} - {author}")
            send_slack_alert(f"Using quote: {quote} - {author}")

            # Process video
            output_video = process_video(f"{quote}\n- {author}")
            if not output_video:
                error_msg = f"No video processed for video {i + 1}. Skipping."
                print(error_msg)
                send_slack_alert(error_msg, is_error=True)
                continue

            # Upload to YouTube
            upload_success = upload_to_youtube(
                video_file=output_video,
                title=f"🔥 {author} - Life-Changing Wisdom #Shorts",
                description=f"{quote} - {author} | #motivation #quotes #shorts",
                tags=["motivation", "quotes", "shorts", author.replace(" ", "_")],
                privacy="public"
            )

            if upload_success:
                success_msg = f"Video {i + 1} uploaded successfully: {output_video}"
                print(success_msg)
                send_slack_alert(success_msg)
            else:
                error_msg = f"Failed to upload video {i + 1}."
                print(error_msg)
                send_slack_alert(error_msg, is_error=True)

            # Wait before next upload (except for last video)
            if i < TOTAL_VIDEOS - 1:
                print(f"Waiting {INTERVAL // 60} minutes before next upload...")
                time.sleep(INTERVAL)

    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        print(error_msg)
        send_slack_alert(error_msg, is_error=True)

if __name__ == "__main__":
    main()
