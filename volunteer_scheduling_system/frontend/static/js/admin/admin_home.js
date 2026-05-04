// frontend/static/js/admin_home.js

/**
 * Fetches and displays all events
 */
async function fetchEvents() {
  try {
    console.log("Fetching events from server...");
    
    // Show loading indicator
    const container = document.getElementById("eventsList");
    container.innerHTML = "<p class='loading-message'>Loading events...</p>";
    
    // Fetch events from the API
    const res = await fetch("/api/events");
    
    // Check if the response is OK
    if (!res.ok) {
      // Try to parse the error message from the response
      let errorMessage = `Server returned ${res.status}`;
      try {
        const errorData = await res.json();
        if (errorData && errorData.error) {
          errorMessage = errorData.error;
        }
      } catch (e) {
        // If we can't parse the JSON, just use the status code
      }
      
      throw new Error(errorMessage);
    }
    
    // Parse the JSON response
    const events = await res.json();
    console.log(`Received ${events.length} events from server`);
    
    // Clear the container
    container.innerHTML = "";

    // If there are no events, show a message
    if (!events.length) {
      container.innerHTML = "<p class='empty-message'>No events found. Click 'Create New Event' to get started.</p>";
      return;
    }

    // Create an element for each event
    events.forEach(e => {
      const div = document.createElement("div");
      div.classList.add("event-item");
      
  // Format dates if available - use direct date string to avoid timezone issues
  let dateInfo = "";
  if (e.event_start_date) {
    const startDate = e.event_start_date.split('T')[0]; // Extract date part directly
    if (e.event_end_date) {
      const endDate = e.event_end_date.split('T')[0]; // Extract date part directly
      dateInfo = `<p><strong>Dates:</strong> ${startDate} to ${endDate}</p>`;
    } else {
      dateInfo = `<p><strong>Date:</strong> ${startDate}</p>`;
    }
  }
      
      // Add location if available
      const locationInfo = e.event_location ? 
        `<p><strong>Location:</strong> ${e.event_location}</p>` : "";
      
      // Add description if available (truncated if too long)
      let descriptionInfo = "";
      if (e.event_description) {
        const shortDesc = e.event_description.length > 100 ? 
          e.event_description.substring(0, 100) + "..." : 
          e.event_description;
        descriptionInfo = `<p><strong>Description:</strong> ${shortDesc}</p>`;
      }
      
      div.innerHTML = `
        <h3>${e.event_name}</h3>
        <p><strong>Event ID:</strong> ${e.event_id}</p>
        ${dateInfo}
        ${locationInfo}
        ${descriptionInfo}
        <div class="event-links">
    <a href="/volunteer/form/${e.event_id}" class="event-link" target="_blank">Volunteer Sign-up Form</a> | 
    <a href="/admin/dashboard/${e.event_id}" class="event-link">View Submissions</a> |
          <button class="edit-event-btn" data-event-id="${e.event_id}">Edit Event</button> |
          <button class="delete-event-btn" data-event-id="${e.event_id}" data-event-name="${e.event_name}">Delete Event</button>
        </div>
      `;
      container.appendChild(div);
    });
  } catch (error) {
    console.error("Error fetching events:", error);
    
    // Show error message in the container
    const container = document.getElementById("eventsList");
    container.innerHTML = `
      <div class="error-message">
        <p><strong>Error loading events:</strong> ${error.message}</p>
        <p>Please try refreshing the page. If the problem persists, check your MongoDB connection.</p>
      </div>
    `;
  }
}

/**
 * Opens the event creation modal
 */
function openEventModal() {
  // Reset the form
  resetEventForm();
  
  // Set create mode
  document.getElementById("editMode").value = "false";
  document.getElementById("originalEventId").value = "";
  document.getElementById("modalTitle").textContent = "Create a New Event";
  document.getElementById("submitEventBtn").textContent = "Create Event";
  
  // Enable event ID field (it's editable in create mode)
  document.getElementById("eventIdInput").disabled = false;
  
  // Show the modal with transition
  const modal = document.getElementById("eventModal");
  modal.style.display = "flex";
  
  // Trigger reflow to ensure transition works
  void modal.offsetWidth;
  
  // Add show class for transition
  modal.classList.add("show");
  
  // Set up event handlers for day checkboxes and shift count inputs
  setupDynamicShiftHandlers();
}

/**
 * Opens the event edit modal with pre-filled data
 */
