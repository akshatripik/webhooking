from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    print(f"\n🔔 GitHub Webhook Triggered at {datetime.now()}")

    try:
        # Log headers
        print("🔐 Headers:", dict(request.headers))

        # Get and print raw payload
        raw_payload = request.get_data(as_text=True)
        print("📦 Raw Payload:", raw_payload)

        # Try to parse JSON (GitHub usually sends application/json)
        payload = request.get_json(silent=True)

        if payload:
            print(f"✅ Repository: {payload['repository']['full_name']}")
            print(f"👤 Pusher: {payload['pusher']['name']}")
            print(f"🌿 Branch: {payload['ref'].split('/')[-1]}")
            print("📝 Commits:")
            for commit in payload['commits']:
                print(f"  - {commit['message']} by {commit['author']['name']}")
        else:
            print("⚠️ JSON payload could not be parsed.")

        return jsonify({"status": "Webhook received"}), 200

    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
