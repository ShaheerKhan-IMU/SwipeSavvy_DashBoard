from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/data")
def getting_data():

    merchant = pd.read_excel("customer_list-4.xlsx")
    merchant.dropna(subset = ["Account Status", "Customer ID"], inplace=True)
    merchant.fillna(0, inplace = True)
    live_Merchants = int((merchant["Account Status"].str.lower() == 'live').sum())
    cancelled_Merchants = int((merchant["Account Status"].str.lower() == 'cancelled').sum())
    not_submitted_Merchants = int((merchant["Account Status"].str.lower() == "not submitted").sum())
    declined_Merchants = int((merchant["Account Status"].str.lower() == "declined").sum())
    other_Merchants = int(((merchant["Account Status"].str.lower() == "pending signature") | (merchant["Account Status"].str.lower() == "boarded")).sum())
    total_Merchants = len(merchant)



    customer = pd.read_csv("Customers-20250808_0920_EDT.csv")
    customer.fillna("", inplace=True)
    total_customers = len(customer)
    name_Customers = customer[customer["First Name"].notna() & (customer["First Name"].str.strip() != "")].shape[0]
    phonenumber_Customers = customer[customer["Phone Number"].str.strip() != ""].shape[0]
    email_Customers = customer[customer["Email Address"].str.strip() != ""].shape[0]
    phone_email_customer = customer[(customer["Phone Number"].str.lower() != "") & (customer["Email Address"].str.lower() != "")].shape[0]
    name_phone_email_customer = customer[(customer["First Name"].str.lower() != "") & (customer["Phone Number"].str.lower() != "") & (customer["Email Address"].str.lower() != "")].shape[0]
    marketting_customer_yes = int((customer["Marketing Allowed"].str.lower() == "yes").sum())
    marketting_customer_no = int((customer["Marketing Allowed"].str.lower() == "no").sum())
    marketting_customer_yes_phone = customer[(customer["Marketing Allowed"].str.lower() == "yes") & (customer["Phone Number"].str.strip() != "")].shape[0]
    marketting_customer_yes_phone_email = customer[(customer["Marketing Allowed"].str.lower() == "yes") & (customer["Phone Number"].str.strip() != "") & (customer["Email Address"].str.strip() != "")].shape[0]
    


    merchants_Volume_data = pd.read_excel("customer_list-4.xlsx", usecols=("Account Status", "Legal Business Name", "Last Month Volume"))
    live_merchants_Volumes = merchants_Volume_data[merchants_Volume_data["Account Status"].str.lower() == "live"]
    live_merchants_Volumes_name = live_merchants_Volumes["Legal Business Name"].head(10)
    live_merchants_Volumes_month = live_merchants_Volumes["Last Month Volume"].head(10)
    


    marathon_gross_sale = pd.read_excel("MARATHON LIQUORS-Revenue Item Sales 08_08_2025.xlsx")
    marathon_gross_sale_value = round(marathon_gross_sale.iloc[8, 1])
    marathon_net_sale_value = round(marathon_gross_sale.iloc[9, 1])
    marathon_GP_margin_value = (marathon_gross_sale.iloc[12, 1])*100


    anthony_gross_sale = pd.read_excel("Anthony's Pizza & Pasta-Revenue Item Sales 08_08_2025 2.xlsx")
    anthony_gross_sale_value = round(anthony_gross_sale.iloc[8, 1])
    anthony_net_sale_value = round(anthony_gross_sale.iloc[9, 1])
    anthony_GP_margin_value = (anthony_gross_sale.iloc[12, 1])*100


    pokehana_gross_sale = pd.read_excel("POKE HANA-Revenue Item Sales 08_08_2025.xlsx")
    pokehana_gross_sale_value = round(pokehana_gross_sale.iloc[9, 1])
    pokehana_net_sale_value = round(pokehana_gross_sale.iloc[10, 1])
    pokehana_GP_margin_value = (pokehana_gross_sale.iloc[13, 1])*100

    SS_gross_revenue = (marathon_gross_sale_value) + (anthony_gross_sale_value) + (pokehana_gross_sale_value)
    SS_net_revenue = (marathon_net_sale_value) + (anthony_net_sale_value) + (pokehana_net_sale_value)


    SS_gross_revenue_daily = round((SS_gross_revenue)/92)
    SS_gross_revenue_weekly = round(((SS_gross_revenue)*7)/92)
    SS_gross_revenue_monthly = round((SS_gross_revenue)/3)

    return {
        "total_Merchants" : total_Merchants,
        "live_Merchants" : live_Merchants,
        "cancelled_Merchants" : cancelled_Merchants,
        "not_submitted_Merchants" : not_submitted_Merchants,
        "declined_Merchants" : declined_Merchants,
        "other_Merchants" : other_Merchants,
        # "merchant": merchant.to_dict(orient="records"),



        "total_customers" : total_customers,
        "name_Customers" : name_Customers,
        "phonenumber_Customers": phonenumber_Customers,
        "email_Customers" : email_Customers,
        "phone_email_customer" : phone_email_customer,
        "name_phone_email_customer" : name_phone_email_customer,
        "marketting_customer_yes" : marketting_customer_yes,
        "marketting_customer_no" : marketting_customer_no,
        "marketting_customer_yes_phone" : marketting_customer_yes_phone,
        "marketting_customer_yes_phone_email" : marketting_customer_yes_phone_email,



        "live_merchants_Volumes_name" : live_merchants_Volumes_name,
        "live_merchants_Volumes_month" : live_merchants_Volumes_month,


        "marathon_gross_sale_value" : marathon_gross_sale_value,
        "marathon_net_sale_value" : marathon_net_sale_value,
        "marathon_GP_margin_value" : marathon_GP_margin_value,


        "anthony_gross_sale_value" : anthony_gross_sale_value,
        "anthony_net_sale_value" : anthony_net_sale_value,
        "anthony_GP_margin_value" : anthony_GP_margin_value,


        "pokehana_gross_sale_value" : pokehana_gross_sale_value,
        "pokehana_net_sale_value" : pokehana_net_sale_value,
        "pokehana_GP_margin_value" : pokehana_GP_margin_value,


        "SS_gross_revenue" : SS_gross_revenue,
        "SS_net_revenue" : SS_net_revenue,


        "SS_gross_revenue_daily" : SS_gross_revenue_daily,
        "SS_gross_revenue_weekly" : SS_gross_revenue_weekly,
        "SS_gross_revenue_monthly" : SS_gross_revenue_monthly,
        }