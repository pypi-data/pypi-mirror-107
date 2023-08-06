# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a Indicators of economic effect of agricultural production.
The economic effect index of agricultural production is a scale 
used to measure and reflect the economic effect of agricultural 
production plans, technical measures, and agricultural investment 
projects. 
It is a specific form of the content of the economic 
effect of agricultural production through numerical values. 
Because agriculture is affected by many factors, in order to 
comprehensively measure the economic effects of agricultural 
production, it is necessary to set a series of indicators to 
reflect the size of the economic effects from a certain aspect 
and a certain range.
It contains all the formulas you will use.
"""

def land_productivity(agricultural_production,land_area):
    """
    According to the calculation formula of land productivity, the area of agricultural land including cultivated land, forest land, pasture land, garden land, nursery, breeding water surface, etc., is used to reflect the comprehensive utilization of land resources
    """
    print("The land productivity is :")
    return agricultural_production / land_area

def productivity_per_sown_area_one(agricultural_production,sown_area_of_crops):
    """
    The land productivity calculated by the sown area reflects the application degree of advanced agricultural technology and the level of intensive farming, and is often used to evaluate the economic effects of individual agricultural technical measures.
    """
    print("The productivity per sown area one is :")
    return agricultural_production / sown_area_of_crops

def productivity_per_sown_area_two(total_output,total_cultivated_land_area):
    """
    It can comprehensively reflect the utilization level of agricultural production resources (arable land) and the application level of advanced agricultural technologies. However, it is limited to the scope of the planting industry and cannot reflect the economic effects of the internal development of agriculture.
    """
    print("The productivity per sown area two is :")
    return total_output / total_cultivated_land_area

def productivity_per_unit_area_of_agricultural_land(agricultural_output_value,agricultural_land_area):
    """
    This is a comprehensive land productivity index that can comprehensively reflect the economic effects of agricultural technology programs and the comprehensive utilization of land resources. It is often used to evaluate the economic effects of comprehensive agricultural technical measures such as agricultural areas, agricultural planning, and arable land system reforms.
    """
    print("The productivity per unit area of agricultural land is :")
    return agricultural_output_value / agricultural_land_area

def land_net_output_value_rate(land_net_output_value_rate,value_of_production_materials_consumed,land_area):
    """
    The net land output value rate index excludes the influence of the value of the production materials in the transferred products. It can accurately explain the value level created by labor per unit of land area and reflect the final requirements and labor results of people’s agricultural production. It is an evaluation An important indicator of land use efficiency.
    """
    print("The land net output value rate is :")
    return (land_net_output_value_rate-value_of_production_materials_consumed) / land_area

def land_operating_rate(total_value_of_agricultural_products,cost_of_production,land_area):
    """
    This indicator reflects the effect of eliminating materialized labor and necessary labor consumption per unit area of land. It shows the size of the contribution per unit area of land to society and can comprehensively reflect the final results of land resource utilization.
    """
    print("The land operating rate is :")
    return (total_value_of_agricultural_products-cost_of_production) / land_area

def labor_productivity(product_output,labor_consumption):
    """
    In actual work, because materialized labor cannot be accurately reduced to labor time, it can generally only be expressed by the number of products produced per unit of living labor time (person-year, labor-hour, labor-day), so it is an exaggerated indicator. Pay special attention in actual application.
    """
    print("The labor productivity is :")
    return product_output / labor_consumption

def labor_net_output_rate(product_output,value_of_production_materials_consumed,labor_consumption):
    """
    This indicator refers to the number of net products produced by a unit of living labor, excluding the value impact transferred from materialized labor, and can accurately reflect the new value created by living labor for society.
    """
    print("The labor net output rate is :")
    return (product_output-value_of_production_materials_consumed) / labor_consumption

def labor_profitability(product_output,cost_of_production,labor_consumption):
    """
    This indicator refers to the number of surplus products created per unit of living labor time, and it reflects the contribution of living labor to society.
    """
    print("The Labor profitability is :")
    return (product_output-cost_of_production) / labor_consumption

def product_cost_rate(product_output,product_cost):
    """
    The cost product ratio is usually expressed by the product volume or output value provided per hundred yuan of cost.
    """
    print("The product cost rate is :")
    return product_output / product_cost

def unit_product_cost(product_cost,product_output):
    """
    Product cost refers to the value of the means of production and labor remuneration consumed by a unit of agricultural products. It includes the consumption of living labor and materialized labor.
    """
    print("The unit product cost is :")
    return product_cost / product_output

def cost_profit_rate(total_profit,product_cost):
    """
    Profit is the value created for society after compensating for all capital consumption. It reflects the proportional relationship between capital consumption and the value of surplus products. It is a widely used economic effect evaluation indicator.
    """
    print("The cost profit rate is :")
    return total_profit / product_cost

def capital_occupation_product_rate(product_output,capital_occupation):
    """
    The rate of capital occupation product refers to the proportional relationship between unit capital occupation and the number of products or output value that can be produced, and it reflects the effect of capital utilization.
    """
    print("The capital occupation product rate is :")
    return product_output / capital_occupation

def fixed_capital_occupation_rate(product_output,fixed_capital_occupation):
    """
    The output or output value produced with a fixed capital of one hundred yuan.
    """
    print("The fixed capital occupation rate is :")
    return product_output / fixed_capital_occupation

def liquidity_occupied_product_rate(product_output,Liquidity_occupation):
    """
    The output or output value produced by taking up one hundred yuan of working capital.
    """
    print("The liquidity occupied product rate is :")
    return product_output / Liquidity_occupation

def profit_rate_of_capital_occupation(the_total_profit,total_amount_of_funds_occupied):
    """
    The profit rate of capital occupation reflects the profit obtained from capital occupation, and is often measured by the profit obtained for every 100 yuan of capital occupied.
    """
    print("The profit rate of capital occupation is :")
    return the_total_profit / total_amount_of_funds_occupied

def production_growth_rate(report_the_increase_in_its_production,base_period_output):
    """
    The output growth rate index can be the output growth rate per unit area or the total output growth rate.
    """
    print("The production growth rate is :")
    return report_the_increase_in_its_production / base_period_output

def revenue_growth_rate(revenue_growth_rate_during_the_reporting_period,base_period_income):
    """
    The income growth rate indicator can be the growth rate of net income per unit area or the growth rate of total income.
    """
    print("The revenue growth rate is :")
    return revenue_growth_rate_during_the_reporting_period / base_period_income

def increased_production_growth_rate(revenue_growth_rate,production_growth_rate):
    """
    In agricultural production, the relationship between output and income is very complex, and the combination between them may also be diverse, and the ratio can appear from positive to negative.
    """
    print("The increased production growth rate is :")
    return revenue_growth_rate / production_growth_rate

def annual_productivity_per_unit_investment(annual_new_production_capacity,total_investment):
    """
    Reflects the comparative relationship between the amount of agricultural investment and the newly increased production capacity. Newly increased production capacity mainly refers to the newly increased output, output value, and net income evaluated annually.
    """
    print("The annual productivity per unit investment is :")
    return annual_new_production_capacity / total_investment

def unit_production_capacity_investment(total_investment_year,new_production_capacity):
    """
    Comparing the amount of investment per unit production capacity reflects the consumption and occupation of capital by unit production capacity, and is the reciprocal of the annual production capacity index of unit investment.
    """
    print("The unit production capacity investment is :")
    return total_investment_year / new_production_capacity

def payback_period(total_investment,annual_profit_increase):
    """
    Reflects the number of years to recover the investment amount from the realized profits in the production process after the agricultural investment is completed.
    """
    print("The payback period is :")
    return total_investment / annual_profit_increase

def investment_effect_coefficient(annual_profit_increase,total_investment):
    """
    Reflecting the ratio of annual new profits to the total investment, it is the reciprocal of the investment payback period indicator, and the calculated value is expressed as a decimal or a percentage.
    """
    print("The investment effect coefficient is :")
    return annual_profit_increase / total_investment

