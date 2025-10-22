import random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# (ส่วนตั้งค่าฟอนต์และ packages เดิม)
# ===============================
# 🔹 ตั้งค่าฟอนต์ภาษาไทย (เพื่อกราฟ)
# ===============================
try:
    font = FontProperties(fname="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=12)
except:
    font = None

# ===============================
# 🔹 ชื่อแพ็กเกจ
# ===============================
packages = {
    1: "Template Website",
    2: "Website Design (Visual)",
    3: "Website + UX/UI (Interaction)",
    4: "Server API + Docs (Backend Only)",
    5: "Full Website + Server (End-to-End)",
    6: "System Analysis",
    7: "AI & Data Analysis",
}

# ===============================
# 🔹 คีย์เวิร์ดเฉพาะแต่ละหมวด (ปรับปรุงใหม่ตามข้อเสนอแนะ)
# ===============================
keywords = {
    # 1️⃣ Template Website – เน้น “มีแบบอยู่แล้ว”
    1: [
        "template", "เทมเพลต", "มีแบบแล้ว", "เว็บต้นแบบ", "เว็บตัวอย่าง", "โครงสร้างเดิม",
        "clone layout", "deploy static site", "upload html", "เว็บเดิม", "convert figma to html", "ตามแบบ"
    ],

    # 2️⃣ Website Design – เน้น “Visual Design / ความสวยงาม”
    2: [
        "Visual Design", "Color Palette", "Mood Board", "Brand Identity", "Aesthetic",
        "ออกแบบเว็บใหม่", "ดีไซน์หน้าเว็บ", "สร้างหน้าแรก", "ปรับโทนสี", "landing page design",
        "rebranding", "mockup", "figma ui", "ปรับโครงสร้างหน้าเว็บ", "ความสวยงาม"
    ],

    # 3️⃣ Website + UX/UI – เน้น “Interaction / Flow / Testing”
    3: [
        "UX/UI", "user journey", "flow ผู้ใช้", "wireframe figma", "prototype", "interaction design",
        "responsive website", "Information Architecture", "Usability Testing", "A/B Testing",
        "user test", "usability", "ออกแบบ UX", "ดีไซน์ระบบ"
    ],

    # 4️⃣ Server API + Docs – เน้น “Backend Only / Microservice”
    4: [
        "API", "หลังบ้าน", "backend", "server", "ฐานข้อมูล", "swagger", "JWT", "RESTful API",
        "express", "node.js", "endpoint", "ระบบจัดการข้อมูล", "เชื่อมฐานข้อมูล", "เอกสาร API",
        "GraphQL", "Microservices", "Serverless Function", "งานหลังบ้านอย่างเดียว"
    ],

    # 5️⃣ Full Website + Server – เน้น “ครบวงจร front + back + deploy (End-to-End)”
    5: [
        "เว็บเต็มระบบ", "ครบ frontend backend", "deploy production", "ครบวงจร", "web + api",
        "ระบบทั้งหมด", "full stack", "maintenance", "security setup", "hosting setup",
        "domain integration", "admin dashboard", "auto backup", "CI/CD Pipeline",
        "DevOps", "End-to-End Solution"
    ],

    # 6️⃣ System Analysis – เน้น “วิเคราะห์ / เอกสารระบบ / โครงสร้างข้อมูล” (เดิมดีอยู่แล้ว)
    6: [
        "วิเคราะห์ระบบ", "system analysis", "ออกแบบโครงสร้าง", "ผังงาน", "SRS", "requirement gathering",
        "ER diagram", "use case", "UML", "architecture plan", "process mapping", "data model", "functional spec",
        "วิเคราะห์ระบบโรงพยาบาล", "ระบบ ERP", "ระบบโรงเรียน", "system design document"
    ],

    # 7️⃣ AI & Data Analysis – เน้น “ข้อมูล / พยากรณ์ / dashboard” (เดิมดีอยู่แล้ว)
    7: [
        "AI", "machine learning", "data analytics", "dashboard", "data visualization",
        "predictive model", "python analysis", "วิเคราะห์ข้อมูล", "data science",
        "sales forecast", "trend analysis", "model training", "business insight",
        "kpi dashboard", "data mining", "forecast system", "ระบบวิเคราะห์ยอดขาย", "วิเคราะห์ข้อมูลผู้ป่วย"
    ],
}

# ===============================
# 🔹 ส่วนขยายเสริมโทนลูกค้าจริง (เดิม)
# ===============================
extras = [
    "ครับ", "ค่ะ", "นะครับ", "นะคะ",
    "รีบหน่อยนะ", "ส่งใบเสนอราคามาให้หน่อย",
    "อยากได้เร็วที่สุด", "ภายในเดือนนี้ได้ไหม",
    "รองรับมือถือด้วย", "Include maintenance",
    "Need admin dashboard", "พร้อม hosting",
    "Include English version", "เน้นความเร็วโหลด",
]

# ===============================
# 🔹 Template เฉพาะแต่ละหมวด (ปรับปรุงใหม่ตามข้อเสนอแนะ)
# ===============================
exclusive_templates = {
    1: ["มีแบบแล้ว อยากให้ทีมช่วยขึ้นเว็บ", "อยากให้ช่วย deploy เว็บตามแบบ", "มีเทมเพลตพร้อม อยากให้ทีมขึ้นจริง"],
    2: ["อยากปรับ Visual Design เว็บให้เข้ากับแบรนด์", "ออกแบบ Mood Board และปรับโทนสีใหม่", "ดีไซน์หน้าเว็บเน้นความสวยงาม"],
    3: ["อยากได้ทีม UX/UI เพื่อปรับปรุง User Flow", "ออกแบบ Information Architecture และ Prototype", "ขอ A/B Testing เพื่อดู Usability"],
    4: ["อยากได้ Backend API สำหรับเชื่อมฐานข้อมูลอย่างเดียว", "ทำ Microservices และ Serverless Function", "ต้องการเอกสาร API Swagger"],
    5: ["อยากได้เว็บครบวงจร Full Stack พร้อม CI/CD", "เว็บพร้อม deploy production และ DevOps", "ขอทีมดูแล End-to-End Solution"],
    6: ["อยากให้ช่วยวิเคราะห์ระบบก่อนพัฒนา", "ขอเอกสาร SRS และผังงานระบบ", "ออกแบบ ER diagram และ use case diagram"],
    7: ["อยากได้ระบบ AI วิเคราะห์ข้อมูล", "ขอ dashboard แสดงยอดขายแบบ realtime", "ระบบคาดการณ์ข้อมูลด้วย machine learning"],
}

# ===============================
# 🔹 Template ภาษาอังกฤษ (ปรับปรุงใหม่ตามข้อเสนอแนะ)
# ===============================
eng_templates = {
    1: ["Deploy existing template", "Upload static website", "Use ready-made layout"],
    2: ["Visual Design for brand alignment", "Need a Color Palette and UI update", "Aesthetic landing page design"],
    3: ["UX/UI flow improvement", "Information Architecture and Prototype", "Need Usability Testing and User Journey"],
    4: ["Backend API Only with database", "Serverless Function for specific services", "Need GraphQL endpoint and docs"],
    5: ["Full Stack web development with CI/CD", "End-to-end Solution and Maintenance", "Complete system with Security Setup"],
    6: ["System analysis and documentation", "Requirement flow diagram", "Architecture plan before coding"],
    7: ["AI dashboard for data insight", "Predictive analytics model", "Machine learning sales forecast"],
}

# ===============================
# 🔹 ฟังก์ชันสร้างข้อความ (เดิม)
# ===============================
def make_random_text(package_num: int) -> tuple[str, str]:
    pkg = packages[package_num]
    kw = random.choice(keywords[package_num])

    lang = "th" if random.random() < 0.6 else "en"

    if lang == "th":
        # เลือก template พิเศษ 50% หรือใช้ kw ผสม 50%
        if random.random() < 0.5:
             base = random.choice(exclusive_templates[package_num])
        else:
            base = f"อยากได้ {kw} สำหรับ {pkg}" # รูปแบบผสม kw
        
        base = base.replace("{pkg}", pkg).replace("{kw}", kw)
        if random.random() < 0.5:
            base += " " + random.choice(extras)
    else:
        # เลือก template พิเศษ 50% หรือใช้ kw ผสม 50%
        if random.random() < 0.5:
            base = random.choice(eng_templates[package_num])
        else:
            base = f"Need {kw} service for {pkg}" # รูปแบบผสม kw
            
        if random.random() < 0.4:
            base += " " + random.choice(["ASAP", "with SEO", "with admin panel", "in 2 weeks", "please include docs"])

    return base.strip(), lang

# ===============================
# 🔹 สร้าง dataset สมดุล (เดิม)
# ===============================
total_rows = 5000
rows_per_pkg = total_rows // len(packages)

rows = []
for pkg_num in packages:
    for _ in range(rows_per_pkg):
        text, lang = make_random_text(pkg_num)
        rows.append((text, pkg_num, lang))

while len(rows) < total_rows:
    pkg_num = random.randint(1, 7)
    text, lang = make_random_text(pkg_num)
    rows.append((text, pkg_num, lang))

random.shuffle(rows)

# ===============================
# 🔹 แปลงเป็น DataFrame (เดิม)
# ===============================
df = pd.DataFrame(rows, columns=["text", "package", "lang"])
df["package_name"] = df["package"].map(packages)

output_file = "auto_generated_conditions_5000_v2_refined.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(df.sample(10))
print("✅ Dataset สร้างเสร็จสมบูรณ์:", len(df), "แถว ->", output_file)