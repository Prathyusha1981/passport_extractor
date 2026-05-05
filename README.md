# 🚀 Passport Scanner using Frappe

Convert passport images into structured data in seconds.

This project extracts passport details directly from an image using **MRZ (Machine Readable Zone) parsing** with a custom UI built in Frappe.

---

## 🎬 Demo

👉 



## ✨ Features

- 📤 Upload passport image  
- 🔍 Detect and read MRZ (Machine Readable Zone)  
- 🧾 Extract key details:
  - Full Name  
  - Passport Number  
  - Date of Birth  
  - Expiry Date  
  - Gender  
  - Nationality  
- ⚡ Instant results in a custom UI  
- 🎨 Clean and interactive Frappe custom page  

---

## 🔍 What is MRZ?

MRZ (Machine Readable Zone) is the encoded text located at the bottom of a passport.  
It contains structured identity information in a standardized format.

---

## 📄 What can be extracted?

From MRZ, we can retrieve:

- Name  
- Passport Number  
- Date of Birth  
- Expiry Date  
- Gender  
- Nationality  

---

## 💡 Key Insight

Accuracy depends on the clarity of the MRZ section in the image.  
Clear and properly captured passport images provide the best results.

For testing, dummy/sample passport images were used.

---

## 🛠 Tech Stack

- **Frappe Framework** – Backend + UI framework  
- **Python** – MRZ extraction using `passporteye`  
- **JavaScript** – Custom page UI & API integration  

---

