from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins=["https://cream-calculator-frontend.vercel.app"])

@app.route('/api/forecast', methods=['POST'])
def forecast():
    try:
        data = request.get_json()

        # Extract data
        selling_price = float(data['sellingPrice'])
        ppc = float(data.get('ppcPerUnit', 0))
        monthly_sales = int(data['monthlySales'])
        bank_balance = float(data['bankBalance'])
        growth_rate = float(data.get('growthRate', 0)) / 100
        forecast_months = int(data.get('forecastMonths', 12))
        components = data.get('components', [])

        # Set up initial stock levels
        stock = {}
        for comp in components:
            stock[comp['name']] = int(comp.get('initialStock', 0))

        # Track results
        results = []

        for month in range(1, forecast_months + 1):
            units_sold = int(monthly_sales)
            total_cogs = 0
            reorder_costs = 0

            # Component stock check and reorder
            for comp in components:
                name = comp['name']
                threshold = int(comp.get('reorderThreshold', 0))
                reorder_qty = int(comp.get('reorderQuantity', 0))
                reorder_cost = float(comp.get('reorderCost', 0))

                # Reduce stock by units sold
                stock[name] -= units_sold

                # Reorder if below threshold
                if stock[name] <= threshold:
                    stock[name] += reorder_qty
                    reorder_costs += reorder_cost

                total_cogs += reorder_costs / forecast_months  # avg monthly component cost

            # Revenue & Profit
            revenue = units_sold * selling_price
            costs = units_sold * ppc + total_cogs
            profit = revenue - costs

            # Bank + Cream
            bank_balance += profit - reorder_costs
            cream = max(0, profit - reorder_costs)

            # Record this month
            result = {
                "Month": month,
                "Units Sold": units_sold,
                "Profit (£)": round(profit),
                "Cash Needed (£)": round(reorder_costs),
                "Cream (£)": round(cream),
                "Bank (£)": round(bank_balance)
            }

            # Include live stock for each component
            for comp in components:
                result[f"{comp['name'].capitalize()} Stock"] = stock[comp['name']]

            results.append(result)

            # Grow for next month
            monthly_sales = int(monthly_sales * (1 + growth_rate))

        return jsonify({"forecast": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)




