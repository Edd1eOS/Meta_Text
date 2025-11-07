# Text Analyzer

Analyzes text logs using C and generates visualizations with Python.

## Components
- C: text processing
- SQLite: storage
- Python: visualization

## Features

- Text processing in C
- Word frequency analysis
- Database storage
- Data visualization

## Tech Stack

### Core Processing (C)
- Custom Text Processing Engine
- Tokenization Algorithm
- Memory-efficient Data Structures
- SQLite3 Integration

### Database
- SQLite3 (for storing analysis results)
- Custom Data Schema
- Query Optimization

### Visualization (Python)
- Matplotlib/Seaborn
- pandas (Data Processing)
- sqlite3 Python Module

## Build
```bash
gcc -o analyzer core/*.c -lsqlite3
pip install -r requirements.txt
```

## Run
```bash
./analyzer input.log
python visualize.py
```

## Structure
```
core/     # C source files
sql/      # Database
viz/      # Visualization
data/     # Results
```

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📮 Contact

- Email: your.email@example.com
- GitHub: [@Edd1eOS](https://github.com/Edd1eOS)

```
文本分析工具
==============

这是一个基于C语言和SQLite数据库的文本分析工具，配合Python脚本进行数据可视化。

功能特性:
--------
1. 文本分词处理
2. 词频统计分析
3. 结果存储到SQLite数据库
4. 数据可视化展示

编译和运行:
----------
1. 编译C程序:
   gcc main.c sqlite-amalgamation-3500400/sqlite3.c -o analyzer

2. 运行文本分析:
   ./analyzer
   然后输入要分析的文本

3. 查看分析结果:
   python vis.py <text_id>
   其中<text_id>是分析完成后返回的文本ID

文件说明:
--------
- main.c: 主程序入口
- analyzer.c/h: 分词器实现
- db.c/h: 数据库操作实现
- vis.py: 数据可视化脚本
- sqlite-amalgamation-3500400/: SQLite数据库源码

注意事项:
--------
1. 需要安装Python的matplotlib库用于可视化:
   pip install matplotlib
   
2. 分析结果保存在analysis.db文件中
3. 可视化图表将保存为PNG格式文件
