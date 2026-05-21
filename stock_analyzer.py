import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import time

class StockAnalyzer:
    def __init__(self):
        self.stock_data = None
        self.ticker = None
        self.info = None
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def fetch_stock_data(self, ticker_name):
        """
        Mengambil data saham dari Yahoo Finance dengan retry logic
        """
        try:
            ticker = ticker_name.upper() + ".JK"
            self.ticker = ticker
            
            max_retries = 5
            retry_delay = 3
            
            for attempt in range(max_retries):
                try:
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=365)
                    
                    self.stock_data = yf.download(
                        ticker, 
                        start=start_date, 
                        end=end_date, 
                        progress=False,
                        timeout=30
                    )
                    
                    if self.stock_data is None or self.stock_data.empty:
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay)
                            retry_delay += 2
                            continue
                        return False, "Saham tidak ditemukan. Pastikan nama emiten benar."
                    
                    try:
                        stock = yf.Ticker(ticker)
                        self.info = stock.info
                    except:
                        self.info = {}
                    
                    return True, "Data berhasil diambil"
                    
                except Exception as e:
                    error_str = str(e).lower()
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay += 2
                        continue
                    else:
                        if "429" in error_str or "too many" in error_str:
                            return False, "Terlalu banyak request. Coba lagi dalam beberapa menit."
                        elif "timeout" in error_str or "connection" in error_str:
                            return False, "Gagal terhubung ke Yahoo Finance. Coba lagi nanti."
                        else:
                            return False, f"Error mengambil data: {str(e)[:100]}"
            
            return False, "Gagal mengambil data saham setelah beberapa kali percobaan."
        except Exception as e:
            return False, f"Error: {str(e)[:100]}"
    
    def calculate_technical_indicators(self):
        """
        Menghitung indikator teknikal
        """
        if self.stock_data is None:
            return None
        
        df = self.stock_data.copy()
        
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        
        df['RSI'] = self.calculate_rsi(df['Close'])
        
        df['MACD'], df['Signal_Line'] = self.calculate_macd(df['Close'])
        
        df['BB_Upper'], df['BB_Middle'], df['BB_Lower'] = self.calculate_bollinger_bands(df['Close'])
        
        return df
    
    def calculate_rsi(self, prices, period=14):
        """
        Menghitung Relative Strength Index (RSI)
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """
        Menghitung MACD (Moving Average Convergence Divergence)
        """
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal).mean()
        return macd, signal_line
    
    def calculate_bollinger_bands(self, prices, period=20, std_dev=2):
        """
        Menghitung Bollinger Bands
        """
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        
        upper = sma + (std * std_dev)
        lower = sma - (std * std_dev)
        
        return upper, sma, lower
    
    def get_fundamental_analysis(self):
        """
        Menganalisis fundamental saham
        """
        if not self.info:
            return {}
        
        analysis = {
            'nama_perusahaan': self.info.get('longName', 'N/A'),
            'sektor': self.info.get('sector', 'N/A'),
            'industri': self.info.get('industry', 'N/A'),
            'harga_saat_ini': self.info.get('currentPrice', 0),
            'pe_ratio': self.info.get('trailingPE', 'N/A'),
            'pb_ratio': self.info.get('priceToBook', 'N/A'),
            'dividend_yield': self.info.get('dividendYield', 0),
            'market_cap': self.info.get('marketCap', 'N/A'),
            'eps': self.info.get('trailingEps', 'N/A'),
            'book_value': self.info.get('bookValue', 'N/A'),
        }
        
        return analysis
    
    def analyze_trend(self, df):
        """
        Menganalisis tren harga
        """
        if df is None or len(df) < 50:
            return None
        
        try:
            current_price = float(df['Close'].iloc[-1].item() if hasattr(df['Close'].iloc[-1], 'item') else df['Close'].iloc[-1])
            
            sma_20_val = df['SMA_20'].iloc[-1]
            sma_50_val = df['SMA_50'].iloc[-1]
            sma_200_val = df['SMA_200'].iloc[-1]
            
            sma_20 = float(sma_20_val.item() if hasattr(sma_20_val, 'item') else sma_20_val) if pd.notna(sma_20_val) else None
            sma_50 = float(sma_50_val.item() if hasattr(sma_50_val, 'item') else sma_50_val) if pd.notna(sma_50_val) else None
            sma_200 = float(sma_200_val.item() if hasattr(sma_200_val, 'item') else sma_200_val) if pd.notna(sma_200_val) else None
            
            trend = {
                'harga_saat_ini': round(current_price, 2),
                'sma_20': round(sma_20, 2) if sma_20 is not None else 'N/A',
                'sma_50': round(sma_50, 2) if sma_50 is not None else 'N/A',
                'sma_200': round(sma_200, 2) if sma_200 is not None else 'N/A',
                'status_tren': 'DATA TIDAK CUKUP'
            }
            
            if sma_20 is not None and sma_50 is not None and sma_200 is not None:
                if current_price > sma_20 > sma_50 > sma_200:
                    trend['status_tren'] = "UPTREND KUAT"
                elif current_price > sma_50 > sma_200:
                    trend['status_tren'] = "UPTREND"
                elif current_price < sma_20 < sma_50 < sma_200:
                    trend['status_tren'] = "DOWNTREND KUAT"
                elif current_price < sma_50 < sma_200:
                    trend['status_tren'] = "DOWNTREND"
                else:
                    trend['status_tren'] = "SIDEWAYS"
            
            return trend
        except Exception as e:
            import traceback
            print(f"Error in analyze_trend: {e}")
            print(traceback.format_exc())
            return {
                'harga_saat_ini': 'N/A',
                'sma_20': 'N/A',
                'sma_50': 'N/A',
                'sma_200': 'N/A',
                'status_tren': 'ERROR'
            }
    
    def analyze_momentum(self, df):
        """
        Menganalisis momentum dengan RSI dan MACD
        """
        if df is None or len(df) < 26:
            return None
        
        try:
            rsi_val = df['RSI'].iloc[-1]
            macd_val = df['MACD'].iloc[-1]
            signal_val = df['Signal_Line'].iloc[-1]
            
            rsi = float(rsi_val.item() if hasattr(rsi_val, 'item') else rsi_val) if pd.notna(rsi_val) else None
            macd = float(macd_val.item() if hasattr(macd_val, 'item') else macd_val) if pd.notna(macd_val) else None
            signal_line = float(signal_val.item() if hasattr(signal_val, 'item') else signal_val) if pd.notna(signal_val) else None
            
            momentum = {
                'rsi': round(rsi, 2) if rsi is not None else 'N/A',
                'macd': round(macd, 2) if macd is not None else 'N/A',
                'signal_line': round(signal_line, 2) if signal_line is not None else 'N/A',
            }
            
            if rsi is not None:
                if rsi > 70:
                    momentum['rsi_status'] = "OVERBOUGHT (Jual)"
                elif rsi < 30:
                    momentum['rsi_status'] = "OVERSOLD (Beli)"
                else:
                    momentum['rsi_status'] = "NORMAL"
            
            if macd is not None and signal_line is not None:
                if macd > signal_line:
                    momentum['macd_status'] = "BULLISH (Beli)"
                else:
                    momentum['macd_status'] = "BEARISH (Jual)"
            
            return momentum
        except Exception as e:
            return {
                'rsi': 'N/A',
                'macd': 'N/A',
                'signal_line': 'N/A',
                'rsi_status': 'ERROR',
                'macd_status': 'ERROR'
            }
    
    def generate_recommendation(self, fundamental, trend, momentum):
        """
        Menghasilkan rekomendasi beli/jual dengan weighted scoring
        """
        score = 50
        signals = []
        
        trend_score = 0
        momentum_score = 0
        fundamental_score = 0
        
        if isinstance(trend, dict) and 'status_tren' in trend:
            status = trend.get('status_tren', '')
            if 'UPTREND KUAT' in status:
                trend_score = 25
                signals.append("✓ Tren naik kuat")
            elif 'UPTREND' in status:
                trend_score = 15
                signals.append("✓ Tren naik")
            elif 'SIDEWAYS' in status:
                trend_score = 5
                signals.append("• Tren sideways (netral)")
            elif 'DOWNTREND' in status:
                trend_score = -15
                signals.append("✗ Tren turun")
            elif 'DOWNTREND KUAT' in status:
                trend_score = -25
                signals.append("✗ Tren turun kuat")
            else:
                trend_score = 0
                signals.append("• Status tren tidak jelas")
        
        if isinstance(momentum, dict):
            rsi_status = momentum.get('rsi_status', '')
            macd_status = momentum.get('macd_status', '')
            
            if rsi_status == "OVERSOLD (Beli)":
                momentum_score += 15
                signals.append("✓ RSI oversold (peluang beli)")
            elif rsi_status == "OVERBOUGHT (Jual)":
                momentum_score -= 10
                signals.append("✗ RSI overbought (hindari)")
            elif rsi_status == "NORMAL":
                momentum_score += 5
                signals.append("• RSI normal")
            
            if macd_status == "BULLISH (Beli)":
                momentum_score += 15
                signals.append("✓ MACD bullish")
            elif macd_status == "BEARISH (Jual)":
                momentum_score -= 10
                signals.append("✗ MACD bearish")
        
        if isinstance(fundamental, dict):
            pe_ratio = fundamental.get('pe_ratio', 'N/A')
            pb_ratio = fundamental.get('pb_ratio', 'N/A')
            dividend_yield = fundamental.get('dividend_yield', 0)
            
            if isinstance(pe_ratio, (int, float)):
                if 0 < pe_ratio < 15:
                    fundamental_score += 15
                    signals.append("✓ P/E ratio sangat rendah (undervalued)")
                elif 15 <= pe_ratio < 25:
                    fundamental_score += 10
                    signals.append("✓ P/E ratio rendah (undervalued)")
                elif 25 <= pe_ratio < 35:
                    fundamental_score += 5
                    signals.append("• P/E ratio wajar")
                else:
                    fundamental_score -= 5
                    signals.append("✗ P/E ratio tinggi (overvalued)")
            
            if isinstance(pb_ratio, (int, float)):
                if 0 < pb_ratio < 1.5:
                    fundamental_score += 10
                    signals.append("✓ P/B ratio rendah (undervalued)")
                elif pb_ratio >= 1.5:
                    fundamental_score += 5
                    signals.append("• P/B ratio wajar")
            
            if isinstance(dividend_yield, (int, float)):
                if dividend_yield > 0.05:
                    fundamental_score += 10
                    signals.append("✓ Dividend yield tinggi")
                elif dividend_yield > 0.03:
                    fundamental_score += 5
                    signals.append("✓ Dividend yield menarik")
                elif dividend_yield > 0:
                    fundamental_score += 2
                    signals.append("• Ada dividend yield")
        
        score = 50 + trend_score + momentum_score + fundamental_score
        score = max(0, min(100, score))
        
        if score >= 75:
            recommendation = "BELI (BUY)"
            confidence = "TINGGI"
        elif score >= 60:
            recommendation = "BELI (BUY)"
            confidence = "SEDANG"
        elif score >= 50:
            recommendation = "PERTIMBANGKAN (HOLD)"
            confidence = "SEDANG"
        elif score >= 40:
            recommendation = "PERTIMBANGKAN (HOLD)"
            confidence = "RENDAH"
        else:
            recommendation = "JANGAN BELI (SELL)"
            confidence = "SEDANG"
        
        return {
            'rekomendasi': recommendation,
            'skor': round(score, 1),
            'kepercayaan': confidence,
            'sinyal': signals
        }
    
    def get_price_history(self):
        """
        Mendapatkan riwayat harga 1 tahun
        """
        if self.stock_data is None:
            return None
        
        return self.stock_data[['Close']].copy()
    
    def generate_trading_plan(self, current_price, trend, momentum, recommendation):
        """
        Menghasilkan trading plan dengan entry, target, dan stop loss
        """
        if current_price is None or current_price <= 0:
            return None
        
        plan = {
            'current_price': round(current_price, 2),
            'strategy': '',
            'entry_points': [],
            'target_prices': [],
            'stop_loss': None,
            'risk_reward_ratio': 'N/A',
            'notes': []
        }
        
        try:
            recommendation_text = recommendation.get('rekomendasi', '')
            score = recommendation.get('skor', 50)
            
            if 'BELI' in recommendation_text:
                plan['strategy'] = 'LONG (Beli)'
                
                entry_price = current_price
                plan['entry_points'].append({
                    'level': round(entry_price, 2),
                    'description': 'Entry point saat ini'
                })
                
                if score >= 75:
                    plan['entry_points'].append({
                        'level': round(current_price * 0.98, 2),
                        'description': 'Entry point alternatif (pullback 2%)'
                    })
                
                target_1 = round(current_price * 1.05, 2)
                target_2 = round(current_price * 1.10, 2)
                target_3 = round(current_price * 1.15, 2)
                
                plan['target_prices'] = [
                    {'level': target_1, 'percentage': '+5%', 'description': 'Target 1 (Take Profit)'},
                    {'level': target_2, 'percentage': '+10%', 'description': 'Target 2 (Take Profit)'},
                    {'level': target_3, 'percentage': '+15%', 'description': 'Target 3 (Take Profit)'}
                ]
                
                stop_loss = round(current_price * 0.95, 2)
                plan['stop_loss'] = {
                    'level': stop_loss,
                    'percentage': '-5%',
                    'description': 'Stop Loss untuk limit risiko'
                }
                
                risk = current_price - stop_loss
                reward = target_2 - current_price
                if risk > 0:
                    plan['risk_reward_ratio'] = f"1:{round(reward/risk, 2)}"
                
                if isinstance(trend, dict) and 'UPTREND' in trend.get('status_tren', ''):
                    plan['notes'].append("✓ Tren mendukung, momentum positif")
                
                if isinstance(momentum, dict) and momentum.get('rsi_status') == "OVERSOLD (Beli)":
                    plan['notes'].append("✓ RSI oversold, peluang bounce up")
                
                if score >= 75:
                    plan['notes'].append("✓ Skor analisis sangat baik, confidence tinggi")
                    plan['notes'].append("• Pertimbangkan posisi lebih besar")
                elif score >= 60:
                    plan['notes'].append("• Skor analisis baik, confidence sedang")
                    plan['notes'].append("• Gunakan posisi normal")
                
            elif 'HOLD' in recommendation_text:
                plan['strategy'] = 'HOLD/WAIT'
                
                entry_price = current_price
                plan['entry_points'].append({
                    'level': round(entry_price * 0.95, 2),
                    'description': 'Entry point jika pullback 5%'
                })
                plan['entry_points'].append({
                    'level': round(entry_price * 0.90, 2),
                    'description': 'Entry point jika pullback 10%'
                })
                
                target_1 = round(current_price * 1.08, 2)
                target_2 = round(current_price * 1.12, 2)
                
                plan['target_prices'] = [
                    {'level': target_1, 'percentage': '+8%', 'description': 'Target 1'},
                    {'level': target_2, 'percentage': '+12%', 'description': 'Target 2'}
                ]
                
                stop_loss = round(current_price * 0.92, 2)
                plan['stop_loss'] = {
                    'level': stop_loss,
                    'percentage': '-8%',
                    'description': 'Stop Loss'
                }
                
                plan['notes'].append("• Tunggu sinyal yang lebih jelas")
                plan['notes'].append("• Monitor pergerakan harga dan volume")
                plan['notes'].append("• Jangan terburu-buru masuk")
                
            else:
                plan['strategy'] = 'AVOID/SELL'
                plan['notes'].append("✗ Hindari membeli saat ini")
                plan['notes'].append("✗ Pertimbangkan untuk exit jika sudah holding")
                plan['notes'].append("• Tunggu hingga ada sinyal positif yang lebih kuat")
            
            return plan
            
        except Exception as e:
            return None
