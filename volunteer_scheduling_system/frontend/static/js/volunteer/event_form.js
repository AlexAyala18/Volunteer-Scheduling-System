// frontend/static/js/event_form.js

// Language translations
const translations = {
  en: {
    // Page elements
    toggleLanguage: "Español",
    loadingText: "Loading sign-up form...",
    volunteerRegistration: "Volunteer Registration",
    pageTitle: "Volunteer Sign-up",
    emailConfirmation: "A confirmation email has been sent to your email address.",
    emailNotSent: "We couldn't send a confirmation email at this time. Please save this receipt for your records.",
    
    // Form sections
    basicInformation: "Basic Information",
    shiftsAvailability: "Shifts & Availability",
    selectShifts: "Select which shift(s) you can commit to for each day:",
    noShiftsAvailable: "No shifts are currently available for this event.",
    commitmentQuestions: "Commitment Questions",
    certificationsTraining: "Certifications & Other Training",
    checkAllThatApply: "Check all that apply:",
    otherTrainingLabel: "Other Training and Certifications",
    otherTrainingPlaceholder: "Write in your training or certifications.",
    emergencyContact: "Emergency Contact",
    
    // Form fields
    firstName: "First Name",
    lastName: "Last Name",
    emailAddress: "Email Address",
    phoneNumber: "Phone Number",
    organization: "Organization/School",
    emergencyContactName: "Emergency Contact Name",
    emergencyContactPhone: "Emergency Contact Phone",
    
    // Shift table
    shiftTime: "Shift Time",
    allDay: "All Day (Both Shifts)",
    
    // Commitment questions
    canCommit: "Can you commit to your shift located at",
    ageRequirement: "Note: You must be at least {0} years old to volunteer for this event.",
    
    // Certifications
    cpr: "CPR",
    firstAid: "First Aid",
    emt: "EMT",
    rn: "RN",
    md: "MD",
    other: "Other",
    
    // Day names
    monday: "Monday",
    tuesday: "Tuesday",
    wednesday: "Wednesday",
    thursday: "Thursday",
    friday: "Friday",
    saturday: "Saturday",
    sunday: "Sunday",
    
    // Button text
    submitButton: "Submit Volunteer Application",
    
    // Modal text
    thankYou: "Thank You!",
    successMessage: "Your volunteer registration has been submitted successfully.",
    signedUpText: "You have signed up for:",
    confirmationMessage: "We look forward to seeing you!",
    downloadReceipt: "Download Receipt",
    addToCalendar: "Add to Calendar",
    addToCalendarMain: "Add your volunteer shifts to your calendar",
    addToGoogleCalendar: "Add to Google Calendar",
    addToAppleCalendar: "Add to Apple Calendar",
    addToOutlookCalendar: "Add to Outlook Calendar",
    addToYahooCalendar: "Add to Yahoo Calendar",
    ageQuestion: "Are you 18 or older?",
    calendarInstructions: "Add your volunteer shifts to your calendar:",
    fillAnotherForm: "Fill Another Form",
    close: "Close",
    noShiftsSelected: "No shifts selected",
    
    // Event details
    eventDate: "Event Date",
    eventDates: "Event Dates",
    location: "Location",
    description: "Description",
    to: "to",
    
    // Receipt text
    receiptTitle: "Volunteer Receipt",
    receiptThankYou: "Thank you for volunteering at",
    receiptDate: "Date",
    receiptKeepRecord: "Please keep this record for your reference.",
    
    // Error messages
    errorLoading: "Error loading form",
    errorSubmitting: "Error submitting form",
    errorFetchingEvent: "Failed to fetch event",
    errorNoConfig: "No form configuration found for this event",
    errorFormNotFound: "Form element not found",
    errorGeneratingReceipt: "There was an error generating your receipt. Please try again.",
    
    // Form validation errors
    validationErrorTitle: "Please fix the following errors:",
    missingRequiredFields: "Please fill in all required fields marked with *",
    missingFirstName: "First Name is required",
    missingLastName: "Last Name is required",
    missingEmail: "Email Address is required",
    missingPhone: "Phone Number is required",
    missingOrganization: "Organization/School is required",
    missingAgeVerification: "Age verification is required",
    missingShifts: "Please select at least one shift",
    missingEmergencyName: "Emergency Contact Name is required",
    missingEmergencyPhone: "Emergency Contact Phone is required",
    missingCommitment: "Please answer all commitment questions",
    
    // Shift names (for translating backend responses)
    "Mon 7:30-12:30": "Mon 7:30-12:30",
    "Mon 12:30-4:00": "Mon 12:30-4:00",
    "Mon All Day": "Mon All Day",
    "Tue 7:30-12:30": "Tue 7:30-12:30",
    "Tue 12:30-4:00": "Tue 12:30-4:00",
    "Tue All Day": "Tue All Day",
    "Wed 7:30-12:30": "Wed 7:30-12:30",
    "Wed 12:30-4:00": "Wed 12:30-4:00",
    "Wed All Day": "Wed All Day",
    "Thu 7:30-12:30": "Thu 7:30-12:30",
    "Thu 12:30-4:00": "Thu 12:30-4:00",
    "Thu All Day": "Thu All Day",
    "Fri 7:30-12:30": "Fri 7:30-12:30",
    "Fri 12:30-4:00": "Fri 12:30-4:00",
    "Fri All Day": "Fri All Day"
  },
  es: {
    // Page elements
    toggleLanguage: "English",
    loadingText: "Cargando formulario de inscripción...",
    volunteerRegistration: "Registro de Voluntarios",
    pageTitle: "Registro de Voluntarios",
    emailConfirmation: "Se ha enviado un correo de confirmación a su dirección de correo electrónico.",
    emailNotSent: "No pudimos enviar un correo electrónico de confirmación en este momento. Por favor guarde este recibo para sus registros.",
    
    // Form sections
    basicInformation: "Información Básica",
    shiftsAvailability: "Turnos y Disponibilidad",
    selectShifts: "Seleccione los turnos a los que puede comprometerse para cada día:",
    noShiftsAvailable: "No hay turnos disponibles para este evento.",
    commitmentQuestions: "Preguntas de Compromiso",
    certificationsTraining: "Certificaciones y Otra Formación",
    checkAllThatApply: "Marque todas las que correspondan:",
    otherTrainingLabel: "Otras Formaciones y Certificaciones",
    otherTrainingPlaceholder: "Escriba su formación o certificaciones.",
    emergencyContact: "Contacto de Emergencia",
    
    // Form fields
    firstName: "Nombre",
    lastName: "Apellido",
    emailAddress: "Correo Electrónico",
    phoneNumber: "Número de Teléfono",
    organization: "Organización/Escuela",
    emergencyContactName: "Nombre de Contacto de Emergencia",
    emergencyContactPhone: "Teléfono de Contacto de Emergencia",
    
    // Shift table
    shiftTime: "Hora del Turno",
    allDay: "Todo el Día (Ambos Turnos)",
    
    // Commitment questions
    canCommit: "¿Puede comprometerse con su turno ubicado en",
    ageRequirement: "Nota: Debe tener al menos {0} años para ser voluntario en este evento.",
    
    // Certifications
    cpr: "RCP",
    firstAid: "Primeros Auxilios",
    emt: "Técnico de Emergencias Médicas",
    rn: "Enfermero/a Registrado/a",
    md: "Doctor/a en Medicina",
    other: "Otro",
    
    // Day names
    monday: "Lunes",
    tuesday: "Martes",
    wednesday: "Miércoles",
    thursday: "Jueves",
    friday: "Viernes",
    saturday: "Sábado",
    sunday: "Domingo",
    
    // Button text
    submitButton: "Enviar Solicitud de Voluntario",
    
    // Modal text
    thankYou: "¡Gracias!",
    successMessage: "Su registro de voluntario ha sido enviado con éxito.",
    signedUpText: "Se ha inscrito para:",
    confirmationMessage: "¡Esperamos verle pronto!",
    downloadReceipt: "Descargar Recibo",
    addToCalendar: "Añadir al Calendario",
    addToCalendarMain: "Añadir sus turnos de voluntario a su calendario",
    addToGoogleCalendar: "Añadir a Google Calendar",
    addToAppleCalendar: "Añadir a Apple Calendar",
    addToOutlookCalendar: "Añadir a Outlook Calendar",
    addToYahooCalendar: "Añadir a Yahoo Calendar",
    ageQuestion: "¿Tiene 18 años o más?",
    calendarInstructions: "Añada sus turnos de voluntario a su calendario:",
    fillAnotherForm: "Completar Otro Formulario",
    close: "Cerrar",
    noShiftsSelected: "No se seleccionaron turnos",
    
    // Event details
    eventDate: "Fecha del Evento",
    eventDates: "Fechas del Evento",
    location: "Ubicación",
    description: "Descripción",
    to: "a",
    
    // Receipt text
    receiptTitle: "Recibo de Voluntario",
    receiptThankYou: "Gracias por ser voluntario en",
    receiptDate: "Fecha",
    receiptKeepRecord: "Por favor guarde este registro para su referencia.",
    
    // Error messages
    errorLoading: "Error al cargar el formulario",
    errorSubmitting: "Error al enviar el formulario",
    errorFetchingEvent: "Error al obtener el evento",
    errorNoConfig: "No se encontró configuración de formulario para este evento",
    errorFormNotFound: "No se encontró el elemento del formulario",
    errorGeneratingReceipt: "Hubo un error al generar su recibo. Por favor intente de nuevo.",
    
    // Form validation errors
    validationErrorTitle: "Por favor corrija los siguientes errores:",
    missingRequiredFields: "Por favor complete todos los campos obligatorios marcados con *",
    missingFirstName: "El Nombre es obligatorio",
    missingLastName: "El Apellido es obligatorio",
    missingEmail: "El Correo Electrónico es obligatorio",
    missingPhone: "El Número de Teléfono es obligatorio",
    missingOrganization: "La Organización/Escuela es obligatoria",
    missingAgeVerification: "La verificación de edad es obligatoria",
    missingShifts: "Por favor seleccione al menos un turno",
    missingEmergencyName: "El Nombre de Contacto de Emergencia es obligatorio",
    missingEmergencyPhone: "El Teléfono de Contacto de Emergencia es obligatorio",
    missingCommitment: "Por favor responda todas las preguntas de compromiso",
    
    // Shift names (for translating backend responses)
    "Mon 7:30-12:30": "Lun 7:30-12:30",
    "Mon 12:30-4:00": "Lun 12:30-4:00",
    "Mon All Day": "Lun Todo el Día",
    "Tue 7:30-12:30": "Mar 7:30-12:30",
    "Tue 12:30-4:00": "Mar 12:30-4:00",
    "Tue All Day": "Mar Todo el Día",
    "Wed 7:30-12:30": "Mié 7:30-12:30",
    "Wed 12:30-4:00": "Mié 12:30-4:00",
    "Wed All Day": "Mié Todo el Día",
    "Thu 7:30-12:30": "Jue 7:30-12:30",
    "Thu 12:30-4:00": "Jue 12:30-4:00",
    "Thu All Day": "Jue Todo el Día",
    "Fri 7:30-12:30": "Vie 7:30-12:30",
    "Fri 12:30-4:00": "Vie 12:30-4:00",
    "Fri All Day": "Vie Todo el Día"
  }
};

