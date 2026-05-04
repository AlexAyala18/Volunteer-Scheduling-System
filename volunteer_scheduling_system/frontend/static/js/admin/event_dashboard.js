// frontend/static/js/event_dashboard.js

// Dynamic shift labels will be loaded from the server
let shiftLabels = {};

/**
 * Loads event information and updates the page title
 */
async function loadEventInfo() {
  try {
    const res = await fetch(`/api/events/${EVENT_ID}`);
    if (!res.ok) {
      throw new Error(`Failed to fetch event: ${res.status}`);
    }
    
    const event = await res.json();
    document.getElementById("eventNameDisplay").textContent = event.event_name || "Volunteer Sign-ups";
    document.title = `${event.event_name} - Volunteer Management`;
    
    // Add event details to the dashboard header
    const dashboardHeader = document.querySelector(".dashboard-header");
    
    // Create event details section
    let detailsHTML = "";
    
    // Add dates if available - use direct date string to avoid timezone issues
    if (event.event_start_date) {
      const startDate = event.event_start_date.split('T')[0]; // Extract date part directly
      if (event.event_end_date) {
        const endDate = event.event_end_date.split('T')[0]; // Extract date part directly
        detailsHTML += `<p><strong>Event Dates:</strong> ${startDate} to ${endDate}</p>`;
      } else {
        detailsHTML += `<p><strong>Event Date:</strong> ${startDate}</p>`;
      }
    }
    
    // Add location if available
    if (event.event_location) {
      detailsHTML += `<p><strong>Location:</strong> ${event.event_location}</p>`;
    }
    
    // Add description if available
    if (event.event_description) {
      detailsHTML += `<p><strong>Description:</strong> ${event.event_description}</p>`;
    }
    
    // Add the details to the dashboard header
    if (detailsHTML) {
      const detailsDiv = document.createElement("div");
      detailsDiv.classList.add("event-details");
      detailsDiv.innerHTML = detailsHTML;
      dashboardHeader.appendChild(detailsDiv);
    }
    
    // Load dynamic shift labels from the event configuration
    if (event.form_config) {
      for (const field of event.form_config) {
        if (field.type === 'shift-selector' && field.schedule) {
          const schedule = field.schedule;
          
          // Process each day in the schedule
          for (const day in schedule) {
            if (schedule[day].enabled && schedule[day].shifts) {
              const dayConfig = schedule[day];
              const dayName = day.charAt(0).toUpperCase() + day.slice(1); // Capitalize first letter
              
              // Process each shift for this day
              for (const shiftKey in dayConfig.shifts) {
                if (dayConfig.shifts[shiftKey].enabled) {
                  const shiftConfig = dayConfig.shifts[shiftKey];
                  const fullShiftKey = `${day}_${shiftKey}`;
                  
                  // Use the label from the configuration, or a default if not available
                  if (shiftConfig.label) {
                    shiftLabels[fullShiftKey] = `${dayName} ${shiftConfig.label}`;
                  }
                }
              }
            }
          }
        }
      }
    }
    
    // Add fallback labels for any shifts that might not be in the configuration
    const defaultLabels = {
      "monday_shift1": "Monday Morning (7:30-12:30)", 
      "monday_shift2": "Monday Afternoon (12:30-4:00)", 
      "monday_shift3": "Monday All Day",
      "tuesday_shift1": "Tuesday Morning (7:30-12:30)", 
      "tuesday_shift2": "Tuesday Afternoon (12:30-4:00)", 
      "tuesday_shift3": "Tuesday All Day",
      "wednesday_shift1": "Wednesday Morning (7:30-12:30)", 
      "wednesday_shift2": "Wednesday Afternoon (12:30-4:00)", 
      "wednesday_shift3": "Wednesday All Day",
      "thursday_shift1": "Thursday Morning (7:30-12:30)", 
      "thursday_shift2": "Thursday Afternoon (12:30-4:00)", 
      "thursday_shift3": "Thursday All Day",
      "friday_shift1": "Friday Morning (7:30-12:30)", 
      "friday_shift2": "Friday Afternoon (12:30-4:00)", 
      "friday_shift3": "Friday All Day",
      "saturday_shift1": "Saturday Morning (9:00-14:00)",
      "saturday_shift2": "Saturday All Day",
      "sunday_shift1": "Sunday Morning (9:00-14:00)",
      "sunday_shift2": "Sunday All Day"
    };
    
    // Merge the default labels with any dynamic labels we found
    shiftLabels = { ...defaultLabels, ...shiftLabels };
    
    console.log("Loaded shift labels:", shiftLabels);
  } catch (error) {
    console.error("Error loading event info:", error);
    document.getElementById("eventNameDisplay").textContent = "Volunteer Sign-ups";
  }
}

