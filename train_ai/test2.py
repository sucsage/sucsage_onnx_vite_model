import joblib
model = joblib.load("logreg_tfidf_keyword_model.joblib")
import pandas as pd
import re

# ===== คำสำคัญแต่ละหมวด (ต้องเหมือนตอนเทรน) =====
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

packages = {
    1: "Template Website",
    2: "Website Design (Visual)",
    3: "Website + UX/UI (Interaction)",
    4: "Server API + Docs (Backend Only)",
    5: "Full Website + Server (End-to-End)",
    6: "System Analysis",
    7: "AI & Data Analysis",
}

def keyword_score(text, keywords):
    scores = []
    for pkg, words in keywords.items():
        count = sum(bool(re.search(w, str(text), re.IGNORECASE)) for w in words)
        scores.append(count)
    return scores

# ==========================================
print("🔹 ระบบทำนายประเภทแพ็กเกจเว็บไซต์")
print("พิมพ์ข้อความ (ภาษาไทย/อังกฤษ) แล้วกด Enter")
print("พิมพ์ 'exit' เพื่อออกจากโปรแกรม\n")

while True:
    text = input("📝 ข้อความของคุณ: ").strip()
    if text.lower() in ["exit", "quit"]:
        print("👋 จบการทดสอบ ขอบคุณครับ!")
        break
    if not text:
        print("⚠️ กรุณากรอกข้อความก่อน\n")
        continue

    # ===== 1️⃣ คำนวณ keyword score =====
    kw = keyword_score(text, keywords)

    # ===== 2️⃣ สร้าง DataFrame แบบเดียวกับตอนเทรน =====
    data = pd.DataFrame([{
        "text": text,
        **{f"kw_{i+1}": kw[i] for i in range(7)}
    }])

    # ===== 3️⃣ ทำนาย =====
    pred = int(model.predict(data)[0])
    proba = model.predict_proba(data)[0]
    confidence = max(proba) * 100

    print(f"→ ผลลัพธ์: {packages[pred]}")
    print(f"→ ความมั่นใจ: {confidence:.2f}%\n")
