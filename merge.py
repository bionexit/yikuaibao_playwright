import os
import re

def merge_md_files(directory, output_file='full-md.txt'):
    """
    将指定目录下的所有.md文件合并为一个输出文件，并按文件名中的数字段排序
    
    参数:
        directory (str): 要搜索的根目录路径
        output_file (str): 输出文件名 (默认为'full-md.txt')
    """
    # 确保目录存在
    if not os.path.isdir(directory):
        print(f"错误: 目录 '{directory}' 不存在")
        return

    # 收集所有.md文件路径
    md_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.md'):
                full_path = os.path.join(root, file)
                md_files.append(full_path)

    if not md_files:
        print("未找到任何.md文件")
        return

    # 定义排序函数：按文件名中的数字段排序
    def sort_key(file_path):
        # 获取不带路径的文件名
        filename = os.path.basename(file_path)
        
        # 使用正则表达式提取文件名开头的数字序列
        matches = re.findall(r'^(\d+)(?:-(\d+))?', filename)
        
        # 如果找到数字序列
        if matches:
            # 获取匹配结果（第一个匹配组）
            nums = matches[0]
            
            # 转换第一部分数字
            part1 = int(nums[0]) if nums[0] else 0
            
            # 转换第二部分数字（如果存在）
            part2 = int(nums[1]) if len(nums) > 1 and nums[1] else 0
            
            return (part1, part2)
        
        # 如果没有数字序列，则排在最后
        return (9999, 9999)

    # 按数字顺序排序文件
    md_files.sort(key=sort_key)
    
    print(f"找到 {len(md_files)} 个.md文件，开始合并...")
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, md_file in enumerate(md_files):
            # 添加分隔符和文件路径
            outfile.write(f"\n\n{'=' * 50}\n")
            outfile.write(f"文件 {i+1}/{len(md_files)}: {md_file}\n")
            outfile.write(f"{'=' * 50}\n\n")
            
            # 读取并写入文件内容
            try:
                with open(md_file, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                print(f"已添加: {os.path.basename(md_file)}")
            except Exception as e:
                print(f"处理文件 {md_file} 时出错: {str(e)}")
    
    print(f"\n合并完成！输出文件: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    target_directory = "./ekuaibao_docs"  # 修改为你的目录路径
    merge_md_files(target_directory)