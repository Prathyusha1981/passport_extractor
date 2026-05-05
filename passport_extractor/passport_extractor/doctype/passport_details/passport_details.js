// Copyright (c) 2026, prathyusha and contributors
// For license information, please see license.txt

frappe.ui.form.on("Passport Details", {
	refresh(frm) {
		frm.add_custom_button(__("Extract Passport Details"), function () {
			if (!frm.doc.passport_image) {
				frappe.msgprint(__("Please attach a passport image first."));
				return;
			}

			frappe.call({
				method: "passport_extractor.api.extract_passport_details",
				args: {
					file_url: frm.doc.passport_image,
				},
				freeze: true,
				freeze_message: __("Extracting passport details..."),
				callback: function (r) {
					if (r.message && r.message.status === 200) {
						const data = r.message.data;
						frm
							.set_value({
								passport_number: data.passport_number,
								full_name: data.name,
								date_of_birth: data.dob,
								date_of_expiry: data.date_of_expiry,
								nationality: data.nationality,
								gender: data.gender,
							})
							.then(() => frm.save())
							.then(() => {
								frappe.show_alert({
									message: __("Passport details extracted and saved successfully."),
									indicator: "green",
								});
							});
					} else {
						frappe.msgprint({
							title: __("Extraction Failed"),
							indicator: "red",
							message: r.message
								? r.message.message || __("Unknown error")
								: __("No response from server"),
						});
					}
				},
			});
		});
	},
});
