from flask import Flask, request, jsonify, render_template
import os
import os
import csv
from collections import defaultdict
import re
import time
import datetime
import calendar
from flask import json
import pymysql
from datetime import datetime  # ÕýÈ·µ¼Èë·½Ê½

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # ½â¾öÖÐÎÄÂÒÂë
datetime1 = 0

# ÐÞ¸´Â·¾¶´¦Àí
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def get_last_day_of_month(year, month):
    _, last_day = calendar.monthrange(year, month)
    return last_day

def extract_date_from_filename(filename):
    match = re.search(r'\d{8}', filename)
    if match:
        date_str = match.group()
        try:
            return datetime.datetime.strptime(date_str, '%Y%m%d')
        except ValueError:
            return None
    return None

# 数据库配置（新增）
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'zhangkaifaA',
    'db': 'mydeal',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def fetch_bill_data_from_db(target_month=None):
    """从数据库读取数据（使用 buttimea 字段）"""
    conn = pymysql.connect(**DB_CONFIG)
    fenlei = ['待定','家庭应急','王者荣耀','滴滴','济南超市','外卖','出去吃','衣服','鞋子','话费','带分类的','淘宝','房租','基金']
    try:
        with conn.cursor() as cursor:
            # 时间范围处理
            if target_month:
                year = int(target_month[:4])
                month = int(target_month[4:6])
                last_day = calendar.monthrange(year, month)[1]
                date_start = f"{year}{month:02d}01"
                date_end = f"{year}{month:02d}{last_day}"
            else:
                date_start = datetime.now().strftime("%Y%m01")
                date_end = datetime.now().strftime("%Y%m%d")

            # 关键修正：使用 buttimea 字段
            sql = """
            SELECT 
                Name, State, Laiyuan, jine, shouzhi, shangpin,
                -- Ö±½ÓÊ¹ÓÃÔ­Ê¼×Ö¶Î
                buttimea AS Buytime,
                -- ÌáÈ¡ÈÕÆÚ²¿·Ö
                DATE_FORMAT(STR_TO_DATE(buttimea, '%%Y%%m%%d%%H:%%i:%%s'), '%%Y%%m%%d') AS Buytime_jian,
                item 
            FROM your_table 
            WHERE 
                STR_TO_DATE(buttimea, '%%Y%%m%%d %%H:%%i:%%s') BETWEEN %s AND %s
            ORDER BY buttimea DESC
            """
            cursor.execute(sql, (date_start, date_end))
            results = cursor.fetchall()

        # 数据转换
        processed_data = [[] for _ in range(len(fenlei))]  # Ô¤³õÊ¼»¯·ÖÀàÁÐ±í           
        for row in results:
            item = BillItem()

            item.Name = row['Name']
            item.State = row['State']
            item.Laiyuan = row['Laiyuan']
            item.jine = float(row['jine'])
            item.shouzhi = row['shouzhi']
            item.shangpin = row['shangpin']
            item.Buytime = row['Buytime']          # 映射到展示字段
            item.Buytime_jian = row['Buytime_jian'] 
            item.item = row['item']
            print(row['Buytime'])
            # ½«Êý¾Ý´æÈë¶ÔÓ¦·ÖÀàË÷ÒýµÄÎ»ÖÃ
            if 0 <= int(row['item']) < len(processed_data):
                processed_data[int(row['item'])].append(item)
            else:
                print(f"Òì³£·ÖÀàË÷Òý: {row['item']}, Êý¾Ý¶ªÆú")

        return processed_data
    
    finally:
        conn.close()
def find_closest_file(target_date, directory):
    closest_file = None
    closest_date_diff = float('inf')
    target_date = datetime.datetime.strptime(target_date, '%Y%m%d')
    
    try:
        for filename in os.listdir(directory):
            file_date = extract_date_from_filename(filename)
            if file_date and file_date.year == target_date.year and file_date.month == target_date.month:
                date_diff = abs((target_date - file_date).days)
                if date_diff < closest_date_diff:
                    closest_date_diff = date_diff
                    closest_file = filename
    except FileNotFoundError:
        return None
    return closest_file

class BillItem:
    def __init__(self):
        self.Name = ""
        self.State = ""
        self.Laiyuan = ""
        self.jine = 0.0
        self.shouzhi = ""
        self.shangpin = ""
        self.Buytime = ""
        self.Buytime_jian = ""
        self.item = 0
        self.Data = []



