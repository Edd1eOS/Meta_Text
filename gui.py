import dearpygui.dearpygui as dpg
import subprocess
import sqlite3
import os
import sys

# 创建上下文
dpg.create_context()

# 全局变量
text_id = None
analysis_db = "analysis.db"

def analyze_text_callback():
    """分析文本回调函数"""
    text = dpg.get_value("input_text")
    
    if not text.strip():
        dpg.set_value("status_text", "Please enter some text to analyze.")
        return
        
    try:
        # Run analyzer
        result = subprocess.run(
            ["./text_analyzer.exe"],
            input=text,
            text=True,
            capture_output=True,
            encoding="utf-8"
        )
        
        # Display results
        dpg.set_value("analysis_output", result.stdout)
        
        # Extract text_id
        lines = result.stdout.split('\n')
        for line in lines:
            if "Text ID:" in line:
                try:
                    global text_id
                    text_id = int(line.split(":")[-1].strip())
                    dpg.set_value("text_id_input", str(text_id))
                    dpg.set_value("status_text", f"Analysis complete! Text ID: {text_id}")
                    refresh_database_info()
                    refresh_available_ids()
                    return
                except ValueError:
                    pass
                    
        dpg.set_value("status_text", "Analysis completed but failed to extract Text ID")
        
    except Exception as e:
        dpg.set_value("analysis_output", f"Analysis failed:\n{str(e)}")
        dpg.set_value("status_text", "Analysis failed")

def file_dialog_callback(sender, app_data):
    """文件对话框回调函数"""
    try:
        # 获取选中的文件路径
        file_path = app_data['file_path_name']
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # 将内容设置到输入文本框
        dpg.set_value("input_text", content)
        dpg.set_value("status_text", f"Loaded file: {file_path}")
        
    except Exception as e:
        dpg.set_value("status_text", f"Failed to load file: {str(e)}")

def load_file_callback():
    """Load file callback function"""
    # Show file dialog
    dpg.show_item("file_dialog")

def clear_text_callback():
    """Clear text callback function"""
    dpg.set_value("input_text", "")
    dpg.set_value("analysis_output", "")
    dpg.set_value("status_text", "Text cleared")

