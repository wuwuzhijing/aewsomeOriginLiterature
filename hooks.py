def on_page_markdown(markdown, **kwargs):
    # 把残留的 '\n' 清理掉
    return markdown.replace("\\n", "\n")