import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from wordcloud import WordCloud
import matplotlib.font_manager as fm

def generate_word_frequency_chart(text_id, output_dir="."):
    """Generate word frequency chart"""
    try:
        conn = sqlite3.connect('analysis.db')
        
        # Query word frequency statistics for the specified text
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
            print(f"No token data found for text ID {text_id}")
            return
        
        tokens = [row[0] for row in data]
        frequencies = [row[1] for row in data]
        
        # Create word frequency bar chart
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(tokens)), frequencies, color='skyblue')
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.title(f'Text #{text_id} Word Frequency')
        plt.xticks(range(len(tokens)), tokens, rotation=45, ha='right')
        
        # Display values on the bars
        for bar, freq in zip(bars, frequencies):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                     str(freq), ha='center', va='bottom')
        
        plt.tight_layout()
        # Use custom output path
        output_path = os.path.join(output_dir, f'word_frequency_{text_id}.png')
        plt.savefig(output_path)
        plt.show()
        
        conn.close()
        print(f"Word frequency chart saved as {output_path}")
        
    except Exception as e:
        print(f"Error generating chart: {e}")

def generate_token_length_distribution(text_id, output_dir="."):
    """Generate token length distribution chart"""
    try:
        conn = sqlite3.connect('analysis.db')
        
        # Query token length distribution
        cursor = conn.execute("""
            SELECT LENGTH(token) as token_length, COUNT(*) as count
            FROM tokens 
            WHERE text_id = ?
            GROUP BY LENGTH(token)
            ORDER BY token_length
        """, (text_id,))
        
        data = cursor.fetchall()
        if not data:
            print(f"No token data found for text ID {text_id}")
            return
        
        lengths = [row[0] for row in data]
        counts = [row[1] for row in data]
        
        # Create token length distribution chart
        plt.figure(figsize=(10, 6))
        plt.plot(lengths, counts, marker='o', linestyle='-', color='green')
        plt.xlabel('Token Length')
        plt.ylabel('Count')
        plt.title(f'Text #{text_id} Token Length Distribution')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        # Use custom output path
        output_path = os.path.join(output_dir, f'token_length_distribution_{text_id}.png')
        plt.savefig(output_path)
        plt.show()
        
        conn.close()
        print(f"Token length distribution chart saved as {output_path}")
        
    except Exception as e:
        print(f"Error generating chart: {e}")

def generate_word_cloud(text_id, output_dir="."):
    """Generate word cloud chart"""
    try:
        conn = sqlite3.connect('analysis.db')
        
        # Query word frequency for word cloud
        cursor = conn.execute("""
            SELECT token, COUNT(*) as frequency 
            FROM tokens 
            WHERE text_id = ? 
            GROUP BY token 
            ORDER BY frequency DESC
        """, (text_id,))
        
        data = cursor.fetchall()
        if not data:
            print(f"No token data found for text ID {text_id}")
            return
        
        # Create frequency dictionary for word cloud
        freq_dict = {row[0]: row[1] for row in data}
        
        # Generate word cloud
        # Note: WordCloud may have issues with non-English characters on some systems
        # We'll try to use a suitable font if available
        try:
            # Try to find a suitable font
            font_path = None
            try:
                # For Windows systems, try to use SimHei font for Chinese characters
                font_names = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
                for font_name in font_names:
                    try:
                        font_path = fm.findfont(fm.FontProperties(family=font_name))
                        if font_path and os.path.exists(font_path):
                            break
                    except:
                        continue
            except:
                pass
            
            if font_path and os.path.exists(font_path):
                wordcloud = WordCloud(
                    width=800, 
                    height=400, 
                    background_color='white',
                    font_path=font_path,
                    relative_scaling=0.5,
                    random_state=42
                )
            else:
                wordcloud = WordCloud(
                    width=800, 
                    height=400, 
                    background_color='white',
                    relative_scaling=0.5,
                    random_state=42
                )
                
            wordcloud.generate_from_frequencies(freq_dict)
            
            # Create word cloud plot
            plt.figure(figsize=(12, 6))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f'Text #{text_id} Word Cloud')
            
            # Save word cloud
            output_path = os.path.join(output_dir, f'word_cloud_{text_id}.png')
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.show()
            
            conn.close()
            print(f"Word cloud chart saved as {output_path}")
        except Exception as wc_error:
            conn.close()
            print(f"Error generating word cloud: {wc_error}")
            print("Note: This might be due to missing fonts or unsupported characters.")
            
    except Exception as e:
        print(f"Error preparing word cloud data: {e}")

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python vis.py <text_id> [output_dir]")
        print("  text_id: ID of the text to visualize")
        print("  output_dir: Directory to save charts (optional, defaults to current directory)")
        sys.exit(1)
    
    try:
        text_id = int(sys.argv[1])
    except ValueError:
        print("Error: text_id must be an integer")
        sys.exit(1)
    
    # Get output directory (if provided)
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except Exception as e:
            print(f"Error: Failed to create output directory '{output_dir}': {e}")
            sys.exit(1)
    
    print(f"Generating visualization charts for text ID {text_id}...")
    print(f"Charts will be saved to: {os.path.abspath(output_dir)}")
    generate_word_frequency_chart(text_id, output_dir)
    generate_token_length_distribution(text_id, output_dir)
    generate_word_cloud(text_id, output_dir)

if __name__ == "__main__":
    main()