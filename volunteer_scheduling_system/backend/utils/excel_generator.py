# backend/utils/excel_generator.py

import io
import pandas as pd
from openpyxl.styles import Font, PatternFill
from flask import send_file, jsonify
from backend.models.mongo import get_volunteer_collection
from backend.utils.shift_config import get_shift_labels, get_days, get_shift_times, format_shifts_summary

def export_event_to_excel(event_id):
    try:
        # Get event configuration to determine which fields to include
        from backend.models.mongo import get_event_collection
        event = get_event_collection().find_one({"event_id": event_id}, {"_id": 0})
        if not event:
            raise ValueError(f"Event with ID '{event_id}' not found")
            
        form_config = event.get("form_config", [])
        
        # Determine which fields are included in the form
        included_fields = {
            "organization": any(f.get("name") == "organization" for f in form_config),
            "certifications": any(f.get("name") == "certifications" for f in form_config),
            "other_training": any(f.get("name") == "other_training" for f in form_config),
            "emergency_contact": any(f.get("name") == "emergency_contact_name" for f in form_config),
            "commit_location": any(f.get("name") == "commit_location" for f in form_config),
            "online_training": any(f.get("name") == "online_training" for f in form_config),
            "moa_ma_ems": any(f.get("name") == "moa_ma_ems" for f in form_config)
        }
        
        # Get volunteers and deduplicate them
        all_volunteers = list(get_volunteer_collection(event_id).find({}, {"_id": 0}))
        
        # Deduplicate volunteers by email (keep only the most recent signup for each email)
        unique_volunteers = {}
        for volunteer in all_volunteers:
            email = volunteer.get("email")
            if not email:
                continue
                
            # If this is the first time we're seeing this email, or if this entry is newer
            if email not in unique_volunteers or (
                volunteer.get("submit_date") and 
                unique_volunteers[email].get("submit_date") and
                volunteer["submit_date"] > unique_volunteers[email]["submit_date"]
            ):
                unique_volunteers[email] = volunteer
                
        # Convert back to list
        volunteers = list(unique_volunteers.values())
        
        if not volunteers:
            # Create a dummy sheet if no volunteers found
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                pd.DataFrame({"Notice": ["No volunteers found"]}).to_excel(
                    writer, index=False, sheet_name="No Data"
                )
            output.seek(0)
            return send_file(
                output,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                download_name=f"{event_id}_volunteers.xlsx",
                as_attachment=True
            )
        
        # Get configuration with dynamic shift times from event
        days = get_days()
        shift_labels = get_shift_labels(event)  # Pass event config to get dynamic shift labels
        
        # Create Excel file with multiple sheets
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Create a sheet for each day
            for day in days:
                day_lower = day.lower()
                
                # Find all shift keys for this day
                day_shift_keys = [key for key in shift_labels.keys() if key.startswith(day_lower)]
                
                # Skip days with no shifts defined
                if not day_shift_keys:
                    continue
                
                # Create DataFrames for each shift
                shift_data = {}
                for shift_key in day_shift_keys:
                    shift_volunteers = []
                    
                    for volunteer in volunteers:
                        if volunteer.get("shifts") and volunteer["shifts"].get(shift_key):
                            shift_volunteers.append(volunteer)
                    
                    shift_data[shift_key] = pd.DataFrame(shift_volunteers)
                
                # Add a title at the top of each day's sheet
                row_position = 0
                title_df = pd.DataFrame({
                    "": [f"{day} Volunteer Schedule"]
                })
                title_df.to_excel(
                    writer,
                    sheet_name=day,
                    startrow=row_position,
                    index=False
                )
                row_position += 2  # Skip a row after the title
                
                # Process each shift for this day
                for shift_key in day_shift_keys:
                    df = shift_data[shift_key]
                    
                    # Get the dynamic label for this shift
                    shift_label = shift_labels.get(shift_key, "Unknown Shift")
                    
                    # Extract just the time part from the label (e.g., "7:30-12:30" from "Mon 7:30-12:30")
                    # This handles both default format and custom labels
                    time_part = shift_label
                    if " " in shift_label:
                        parts = shift_label.split(" ", 1)
                        if len(parts) > 1:
                            time_part = parts[1]
                    
                    # Only write this shift if there are volunteers assigned
                    if not df.empty:
                        # Write the shift header with the dynamic label's time part
                        header_df = pd.DataFrame({
                            "Shift Time": [time_part]
                        })
                        header_df.to_excel(
                            writer, 
                            sheet_name=day,
                            startrow=row_position,
                            index=False
                        )
                        row_position += 2  # Skip a row after the header
                        
                        # Create a DataFrame with volunteer information
                        volunteer_data = []
                        for volunteer in shift_data[shift_key].to_dict('records'):
                            data = {
                                "First Name": volunteer.get("first_name", ""),
                                "Last Name": volunteer.get("last_name", ""),
                                "Phone": volunteer.get("phone", ""),
                                "Email": volunteer.get("email", "")
                            }
                            
                            # Add optional fields based on form configuration
                            if included_fields["organization"]:
                                data["Organization"] = volunteer.get("organization", "")
                                
                            if included_fields["commit_location"]:
                                data["Commitment"] = volunteer.get("commit_location", "")
                                
                            if included_fields["online_training"]:
                                data["Training"] = volunteer.get("online_training", "")
                                
                            if included_fields["moa_ma_ems"]:
                                data["Cert Enrollment"] = volunteer.get("moa_ma_ems", "")
                                
                            if included_fields["certifications"]:
                                data["Certifications"] = ", ".join(volunteer.get("certifications", [])) if isinstance(volunteer.get("certifications"), list) else ""
                                
                            if included_fields["other_training"]:
                                data["Other Training"] = volunteer.get("other_training", "")
                                
                            if included_fields["emergency_contact"]:
                                data["Emergency Contact Name"] = volunteer.get("emergency_contact_name", "")
                                data["Emergency Contact Phone"] = volunteer.get("emergency_contact_phone", "")
                            
                            volunteer_data.append(data)
                        
                        # Write the volunteer data
                        volunteer_df = pd.DataFrame(volunteer_data)
                        volunteer_df.to_excel(
                            writer,
                            sheet_name=day,
                            startrow=row_position,
                            index=False
                        )
                        row_position += len(df) + 3  # Skip 3 rows after the data
                    
                # If no volunteers for this day, add a "No volunteers" note
                if row_position == 2:
                    pd.DataFrame({
                        "Notice": ["No volunteers scheduled for this day"]
                    }).to_excel(
                        writer,
                        sheet_name=day,
                        index=False
                    )
            
            # Create "All Volunteers" sheet
            processed_volunteers = []
            for volunteer in volunteers:
                data = {
                    "First Name": volunteer.get("first_name", ""),
                    "Last Name": volunteer.get("last_name", ""),
                    "Phone": volunteer.get("phone", ""),
                    "Email": volunteer.get("email", ""),
                    "Scheduled Shifts": format_shifts_summary(volunteer.get("shifts", {}), event)
                }
                
                # Add optional fields based on form configuration
                if included_fields["organization"]:
                    data["Organization"] = volunteer.get("organization", "")
                    
                if included_fields["commit_location"]:
                    data["Commitment"] = volunteer.get("commit_location", "")
                    
                if included_fields["online_training"]:
                    data["Training"] = volunteer.get("online_training", "")
                    
                if included_fields["moa_ma_ems"]:
                    data["Cert Enrollment"] = volunteer.get("moa_ma_ems", "")
                    
                if included_fields["certifications"]:
                    data["Certifications"] = ", ".join(volunteer.get("certifications", [])) if isinstance(volunteer.get("certifications"), list) else ""
                    
                if included_fields["other_training"]:
                    data["Other Training"] = volunteer.get("other_training", "")
                    
                if included_fields["emergency_contact"]:
                    data["Emergency Contact Name"] = volunteer.get("emergency_contact_name", "")
                    data["Emergency Contact Phone"] = volunteer.get("emergency_contact_phone", "")
                
                processed_volunteers.append(data)

            # Add the "All Volunteers" sheet
            pd.DataFrame(processed_volunteers).to_excel(
                writer, 
                index=False, 
                sheet_name="All Volunteers"
            )
        
            # Auto-adjust column widths
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    
                    # Find the longest content in the column
                    for cell in column:
                        try:
                            if cell.value:
                                cell_length = len(str(cell.value))
                                if cell_length > max_length:
                                    max_length = cell_length
                        except:
                            pass
                    
                    # Add a buffer for better readability
                    adjusted_width = (max_length + 2)
                    
                    # Set the column width (minimum 10, maximum 50)
                    worksheet.column_dimensions[column_letter].width = min(max(adjusted_width, 10), 50)
                    
                    # Make headers bold with background color
                    for cell in column[:1]:  # Just the header row
                        if cell.value:  # Only style cells with content
                            cell.font = Font(bold=True)
                            cell.fill = PatternFill(start_color="E0E0E0", end_color="E0E0E0", fill_type="solid")
        
        output.seek(0)
        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            download_name=f"{event_id}_volunteers.xlsx",
            as_attachment=True
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
