import json
import os
import requests

def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Method not allowed"})
        }

    try:
        data = request.json()
    except Exception:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON"})
        }

    asistentes = data.get("asistentes")
    intolerancias = data.get("intolerancias")
    intolerancias_text = data.get("intolerancias_text", "")
    if not asistentes or not intolerancias:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing fields"})
        }


    res = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {os.environ['RESEND_API_KEY']}",
            "Content-Type": "application/json"
        },
        json={
            "from": "Web <onboarding@resend.dev>",
            "to": ["angelrodriguezbobes@gmail.com"],
            "subject": "Nueva confirmación de asistencia desde la web",
            "html": f"""
                <p><strong>Asistentes:</strong> {asistentes}</p>
                <br>
                <p><strong>Intolerancias:</strong>{intolerancias}</p>
                {'<p><strong>Intolerancia a:</strong><br><p>' + intolerancias_text if intolerancias_text else ''+'</p>'}
            """
        },
        timeout=10
    )

    if res.status_code >= 400:
        return {
            "statusCode": 502,
            "body": json.dumps({"error": "Email provider error"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"ok": True})
    }
