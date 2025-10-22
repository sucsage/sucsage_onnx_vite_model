import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import StringTensorType, FloatTensorType
import joblib

# ==========================================
# 1️⃣ Keyword dictionary
# ==========================================
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

# ==========================================
# 2️⃣ ฟังก์ชันนับ keyword score
# ==========================================
def keyword_score(text: str, keywords: dict):
    scores = []
    for pkg, words in keywords.items():
        count = sum(bool(re.search(w, str(text), re.IGNORECASE)) for w in words)
        scores.append(count)
    return scores

# ==========================================
# 3️⃣ โหลด dataset
# ==========================================
df = pd.read_csv("auto_generated_conditions_5000_v2_refined.csv")  # ต้องมี column: text, package

# เพิ่ม keyword scores
df_keyword = df["text"].apply(lambda t: keyword_score(t, keywords))
kw_df = pd.DataFrame(df_keyword.tolist(), columns=[f"kw_{i}" for i in range(1,8)])
df = pd.concat([df, kw_df], axis=1)

# ==========================================
# 4️⃣ แบ่ง train/test
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(
    df.drop(columns=["package"]),
    df["package"],
    test_size=0.2, random_state=42, stratify=df["package"]
)

# ==========================================
# 5️⃣ Feature + Model (pure scikit-learn)
# ==========================================
feature_processor = ColumnTransformer([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), max_df=0.9, min_df=2), "text"),
    ("kw", StandardScaler(), [f"kw_{i}" for i in range(1,8)])
])

model = Pipeline([
    ("features", feature_processor),
    ("clf", LogisticRegression(max_iter=300, class_weight='balanced', solver='liblinear'))
])

# ==========================================
# 6️⃣ เทรน + ประเมิน
# ==========================================
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, digits=3))

# ==========================================
# 7️⃣ Export เป็น ONNX (100% compatible)
# ==========================================
initial_type = [
    ("text", StringTensorType([None, 1])),
    ("kw_1", FloatTensorType([None, 1])),
    ("kw_2", FloatTensorType([None, 1])),
    ("kw_3", FloatTensorType([None, 1])),
    ("kw_4", FloatTensorType([None, 1])),
    ("kw_5", FloatTensorType([None, 1])),
    ("kw_6", FloatTensorType([None, 1])),
    ("kw_7", FloatTensorType([None, 1])),
]

onnx_model = convert_sklearn(
    model,
    initial_types=initial_type,
    target_opset=17,
    options={id(model): {'zipmap': False}}  # 👈 ปิด ZipMap
)

if isinstance(onnx_model, tuple):
    onnx_model = onnx_model[0]

with open("logreg_tfidf_keyword_model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

print("✅ Exported ONNX model: logreg_tfidf_keyword_model.onnx")

# ==========================================
# 8️⃣ บันทึกโมเดล sklearn ปกติ
# ==========================================
joblib.dump(model, "logreg_tfidf_keyword_model.joblib")
print("✅ Saved scikit-learn model: logreg_tfidf_keyword_model.joblib")

# ==========================================
# 9️⃣ ทดสอบข้อความใหม่
# ==========================================
packages = {
    1: "Template Website",
    2: "Website Design (Visual)",
    3: "Website + UX/UI (Interaction)",
    4: "Server API + Docs (Backend Only)",
    5: "Full Website + Server (End-to-End)",
    6: "System Analysis",
    7: "AI & Data Analysis",
}

sample_texts = [
    "อยากได้ระบบวิเคราะห์ข้อมูล AI + dashboard สรุปยอดขาย",
    "ออกแบบ UX/UI หน้าเว็บให้สวยและใช้งานง่าย",
    "ทำ backend API เชื่อมฐานข้อมูล",
]

for t in sample_texts:
    kw = keyword_score(t, keywords)
    input_df = pd.DataFrame([{ "text": t, **{f"kw_{i+1}": kw[i] for i in range(7)} }])
    pred = int(model.predict(input_df)[0])
    print(f"ข้อความ: {t}\n→ ทำนายเป็น: {packages[pred]}\n")