def find_closest_file(target_date_str, directory):
    """¾«È·Æ¥ÅäÄêÔÂ²éÕÒÎÄ¼þ"""
    try:
        # ½âÎöÄ¿±êÄêÔÂ£¨¸ñÊ½£ºYYYYMMDD -> YYYYMM£©
        target_ym = target_date_str[:6]
        target_year = int(target_ym[:4])
        target_month = int(target_ym[4:6])
        
        # ±éÀúÄ¿Â¼ÎÄ¼þ
        valid_files = []
        for filename in os.listdir(directory):
            # Æ¥ÅäÎÄ¼þÃûÖÐµÄ8Î»ÈÕÆÚÊý×Ö
            date_match = re.search(r'(\d{4})(\d{2})\d{2}', filename)
            if date_match:
                file_year = int(date_match.group(1))
                file_month = int(date_match.group(2))
                
                # ÄêÔÂÆ¥ÅäÔò¼ÓÈëºòÑ¡ÁÐ±í
                if file_year == target_year and file_month == target_month:
                    valid_files.append(filename)
        
        # ´æÔÚÆ¥ÅäÎÄ¼þÊ±·µ»Ø×îÐÂÈÕÆÚµÄÎÄ¼þ
        if valid_files:
            # °´ÎÄ¼þÃûÈÕÆÚÅÅÐò
            valid_files.sort(key=lambda x: re.search(r'\d{8}', x).group(), reverse=True)
            return valid_files[0]
        
        # ÎÞÆ¥ÅäÎÄ¼þÊ±·µ»ØNone
        return None

    except Exception as e:
        print(f"ÎÄ¼þ²éÕÒÒì³£: {str(e)}")
        return None

def Thedate():
    global datetime1
    
    # 获取目标月份（格式YYYYMM）
    target_month = datetime1[:6] if datetime1 else None
    
    # 从数据库获取数据
    data = fetch_bill_data_from_db(target_month)
    
    # 分类规则（保留原有逻辑）
    fenlei = ['待定','家庭应急','王者荣耀','滴滴','济南超市','外卖','出去吃','衣服','鞋子','话费','带分类的','淘宝','房租','基金']
    
    # 获取更新时间（需要根据实际情况调整）
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not data or not isinstance(data, list):
        data = [[] for _ in fenlei]  # ³õÊ¼»¯¿ÕÁÐ±í½á¹¹
    
    return data, fenlei, update_time



@app.route('/get-bill-data', methods=['POST'])
def get_filtered_bill_data():
    global datetime1
    
    # 获取前端选择的月份（格式：YYYY-MM）
    selected_month = request.form.get('month')
    print(selected_month)
    try:
        # 转换月份格式为 YYYYMM
        year_month = selected_month.replace("-", "")[:6]
        if len(year_month) != 6 or not year_month.isdigit():
            raise ValueError("无效的月份格式")

        # 解析年份和月份
        year = int(year_month[:4])
        month = int(year_month[4:6])
        last_day = calendar.monthrange(year, month)[1]

        # 生成符合 buttimea 格式的时间范围（注意空格）
        date_start = f"{year:04d}{month:02d}01 00:00:00"
        date_end = f"{year:04d}{month:02d}{last_day:02d} 23:59:59"

        # 存储目标日期（用于后续查询）
        datetime1 = f"{year_month}{last_day:02d}"

        # 获取数据
        data, categories, update_time = Thedate()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "未找到该月份的数据"
            }), 404

        # 处理可视化数据
        dates, amounts, large_expenses = prepare_visualization_data(data)
 
        large_threshold = 4000  # ´ó¶îÏû·ÑãÐÖµ
        filtered_amounts = [x for x in amounts if x < large_threshold]
        total_amount_filtered = round(sum(filtered_amounts), 2)
        print(total_amount_filtered)
        # 返回标准化响应
        return jsonify({
            "status": "success",
            "data": {
                "dates": dates,
                "amounts": amounts,
                "bills": format_categories(data, categories),  # ×Ö¶ÎÃû³Æ¶ÔÆë
                "total_amount": total_amount_filtered,
                "large_expenses": large_expenses,  # ÐÂÔö×Ö¶Î
                "update_time": update_time
            }
        })
        
    except ValueError as ve:
        print(f"参数错误: {str(ve)}")
        return jsonify({
            "status": "error",
            "message": f"无效的请求参数: {str(ve)}"
        }), 400
    except Exception as e:
        print(f"服务器内部错误: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "服务器处理请求时发生错误"
        }), 500

def prepare_visualization_data(data):
    daily_amounts = defaultdict(float)
    large_expenses = []  # ÐÂÔö´ó¶îÏû·Ñ¼ÇÂ¼

    for category_data in data:
        for item in category_data:
            try:
                date_str = item.Buytime.split()[0]
                date_obj = datetime.strptime(date_str, "%Y%m%d")
                formatted_date = date_obj.strftime("%Y-%m-%d")
                
                # ¼ÇÂ¼´ó¶îÏû·Ñ
                if item.jine > 4000:
                    large_expenses.append({
                        "category": "大额消费",
                        "amount": item.jine,
                        "id":item.Name,
                        "date": formatted_date
                    })
                else:
                    daily_amounts[formatted_date] += item.jine
            except Exception as e:
                print(f"ÎÞÐ§ÈÕÆÚ¸ñÊ½: {item.Buytime}, ´íÎó: {str(e)}")
    
    sorted_dates = sorted(daily_amounts.keys())
    return sorted_dates, [round(daily_amounts[d], 2) for d in sorted_dates], large_expenses

