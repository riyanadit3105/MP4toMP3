import os
from moviepy.editor import VideoFileClip
from concurrent.futures import ProcessPoolExecutor, as_completed


def convert_mp4_to_mp3(mp4_path: str, mp3_path: str) -> None:
    """
    Mengonversi file MP4 ke MP3 dengan mengekstrak audio menggunakan MoviePy.

    Args:
        mp4_path (str): Path lengkap file MP4.
        mp3_path (str): Path lengkap file MP3 yang akan dihasilkan.
    """
    try:
        # Gunakan context manager untuk memastikan resource tertutup dengan benar.
        with VideoFileClip(mp4_path) as video_clip:
            # Ekstrak dan simpan audio ke file MP3; nonaktifkan logger bawaan untuk mempercepat proses.
            video_clip.audio.write_audiofile(mp3_path, logger=None)
        print(f"Berhasil mengonversi '{mp4_path}' ke '{mp3_path}'")
    except Exception as error:
        print(f"Gagal mengonversi '{mp4_path}': {error}")


def main():
    # Tentukan folder sumber tempat file MP4 berada.
    source_folder = r"Folder sumber"

    # Kumpulkan semua file MP4 (perhatikan perbandingan case-insensitive)
    mp4_files = [
        os.path.join(source_folder, file)
        for file in os.listdir(source_folder)
        if file.lower().endswith(".mp4")
    ]

    if not mp4_files:
        print("Tidak ada file MP4 yang ditemukan di folder.")
        return

    # Atur jumlah pekerja sesuai dengan jumlah CPU yang tersedia
    max_workers = min(len(mp4_files), os.cpu_count() or 1)

    # Proses konversi secara paralel
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for mp4_path in mp4_files:
            mp3_path = os.path.splitext(mp4_path)[0] + ".mp3"
            futures.append(executor.submit(convert_mp4_to_mp3, mp4_path, mp3_path))

        # Pastikan semua task selesai dan tangani kemungkinan error
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as error:
                print(f"Terjadi kesalahan saat memproses konversi: {error}")


if __name__ == "__main__":
    main()