async function openEditEventModal(eventId) {
  try {
    // Reset the form first
    resetEventForm();
    
    // Set edit mode
    document.getElementById("editMode").value = "true";
    document.getElementById("originalEventId").value = eventId;
    document.getElementById("modalTitle").textContent = "Edit Event";
    document.getElementById("submitEventBtn").textContent = "Update Event";
    
    // Fetch the event data
    const res = await fetch(`/api/events/${eventId}`);
    if (!res.ok) {
      throw new Error(`Failed to fetch event: ${res.status}`);
    }
    
    const event = await res.json();
    console.log("Loaded event data for editing:", event);
    
    // Fill in the form fields
    document.getElementById("eventIdInput").value = event.event_id;
    document.getElementById("eventIdInput").disabled = false; // Allow changing event ID
    document.getElementById("eventNameInput").value = event.event_name || "";
    document.getElementById("eventLocationInput").value = event.event_location || "";
    document.getElementById("minAgeInput").value = event.min_age || 0;
    document.getElementById("eventDescriptionInput").value = event.event_description || "";
    
    // Set dates if available
    if (event.event_start_date) {
      document.getElementById("eventStartDateInput").value = event.event_start_date.split("T")[0];
    }
    if (event.event_end_date) {
      document.getElementById("eventEndDateInput").value = event.event_end_date.split("T")[0];
    }
    
    // Set form fields based on form_config
    if (event.form_config) {
      // Reset all optional checkboxes first
      document.getElementById("field_organization").checked = false;
      document.getElementById("field_certifications").checked = false;
      document.getElementById("field_emergency_contact").checked = false;
      document.getElementById("field_commit_location").checked = false;
      document.getElementById("field_online_training").checked = false;
      document.getElementById("field_moa_ma_ems").checked = false;
      
      // Check the appropriate boxes based on form_config
      let hasOtherTraining = false;
      
      event.form_config.forEach(field => {
        if (field.name === "organization") {
          document.getElementById("field_organization").checked = true;
        } else if (field.name === "certifications") {
          document.getElementById("field_certifications").checked = true;
        } else if (field.name === "other_training") {
          hasOtherTraining = true;
        } else if (field.name === "emergency_contact_name") {
          document.getElementById("field_emergency_contact").checked = true;
        } else if (field.name === "commit_location") {
          document.getElementById("field_commit_location").checked = true;
        } else if (field.name === "online_training") {
          document.getElementById("field_online_training").checked = true;
        } else if (field.name === "moa_ma_ems") {
          document.getElementById("field_moa_ma_ems").checked = true;
        }
      });
      
      // If we have other_training but not certifications, check certifications anyway
      // since they're now combined
      if (hasOtherTraining && !document.getElementById("field_certifications").checked) {
        document.getElementById("field_certifications").checked = true;
      }
      
      // Set schedule if available
      const shiftField = event.form_config.find(f => f.type === "shift-selector");
      if (shiftField && shiftField.schedule) {
        const schedule = shiftField.schedule;
        
        // Reset all day checkboxes first
        const days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"];
        days.forEach(day => {
          document.getElementById(`include_${day}`).checked = false;
          // Hide the shifts section initially
          document.getElementById(`${day}_shifts`).style.display = "none";
        });
        
        // Set the appropriate checkboxes based on schedule
        Object.keys(schedule).forEach(day => {
          if (schedule[day].enabled) {
            document.getElementById(`include_${day}`).checked = true;
            // Show the shifts section
            document.getElementById(`${day}_shifts`).style.display = "block";
            
            // Set shifts
            if (schedule[day].shifts) {
              const shifts = Object.keys(schedule[day].shifts).filter(s => s.startsWith('shift'));
              
              // Set the shift count
              document.getElementById(`${day}_shift_count`).value = shifts.length;
              
              // Clear existing shift times
              const shiftTimesContainer = document.getElementById(`${day}_shift_times`);
              shiftTimesContainer.innerHTML = '';
              
              // Add each shift with its time
              shifts.forEach((shift, index) => {
                const shiftInfo = schedule[day].shifts[shift];
                const shiftNum = index + 1;
                
                // Parse the time from the label (e.g., "7:30 am - 12:30 pm")
                let startTime = "09:00";
                let endTime = "17:00";
                
                if (shiftInfo.start_time && shiftInfo.end_time) {
                  startTime = shiftInfo.start_time;
                  endTime = shiftInfo.end_time;
                } else if (shiftInfo.label) {
                  // Try to parse from label if available
                  const timeParts = shiftInfo.label.split('-').map(part => part.trim());
                  if (timeParts.length === 2) {
                    // Convert to 24h format for the input
                    startTime = convertTo24Hour(timeParts[0]);
                    endTime = convertTo24Hour(timeParts[1]);
                  }
                }
                
                // Add the shift time row
                const shiftRow = document.createElement('div');
                shiftRow.className = 'shift-time-row';
                shiftRow.innerHTML = `
                  <label>Shift ${shiftNum}:</label>
                  <input type="time" class="shift-start-time" id="${day}_shift${shiftNum}_start" value="${startTime}">
                  <span>to</span>
                  <input type="time" class="shift-end-time" id="${day}_shift${shiftNum}_end" value="${endTime}">
                `;
                shiftTimesContainer.appendChild(shiftRow);
              });
            }
          }
        });
      }
    }
    
    // Show the modal with transition
    const modal = document.getElementById("eventModal");
    modal.style.display = "flex";
    
    // Trigger reflow to ensure transition works
    void modal.offsetWidth;
    
    // Add show class for transition
    modal.classList.add("show");
    
    // Set up event handlers for day checkboxes and shift count inputs
    setupDynamicShiftHandlers();
  } catch (error) {
    console.error("Error loading event for editing:", error);
    alert(`Failed to load event for editing: ${error.message}`);
  }
}

