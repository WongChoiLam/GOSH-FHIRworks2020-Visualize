import requests
import datetime

import matplotlib.pyplot as plt

class Address:
    def __init__(self, address):
        self.city = address["city"]
        self.state = address["state"]
        #self.postalCode = address["postalCode"]
        self.country = address["country"]

class Patient:
    def __init__(self, patient):
        self.pid = patient["id"]
        self.gender = patient["gender"]
        ymd = patient["birthDate"].split("-")
        self.birthDate = datetime.datetime(int(ymd[0]), int(ymd[1]), int(ymd[2]))
        self.address = None
        if("address" in patient and len(patient["address"]) > 0):
            self.address = Address(patient["address"][0])
        self.maritalStatus = None
        if("maritalStatus" in patient):
            self.maritalStatus = patient["maritalStatus"]["text"]

URL = """https://localhost:5001/api/"""


r = requests.get(url = URL + "Patient", verify = False)
print(r)
data = r.json()

patients = []

country_dict = {}
gender_dict = {}
maritalStatus_dict = {}
under20 = []
under40 = []
under60 = []
above60 = []


for bundle in data:
    for entry in bundle["entry"]:
        #print(entry["resource"]["id"])
        patient = Patient(entry["resource"])
        patients.append(patient)
        print(patient.pid)

print(len(patients))

for patient in patients:
    age = (datetime.datetime.now() - patient.birthDate).days / 365
    if(age < 20):
        under20.append(patient)
    elif(age < 40):
        under40.append(patient)
    elif(age < 60):
        under60.append(patient)
    else:
        above60.append(patient)
    if not patient.address is None:
        country = patient.address.country
        if not country in country_dict:
            country_dict[country] = 1
        else:
            country_dict[country] = country_dict[country] + 1
    if not patient.gender is None:
        gender = patient.gender
        if not gender in gender_dict:
            gender_dict[gender] = 1
        else:
            gender_dict[gender] = gender_dict[gender] + 1
    if not patient.maritalStatus is None:
        maritalStatus = patient.maritalStatus
        if not maritalStatus in maritalStatus_dict:
            maritalStatus_dict[maritalStatus] = 1
        else:
            maritalStatus_dict[maritalStatus] = maritalStatus_dict[maritalStatus] + 1
    
    
print("under 20 >>\t" + str(len(under20)))
print("under 40 >>\t" + str(len(under40)))
print("under 60 >>\t" + str(len(under60)))
print("above 60 >>\t" + str(len(above60)))

print(list(gender_dict))
print(list(country_dict))

fig1, axs = plt.subplots(2, 2)
age_label = '<20', '<40', '<60', '60+'
age_size = [len(under20), len(under40), len(under60), len(above60)]
axs[0, 0].pie(age_size, labels = age_label, autopct='%1.1f%%')
axs[0, 0].axis('equal')
axs[0, 0].set_title("Age Group")

gender_label = tuple(gender_dict)
gender_size = []
for label in gender_label:
    gender_size.append(gender_dict[label])
axs[0, 1].pie(gender_size, labels = gender_label, autopct='%1.1f%%')
axs[0, 1].axis('equal')
axs[0, 1].set_title("Gender")

country_label = tuple(country_dict)
country_size = []
for label in country_label:
    country_size.append(country_dict[label])
axs[1, 0].pie(country_size, labels = country_label, autopct='%1.1f%%')
axs[1, 0].axis('equal')
axs[1, 0].set_title("Country")  

maritalStatus_label = tuple(maritalStatus_dict)
maritalStatus_size = []
for label in maritalStatus_label:
    maritalStatus_size.append(maritalStatus_dict[label])
axs[1, 1].pie(maritalStatus_size, labels = maritalStatus_label, autopct='%1.1f%%')
axs[1, 1].axis('equal')
axs[1, 1].set_title("Martial Status")  

plt.show()