from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="釣魚郵件偵測 API")

class EmailRequest(BaseModel):
    sender_email: str
    content: str


@app.get("/")
def read_root():
    return {"message": "歡迎來到 AI 釣魚郵件偵測 API！系統運作正常。"}


@app.post("/predict")
def predict_phishing(email: EmailRequest):

    suspicious_keywords = ["密碼", "銀行帳號", "中獎", "立即點擊", "帳戶凍結"]
    free_email_domains = ["@gmail.com", "@yahoo.com", "@hotmail.com"]

    has_suspicious_keyword = any(keyword in email.content for keyword in suspicious_keywords)

    is_free_email = any(domain in email.sender_email for domain in free_email_domains)

    if has_suspicious_keyword and is_free_email:
        return{
            "status": "critical",
            "prediction": "極度危險！免費信箱要求敏感操作，高機率為釣魚郵件!",
            "sender_analyzed": email.sender_email
        }
    elif has_suspicious_keyword:
        return{
            "status": "warning",
            "prediction": "警告：包含敏感關鍵字，請小心確認寄件者身分。",
            "sender_analyzed": email.sender_email
        }
    else:
        return{
            "status": "safe",
            "prediction": "看起來安全",
            "sender_analyzed": email.sender_email
        }