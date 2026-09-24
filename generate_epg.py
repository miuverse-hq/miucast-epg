import datetime
import gzip

def generate_epg(days_count=30, output_path="epg.xml.gz"):
    # ปรับปรุงคำอธิบาย (desc) ให้เป็นทางการโดยใช้คำว่า IPTV ในทุกภาษา
    channels = [
        {
            "id": "EPG.th", "name": "MIUCAST-TH", "lang": "th",
            "title": "MIUCAST ผังรายการอิเล็กทรอนิกส์", 
            "desc": "บริการ IPTV จาก MIUCAST"
        },
        {
            "id": "EPG.en", "name": "MIUCAST-EN", "lang": "en",
            "title": "MIUCAST EPG", 
            "desc": "IPTV Broadcast from MIUCAST"
        },
        {
            "id": "EPG.kr", "name": "MIUCAST-KR", "lang": "ko",
            "title": "미우캐스트 EPG", 
            "desc": "MIUCAST의 IPTV 서비스"
        },
        {
            "id": "EPG.zh", "name": "MIUCAST-CN", "lang": "zh-Hans",
            "title": "MIUCAST 节目表", 
            "desc": "来自 MIUCAST 的 IPTV 服务"
        },
        {
            "id": "EPG.tw", "name": "MIUCAST-TW", "lang": "zh-Hant",
            "title": "MIUCAST 節目表", 
            "desc": "來自 MIUCAST 的 IPTV 服務"
        },
        {
            "id": "EPG.jp", "name": "MIUCAST-CN", "lang": "zh-Hans",
            "title": "ミユカスト EPG", 
            "desc": "MIUCAST からのIPTVサービス"
        }
    ]
    
    start_date = datetime.date.today()
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<tv generator-info-name="MIUCAST-EPG-AUTO">\n'
    ]
    
    # สร้างข้อมูล Channel
    for ch in channels:
        xml_lines.append(f'\t<channel id="{ch["id"]}">')
        xml_lines.append(f'\t\t<display-name lang="{ch["lang"]}">{ch["name"]}</display-name>')
        xml_lines.append('\t</channel>')
    xml_lines.append('')
    
    # สร้างข้อมูลโปรแกรมล่วงหน้า 30 วัน ในรูปแบบ GMT+7 (+0700)
    for i in range(days_count):
        current_day = start_date + datetime.timedelta(days=i)
        next_day = current_day + datetime.timedelta(days=1)
        
        day_str = current_day.strftime("%Y%m%d")
        next_day_str = next_day.strftime("%Y%m%d")
        
        for ch in channels:
            # ช่วงเวลา 12:00 ถึง 00:00 (ของวันเดียวกันถึงเที่ยงคืน)
            xml_lines.append(f'\t<programme start="{day_str}120000 +0700" stop="{next_day_str}000000 +0700" channel="{ch["id"]}">')
            xml_lines.append(f'\t\t<title lang="{ch["lang"]}">{ch["title"]}</title>')
            xml_lines.append(f'\t\t<desc lang="{ch["lang"]}">{ch["desc"]}</desc>')
            xml_lines.append('\t</programme>')
            
            # ช่วงเวลา 00:00 ถึง 12:00 (ของวันถัดไป)
            xml_lines.append(f'\t<programme start="{next_day_str}000000 +0700" stop="{next_day_str}120000 +0700" channel="{ch["id"]}">')
            xml_lines.append(f'\t\t<title lang="{ch["lang"]}">{ch["title"]}</title>')
            xml_lines.append(f'\t\t<desc lang="{ch["lang"]}">{ch["desc"]}</desc>')
            xml_lines.append('\t</programme>')
            xml_lines.append('')
            
    xml_lines.append('</tv>')
    
    xml_content = "\n".join(xml_lines)
    
    # เขียนไฟล์และบีบอัดข้อมูลแบบ Gzip
    if output_path.endswith(".gz"):
        with gzip.open(output_path, "wb") as f:
            f.write(xml_content.encode("utf-8"))
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(xml_content)

if __name__ == "__main__":
    generate_epg(30, "epg.xml.gz")
