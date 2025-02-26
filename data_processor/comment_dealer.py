import pandas as pd
from deep_translator import GoogleTranslator
from tqdm import tqdm

# 读取 CSV 文件（替换为你的文件路径）
file_path = "../data/raw_data/comment.csv"
df = pd.read_csv(file_path)
df = df.head(3000)

# 创建翻译器实例（注意 zh-CN）
translator = GoogleTranslator(source="zh-CN", target="en")

# 初始化 tqdm 进度条
tqdm.pandas(desc="Translating")

# 定义带进度条的翻译函数
def translate_text(text):
    if pd.notnull(text):
        try:
            return translator.translate(text)
        except Exception as e:
            return f"Error: {e}"  # 遇到错误返回错误信息，防止中断
    return text

# 逐行翻译
df["text"] = df["text"].progress_apply(translate_text)

# 保存翻译后的数据
translated_file = "../data/dealed_data/translated_comment.csv"
df.to_csv(translated_file, index=False, encoding="utf-8-sig")

# # 显示翻译后的数据
# import ace_tools as tools
# tools.display_dataframe_to_user(name="Translated CSV", dataframe=df)
