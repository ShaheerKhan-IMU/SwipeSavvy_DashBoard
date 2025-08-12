from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
    name_Customers = customer[customer["First Name"].notna() & (customer["First Name"].str.strip() != "")].shape[0]
    phonenumber_Customers = customer[customer["Phone Number"].str.strip() != ""].shape[0]
    email_Customers = customer[customer["Email Address"].str.strip() != ""].shape[0]
    phone_email_customer = customer[(customer["Phone Number"].str.lower() != "") & (customer["Email Address"].str.lower() != "")].shape[0]
    name_phone_email_customer = customer[(customer["First Name"].str.lower() != "") & (customer["Phone Number"].str.lower() != "") & (customer["Email Address"].str.lower() != "")].shape[0]
    marketting_customer_yes = int((customer["Marketing Allowed"].str.lower() == "yes").sum())
    marketting_customer_no = int((customer["Marketing Allowed"].str.lower() == "no").sum())
    marketting_customer_yes_phone = customer[(customer["Marketing Allowed"].str.lower() == "yes") & (customer["Phone Number"].str.strip() != "")].shape[0]
    marketting_customer_yes_phone_email = customer[(customer["Marketing Allowed"].str.lower() == "yes") & (customer["Phone Number"].str.strip() != "") & (customer["Email Address"].str.strip() != "")].shape[0]
    
    return {
        "total_Merchants" : total_Merchants,
        "live_Merchants" : live_Merchants,
        "cancelled_Merchants" : cancelled_Merchants,
        "not_submitted_Merchants" : not_submitted_Merchants,
        "declined_Merchants" : declined_Merchants,
        "other_Merchants" : other_Merchants,
        # "merchant": merchant.to_dict(orient="records"),




        "name_Customers" : name_Customers,
        "phonenumber_Customers": phonenumber_Customers,
        "email_Customers" : email_Customers,
        "phone_email_customer" : phone_email_customer,
        "name_phone_email_customer" : name_phone_email_customer,
        "marketting_customer_yes" : marketting_customer_yes,
        "marketting_customer_no" : marketting_customer_no,
        "marketting_customer_yes_phone" : marketting_customer_yes_phone,
        "marketting_customer_yes_phone_email" : marketting_customer_yes_phone_email,
        }