/**
 * Convert time from 12-hour format to 24-hour format
 */
function convertTo24Hour(time12h) {
  // Default values if parsing fails
  let hours = 9;
  let minutes = 0;
  
  // Try to parse the time
  const timeRegex = /(\d+):?(\d*)?\s*(am|pm)/i;
  const match = time12h.match(timeRegex);
  
  if (match) {
    hours = parseInt(match[1]);
    minutes = match[2] ? parseInt(match[2]) : 0;
    const period = match[3].toLowerCase();
    
    // Convert to 24-hour format
    if (period === 'pm' && hours < 12) {
      hours += 12;
    } else if (period === 'am' && hours === 12) {
      hours = 0;
    }
  }
  
  // Format as HH:MM
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
}

/**
 * Set up event handlers for the dynamic shifts interface
 */
function setupDynamicShiftHandlers() {
  const days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"];
  
  // Set up day checkbox handlers
  days.forEach(day => {
    const checkbox = document.getElementById(`include_${day}`);
    checkbox.addEventListener('change', function() {
      const shiftsSection = document.getElementById(`${day}_shifts`);
      shiftsSection.style.display = this.checked ? 'block' : 'none';
    });
    
    // Set up shift count change handlers
    const shiftCountInput = document.getElementById(`${day}_shift_count`);
    const updateButton = document.querySelector(`.add-shift-btn[data-day="${day}"]`);
    
    updateButton.addEventListener('click', function() {
      updateShiftRows(day, parseInt(shiftCountInput.value) || 0);
    });
  });
}

/**
 * Update the shift time rows based on the shift count
 */
function updateShiftRows(day, count) {
  // Limit the count to a reasonable range
  count = Math.max(1, Math.min(5, count));
  
  // Update the input value to reflect the actual count
  document.getElementById(`${day}_shift_count`).value = count;
  
  const container = document.getElementById(`${day}_shift_times`);
  container.innerHTML = '';
  
  // Add the specified number of shift rows
  for (let i = 1; i <= count; i++) {
    // Default times based on shift number
    let startTime, endTime;
    
    if (i === 1) {
      startTime = "07:30";
      endTime = "12:30";
    } else if (i === 2) {
      startTime = "12:30";
      endTime = "16:00";
    } else {
      // For additional shifts, use reasonable defaults
      startTime = "09:00";
      endTime = "17:00";
    }
    
    const row = document.createElement('div');
    row.className = 'shift-time-row';
    row.innerHTML = `
      <label>Shift ${i}:</label>
      <input type="time" class="shift-start-time" id="${day}_shift${i}_start" value="${startTime}">
      <span>to</span>
      <input type="time" class="shift-end-time" id="${day}_shift${i}_end" value="${endTime}">
    `;
    container.appendChild(row);
  }
}

/**
 * Resets the event form to default values
 */