/**
 * Fetches volunteer data and form configuration from the server and populates the table
 */
async function fetchVolunteers() {
  try {
    // First, get the event configuration to determine which fields to display
    const eventRes = await fetch(`/api/events/${EVENT_ID}`);
    if (!eventRes.ok) {
      throw new Error(`Failed to fetch event: ${eventRes.status}`);
    }
    
    const eventData = await eventRes.json();
    const formConfig = eventData.form_config || [];
    
    // Determine which fields are included in the form
    const includedFields = {
      organization: formConfig.some(f => f.name === "organization"),
      certifications: formConfig.some(f => f.name === "certifications"),
      emergency_contact: formConfig.some(f => f.name === "emergency_contact_name"),
      commit_location: formConfig.some(f => f.name === "commit_location"),
      online_training: formConfig.some(f => f.name === "online_training"),
      moa_ma_ems: formConfig.some(f => f.name === "moa_ma_ems")
    };
    
    // Update the table headers based on included fields
    const tableHeaders = document.querySelector("#volunteers-table thead tr");
    tableHeaders.innerHTML = `
      <th>First Name</th>
      <th>Last Name</th>
      <th>Phone</th>
      <th>Email</th>
    `;
    
    if (includedFields.organization) {
      tableHeaders.innerHTML += `<th>Organization</th>`;
    }
    
    tableHeaders.innerHTML += `<th>Shifts</th>`;
    
    if (includedFields.certifications) {
      tableHeaders.innerHTML += `<th>Certifications</th>`;
    }
    
    if (includedFields.emergency_contact) {
      tableHeaders.innerHTML += `<th>Emergency Contact</th>`;
    }
    
    if (includedFields.commit_location || includedFields.online_training || includedFields.moa_ma_ems) {
      tableHeaders.innerHTML += `<th>Commitments</th>`;
    }
    
    tableHeaders.innerHTML += `<th>Actions</th>`;
    
    // Now fetch the volunteers
    const res = await fetch(`/api/volunteers/${EVENT_ID}`);
    if (!res.ok) {
      throw new Error(`Failed to fetch volunteers: ${res.status}`);
    }
    
    const volunteers = await res.json();
    const tableBody = document.querySelector("#volunteers-table tbody");
    tableBody.innerHTML = "";
    
    if (volunteers.length === 0) {
      const columnCount = tableHeaders.querySelectorAll("th").length;
      const emptyRow = document.createElement("tr");
      emptyRow.innerHTML = `<td colspan="${columnCount}" class="empty-message">No volunteers have signed up yet.</td>`;
      tableBody.appendChild(emptyRow);
      return;
    }
    
    // Check for duplicate volunteers (same email address)
    const emailCounts = {};
    volunteers.forEach(v => {
      if (v.email) {
        emailCounts[v.email] = (emailCounts[v.email] || 0) + 1;
      }
    });
    
    // Get unique volunteers (keep only the most recent signup for each email)
    const uniqueVolunteers = [];
    const processedEmails = new Set();
    
    // Sort volunteers by submit_date in descending order (most recent first)
    const sortedVolunteers = [...volunteers].sort((a, b) => {
      const dateA = a.submit_date ? new Date(a.submit_date) : new Date(0);
      const dateB = b.submit_date ? new Date(b.submit_date) : new Date(0);
      return dateB - dateA;
    });
    
    // Keep only the most recent signup for each email
    sortedVolunteers.forEach(v => {
      if (v.email && !processedEmails.has(v.email)) {
        uniqueVolunteers.push(v);
        processedEmails.add(v.email);
      }
    });
    
    // Display the unique volunteers
    uniqueVolunteers.forEach(v => {
      // Format shifts
      let shifts = "None";
      if (v.shifts && typeof v.shifts === 'object') {
        const selectedShifts = Object.entries(v.shifts)
          .filter(([k, val]) => val)
          .map(([k]) => shiftLabels[k] || k);
          
        shifts = selectedShifts.length > 0 ? selectedShifts.join(",<br>") : "None";
      }
      
      // Format certifications
      const certs = Array.isArray(v.certifications) ? v.certifications.join(", ") : (v.certifications || "");
      
      // Format emergency contact
      const emergencyContact = v.emergency_contact_name ? 
        `${v.emergency_contact_name}<br>${v.emergency_contact_phone || ""}` : 
        "";
      
      // Format commitments
      let commitments = [];
      if (includedFields.commit_location && v.commit_location) {
        commitments.push(`Location: ${v.commit_location}`);
      }
      if (includedFields.online_training && v.online_training) {
        commitments.push(`Training: ${v.online_training}`);
      }
      if (includedFields.moa_ma_ems && v.moa_ma_ems) {
        commitments.push(`MOA/MA/EMS: ${v.moa_ma_ems}`);
      }
      const commitmentsHtml = commitments.length > 0 ? commitments.join("<br>") : "";
      
      // Create table row
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${v.first_name || ""}</td>
        <td>${v.last_name || ""}</td>
        <td>${v.phone || ""}</td>
        <td>${v.email || ""}</td>
      `;
      
      if (includedFields.organization) {
        row.innerHTML += `<td>${v.organization || ""}</td>`;
      }
      
      row.innerHTML += `<td class="shifts-list">${shifts}</td>`;
      
      if (includedFields.certifications) {
        row.innerHTML += `<td class="cert-list">${certs}</td>`;
      }
      
      if (includedFields.emergency_contact) {
        row.innerHTML += `<td>${emergencyContact}</td>`;
      }
      
      if (includedFields.commit_location || includedFields.online_training || includedFields.moa_ma_ems) {
        row.innerHTML += `<td class="yes-no-list">${commitmentsHtml}</td>`;
      }
      
      row.innerHTML += `
        <td>
          <button class="delete-btn" data-email="${v.email}" 
                  data-name="${v.first_name} ${v.last_name}">Remove</button>
        </td>
      `;
      
      tableBody.appendChild(row);
    });
    
    // If we found duplicates, log a message
    const duplicateCount = volunteers.length - uniqueVolunteers.length;
    if (duplicateCount > 0) {
      console.log(`Found and removed ${duplicateCount} duplicate volunteer entries.`);
    }
  } catch (error) {
    console.error("Error fetching volunteers:", error);
    const tableBody = document.querySelector("#volunteers-table tbody");
    tableBody.innerHTML = `<tr><td colspan="9" class="error-message">Error loading volunteer data. Please try refreshing the page.</td></tr>`;
  }
}

/**
 * Handle delete button clicks with confirmation
 */
document.querySelector("#volunteers-table").addEventListener("click", async e => {
  const btn = e.target.closest(".delete-btn");
  if (btn) {
    const email = btn.dataset.email;
    const name = btn.dataset.name || email;
    
    const confirmed = confirm(`Are you sure you want to remove ${name} from the volunteer list?`);
    if (!confirmed) return;
    
    try {
      const res = await fetch(`/api/volunteer/${EVENT_ID}/${email}`, {
        method: "DELETE"
      });
      
      if (!res.ok) {
        throw new Error(`Server returned ${res.status}`);
      }
      
      // Refresh the volunteer list
      fetchVolunteers();
    } catch (error) {
      console.error("Error deleting volunteer:", error);
      alert(`Failed to delete volunteer: ${error.message}`);
    }
  }
});

/**
 * Debounce function to limit how often a function is called
 */
function debounce(func, wait) {
  let timeout;
  return function(...args) {
    const context = this;
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(context, args), wait);
  };
}

/**
 * Search functionality with improved matching and performance
 */
const searchInput = document.getElementById("searchInput");
const searchContainer = searchInput.closest('.search-container');

// Add a visual indicator for active search
searchInput.addEventListener('focus', () => {
  searchContainer.classList.add('search-active');
});

searchInput.addEventListener('blur', () => {
  if (!searchInput.value.trim()) {
    searchContainer.classList.remove('search-active');
  }
});


// Perform the actual search with debounce for better performance
const performSearch = debounce(function(term) {
  // If search is empty, show all rows
  if (!term) {
    document.querySelectorAll("#volunteers-table tbody tr").forEach(row => {
      row.style.display = "";
    });
    searchContainer.classList.remove('search-active');
    return;
  }
  
  searchContainer.classList.add('search-active');
  
  // Split search terms by space to allow searching for multiple terms
  const searchTerms = term.split(/\s+/).filter(t => t.length > 0);
  
  // Track if we found any matches
  let matchFound = false;
  
  // Otherwise filter by all relevant fields
  document.querySelectorAll("#volunteers-table tbody tr").forEach(row => {
    // Skip the "no volunteers" row if it exists
    if (row.querySelector(".empty-message") || row.querySelector(".error-message")) {
      return;
    }
    
    // Get all cell text content for searching
    const firstName = row.cells[0]?.textContent?.toLowerCase() || "";
    const lastName = row.cells[1]?.textContent?.toLowerCase() || "";
    const phone = row.cells[2]?.textContent?.toLowerCase() || "";
    const email = row.cells[3]?.textContent?.toLowerCase() || "";
    
    // Organization might be in different positions depending on form config
    // So we'll search all cells
    const allCellText = Array.from(row.cells).map(cell => 
      cell.textContent.toLowerCase()
    ).join(" ");
    
    // Also create a full name for searching
    const fullName = `${firstName} ${lastName}`.toLowerCase();
    const reverseName = `${lastName} ${firstName}`.toLowerCase();
    
    // Check if all search terms match any field
    const matches = searchTerms.every(searchTerm => {
      return firstName.includes(searchTerm) || 
             lastName.includes(searchTerm) || 
             fullName.includes(searchTerm) ||
             reverseName.includes(searchTerm) ||
             email.includes(searchTerm) ||
             phone.includes(searchTerm) ||
             allCellText.includes(searchTerm);
    });
    
    if (matches) {
      matchFound = true;
    }
    
    row.style.display = matches ? "" : "none";
  });
  
  // Add a class to the table if no results found
  const tableContainer = document.querySelector('.table-container');
  if (!matchFound && searchTerms.length > 0) {
    tableContainer.classList.add('no-results');
  } else {
    tableContainer.classList.remove('no-results');
  }
}, 300); // 300ms debounce delay

// Attach the search input event
searchInput.addEventListener("input", function() {
  const term = this.value.toLowerCase().trim();
  performSearch(term);
});

/**
 * Excel export button handler
 */
document.getElementById("exportExcelBtn").addEventListener("click", function() {
  window.location.href = `/api/export-excel/${EVENT_ID}`;
});

// Initialize dashboard when page loads
window.onload = function() {
  loadEventInfo();
  fetchVolunteers();
};