// Current language (default: English)
let currentLanguage = localStorage.getItem('volunteerFormLanguage') || 'en';

// Function to show modal with transition
function showModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.style.display = "flex";
  
  // Trigger reflow to ensure transition works
  void modal.offsetWidth;
  
  // Add show class for transition
  modal.classList.add("show");
}

// Function to hide modal with transition
function hideModal(modalId) {
  const modal = document.getElementById(modalId);
  
  // Remove show class to start transition
  modal.classList.remove("show");
  
  // Wait for transition to complete before hiding
  setTimeout(() => {
    modal.style.display = "none";
  }, 300); // Match this with the CSS transition duration
}

// Function to update UI text based on selected language
function updateLanguageUI() {
  const lang = translations[currentLanguage];
  
  // Update toggle button text
  document.getElementById("toggleLanguage").textContent = lang.toggleLanguage;
  
  // Update loading text if visible
  const loadingText = document.getElementById("loadingText");
  if (loadingText) {
    loadingText.textContent = lang.loadingText;
  }
  
  // Update page title
  const eventTitle = document.getElementById("eventTitle");
  if (eventTitle && eventTitle.dataset.originalText) {
    eventTitle.textContent = eventTitle.dataset.originalText;
  }
  
  // Update document title
  document.title = lang.pageTitle;
  
  // Update modal text
  document.getElementById("thankYouText").textContent = lang.thankYou;
  document.getElementById("successMessage").textContent = lang.successMessage;
  document.getElementById("signedUpText").textContent = lang.signedUpText;
  document.getElementById("confirmationMessage").textContent = lang.confirmationMessage;
  document.getElementById("fillAnotherBtn").textContent = lang.fillAnotherForm;
  document.getElementById("closeBtn").textContent = lang.close;
  
  // Update calendar section text if visible
  const calendarInstructions = document.getElementById("calendarInstructions");
  if (calendarInstructions) {
    calendarInstructions.textContent = lang.calendarInstructions;
  }
  
  const googleCalendarBtn = document.getElementById("googleCalendarBtn");
  if (googleCalendarBtn) {
    googleCalendarBtn.textContent = lang.addToGoogleCalendar;
  }
  
  const appleCalendarBtn = document.getElementById("appleCalendarBtn");
  if (appleCalendarBtn) {
    appleCalendarBtn.textContent = lang.addToAppleCalendar;
  }
  
  const outlookCalendarBtn = document.getElementById("outlookCalendarBtn");
  if (outlookCalendarBtn) {
    outlookCalendarBtn.textContent = lang.addToOutlookCalendar;
  }
  
  const yahooCalendarBtn = document.getElementById("yahooCalendarBtn");
  if (yahooCalendarBtn) {
    yahooCalendarBtn.textContent = lang.addToYahooCalendar;
  }
  
  // Update the main calendar button text
  const addToCalendarBtn = document.getElementById("addToCalendarBtn");
  if (addToCalendarBtn && addToCalendarBtn.querySelector("span")) {
    addToCalendarBtn.querySelector("span").textContent = lang.addToCalendarMain;
  }
}