function resetEventForm() {
  // Reset basic fields
  document.getElementById("eventIdInput").value = "";
  document.getElementById("eventNameInput").value = "";
  document.getElementById("eventLocationInput").value = "";
  document.getElementById("minAgeInput").value = "18";
  document.getElementById("eventStartDateInput").value = "";
  document.getElementById("eventEndDateInput").value = "";
  document.getElementById("eventDescriptionInput").value = "";
  
  // Reset schedule
  const days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"];
  days.forEach(day => {
    const isWeekday = ["monday", "tuesday", "wednesday", "thursday", "friday"].includes(day);
    document.getElementById(`include_${day}`).checked = isWeekday;
    
    // Show/hide the shifts section based on whether the day is included
    const shiftsSection = document.getElementById(`${day}_shifts`);
    shiftsSection.style.display = isWeekday ? "block" : "none";
    
    // Reset shift count to default (2 for weekdays, 1 for weekends)
    document.getElementById(`${day}_shift_count`).value = isWeekday ? "2" : "1";
    
    // Reset shift times to defaults
    if (isWeekday) {
      // Set default weekday shifts (7:30-12:30 and 12:30-16:00)
      const shiftTimesContainer = document.getElementById(`${day}_shift_times`);
      shiftTimesContainer.innerHTML = `
        <div class="shift-time-row">
          <label>Shift 1:</label>
          <input type="time" class="shift-start-time" id="${day}_shift1_start" value="07:30">
          <span>to</span>
          <input type="time" class="shift-end-time" id="${day}_shift1_end" value="12:30">
        </div>
        <div class="shift-time-row">
          <label>Shift 2:</label>
          <input type="time" class="shift-start-time" id="${day}_shift2_start" value="12:30">
          <span>to</span>
          <input type="time" class="shift-end-time" id="${day}_shift2_end" value="16:00">
        </div>
      `;
    } else {
      // Set default weekend shift (9:00-14:00)
      const shiftTimesContainer = document.getElementById(`${day}_shift_times`);
      shiftTimesContainer.innerHTML = `
        <div class="shift-time-row">
          <label>Shift 1:</label>
          <input type="time" class="shift-start-time" id="${day}_shift1_start" value="09:00">
          <span>to</span>
          <input type="time" class="shift-end-time" id="${day}_shift1_end" value="14:00">
        </div>
      `;
    }
  });
  
  // Reset form fields
  document.getElementById("field_organization").checked = true;
  document.getElementById("field_certifications").checked = true;
  document.getElementById("field_emergency_contact").checked = true;
  document.getElementById("field_commit_location").checked = true;
  document.getElementById("field_online_training").checked = true;
  document.getElementById("field_moa_ma_ems").checked = false;
}

/**
 * Closes the event creation modal
 */
function closeEventModal() {
  const modal = document.getElementById("eventModal");
  
  // Remove show class to start transition
  modal.classList.remove("show");
  
  // Wait for transition to complete before hiding
  setTimeout(() => {
    modal.style.display = "none";
  }, 300); // Match this with the CSS transition duration
}

/**
 * Collects the schedule configuration from the form
 */
function getScheduleConfig() {
  const days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"];
  const schedule = {};
  
  days.forEach(day => {
    const includeDay = document.getElementById(`include_${day}`).checked;
    
    if (includeDay) {
      schedule[day] = {
        enabled: true,
        shifts: {}
      };
      
      // Get the number of shifts for this day
      const shiftCount = parseInt(document.getElementById(`${day}_shift_count`).value) || 0;
      
      // Add each shift with its time range
      for (let i = 1; i <= shiftCount; i++) {
        const startTime = document.getElementById(`${day}_shift${i}_start`).value;
        const endTime = document.getElementById(`${day}_shift${i}_end`).value;
        
        if (startTime && endTime) {
          // Format the times for display (convert from 24h to 12h format)
          const formattedStartTime = formatTime(startTime);
          const formattedEndTime = formatTime(endTime);
          const shiftLabel = `${formattedStartTime} - ${formattedEndTime}`;
          
          schedule[day].shifts[`shift${i}`] = {
            enabled: true,
            label: shiftLabel,
            start_time: startTime,
            end_time: endTime
          };
        }
      }
    }
  });
  
  return schedule;
}

/**
 * Format time from 24-hour format to 12-hour format with am/pm
 */
function formatTime(time24h) {
  if (!time24h) return "";
  
  const [hours, minutes] = time24h.split(':');
  let hour = parseInt(hours);
  const ampm = hour >= 12 ? 'pm' : 'am';
  
  // Convert to 12-hour format
  hour = hour % 12;
  hour = hour ? hour : 12; // Convert 0 to 12
  
  return `${hour}:${minutes} ${ampm}`;
}

/**
 * Creates a form configuration based on selected fields
 */
