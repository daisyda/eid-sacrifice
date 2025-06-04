import requests

ZAPIER_SMS_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/21208618/2vf7hd5/"  # ✅ updated

def send_status_update_to_zapier(instance):
    data = {
        "name": instance.name,
        "phone": instance.phone_number,
        "status": instance.status,
        "order": instance.order_number,
    }
    try:
        requests.post(ZAPIER_SMS_WEBHOOK_URL, json=data, timeout=5)
        print("✅ Sent status update to Zapier")
    except Exception as e:
        print(f"❌ Zapier error: {e}")
