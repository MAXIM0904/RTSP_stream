import cv2
import time
import ffmpeg
import os


def convert_video(video_input, flow, codec, video_output):
    """
    Функция конвертирует видео
    """
    os.system(f"ffmpeg -r {flow} -i {video_input} -vcodec {codec} -y {video_output}")
    return True


def compress_video(video_input, video_output):
    """ Функция сжатия видео
    """

    fpsize = os.path.getsize('video.avi')/1024
    if fpsize >= 150.0:
        compress = f"ffmpeg -i {video_input} -r 10 -pix_fmt yuv420p -vcodec " \
                       f"libx264 -preset veryslow -profile:v baseline  -crf 23 -acodec aac " \
                       f"-b:a 32k -strict -5 {video_output}"
        is_run = os.system(compress)
        if is_run != 0:
            return "Ошибка сжатия"
        return True
    else:
        return "Файл не может быть сжат так как его размер больше 150 КБ"


def rtsp_stream(seconds_end=None):
    """
    Функция записи RTSP-потока
    seconds_end - параметр для окончания записи через переданное пользователем число секунд.
    """
    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter(
        'video.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20.0, (int(cap.get(3)), int(cap.get(4)))
    )
    time_start = time.time()
    while True:
        seconds = int(time.time() - time_start)
        if cap.isOpened():
            ret, frame = cap.read()

            if ret is True:
                out.write(frame)
                cv2.imshow('RTSP stream', frame)

                if seconds_end:
                    if seconds_end <= seconds:
                        print("Выход по таймеру")
                        break

                if cv2.waitKey(1) == 27:
                    print("Штатный выход")
                    break
            else:
                print("Битый кадр")
        else:
            print("Потеря потока/соединения")
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


# Вызов функции перехвата RTSP-потока и записи видео.
rtsp_stream(seconds_end=10)

# Вызов функции конвертации видео
convert_video('video.avi', '20', 'mpeg4', 'video.mp4')

# Вызов функции сжатия видео.
compress_video('video.avi', 'video_compress.avi')