function buildFormConfig() {
  const formConfig = [];
  
  // Add required fields
  formConfig.push({
    type: "text",
    label: "First Name",
    name: "first_name",
    required: true
  });
  
  formConfig.push({
    type: "text",
    label: "Last Name",
    name: "last_name",
    required: true
  });
  
  formConfig.push({
    type: "email",
    label: "Email Address",
    name: "email",
    required: true
  });
  
  formConfig.push({
    type: "text",
    label: "Phone Number",
    name: "phone",
    required: true
  });
  
  // Add optional fields based on checkboxes
  if (document.getElementById("field_organization").checked) {
    formConfig.push({
      type: "text",
      label: "Organization",
      name: "organization",
      required: false
    });
  }
  
  if (document.getElementById("field_certifications").checked) {
    // Add certifications checkbox group
    formConfig.push({
      type: "checkbox-group",
      label: "Certifications",
      name: "certifications",
      options: ["CPR", "First Aid", "EMT", "RN", "MD", "Other"],
      required: false
    });
    
    // Also add other training field when certifications is checked
    formConfig.push({
      type: "text",
      label: "Other Training",
      name: "other_training",
      required: false
    });
  }
  
  if (document.getElementById("field_emergency_contact").checked) {
    formConfig.push({
      type: "text",
      label: "Emergency Contact Name",
      name: "emergency_contact_name",
      required: false
    });
    
    formConfig.push({
      type: "text",
      label: "Emergency Contact Phone",
      name: "emergency_contact_phone",
      required: false
    });
  }
  
  // Add commitment fields
  if (document.getElementById("field_commit_location").checked) {
    formConfig.push({
      type: "radio-group",
      label: "Can you commit to your shift located at event location?",
      name: "commit_location",
      options: ["Yes", "No"],
      required: false
    });
  }
  
  if (document.getElementById("field_online_training").checked) {
    formConfig.push({
      type: "radio-group",
      label: "Will you be able to complete online self-paced training before the event?",
      name: "online_training",
      options: ["Yes", "No"],
      required: false
    });
  }
  
  if (document.getElementById("field_moa_ma_ems").checked) {
    formConfig.push({
      type: "radio-group",
      label: "Do you have an MOA/MA/EMS certificate or currently enrolled in classes?",
      name: "moa_ma_ems",
      options: ["Yes", "No"],
      required: false
    });
  }
  
  // Add age verification field if minimum age is set
  const minAge = parseInt(document.getElementById("minAgeInput").value) || 0;
  if (minAge > 0) {
    formConfig.push({
      type: "radio-group",
      label: `Are you ${minAge} or older?`,
      name: "age_check",
      options: ["Yes", "No"],
      required: true,
      min_age: minAge
    });
  }
  
  // Always add shifts selector (required)
  formConfig.push({
    type: "shift-selector",
    label: "Available Shifts",
    name: "shifts",
    required: true,
    schedule: getScheduleConfig() // Add the schedule configuration
  });
  
  return formConfig;
}

/**
 * Submits the event with selected fields
 */
