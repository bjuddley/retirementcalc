import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Allow only your GitHub Pages frontend to access this API
CORS(app, resources={r"/*": {"origins": "https://bjuddley.github.io"}})

def calculate_benefit(fra, benefit, retirement_age):
    """
    Calculate Social Security benefit based on retirement age.
    """
    if retirement_age < fra:
        reduction = (fra - retirement_age) * 0.06  # 6% reduction per year
        final_benefit = round(benefit * (1 - reduction), 2)
    elif retirement_age == fra:
        final_benefit = round(benefit, 2)
    else:
        increase = (retirement_age - fra) * 0.08  # 8% increase per year
        final_benefit = round(benefit * (1 + increase), 2)

    return final_benefit

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    print("Received data:", data)

    try:
        benefit = float(data['benefit'])
        fra = int(data['fra'])

        # Compute benefits for different scenarios
        results = {
            "earliest": calculate_benefit(fra, benefit, 62),
            "fra": calculate_benefit(fra, benefit, fra),
            "age_70": calculate_benefit(fra, benefit, 70),
            "custom": calculate_benefit(fra, benefit, int(data.get('retirement_age', fra)))
        }

        print("Calculated results:", results)
        return jsonify(results)
    
    except Exception as e:
        print("Error during calculations:", e)
        return jsonify({"error": "Invalid input"}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
