import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import sys

def generate_word_frequency_chart(text_id):
    """生成词频统计图表"""
    try:
        conn = sqlite3.connect('analysis.db')
        
        # 查询指定文本的词频统计
        cursor = conn.execute("""
            SELECT token, COUNT(*) as frequency 
            FROM tokens 
            WHERE text_id = ? 
            GROUP BY token 
            ORDER BY frequency DESC 
            LIMIT 15
        """, (text_id,))
        
        data = cursor.fetchall()
        if not data:
            print(f"未找到文本ID {text_id} 的分词数据")
            return
        
        tokens = [row[0] for row in data]
        frequencies = [row[1] for row in data]
        
        # 创建词频柱状图
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(tokens)), frequencies, color='skyblue')
        plt.xlabel('词汇')
        plt.ylabel('频次')
        plt.title(f'文本 #{text_id} 词频统计')
        plt.xticks(range(len(tokens)), tokens, rotation=45, ha='right')
        
        # 在柱状图上显示数值
        for bar, freq in zip(bars, frequencies):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                     str(freq), ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(f'word_frequency_{text_id}.png')
        plt.show()
        
        conn.close()
        print(f"词频统计图表已保存为 word_frequency_{text_id}.png")
        
    except Exception as e:
        print(f"生成图表时出错: {e}")

def generate_token_length_distribution(text_id):
    """生成词长度分布图表"""
    try:
        conn = sqlite3.connect('analysis.db')
        
        # 查询词长度分布
        cursor = conn.execute("""
            SELECT LENGTH(token) as token_length, COUNT(*) as count
            FROM tokens 
            WHERE text_id = ?
            GROUP BY LENGTH(token)
            ORDER BY token_length
        """, (text_id,))
        
        data = cursor.fetchall()
        if not data:
            print(f"未找到文本ID {text_id} 的分词数据")
            return
        
        lengths = [row[0] for row in data]
        counts = [row[1] for row in data]
        
        # 创建词长度分布图
        plt.figure(figsize=(10, 6))
        plt.plot(lengths, counts, marker='o', linestyle='-', color='green')
        plt.xlabel('词长度')
        plt.ylabel('数量')
        plt.title(f'文本 #{text_id} 词长度分布')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'token_length_distribution_{text_id}.png')
        plt.show()
        
        conn.close()
        print(f"词长度分布图表已保存为 token_length_distribution_{text_id}.png")
        
    except Exception as e:
        print(f"生成图表时出错: {e}")

def main():
    if len(sys.argv) != 2:
        print("用法: python vis.py <text_id>")
        sys.exit(1)
    
    try:
        text_id = int(sys.argv[1])
    except ValueError:
        print("错误: text_id 必须是一个整数")
        sys.exit(1)
    
    print(f"正在为文本ID {text_id} 生成可视化图表...")
    generate_word_frequency_chart(text_id)
    generate_token_length_distribution(text_id)

if __name__ == "__main__":
    main()