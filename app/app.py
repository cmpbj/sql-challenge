import psycopg2
import pandas as pd
import streamlit as st
import os

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST', 'postgres')  # Default to 'postgres' if not set
db_port = os.getenv('DB_PORT', '5432')

# Connection
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    port=db_port,
    host=db_host,
    password=db_password
)


cur = conn.cursor()

st.markdown(
    """
    # **Jornada de Dados** - SQL Bootcamp Challenges

    ### This app aims to present some of the questions asked in this challenge and the way i answered it

    """
)


st.divider()

st.subheader("Question 01")
st.subheader("a) What was the total revenue in 1997?")

code = st.toggle("Click to see the code", key="question_1")

if code:
    code = '''
with
	order_details as (
		select *
		from mydatabase.public.order_details
	)
	, orders as (
		select *
		from mydatabase.public.orders
	)
	, price_with_discount as (
		select
			*
			, unit_price - (unit_price * discount) as unit_price_with_discount
		from order_details
	)
	, total_revenue_per_year as (
		select
			extract(year from orders.order_date) as year
			, sum(
				price_with_discount.unit_price_with_discount * price_with_discount.quantity
			) as revenue
		from price_with_discount
		left join orders
			on price_with_discount.order_id = orders.order_id
		group by extract(year from orders.order_date)
		order by extract(year from orders.order_date)
	)
select *
from total_revenue_per_year
where year = 1997
'''
    st.code(code, language="sql")


cur.execute("SELECT * FROM mydatabase.public.vw_total_revenue_1977")


records = cur.fetchall()

columns = ['year', 'revenue']

df = pd.DataFrame(records, columns=columns)
st.dataframe(df)

st.subheader("b) Perform a monthly growth analysis and YTD calculation")

code = st.toggle("Click to see the code", key="question_2")

if code:
    code = '''
with
	order_details as (
		select *
		from mydatabase.public.order_details
	)
	, orders as (
		select *
		from mydatabase.public.orders
	)
	, price_with_discount as (
		select
			*
			, unit_price - (unit_price * discount) as unit_price_with_discount
		from order_details
	)
	, total_revenue_per_year as (
		select
			extract(year from orders.order_date) as year
			, extract(month from orders.order_date) as month
			, sum(
				price_with_discount.unit_price_with_discount * price_with_discount.quantity
			) as revenue
		from price_with_discount
		left join orders
			on price_with_discount.order_id = orders.order_id
		group by 
			extract(year from orders.order_date)
			, extract(month from orders.order_date)
		order by
			extract(year from orders.order_date)
			, extract(month from orders.order_date)
	)
	, get_last_revenue as (
		select
			*
			, lag(revenue, 1) over(
				order by year
			) as last_revenue
		from total_revenue_per_year
	)
	, cummulative_sum as (
		select
			*
			, sum(revenue) over(partition by year order by month) as month_revenue_ytd
		from get_last_revenue
	)
	, year_to_date_calc as (
		select
			*
			, ((revenue - last_revenue) / last_revenue) * 100 as ytd
		from get_last_revenue
	)
select *
from year_to_date_calc
'''
    st.code(code, language="sql")


cur.execute("SELECT * FROM mydatabase.public.vw_ytd_calculation")


records = cur.fetchall()

columns = ['year', 'month', 'revenue', 'last_revenue', 'ytd']

df = pd.DataFrame(records, columns=columns)
st.dataframe(df)

st.divider()

st.subheader("Question 02")
st.subheader("a) What is the total amount each customer has paid so far?")

code = st.toggle("Click to see the code", key="question_3")

if code:
    code = '''
with
	order_details as (
		select *
		from mydatabase.public.order_details
	)
	, orders as (
		select *
		from mydatabase.public.orders
	)
	, customers as (
		select *
		from mydatabase.public.customers
	)
	, orders_with_customer_name as (
		select
			orders.*
			, customers.company_name
		from orders
		left join customers
			on orders.customer_id = customers.customer_id
	)
	, spent_value_by_customers as (
		select
			orders_with_customer_name.company_name
			, sum((unit_price - (unit_price * discount)) * quantity) as total_spend
		from order_details
		left join orders_with_customer_name
			on order_details.order_id = orders_with_customer_name.order_id
		group by orders_with_customer_name.company_name
	)
select *
from spent_value_by_customers
order by total_spend desc
'''
    st.code(code, language="sql")


cur.execute("SELECT * FROM mydatabase.public.vw_total_revenue_per_customer")


records = cur.fetchall()

columns = ['company_name', 'total_spend']

df = pd.DataFrame(records, columns=columns)
st.dataframe(df)

st.subheader("b) Separate customers into 5 groups according to the amount paid per customer?")

code = st.toggle("Click to see the code", key="question_4")

