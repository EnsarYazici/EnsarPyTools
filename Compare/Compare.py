import os
import filecmp
import difflib
from datetime import datetime

def compare_directories(dir1, dir2, output_md="comparison_report.md"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(output_md, "w", encoding="utf-8") as md_file:
        md_file.write(f"# Comparison Report\n\n")
        md_file.write(f"Comparing `{dir1}` with `{dir2}`\n")
        md_file.write(f"Report generated on: {current_time}\n\n")

        # İlk olarak klasör farklarını buluyoruz
        dir_comparison = filecmp.dircmp(dir1, dir2)

        # Klasörlerin içerik farklarını yazıyoruz
        write_dir_diffs(md_file, dir_comparison)

        # Aynı dosya isimli dosyalar arasındaki farkları yazıyoruz
        for filename in dir_comparison.common_files:
            filepath1 = os.path.join(dir1, filename)
            filepath2 = os.path.join(dir2, filename)
            write_file_diff(md_file, filepath1, filepath2)
            
        md_file.write("\n\n## Comparison Complete\n")

def write_dir_diffs(md_file, dir_comparison):
    # Sadece ilk klasörde bulunan dosya ve klasörler
    if dir_comparison.left_only:
        md_file.write("## Files only in the first directory:\n")
        for item in dir_comparison.left_only:
            md_file.write(f"- {item}\n")
        md_file.write("\n")

    # Sadece ikinci klasörde bulunan dosya ve klasörler
    if dir_comparison.right_only:
        md_file.write("## Files only in the second directory:\n")
        for item in dir_comparison.right_only:
            md_file.write(f"- {item}\n")
        md_file.write("\n")

    # Her iki klasörde ortak olan ancak içerikleri farklı olan dosyalar
    if dir_comparison.diff_files:
        md_file.write("## Files that differ in content:\n")
        for item in dir_comparison.diff_files:
            md_file.write(f"- {item}\n")
        md_file.write("\n")

def write_file_diff(md_file, filepath1, filepath2):
    # Dosyaların içeriğini satır satır karşılaştırıyoruz
    with open(filepath1, "r", encoding="utf-8") as file1, open(filepath2, "r", encoding="utf-8") as file2:
        diff = list(difflib.unified_diff(
            file1.readlines(),
            file2.readlines(),
            fromfile=filepath1,
            tofile=filepath2,
            lineterm=""
        ))

    # Eğer diff boşsa, herhangi bir şey yazmadan fonksiyondan çık
    if not diff:
        return

    # Fark varsa yaz
    md_file.write(f"\n### Differences in `{os.path.basename(filepath1)}`:\n")
    md_file.write("```diff\n")
    for line in diff:
        md_file.write(line + "\n")
    md_file.write("```\n\n")

def run(dir1=None, dir2=None):

    if dir1 is None or dir2 is None:
        dir1 = input("Enter the path to the first directory: ").strip('"')
        dir2 = input("Enter the path to the second directory: ").strip('"')
    current_time = datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
    compare_directories(dir1, dir2, f"comparison_report_{current_time}.md")

if __name__ == "__main__":
    run()
