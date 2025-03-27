from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins=["https://cream-calculator-frontend.vercel.app"])

@app.route('/api/forecast', methods=['POST'])
def forecast():
    data = request.get_json()

    # Extract key inputs
    selling_price = float(data['sellingPrice'])
    ppc_per_unit = float(data['ppcPerUnit'])
    monthly_sales = int(data['monthlySales'])
    growth_rate = float(data['growthRate']) / 100
    months = int(data['forecastMonths'])
    bank_balance = float(data['bankBalance'])

    # Extract dynamic components list
    components = data.get('components', [])

    # Track inventory and output
    inventory = {}
    forecast_rows = []

    # Initialize inventory levels
    for comp in components:
        name = comp['name']
        inventory[name] = comp['initialStock']

    for month in range(1, months + 1):
        units_sold = int(monthly_sales * ((1 + growth_rate) ** (month - 1)))
        revenue = units_sold * selling_price

        # Track costs and reorders
        component_reorders = []
        total_reorder_cost = 0

        for comp in components:
            name = comp['name']
            reorder_threshold = int(comp['reorderThreshold'])
            reorder_quantity = int(comp['reorderQuantity'])
            reorder_cost = float(comp['reorderCost'])

            inventory[name] -= units_sold

            if inventory[name] <= reorder_threshold:
                inventory[name] += reorder_quantity
                total_reorder_cost += reorder_cost
                component_reorders.append(f"{name}: {reorder_quantity}")
            else:
                component_reorders.append("")

        ppc_cost = units_sold * ppc_per_unit
        total_cost = total_reorder_cost + ppc_cost
        profit = revenue - total_cost
        bank_balance += profit - total_reorder_cost
        cream = profit - total_reorder_cost

        forecast_rows.append({
            "Month": month,
            "Units Sold": units_sold,
            "Revenue": int(revenue),
            "Profit": int(profit),
            "PPC Cost": int(ppc_cost),
            "Cash Needed": int(total_reorder_cost),
            "Cream": int(cream),
            "Bank Balance": int(bank_balance),
            "Reorders": component_reorders,
            "Inventory Levels": {k: int(v) for k, v in inventory.items()}
        })

    return jsonify(forecast_rows)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