def format_categories(data, categories):
    """统一字段名称和数据结构"""
    formatted = defaultdict(list)
    for index, category_data in enumerate(data):
        category_name = categories[index] if index < len(categories) else f"未知分类_{index}"
        for item in category_data:
            formatted[category_name].append({
                "id": item.shangpin,       # 添加前端需要的id字段
                "amount": item.jine,
                "date": item.Buytime,      # 使用完整时间戳
                "note": item.Laiyuan       # 添加备注字段
            })
    return dict(formatted)
def prepare_data(bills):
    daily_amounts = defaultdict(float)
    for category_bills in bills.values():
        for bill in category_bills:
            try:
                # È·±£ÈÕÆÚ¸ñÊ½ÕýÈ·
                date_str = bill['data_jian']
                if len(date_str) == 8:  # ¸ñÊ½Ó¦ÎªYYYYMMDD
                    formatted_date = datetime.datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")
                    amount = round(float(bill['amount']), 2)
                    if amount < 4000:

                        daily_amounts[formatted_date] += amount
            except Exception as e:
                print(f"Êý¾Ý´¦Àí´íÎó: {str(e)}")
                continue
    
    # °´ÈÕÆÚÅÅÐò²¢Ìî²¹È±Ê§ÈÕÆÚ
    dates = sorted(daily_amounts.keys(), key=lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
    start_date = min(dates) if dates else ""
    end_date = max(dates) if dates else ""
    
    # Éú³ÉÍêÕûÈÕÆÚÐòÁÐ
    full_dates = []
    current_date = datetime.datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    while current_date and current_date <= end_date:
        full_dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += datetime.timedelta(days=1)
    
    # Ìî³ä½ð¶îÊý¾Ý
    amounts = [round(daily_amounts.get(date, 0), 2) for date in full_dates]
    print(full_dates)
    return full_dates, amounts
@app.route('/')
def bill_details():
    global datetime1
    
    # »ñÈ¡Êý¾Ý£¨data ÏÖÔÚÊÇÁÐ±í½á¹¹£©
    data, fenlei, readable_time = Thedate()
    
    # ³õÊ¼»¯Êý¾Ý½á¹¹
    bills = {}
    sun_cn = []
    dae = []
    large_expenditures = []

    try:
        # ±éÀú·ÖÀàË÷Òý£¨È·±£Óë fenlei Ë³ÐòÒ»ÖÂ£©
        for index in range(len(fenlei)):
            category_name = fenlei[index]
            current_data = data[index] if index < len(data) else []
            
            category_total = 0.0
            bills[category_name] = []
            
            for dd in current_data:
                # ´¦Àí½ð¶î
                amount = float(dd.jine)
                category_total += amount
                
                # ´ó¶îÏû·Ñ¼ÇÂ¼
                if amount > 4000 or "·¿¶«" in dd.Name:
                    dae.append(dd)
                
                # ¹¹½¨ÕËµ¥Ïî
                bills[category_name].append({
                    'id': dd.shangpin,
                    'amount': amount,
                    'date': dd.Buytime,
                    'note': dd.Laiyuan,
                    'data_jian': dd.Buytime_jian
                })
            
            sun_cn.append(round(category_total, 2))

        # 总额计算
        total_amount = sum(sun_cn[:-1]) if len(sun_cn) > 1 else sum(sun_cn)  # 排除最后一项（假设最后是基金）
        total_amount_no = total_amount - sum(dd.jine for dd in dae if "基金" not in getattr(dd, 'shangpin', ''))

        # 格式化输出
        formatted_bills = {
            f"{name} 金额: {sun_cn[i]}": items 
            for i, (name, items) in enumerate(bills.items())
        }

        # 可视化数据处理
        dates, amounts = prepare_data(formatted_bills)

    except Exception as e:
        print(f"数据处理异常: {str(e)}")
        # 异常时返回空数据
        return render_template('bill_details.html',
                             bills={},
                             update_time=readable_time,
                             total_amount=0,
                             large_expenditures=[],
                             total_amount_no=0,
                             dates=[],
                             amounts=[])

    return render_template('bill_details.html',
                         bills=formatted_bills,
                         update_time=readable_time,
                         total_amount=round(total_amount, 2),
                         large_expenditures=[{
                             'category': "大额消费",
                             'bill': {
                                 'id': dd.Name,
                                 'amount': dd.jine,
                                 'date': dd.Buytime,
                                 'note': dd.Laiyuan
                             }
                         } for dd in dae],
                         total_amount_no=round(total_amount_no, 2),
                         dates=dates,
                         amounts=amounts)
    
if __name__ == '__main__':
    app.run(host="192.168.31.16",port=5555,debug=True)