async function submitEventWithFields() {
  // Get the form values
  const id = document.getElementById("eventIdInput").value.trim();
  const name = document.getElementById("eventNameInput").value.trim();
  const location = document.getElementById("eventLocationInput").value.trim();
  const minAge = parseInt(document.getElementById("minAgeInput").value) || 0;
  const description = document.getElementById("eventDescriptionInput").value.trim();
  const startDate = document.getElementById("eventStartDateInput").value;
  const endDate = document.getElementById("eventEndDateInput").value;
  
  // Debug: Log the state of form field checkboxes
  console.log("Form field selections:");
  console.log("Organization:", document.getElementById("field_organization").checked);
  console.log("Certifications:", document.getElementById("field_certifications").checked);
  console.log("Emergency Contact:", document.getElementById("field_emergency_contact").checked);
  console.log("Commitment to Location:", document.getElementById("field_commit_location").checked);
  console.log("Online Training:", document.getElementById("field_online_training").checked);
  console.log("MOA/MA/EMS:", document.getElementById("field_moa_ma_ems").checked);

  // Validate inputs
  if (!id) {
    alert("Please enter an Event ID");
    document.getElementById("eventIdInput").focus();
    return;
  }
  
  if (!name) {
    alert("Please enter an Event Name");
    document.getElementById("eventNameInput").focus();
    return;
  }
  
  // Check for spaces and special characters in event ID
  if (!id.match(/^[a-zA-Z0-9]+$/)) {
    alert("Event ID must contain only letters and numbers (no spaces or special characters)");
    document.getElementById("eventIdInput").focus();
    return;
  }

  // Show loading state
  const submitButton = document.getElementById("submitEventBtn");
  const originalButtonText = submitButton.textContent;
  submitButton.textContent = originalButtonText === "Create Event" ? "Creating..." : "Updating...";
  submitButton.disabled = true;
  
  // Build form configuration from selected fields
  const formConfig = buildFormConfig();
  
  // Debug: Log the generated form configuration
  console.log("Generated form configuration:", formConfig);
  
  // Prepare the event data
  const eventData = { 
    event_id: id, 
    event_name: name,
    event_location: location,
    min_age: minAge,
    event_description: description,
    event_start_date: startDate,
    event_end_date: endDate,
    form_config: formConfig 
  };
  
  // Debug: Log the complete event data being sent
  console.log("Event data being sent:", eventData);
  
  try {
    // Check if we're in edit mode
    const isEditMode = document.getElementById("editMode").value === "true";
    const originalEventId = document.getElementById("originalEventId").value;
    
    let url, method;
    if (isEditMode) {
      url = `/api/events/${originalEventId}`;
      method = "PUT";
      console.log(`Updating event: ${originalEventId} -> ${id} - ${name} with ${formConfig.length} form fields`);
    } else {
      url = "/api/events";
      method = "POST";
      console.log(`Creating event: ${id} - ${name} with ${formConfig.length} form fields`);
    }
    
    // Send the request
    const res = await fetch(url, {
      method: method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(eventData)
    });

    // Parse the response
    const data = await res.json();
    
    // Check if the request was successful
    if (!res.ok) {
      throw new Error(data.error || `Server returned ${res.status}`);
    }
    
    console.log(isEditMode ? "Event updated successfully:" : "Event created successfully:", data);
    
    // Success - close modal and refresh events list
    closeEventModal();
    fetchEvents();
    
    // Show success message with links
    const formUrl = `/volunteer/form/${id}`;
    const dashboardUrl = `/admin/dashboard/${id}`;
    
    if (isEditMode) {
      alert(`Event "${name}" updated successfully!`);
    } else {
      alert(`Event "${name}" created successfully!\n\nForm URL: ${window.location.origin}${formUrl}\nDashboard URL: ${window.location.origin}${dashboardUrl}`);
    }
  } catch (error) {
    console.error(originalButtonText === "Create Event" ? "Error creating event:" : "Error updating event:", error);
    
    // Show a more detailed error message
    alert(`Failed to ${originalButtonText === "Create Event" ? "create" : "update"} event: ${error.message}\n\nPlease check your MongoDB connection and try again.`);
    
    // Reset the button
    submitButton.textContent = originalButtonText;
    submitButton.disabled = false;
  }
}

/**
 * Handle event button clicks (edit and delete)
 */
document.getElementById("eventsList").addEventListener("click", async e => {
  // Handle delete button clicks
  const deleteBtn = e.target.closest(".delete-event-btn");
  if (deleteBtn) {
    const eventId = deleteBtn.dataset.eventId;
    const eventName = deleteBtn.dataset.eventName;
    
    const confirmed = confirm(`Are you sure you want to delete the event "${eventName}" (${eventId})?\n\nThis will permanently delete all volunteer data associated with this event. This action cannot be undone.`);
    if (!confirmed) return;
    
    try {
      const res = await fetch(`/api/events/${eventId}`, {
        method: "DELETE"
      });
      
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || `Server returned ${res.status}`);
      }
      
      // Refresh the events list
      fetchEvents();
      
      // Show success message
      alert(`Event "${eventName}" deleted successfully.`);
    } catch (error) {
      console.error("Error deleting event:", error);
      alert(`Failed to delete event: ${error.message}`);
    }
  }
  
  // Handle edit button clicks
  const editBtn = e.target.closest(".edit-event-btn");
  if (editBtn) {
    const eventId = editBtn.dataset.eventId;
    openEditEventModal(eventId);
  }
});

// Set up event handlers when the page loads
window.addEventListener("DOMContentLoaded", () => {
  // Fetch events when the page loads
  fetchEvents();
  
  // Set up event handlers for the create event button
  // Note: The button already has an onclick attribute in the HTML
  // document.getElementById("createEventBtn").addEventListener("click", openEventModal);
  
  // The submit button already has an onclick attribute in the HTML
  // No need to add another event listener here
  
  // Close the modal when clicking outside of it
  const modal = document.getElementById("eventModal");
  window.addEventListener("click", e => {
    if (e.target === modal) {
      closeEventModal();
    }
  });
});
