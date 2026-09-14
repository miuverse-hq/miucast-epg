import datetime

def generate_epg(days_count=30, output_path="epg.xml"):
    channels = [
        {"id": "EPG.null", "name": "MIUCAST"}
    ]
    
    start_date = datetime.date.today()
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<tv generator-info-name="MIUCAST-EPG-AUTO">\n'
    ]
    
    # สร้างข้อมูล Channel
    for ch in channels:
        xml_lines.append(f'\t<channel id="{ch["id"]}">')
        xml_lines.append(f'\t\t<display-name lang="th">{ch["name"]}</display-name>')
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
            xml_lines.append('\t\t<title lang="th">MIUCAST EPG</title>')
            xml_lines.append('\t</programme>')
            
            # ช่วงเวลา 00:00 ถึง 12:00 (ของวันถัดไป)
            xml_lines.append(f'\t<programme start="{next_day_str}000000 +0700" stop="{next_day_str}120000 +0700" channel="{ch["id"]}">')
            xml_lines.append('\t\t<title lang="th">MIUCAST EPG</title>')
            xml_lines.append('\t</programme>')
            xml_lines.append('')
            
    xml_lines.append('</tv>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines))

if __name__ == "__main__":
    generate_epg(30, "epg.xml")