if code:
    code = '''
with
	order_details as (
		select *
		from mydatabase.public.order_details
	)
	, orders as (
		select *
		from mydatabase.public.orders
	)
	, customers as (
		select *
		from mydatabase.public.customers
	)
	, orders_with_customer_name as (
		select
			orders.*
			, customers.company_name
		from orders
		left join customers
			on orders.customer_id = customers.customer_id
	)
	, spent_value_by_customers as (
		select
			orders_with_customer_name.company_name
			, sum((unit_price - (unit_price * discount)) * quantity) as total_spend
		from order_details
		left join orders_with_customer_name
			on order_details.order_id = orders_with_customer_name.order_id
		group by orders_with_customer_name.company_name
	)
	, get_groups as (
		select
			*
			, ntile(5) over (order by total_spend desc) as group_number
		from spent_value_by_customers
	)
select *
from get_groups
order by total_spend desc
'''
    st.code(code, language="sql")


cur.execute("SELECT * FROM mydatabase.public.vw_total_revenue_per_customer_group")


records = cur.fetchall()

columns = ['company_name', 'total_spend', 'group_number']

df = pd.DataFrame(records, columns=columns)
st.dataframe(df)

st.subheader("c) Now only customers who are in groups 3, 4 and 5 can have a special Marketing analysis carried out with them?")

code = st.toggle("Click to see the code", key="question_5")

if code:
    code = '''
with
	order_details as (
		select *
		from mydatabase.public.order_details
	)
	, orders as (
		select *
		from mydatabase.public.orders
	)
	, customers as (
		select *
		from mydatabase.public.customers
	)
	, orders_with_customer_name as (
		select
			orders.*
			, customers.company_name
		from orders
		left join customers
			on orders.customer_id = customers.customer_id
	)
	, spent_value_by_customers as (
		select
			orders_with_customer_name.company_name
			, sum((unit_price - (unit_price * discount)) * quantity) as total_spend
		from order_details
		left join orders_with_customer_name
			on order_details.order_id = orders_with_customer_name.order_id
		group by orders_with_customer_name.company_name
	)
	, get_groups as (
		select
			*
			, ntile(5) over (order by total_spend desc) as group_number
		from spent_value_by_customers
	)
select *
from get_groups
where group_number >= 3
order by total_spend desc
'''
    st.code(code, language="sql")


cur.execute("SELECT * FROM mydatabase.public.vw_total_revenue_per_customer_group_filtered")


records = cur.fetchall()

columns = ['company_name', 'total_spend', 'group_number']

df = pd.DataFrame(records, columns=columns)
st.dataframe(df)

st.divider()
st.subheader("Question 03")
st.subheader("Top 10 Best Selling Products")

code = st.toggle("Click to see the code", key="question_6")

if code:
    code = '''
with
	order_details as (
		select *
		from mydatabase.public.order_details
	)
	, products as (
		select *
		from mydatabase.public.products
	)
	, get_products_name as (
		select
			order_details.*
			, products.product_name
		from order_details
		left join products
			on order_details.product_id = products.product_id
	)
	, top_10_products as (
		select
			product_name
			, sum(quantity) as qtd
			, dense_rank() over(
				order by sum(quantity) desc
			) as ranking
		from get_products_name
		group by product_name
	)
select *
from top_10_products
limit 10
'''
    st.code(code, language="sql")


cur.execute("SELECT * FROM mydatabase.public.vw_top_10_products")


records = cur.fetchall()

columns = ['product_name', 'qtd', 'ranking']

df = pd.DataFrame(records, columns=columns)
st.dataframe(df)

st.divider()
st.subheader("Question 04")
st.subheader("Which UK customers paid more than $1000?")

code = st.toggle("Click to see the code", key="question_7")

if code:
    code = '''
with
	order_details as (
		select *
		from mydatabase.public.order_details
	)
	, orders as (
		select *
		from mydatabase.public.orders
	)
	, customers as (
		select *
		from mydatabase.public.customers
	)
	, price_with_discount as (
		select
			*
			, unit_price - (unit_price * discount) as unit_price_with_discount
		from order_details
	)
	, total_spend as (
		select
			customers.contact_name
			, sum(
				price_with_discount.unit_price_with_discount * price_with_discount.quantity
			) as total_spend
		from price_with_discount
		left join orders
			on price_with_discount.order_id = orders.order_id
		left join customers
			on orders.customer_id = customers.customer_id
		where customers.country = 'UK'
		group by customers.contact_name
		having 
			sum(
				price_with_discount.unit_price_with_discount * price_with_discount.quantity
			) > 1000
	)

select *
from total_spend
'''
    st.code(code, language="sql")


cur.execute("SELECT * FROM mydatabase.public.vw_uk_customers_spend_1000")


records = cur.fetchall()

columns = ['contact_name', 'total_spend']

df = pd.DataFrame(records, columns=columns)
st.dataframe(df)