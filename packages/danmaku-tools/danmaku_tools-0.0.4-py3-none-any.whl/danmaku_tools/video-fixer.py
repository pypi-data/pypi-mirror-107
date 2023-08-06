import argparse
import os

parser = argparse.ArgumentParser(description='Merge BiliLiveReocrder XML')
parser.add_argument('--video_file', type=str, help='path to the danmaku file')

if __name__ == '__main__':
    args = parser.parse_args()

    original_video_file = args.video_file
    video_file_base = original_video_file.rpartition(".")[0]

    assert os.system(
        ""
        "dotnet run "
        "--project BililiveStreamFileFixer/BililiveStreamFileFixer.csproj "
        "--framework netcoreapp2.2 "
        f"{original_video_file}"
    ) == 0 or True
    segments_num = int(input("number of segments"))

    target_files = []
    for i in range(segments_num):
        file_name_base = f"{video_file_base}_fixed_{i}"
        file_name_old = f"{file_name_base}.flv"
        file_name_new = f"{file_name_base}.fixed.mp4"
        assert os.system(
            f"ffmpeg -y -i {file_name_old} -video_track_timescale 600 -c copy {file_name_new}"
        ) == 0
        target_files += [file_name_new]

    concat_file_name = f"{video_file_base}.concat.txt"
    with open(concat_file_name, "w") as concat_file:
        for target_file in target_files:
            concat_file.write(f"file '{os.path.basename(target_file)}'\n")

    output_file = f"{video_file_base}.fixed.mp4"
    os.system(
        f"ffmpeg -f concat -safe 0 -i {concat_file_name} -c copy {output_file}"
    )