// Toggle language function
function toggleLanguage() {
  currentLanguage = currentLanguage === 'en' ? 'es' : 'en';
  localStorage.setItem('volunteerFormLanguage', currentLanguage);
  updateLanguageUI();
  
  // Update calendar button text if the success modal is visible
  if (document.getElementById("successModal").style.display === "flex") {
    updateCalendarButtonText();
  }
  
  // Reload the form to update all dynamically generated content
  loadForm();
}

// Add event listener to language toggle button
document.getElementById("toggleLanguage").addEventListener("click", toggleLanguage);

async function loadForm() {
  try {
    // Get translations for current language
    const lang = translations[currentLanguage];
    
    // Update UI text based on selected language
    updateLanguageUI();
    
    const res = await fetch(`/api/events/${EVENT_ID}`);
    if (!res.ok) {
      throw new Error(`Failed to fetch event: ${res.status}`);
    }
    
    const data = await res.json();
    if (!data.form_config) {
      throw new Error("No form configuration found for this event");
    }
    
    // Debug: Log the form configuration to see if age_check field is present
    console.log("Form configuration received:", data.form_config);
    console.log("Age requirement field present:", data.form_config.some(field => field.name === "age_check"));
    if (data.form_config.some(field => field.name === "age_check")) {
      const ageField = data.form_config.find(field => field.name === "age_check");
      console.log("Age field details:", ageField);
    }
    
    // Update page title with event name
    const eventTitle = document.getElementById("eventTitle");
    eventTitle.innerText = data.event_name || lang.volunteerRegistration;
    eventTitle.dataset.originalText = data.event_name || lang.volunteerRegistration;
    
    // Remove any existing event details section first
    const existingDetails = document.querySelector(".event-details");
    if (existingDetails) {
      existingDetails.remove();
    }
    
    // Add event details section if we have date, location or description
    if (data.event_description || data.event_location || data.event_start_date) {
      const eventDetailsSection = document.createElement("div");
      eventDetailsSection.classList.add("event-details");
      
      let detailsHTML = "";
      
      // Add dates if available
      if (data.event_start_date) {
        const startDate = new Date(data.event_start_date).toLocaleDateString(
          currentLanguage === 'es' ? 'es-ES' : 'en-US'
        );
        if (data.event_end_date) {
          const endDate = new Date(data.event_end_date).toLocaleDateString(
            currentLanguage === 'es' ? 'es-ES' : 'en-US'
          );
          detailsHTML += `<p><strong>${lang.eventDates}:</strong> ${startDate} ${lang.to} ${endDate}</p>`;
        } else {
          detailsHTML += `<p><strong>${lang.eventDate}:</strong> ${startDate}</p>`;
        }
      }
      
      // Add location if available
      if (data.event_location) {
        detailsHTML += `<p><strong>${lang.location}:</strong> ${data.event_location}</p>`;
      }
      
      // Add description if available
      if (data.event_description) {
        detailsHTML += `<p><strong>${lang.description}:</strong> ${data.event_description}</p>`;
      }
      
      eventDetailsSection.innerHTML = detailsHTML;
      
      // Insert after the title
      const titleElement = document.getElementById("eventTitle");
      titleElement.parentNode.insertBefore(eventDetailsSection, titleElement.nextSibling);
    }
    
    // Get the form element
    const form = document.getElementById("dynamicVolunteerForm");
    if (!form) {
      throw new Error("Form element not found");
    }
    
    // Clear any existing content
    form.innerHTML = "";
    
    // Group fields by section
    let basicInfoFields = [];
    let shiftFields = [];
    let certFields = [];
    let commitmentFields = [];
    let emergencyFields = [];
    
    // Sort fields into appropriate sections
    data.form_config.forEach(field => {
      if (field.type === "shift-selector") {
        shiftFields.push(field);
      } else if (field.name === "emergency_contact_name" || field.name === "emergency_contact_phone") {
        emergencyFields.push(field);
      } else if (field.name === "certifications" || field.name === "other_training") {
        certFields.push(field);
      } else if (field.name.includes("commit") || field.name === "age_check") {
        commitmentFields.push(field);
        // Debug: Log when age_check field is added to commitmentFields
        if (field.name === "age_check") {
          console.log("Age check field added to commitmentFields:", field);
        }
      } else {
        basicInfoFields.push(field);
      }
    });
    
    // Debug: Log all field arrays after sorting
    console.log("Basic info fields:", basicInfoFields);
    console.log("Shift fields:", shiftFields);
    console.log("Certification fields:", certFields);
    console.log("Commitment fields:", commitmentFields);
    console.log("Emergency fields:", emergencyFields);
    
    // Create Basic Info Section
    if (basicInfoFields.length > 0) {
      const basicSection = document.createElement("div");
      basicSection.classList.add("section");
      basicSection.innerHTML = `<h2>${lang.basicInformation}</h2>`;
      
      basicInfoFields.forEach(field => {
        const div = document.createElement("div");
        div.classList.add("field-group");
        
        if (field.type === "text" || field.type === "email") {
          // Use translated field labels if available
          let fieldLabel = field.label;
          
          // Map common field names to translations
          if (field.name === "first_name") {
            fieldLabel = lang.firstName;
          } else if (field.name === "last_name") {
            fieldLabel = lang.lastName;
          } else if (field.name === "email") {
            fieldLabel = lang.emailAddress;
          } else if (field.name === "phone") {
            fieldLabel = lang.phoneNumber;
          } else if (field.name === "organization") {
            fieldLabel = lang.organization;
          }
          
          div.innerHTML = `
            <label for="${field.name}">${fieldLabel}:<span class='required-asterisk'>${field.required ? " *" : ""}</span></label>
            <input type="${field.type}" id="${field.name}" name="${field.name}" ${field.required ? "required" : ""}>
          `;
        }
        
        basicSection.appendChild(div);
      });
      
      form.appendChild(basicSection);
    }
    
    // Create Shifts Section
    if (shiftFields.length > 0) {
      const shiftsSection = document.createElement("div");
      shiftsSection.classList.add("section");
      shiftsSection.innerHTML = `<h2>${lang.shiftsAvailability}</h2>`;
      
      shiftFields.forEach(field => {
        const div = document.createElement("div");
        div.classList.add("field-group");
        
        div.innerHTML = `<p>${lang.selectShifts}</p>`;
        
        // Get the schedule configuration
        const schedule = field.schedule || {};
        
        // Create shift selector with days and times from the schedule
        const days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"];
        const dayNames = {
          "monday": lang.monday,
          "tuesday": lang.tuesday,
          "wednesday": lang.wednesday,
          "thursday": lang.thursday,
          "friday": lang.friday,
          "saturday": lang.saturday,
          "sunday": lang.sunday
        };
        
        // Check if we're on a mobile device
        const isMobile = window.innerWidth <= 576;
        
        // Debug the schedule configuration
        console.log("Schedule configuration:", schedule);
        
        // Create a table for shifts based on the schedule configuration
        let tableHTML = '';
        
        // Check if we have any enabled days
        const enabledDays = days.filter(day => schedule[day]?.enabled);
        
        if (enabledDays.length === 0) {
          // No days are enabled, show a message
          tableHTML = `<p>${lang.noShiftsAvailable}</p>`;
        } else {
          // Start building the table
          tableHTML = `
            <div class="shifts-table-container">
              <table class="shifts-table">
                <thead>
                  <tr>
                    <th>${currentLanguage === 'es' ? 'Hora del Turno' : 'Shift Time'}</th>
          `;
          
          // Add column headers for each day that's enabled
          enabledDays.forEach(day => {
            // For mobile, abbreviate day names to first 3 letters
            const dayName = isMobile ? dayNames[day].substring(0, 3) : dayNames[day];
            tableHTML += `<th>${dayName}</th>`;
          });
          
          tableHTML += `
                  </tr>
                </thead>
                <tbody>
          `;
          
          // Get all unique shifts across all days
          const allShifts = new Set();
          enabledDays.forEach(day => {
            if (schedule[day]?.shifts) {
              Object.keys(schedule[day].shifts).forEach(shift => {
                if (schedule[day].shifts[shift].enabled) {
                  allShifts.add(shift);
                }
              });
            }
          });
          
          // Check if we have any shifts
          if (allShifts.size === 0) {
            tableHTML += `
              <tr>
                <td colspan="${enabledDays.length + 1}" style="text-align: center;">
                  ${lang.noShiftsAvailable}
                </td>
              </tr>
            `;
          } else {
            // Add rows for each shift
            Array.from(allShifts).forEach(shiftKey => {
              // Get the label for this shift from the first day that has it
              let shiftLabel = "";
              for (const day of enabledDays) {
                if (schedule[day]?.shifts?.[shiftKey]?.enabled && 
                    schedule[day]?.shifts?.[shiftKey]?.label) {
                  shiftLabel = schedule[day].shifts[shiftKey].label;
                  break;
                }
              }
              
              // Translate "All Day" if present
              if (shiftLabel === "All Day") {
                shiftLabel = lang.allDay;
              }
              
              tableHTML += `
                <tr>
                  <td><strong>${shiftLabel}</strong></td>
              `;
              
              // Add cells for each day
              enabledDays.forEach(day => {
                const isEnabled = schedule[day]?.shifts?.[shiftKey]?.enabled;
                if (isEnabled) {
                  const id = `${day}_${shiftKey}`;
                  tableHTML += `
                    <td>
                      <input type="checkbox" id="${id}" name="shifts[${id}]">
                    </td>
                  `;
                } else {
                  tableHTML += `<td>-</td>`;
                }
              });
              
              tableHTML += `</tr>`;
            });
          }
          
          tableHTML += `
                </tbody>
              </table>
            </div>
          `;
        }
        
        div.innerHTML += tableHTML;
        
        shiftsSection.appendChild(div);
      });
      
      form.appendChild(shiftsSection);
    }
    
    // Create Commitment Questions Section
    if (commitmentFields.length > 0) {
      const commitSection = document.createElement("div");
      commitSection.classList.add("section");
      commitSection.innerHTML = `<h2>${lang.commitmentQuestions}</h2>`;
      
      commitmentFields.forEach(field => {
        const div = document.createElement("div");
        div.classList.add("field-group");
        
        if (field.type === "radio-group") {
          // Check if this is a commitment question
          let label = field.label;
          
          // Special handling for age verification field
          if (field.name === "age_check" && field.min_age) {
            const minAge = field.min_age;
            // Use the translated label for age verification
            div.innerHTML = `<label>${lang.ageQuestion}<span class='required-asterisk'>${field.required ? " *" : ""}</span></label>
                            <div class="yes-no-container">
                              <label class="radio-label">
                                <input type="radio" name="${field.name}" value="Yes" ${field.required ? "required" : ""}> ${currentLanguage === 'es' ? 'Sí' : 'Yes'}
                              </label>
                              <label class="radio-label">
                                <input type="radio" name="${field.name}" value="No" ${field.required ? "required" : ""}> No
                              </label>
                            </div>
                            <small>${currentLanguage === 'es' ? 
                              `Nota: Debe tener al menos ${minAge} años para ser voluntario en este evento.` : 
                              `Note: You must be at least ${minAge} years old to volunteer for this event.`}</small>`;
          } 
            // If it's a commitment question about location, use the translated version
            else if (label.toLowerCase().includes("can you commit") || 
                label.toLowerCase().includes("commit to your shift")) {
              label = `${lang.canCommit} ${data.event_location}?`;
              
              // Remove "the" before location name if present
              if (label.includes("at the ")) {
                label = label.replace("at the ", "at ");
              }
              
              // Always add the asterisk to commitment questions
              div.innerHTML = `<label>${label}<span class='required-asterisk'> *</span></label>
                              <div class="yes-no-container">
                                <label class="radio-label">
                                  <input type="radio" name="${field.name}" value="Yes" required> ${currentLanguage === 'es' ? 'Sí' : 'Yes'}
                                </label>
                                <label class="radio-label">
                                  <input type="radio" name="${field.name}" value="No" required> No
                                </label>
                              </div>`;
            } 
          // Handle other commitment questions
          else {
            // Replace placeholder text with actual location if needed
            if (label.includes("event location") && data.event_location) {
              label = label.replace("event location", data.event_location);
            }
            
            div.innerHTML = `<label>${label}</label>
                            <div class="yes-no-container">
                              <label class="radio-label">
                                <input type="radio" name="${field.name}" value="Yes" ${field.required ? "required" : ""}> ${currentLanguage === 'es' ? 'Sí' : 'Yes'}
                              </label>
                              <label class="radio-label">
                                <input type="radio" name="${field.name}" value="No" ${field.required ? "required" : ""}> No
                              </label>
                            </div>`;
          }
        } else {
          div.innerHTML = `<label for="${field.name}">${field.label}</label>
                          <input type="${field.type}" id="${field.name}" name="${field.name}" ${field.required ? "required" : ""}>`;
        }
        
        commitSection.appendChild(div);
      });
      
      form.appendChild(commitSection);
    }
    
    // Create Certifications Section
    if (certFields.length > 0) {
      const certSection = document.createElement("div");
      certSection.classList.add("section");
      certSection.innerHTML = `<h2>${lang.certificationsTraining}</h2>`;
      certSection.innerHTML += `<p>${lang.checkAllThatApply}</p>`;
      
      // First add the certifications checkbox group
      const certField = certFields.find(f => f.name === "certifications");
      if (certField) {
        const div = document.createElement("div");
        div.classList.add("field-group");
        
        // Create a container for the checkboxes
        const certContainer = document.createElement("div");
        certContainer.className = "certifications-container";
        
        // Add each certification option as a checkbox
        if (certField.options && Array.isArray(certField.options)) {
          certField.options.forEach(opt => {
            const id = `${certField.name}_${opt.replace(/\s+/g, '_').toLowerCase()}`;
            
            // Create the label element
            const label = document.createElement("label");
            label.className = "checkbox-label";
            
            // Create the checkbox input
            const input = document.createElement("input");
            input.type = "checkbox";
            input.id = id;
            input.name = certField.name;
            input.value = opt;
            
            // Translate common certification options
            let displayText = opt;
            if (opt === "CPR") {
              displayText = lang.cpr;
            } else if (opt === "First Aid") {
              displayText = lang.firstAid;
            } else if (opt === "EMT") {
              displayText = lang.emt;
            } else if (opt === "RN") {
              displayText = lang.rn;
            } else if (opt === "MD") {
              displayText = lang.md;
            } else if (opt === "Other") {
              displayText = lang.other;
            }
            
            // Add the input and text to the label
            label.appendChild(input);
            label.appendChild(document.createTextNode(` ${displayText}`));
            
            // Add the label to the container
            certContainer.appendChild(label);
          });
        } else {
          console.error("Certification options missing or not an array:", certField);
          certContainer.innerHTML = "<p>Error: No certification options available</p>";
        }
        
        // Add the container to the div
        div.appendChild(certContainer);
        certSection.appendChild(div);
      }
      
      // Then add the other training text field
      const trainingField = certFields.find(f => f.name === "other_training");
      if (trainingField) {
        const div = document.createElement("div");
        div.classList.add("field-group");
        
        div.innerHTML = `<label for="${trainingField.name}">${lang.otherTrainingLabel}</label>
                        <input type="${trainingField.type}" id="${trainingField.name}" name="${trainingField.name}" placeholder="${lang.otherTrainingPlaceholder}">`;
        
        certSection.appendChild(div);
      }
      
      form.appendChild(certSection);
    }
    
    // Create Emergency Contact Section
    if (emergencyFields.length > 0) {
      const emergencySection = document.createElement("div");
      emergencySection.classList.add("section");
      emergencySection.innerHTML = `<h2>${lang.emergencyContact}</h2>`;
      
      emergencyFields.forEach(field => {
        const div = document.createElement("div");
        div.classList.add("field-group");
        
        // Translate emergency contact field labels
        let fieldLabel = field.label;
        if (field.name === "emergency_contact_name") {
          fieldLabel = currentLanguage === 'es' ? "Nombre de Contacto de Emergencia" : "Emergency Contact Name";
        } else if (field.name === "emergency_contact_phone") {
          fieldLabel = currentLanguage === 'es' ? "Teléfono de Contacto de Emergencia" : "Emergency Contact Phone";
        }
        
        div.innerHTML = `
          <label for="${field.name}">${fieldLabel}:<span class='required-asterisk'>${field.required ? " *" : ""}</span></label>
          <input type="text" id="${field.name}" name="${field.name}" ${field.required ? "required" : ""}>
        `;
        
        emergencySection.appendChild(div);
      });
      
      form.appendChild(emergencySection);
    }
    
    // Add submit button
    const submitDiv = document.createElement("div");
    submitDiv.classList.add("submit-container");
    
    const submit = document.createElement("button");
    submit.textContent = lang.submitButton;
    submit.type = "submit";
    
    submitDiv.appendChild(submit);
    form.appendChild(submitDiv);
    
    // Debug: Check for any empty sections that might be causing the blank grey box
    console.log("Form structure after generation:");
    const sections = form.querySelectorAll('.section');
    sections.forEach((section, index) => {
      console.log(`Section ${index + 1}:`, section);
      console.log(`  - Has heading:`, section.querySelector('h2') !== null);
      console.log(`  - Number of field groups:`, section.querySelectorAll('.field-group').length);
      console.log(`  - Empty:`, section.innerHTML.trim() === '');
      console.log(`  - Content:`, section.innerHTML);
    });
    
    // Remove any empty sections or divs that might be causing the blank grey box
    const allDivs = form.querySelectorAll('div');
    allDivs.forEach(div => {
      // Check if the div is empty or contains only whitespace
      if (div.innerHTML.trim() === '' || !div.hasChildNodes()) {
        console.log("Removing empty div:", div);
        div.remove();
      }
    });
    
    // Fix the specific issue with the blank grey box between Organization and Shifts
    // Find all elements with class "field-group" that might be causing the issue
    const fieldGroups = form.querySelectorAll('.field-group');
    fieldGroups.forEach(group => {
      // Remove any empty paragraphs, divs, or other elements that might be causing the issue
      const emptyElements = group.querySelectorAll('p:empty, div:empty, span:empty');
      emptyElements.forEach(el => el.remove());
      
      // Remove any elements that contain only whitespace
      Array.from(group.childNodes).forEach(node => {
        if (node.nodeType === Node.TEXT_NODE && node.textContent.trim() === '') {
          node.remove();
        }
      });
    });
    
    // Remove any whitespace text nodes directly in the form
    Array.from(form.childNodes).forEach(node => {
      if (node.nodeType === Node.TEXT_NODE && node.textContent.trim() === '') {
        node.remove();
      }
    });
    
    // Function to validate the form
    function validateForm(form) {
      const lang = translations[currentLanguage];
      const formData = new FormData(form);
      const errors = [];
      const missingFields = [];
      
      // Remove any existing error messages
      const existingErrorContainer = document.querySelector('.validation-error-container');
      if (existingErrorContainer) {
        existingErrorContainer.remove();
      }
      
      // Remove error highlighting from all fields
      const allInputs = form.querySelectorAll('input, select, textarea');
      allInputs.forEach(input => {
        input.classList.remove('field-error');
        const errorMsg = input.parentNode.querySelector('.field-error-message');
        if (errorMsg) {
          errorMsg.remove();
        }
      });
      
      // Check required basic info fields
      const basicInfoFields = [
        { name: 'first_name', message: lang.missingFirstName },
        { name: 'last_name', message: lang.missingLastName },
        { name: 'email', message: lang.missingEmail },
        { name: 'phone', message: lang.missingPhone },
        { name: 'organization', message: lang.missingOrganization }
      ];
      
      basicInfoFields.forEach(field => {
        const input = form.querySelector(`#${field.name}`);
        if (input && input.required && !formData.get(field.name)) {
          errors.push(field.message);
          missingFields.push(input);
          
          // Add error class to the input
          input.classList.add('field-error');
          
          // Add error message below the input
          const errorMsg = document.createElement('span');
          errorMsg.className = 'field-error-message';
          errorMsg.textContent = field.message;
          input.parentNode.appendChild(errorMsg);
        }
      });
      
      // Check if at least one shift is selected
      let shiftsSelected = false;
      for (const [key, value] of formData.entries()) {
        if (key.startsWith('shifts[')) {
          shiftsSelected = true;
          break;
        }
      }
      
      if (!shiftsSelected) {
        errors.push(lang.missingShifts);
        
        // Highlight the shifts section
        const shiftsSection = form.querySelector('.section:has(table.shifts-table)');
        if (shiftsSection) {
          const errorMsg = document.createElement('span');
          errorMsg.className = 'field-error-message';
          errorMsg.textContent = lang.missingShifts;
          shiftsSection.querySelector('.field-group').appendChild(errorMsg);
        }
      }
      
      // Check age verification if required
      const ageCheckInputs = form.querySelectorAll('input[name="age_check"]');
      if (ageCheckInputs.length > 0 && ageCheckInputs[0].required) {
        const ageChecked = Array.from(ageCheckInputs).some(input => input.checked);
        if (!ageChecked) {
          errors.push(lang.missingAgeVerification);
          
          // Find the age check container and add error class
          const ageCheckContainer = ageCheckInputs[0].closest('.field-group');
          if (ageCheckContainer) {
            const errorMsg = document.createElement('span');
            errorMsg.className = 'field-error-message';
            errorMsg.textContent = lang.missingAgeVerification;
            ageCheckContainer.appendChild(errorMsg);
          }
        } else {
          // Check if the user selected "No" for age verification
          const noSelected = Array.from(ageCheckInputs).find(input => input.value === "No" && input.checked);
          if (noSelected) {
            // Get the min_age from the small text if available
            let minAgeText = "";
            const ageCheckContainer = ageCheckInputs[0].closest('.field-group');
            if (ageCheckContainer) {
              const smallText = ageCheckContainer.querySelector('small');
              if (smallText) {
                minAgeText = smallText.textContent;
              }
            }
            
            // Add error message about age requirement
            errors.push(currentLanguage === 'es' ? 
              `Debe tener la edad mínima requerida para ser voluntario en este evento.` : 
              `You must meet the minimum age requirement to volunteer for this event.`);
            
            // Find the age check container and add error class
            const ageCheckContainerElement = ageCheckInputs[0].closest('.field-group');
            if (ageCheckContainerElement) {
              const errorMsg = document.createElement('span');
              errorMsg.className = 'field-error-message';
              errorMsg.style.color = "#f44336"; // Red color for emphasis
              errorMsg.style.fontWeight = "bold";
              errorMsg.textContent = currentLanguage === 'es' ? 
                `Debe tener la edad mínima requerida para ser voluntario en este evento.` : 
                `You must meet the minimum age requirement to volunteer for this event.`;
              ageCheckContainerElement.appendChild(errorMsg);
            }
          }
        }
      }
      
      // Check commitment questions
      const commitmentQuestions = form.querySelectorAll('.field-group:has(input[type="radio"][required])');
      commitmentQuestions.forEach(question => {
        const name = question.querySelector('input[type="radio"]').name;
        if (name !== 'age_check') { // Skip age check as it's handled separately
          const answered = Array.from(question.querySelectorAll(`input[name="${name}"]`)).some(input => input.checked);
          if (!answered) {
            errors.push(lang.missingCommitment);
            
            // Add error class to the question container
            const errorMsg = document.createElement('span');
            errorMsg.className = 'field-error-message';
            errorMsg.textContent = lang.missingCommitment;
            question.appendChild(errorMsg);
          }
        }
      });
      
      // Check emergency contact fields if required
      const emergencyFields = [
        { name: 'emergency_contact_name', message: lang.missingEmergencyName },
        { name: 'emergency_contact_phone', message: lang.missingEmergencyPhone }
      ];
      
      emergencyFields.forEach(field => {
        const input = form.querySelector(`#${field.name}`);
        if (input && input.required && !formData.get(field.name)) {
          errors.push(field.message);
          missingFields.push(input);
          
          // Add error class to the input
          input.classList.add('field-error');
          
          // Add error message below the input
          const errorMsg = document.createElement('span');
          errorMsg.className = 'field-error-message';
          errorMsg.textContent = field.message;
          input.parentNode.appendChild(errorMsg);
        }
      });
      
      // If there are errors, display them
      if (errors.length > 0) {
        // Create error container
        const errorContainer = document.createElement('div');
        errorContainer.className = 'validation-error-container';
        
        // Add error title
        const errorTitle = document.createElement('div');
        errorTitle.className = 'validation-error-title';
        errorTitle.textContent = lang.validationErrorTitle;
        errorContainer.appendChild(errorTitle);
        
        // Add error list
        const errorList = document.createElement('ul');
        errorList.className = 'validation-error-list';
        errors.forEach(error => {
          const li = document.createElement('li');
          li.textContent = error;
          errorList.appendChild(li);
        });
        errorContainer.appendChild(errorList);
        
        // Insert at the top of the form
        form.insertBefore(errorContainer, form.firstChild);
        
        // Scroll to the error container
        errorContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        return false;
      }
      
      return true;
    }
    
    // Handle form submission
    form.onsubmit = async e => {
      e.preventDefault();
      
      // Validate the form
      if (!validateForm(form)) {
        return false;
      }
      
      // Collect form data
      const formData = new FormData(form);
      const payload = {
        shifts: {},
        language_preference: currentLanguage // Add the current language preference
      };
      
      // Store volunteer data for receipt generation
      window.volunteerData = {
        first_name: formData.get("first_name") || "",
        last_name: formData.get("last_name") || "",
        email: formData.get("email") || "",
        phone: formData.get("phone") || "",
        organization: formData.get("organization") || "",
        emergency_contact_name: formData.get("emergency_contact_name") || "",
        emergency_contact_phone: formData.get("emergency_contact_phone") || "",
        certifications: [],
        other_training: formData.get("other_training") || ""
      };
      
      // Process form data
      for (const [key, value] of formData.entries()) {
        if (key.startsWith("shifts[")) {
          // Extract shift key from shifts[day_shift] format
          const shiftKey = key.match(/\[(.*?)\]/)[1];
          payload.shifts[shiftKey] = true;
        } else if (key === "certifications") {
          // Handle certifications specially since they're checkboxes with the same name
          if (!payload.certifications) {
            payload.certifications = [];
          }
          payload.certifications.push(value);
          
          // Also store in volunteerData
          window.volunteerData.certifications.push(value);
        } else if (payload[key]) {
          // Handle other multiple values
          if (!Array.isArray(payload[key])) {
            payload[key] = [payload[key]];
          }
          payload[key].push(value);
        } else {
          payload[key] = value;
        }
      }
      
      console.log("Form submission payload:", payload);
      console.log("Stored volunteer data for receipt:", window.volunteerData);
      
      try {
        const res = await fetch(`/api/submit/${EVENT_ID}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        
        if (!res.ok) {
          const error = await res.json();
          throw new Error(error.error || "Failed to submit form");
        }
        
        const result = await res.json();
        
        // Show success modal with shift summary
        let shiftSummary = result.shiftSummary || lang.noShiftsSelected;
        
        // Translate shift names if in Spanish
        if (currentLanguage === 'es' && shiftSummary !== lang.noShiftsSelected) {
          // Split by commas and translate each shift name
          const shifts = shiftSummary.split(', ');
          const translatedShifts = shifts.map(shift => {
            // For dynamic shift times, we need to handle translation differently
            // First, try to find an exact match in the translations
            if (lang[shift.trim()]) {
              return lang[shift.trim()];
            }
            
            // If no exact match, try to translate the day abbreviation and keep the time
            const dayMatch = shift.match(/^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(.+)$/);
            if (dayMatch) {
              const day = dayMatch[1];
              const timeInfo = dayMatch[2];
              
              // Translate day abbreviations
              let translatedDay = day;
              if (day === 'Mon') translatedDay = 'Lun';
              else if (day === 'Tue') translatedDay = 'Mar';
              else if (day === 'Wed') translatedDay = 'Mié';
              else if (day === 'Thu') translatedDay = 'Jue';
              else if (day === 'Fri') translatedDay = 'Vie';
              else if (day === 'Sat') translatedDay = 'Sáb';
              else if (day === 'Sun') translatedDay = 'Dom';
              
              // Handle "All Day" specifically
              if (timeInfo === 'All Day') {
                return `${translatedDay} Todo el Día`;
              }
              
              // Return the translated day with the original time
              return `${translatedDay} ${timeInfo}`;
            }
            
            // If all else fails, return the original shift name
            return shift;
          });
          shiftSummary = translatedShifts.join(', ');
        }
        
        // Set the shift summary in the modal
        document.getElementById("shiftReceipt").textContent = shiftSummary;
        
        // Show email confirmation message if email was sent
        const emailConfirmationEl = document.getElementById("emailConfirmation");
        if (result.emailSent) {
          emailConfirmationEl.textContent = lang.emailConfirmation;
          emailConfirmationEl.style.color = "#4CAF50"; // Green color for success
        } else {
          emailConfirmationEl.textContent = lang.emailNotSent;
          emailConfirmationEl.style.color = "#FF9800"; // Orange color for warning
        }
        
        // Show the success modal with transition
        showModal("successModal");
      } catch (error) {
        alert(`${lang.errorSubmitting}: ${error.message}`);
      }
    };
  } catch (error) {
    alert(`${lang.errorLoading}: ${error.message}`);
    console.error(error);
  }
}

// Modal button handlers
document.getElementById("fillAnotherBtn").addEventListener("click", function() {
  hideModal("successModal");
  document.getElementById("dynamicVolunteerForm").reset();
});

document.getElementById("closeBtn").addEventListener("click", function() {
  hideModal("successModal");
  // Redirect to the volunteer opportunities page
  window.location.href = "/volunteer/events";
});

// Initialize form when page loads
window.onload = loadForm;
