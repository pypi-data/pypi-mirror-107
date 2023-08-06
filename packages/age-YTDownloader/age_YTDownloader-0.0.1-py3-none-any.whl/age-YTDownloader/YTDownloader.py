import pytube.exceptions
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from ffmpy import FFmpeg
import io


class AgeRestrictedYTVideo:
    def __init__(self, url):
        try:
            self.url = url
            self.yt = YouTube(self.url)
            self.title = self.yt.title
            self.length = self.yt.length
            self.age_restricted = self.yt.age_restricted
        except VideoUnavailable:
            print(f'Video "{self.url}" is unavailable, skipping.')
            exit()
        except pytube.exceptions.RegexMatchError:
            print(f'Input "{self.url}" is not valid, skipping.')
            exit()

    def is_age_restricted(self) -> bool:
        return self.age_restricted

    def get_video(self):
        print("Title: ", self.title)
        print("Length of video: ", self.length, "seconds")
        print("Age restricted?: ", self.age_restricted)

        print(f'Searching for progressive stream for {self.url}')
        stream = self.yt.streams.filter(progressive=True).get_highest_resolution()

        if stream == None:
            print(f'No progressive stream found for {self.url}')
            '''
            print(f'Searching for adaptive stream for {self.url}')
            stream = self.yt.streams.filter(adaptive=True).get_highest_resolution()
            if stream == None:
                print(f'No adaptive stream available for {self.url}')
                return None
            else:
                audio = self.yt.streams.filter(only_audio=True).first()
                if audio == None:
                    print(f'No audio stream found for {self.url}')
                else:
                    stream.stream_to_buffer()
                    print("merging video and audio")
                    # DOWNLOAD VIDEO AND AUDIO FILE
                    # MERGE VIDEO AND AUDIO

                    # ff = FFmpeg(
                    # ...     inputs={'video.mp4': None, 'audio.mp3': None},
                    # ...     outputs={'output.ts': '-c:v h264 -c:a ac3'}
                    # ... )
                    # >>> ff.cmd
                    # 'ffmpeg -i audio.mp4 -i video.mp4 -c:v h264 -c:a ac3 output.ts'
                    # >>> ff.run()
            '''
            return None
        else:
            print(f'Progressive stream found for {self.url}')

            bytes_obj = io.BytesIO()
            stream.stream_to_buffer(bytes_obj)

            return bytes_obj