def generate_visualizations_callback():
    """Generate visualizations callback function"""
    global text_id
    text_id_str = dpg.get_value("text_id_input")
    output_dir = dpg.get_value("output_dir_input")
    
    if not text_id_str:
        dpg.set_value("status_text", "Please enter a Text ID.")
        return
        
    try:
        text_id = int(text_id_str)
    except ValueError:
        dpg.set_value("status_text", "Text ID must be a number.")
        return
    
    # Use default value "." if no output directory is specified
    if not output_dir:
        output_dir = "."
        
    try:
        # Check if the text_id exists in the database
        conn = sqlite3.connect(analysis_db)
        cursor = conn.execute("SELECT COUNT(*) FROM texts WHERE id = ?", (text_id,))
        count = cursor.fetchone()[0]
        conn.close()
        
        if count == 0:
            dpg.set_value("status_text", f"No text found with ID {text_id}")
            return
            
        # Run visualization script with output directory parameter
        result = subprocess.run(
            [sys.executable, "vis.py", str(text_id), output_dir],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            dpg.set_value("status_text", f"Visualizations generated for Text ID {text_id} in {output_dir}")
            # In actual implementation, generated images should be displayed here
        else:
            dpg.set_value("status_text", f"Visualization failed:\n{result.stderr}")
            
    except Exception as e:
        dpg.set_value("status_text", f"Visualization failed:\n{str(e)}")

def select_output_directory():
    """Select output directory callback function"""
    # Get current output directory as initial directory
    current_dir = dpg.get_value("output_dir_input")
    if not current_dir or not os.path.exists(current_dir):
        current_dir = "."
    
    # Dear PyGui doesn't have a built-in directory selection dialog, so we use tkinter's
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()  # Hide main window
    directory = filedialog.askdirectory(initialdir=current_dir, title="Select Output Directory")
    if directory:
        dpg.set_value("output_dir_input", directory)
    root.destroy()

def refresh_database_info():
    """Refresh database information"""
    try:
        conn = sqlite3.connect(analysis_db)
        
        # Get total number of texts
        cursor = conn.execute("SELECT COUNT(*) FROM texts")
        texts_count = cursor.fetchone()[0]
        
        # Get total number of tokens
        cursor = conn.execute("SELECT COUNT(*) FROM tokens")
        tokens_count = cursor.fetchone()[0]
        
        # Get latest text IDs
        cursor = conn.execute("SELECT id, LENGTH(content) FROM texts ORDER BY id DESC LIMIT 5")
        latest_texts = cursor.fetchall()
        
        conn.close()
        
        # Display information
        info = f"Database: {analysis_db}\n"
        info += f"Total texts analyzed: {texts_count}\n"
        info += f"Total tokens: {tokens_count}\n\n"
        info += "Latest texts:\n"
        
        for text_id, content_length in latest_texts:
            info += f"  ID {text_id}: {content_length} characters\n"
            
        dpg.set_value("database_info", info)
        
    except Exception as e:
        dpg.set_value("database_info", f"Failed to get database info:\n{str(e)}")

def refresh_available_ids():
    """Refresh available IDs list"""
    try:
        conn = sqlite3.connect(analysis_db)
        cursor = conn.execute("SELECT id FROM texts ORDER BY id DESC LIMIT 10")
        ids = [str(row[0]) for row in cursor.fetchall()]
        conn.close()
        
        if ids:
            dpg.set_value("available_ids", "Available IDs: " + ", ".join(ids))
        else:
            dpg.set_value("available_ids", "No texts analyzed yet")
    except Exception as e:
        dpg.set_value("available_ids", f"Error: {str(e)}")

# ==================== 可自定义部分 1: 文件对话框 ====================
# Create file dialog
with dpg.file_dialog(directory_selector=False, show=False, callback=file_dialog_callback, tag="file_dialog", width=700, height=400):
    dpg.add_file_extension(".*")
    dpg.add_file_extension(".txt", color=(0, 255, 0, 255), custom_text="[Text files]")
    dpg.add_file_extension(".log", color=(255, 255, 0, 255), custom_text="[Log files]")
# ==================== File Dialog End ====================

# 创建主窗口
with dpg.window(label="Text Analyzer", width=1000, height=700, tag="main_window"):
    # ==================== 可自定义部分 2: 菜单栏 ====================
    # 可在此处添加自定义菜单项
    with dpg.menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Load from File", callback=load_file_callback)
            dpg.add_menu_item(label="Save Analysis", callback=lambda: print("Save functionality can be implemented here"))
            dpg.add_menu_item(label="Exit", callback=lambda: dpg.stop_dearpygui())
        with dpg.menu(label="Tools"):
            dpg.add_menu_item(label="Settings", callback=lambda: print("Settings can be implemented here"))
        with dpg.menu(label="Help"):
            dpg.add_menu_item(label="About", callback=lambda: print("About information can be shown here"))
    # ==================== 菜单栏结束 ====================
    
    # ==================== 可自定义部分 3: 工具栏 ====================
    # 可在此处添加自定义工具按钮
    with dpg.group(horizontal=True):
        dpg.add_button(label="Analyze", callback=analyze_text_callback)
        dpg.add_button(label="Load File", callback=load_file_callback)
        dpg.add_button(label="Clear", callback=clear_text_callback)
        dpg.add_button(label="Visualize", callback=generate_visualizations_callback)
        dpg.add_button(label="Refresh DB Info", callback=refresh_database_info)
    # ==================== 工具栏结束 ====================
    
    # 状态文本
    dpg.add_text("Ready", tag="status_text")
    
    # 可用ID文本
    dpg.add_text("", tag="available_ids")
    refresh_available_ids()
    
    # ==================== 可自定义部分 4: 主内容区域 ====================
    with dpg.tab_bar():
        # 分析标签页
        with dpg.tab(label="Text Analysis"):
            # 输入区域
            dpg.add_input_text(label="Input Text", multiline=True, height=200, tag="input_text")
            
            # 按钮组
            with dpg.group(horizontal=True):
                dpg.add_button(label="Analyze Text", callback=analyze_text_callback)
                dpg.add_button(label="Load from File", callback=load_file_callback)
                dpg.add_button(label="Clear", callback=clear_text_callback)
            
            # 分隔线
            dpg.add_separator()
            
            # 输出区域
            dpg.add_text("Analysis Results:")
            dpg.add_input_text(label="", multiline=True, height=150, readonly=True, tag="analysis_output")
        
        # 可视化标签页
        with dpg.tab(label="Visualization"):
            # 可视化控制
            with dpg.group():
                dpg.add_input_text(label="Text ID", tag="text_id_input", width=100)
                
                # 输出目录选择
                with dpg.group(horizontal=True):
                    dpg.add_input_text(label="Output Directory", tag="output_dir_input", width=300, default_value=".")
                    dpg.add_button(label="Browse", callback=select_output_directory)
                
                dpg.add_button(label="Generate Visualizations", callback=generate_visualizations_callback)
                dpg.add_text("Enter a Text ID and select output directory to generate visualizations")
            
            # 分隔线
            dpg.add_separator()
            
            # 可视化显示区域（在实际实现中应该显示生成的图像）
            with dpg.group():
                dpg.add_text("Visualization Area")
                dpg.add_text("Generated charts will be displayed here")
                # 可自定义部分: 添加图像显示组件
                
        # 数据库信息标签页
        with dpg.tab(label="Database Info"):
            dpg.add_button(label="Refresh Database Info", callback=refresh_database_info)
            dpg.add_input_text(label="", multiline=True, height=400, readonly=True, tag="database_info")
            refresh_database_info()
    # ==================== 主内容区域结束 ====================

# Create viewport
dpg.create_viewport(title="Text Analyzer GUI", width=1050, height=750)

# Setup and show GUI
dpg.setup_dearpygui()
dpg.show_viewport()

# Start main loop
dpg.start_dearpygui()

# Destroy context
dpg.destroy_context()