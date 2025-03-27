from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/forecast', methods=['POST'])
def forecast():
    data = request.get_json()

    # Extract inputs
    selling_price = float(data['sellingPrice'])
    manufacturing_cost = float(data['manufacturingCost'])
    amazon_fee = float(data['amazonFee'])
    fulfilment_fee = float(data['fulfilmentFee'])
    ppc_per_unit = float(data['ppcPerUnit'])
    monthly_sales = int(data['monthlySales'])
    bank_balance = float(data['bankBalance'])
    growth_rate = float(data['growthRate']) / 100
    forecast_months = int(data['forecastMonths'])

    oil_cost = float(data['oilCost'])
    alcohol_cost = float(data['alcoholCost'])
    component_cost = float(data['componentCost'])
    reorder_threshold = int(data['reorderThreshold'])

    oil_pack_units = 155
    alcohol_pack_units = 300
    component_pack_units = 1000

    oil_stock = oil_pack_units
    alcohol_stock = alcohol_pack_units
    component_stock = component_pack_units

    results = []

    for month in range(1, forecast_months + 1):
        revenue = selling_price * monthly_sales
        cogs = (manufacturing_cost + amazon_fee + fulfilment_fee + ppc_per_unit) * monthly_sales
        profit = revenue - cogs

        reorder_cost = 0
        oil_stock -= monthly_sales
        alcohol_stock -= monthly_sales
        component_stock -= monthly_sales

        if oil_stock < reorder_threshold:
            oil_stock += oil_pack_units
            reorder_cost += oil_cost
        if alcohol_stock < reorder_threshold:
            alcohol_stock += alcohol_pack_units
            reorder_cost += alcohol_cost
        if component_stock < reorder_threshold:
            component_stock += component_pack_units
            reorder_cost += component_cost

        bank_balance += profit - reorder_cost
        cream = max(0, profit - reorder_cost)

        results.append({
            'Month': month,
            'Units Sold': monthly_sales,
            'Revenue': f"£{int(revenue)}",
            'Profit': f"£{int(profit)}",
            'Cash Needed for Stock': f"£{int(reorder_cost)}",
            'Cream': f"£{int(cream)}",
            'Bank Balance': f"£{int(bank_balance)}",
            'Oil Stock': oil_stock,
            'Alcohol Stock': alcohol_stock,
            'Component Stock': component_stock
        })

        monthly_sales = int(monthly_sales * (1 + growth_rate))

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
