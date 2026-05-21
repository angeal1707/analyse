from flask import Flask, render_template, request, jsonify
from stock_analyzer import StockAnalyzer
import json
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pandas as pd
import numpy as np

app = Flask(__name__)
analyzer = StockAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

def convert_to_serializable(obj):
    """Convert numpy/pandas types to JSON-serializable types"""
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_to_serializable(item) for item in obj]
    elif isinstance(obj, (np.integer, np.floating)):
        return float(obj)
    elif pd.isna(obj):
        return None
    elif isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    else:
        return str(obj)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        ticker = data.get('ticker', '').strip().upper()
        
        if not ticker:
            return jsonify({'success': False, 'message': 'Masukkan nama emiten terlebih dahulu!'}), 400
        
        success, message = analyzer.fetch_stock_data(ticker)
        
        if not success:
            return jsonify({'success': False, 'message': message}), 400
        
        df = analyzer.calculate_technical_indicators()
        
        fundamental = analyzer.get_fundamental_analysis()
        trend = analyzer.analyze_trend(df)
        momentum = analyzer.analyze_momentum(df)
        recommendation = analyzer.generate_recommendation(fundamental, trend, momentum)
        
        chart_base64 = generate_chart(df)
        
        trading_plan = analyzer.generate_trading_plan(
            fundamental.get('harga_saat_ini', 0),
            trend,
            momentum,
            recommendation
        )
        
        result = {
            'success': True,
            'fundamental': convert_to_serializable(fundamental),
            'trend': convert_to_serializable(trend),
            'momentum': convert_to_serializable(momentum),
            'recommendation': convert_to_serializable(recommendation),
            'trading_plan': convert_to_serializable(trading_plan),
            'chart': chart_base64
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

def generate_chart(df):
    """
    Generate chart as base64 string
    """
    if df is None or len(df) < 20:
        return None
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    ax1.plot(df.index, df['Close'], label='Harga Penutupan', linewidth=2, color='blue')
    ax1.plot(df.index, df['SMA_20'], label='SMA 20', linewidth=1, color='orange', alpha=0.7)
    ax1.plot(df.index, df['SMA_50'], label='SMA 50', linewidth=1, color='red', alpha=0.7)
    ax1.set_title('Harga Saham & Moving Averages', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Harga (Rp)', fontsize=10)
    ax1.legend(loc='upper left', fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(df.index, df['RSI'], label='RSI (14)', linewidth=2, color='purple')
    ax2.axhline(y=70, color='r', linestyle='--', linewidth=1, alpha=0.5, label='Overbought (70)')
    ax2.axhline(y=30, color='g', linestyle='--', linewidth=1, alpha=0.5, label='Oversold (30)')
    ax2.set_title('Relative Strength Index (RSI)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('RSI', fontsize=10)
    ax2.set_xlabel('Tanggal', fontsize=10)
    ax2.legend(loc='upper left', fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 100)
    
    fig.tight_layout()
    
    img = io.BytesIO()
    FigureCanvasAgg(fig).print_png(img)
    img.seek(0)
    chart_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    
    return chart_base64

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
