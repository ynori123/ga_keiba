import re

text = "牡３"
pattern = r"(?:牡|牝|セ)(\d+)"

match = re.search(pattern, text)
if match:
    extracted_number = int(match.group(1))
    print(extracted_number)  # これにより整数「3」が出力されます。
else:
    print("マッチする数字が見つかりませんでした。")
