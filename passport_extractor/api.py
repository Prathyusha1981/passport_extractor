# Copyright (c) 2026, prathyusha and contributors
# For license information, please see license.txt

import re
from datetime import date, datetime

import frappe
from passporteye import read_mrz


def _parse_mrz_date(date_str, is_dob=False):
	"""Parse MRZ date string (YYMMDD) into a YYYY-MM-DD string.

	For date-of-birth, if the parsed year falls in the future it means
	the person was born in the previous century, so subtract 100 years.
	"""
	parsed = datetime.strptime(date_str, "%y%m%d").date()
	if is_dob and parsed > date.today():
		parsed = parsed.replace(year=parsed.year - 100)
	return parsed.strftime("%Y-%m-%d")


@frappe.whitelist()
def extract_passport_details(file_url):
	"""Read MRZ from an already-uploaded Frappe file and return extracted fields."""
	status, message, response = 200, "Success", {}
	try:
		# Resolve the Frappe file to an absolute path on disk
		file_doc = frappe.get_doc("File", {"file_url": file_url})
		file_path = file_doc.get_full_path()

		mrz = read_mrz(file_path)
		if mrz is None:
			return {"status": 400, "message": "Invalid passport image – MRZ could not be read"}

		mrz_data = mrz.to_dict()

		# --- Passport number ---
		passno = mrz_data.get("number", "")
		passno = passno.replace("<", "")
		passno = re.sub(r"\s+", " ", passno).strip()

		# --- Full name ---
		name = (mrz_data.get("names", "") + " " + mrz_data.get("surname", "")).strip()
		name = re.sub(r"\s*<\s*", " ", name)
		name = re.sub(r"\s+", " ", name).strip()

		# --- Dates ---
		dob = _parse_mrz_date(mrz_data["date_of_birth"], is_dob=True)
		date_of_expiry = _parse_mrz_date(mrz_data["expiration_date"])

		# --- Gender ---
		gender = "Female" if mrz_data.get("sex") == "F" else "Male"

		# --- Nationality (resolve country name via Country doctype) ---
		nationality_code = mrz_data.get("nationality", "")
		country_name = nationality_code
		try:
			countries = frappe.get_all(
				"Country",
				filters={"custom_iso_code": nationality_code},
				fields=["country_name"],
			)
			if countries:
				country_name = countries[0]["country_name"]
		except Exception:
			# custom_iso_code field may not exist; keep raw MRZ nationality code
			pass

		response = {
			"passport_number": passno,
			"name": name,
			"dob": dob,
			"nationality": country_name,
			"gender": gender,
			"date_of_expiry": date_of_expiry,
		}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Passport Extraction Error")
		return {"status": 400, "message": "Error while extracting data from passport", "error": str(e)}

	return {"status": status, "message": message, "data": response}
