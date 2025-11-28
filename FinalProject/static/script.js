function newCourse() {
    const container = document.querySelector(".rounded-text-body");

    const wrapper = document.createElement("div");
    wrapper.className = "rounded-text-entry";

    wrapper.innerHTML = `
        <div class="input-row">
                <input id="new-course-input" placeholder="Enter subject code (e.g. ENGL 11)" 
                class="new-input" 
                style="width:100%; 
                border:none; 
                outline:none; 
                background:#fff;
                font-size: 13px"/>
                <button class="btn-sched" onclick="openSchedules(event, this)" 
                style="background:#1E90FF; 
                color:white; 
                padding:8px 10px; 
                border-radius:6px; 
                border:none;">
                Sched</button>
                <button class="btn-cancel" onclick="this.parentElement.parentElement.remove()" 
                style="background:#ff6b6b; 
                color:white; 
                padding:8px 10px; 
                border-radius:6px; 
                border:none;">
                Cancel</button>

        </div>
    `;

    container.appendChild(wrapper);
}

function openSchedules(event, btn) {
    event.preventDefault();  // prevents page refresh

    const input = btn.parentElement.querySelector("input");
    const code = input.value.trim();

    console.log("Sending code:", code);

    if (code === "") {
        alert("Please enter a subject code.");
        return;
    }

    fetch("/get_schedules", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ code: code })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Received data:", data);
        renderSections(data.sections, code);
    })
    .catch(err => console.error("Error fetching schedules:", err));
}

function renderSections(sectionList, subjectCode) {
    const container = document.querySelector(".rounded-text-body + .rounded-text-body");

    container.innerHTML = `<b>Select from the following sections:</b><br><br>`;

    // Add safety check
    if (!Array.isArray(sectionList) || sectionList.length === 0) {
        container.innerHTML += `<p>No sections found for ${subjectCode}</p>`;
        return;
    }

    sectionList.forEach(section => {
        const card = document.createElement("div");
        card.className = "rounded-text-entry";

        card.innerHTML = `
            <div class="input-row">
                <div style="width: 80%; font-size:14px;">
                    <b>${subjectCode} — ${section["Section"] || section.section}</b><br>
                    ${section["Time"] || section.time || 'TBA'}<br>
                    ${section["Room"] || section.room || 'TBA'}<br>
                    ${section["Instructor"] || section.instructor || 'TBA'}
                </div>

                <button class="btn-sched" onclick="openSection('${subjectCode}', '${section["Section"] || section.section}')">
                    Add
                </button>
            </div>
        `;

        container.appendChild(card);
    });
}

function openSection(code, selectedSection) {

    fetch("/select_section", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            new_code: code,
            new_section: selectedSection
        })
    })
    .then(res => res.json())
    .then(data => {
        placeClassOnSchedule(data);
    })
    .catch(err => console.error("Error selecting section:", err));
}

function parseTimeString(timeStr) {
    // Example: "M-TH 1230-1400\n(FULLY ONSITE)"
    // Remove anything in parentheses and extra whitespace
    const cleaned = timeStr.replace(/\(.*?\)/g, '').trim();
    
    // Split by space to get day part and time part
    const parts = cleaned.split(/\s+/);
    if (parts.length < 2) return null;
    
    const dayPart = parts[0];
    const timePart = parts[1];
    
    // Parse days
    const days = parseDays(dayPart);
    
    // Parse time range
    const [startTime, endTime] = timePart.split('-');
    
    return {
        days: days,
        startTime: startTime,
        endTime: endTime
    };
}

function parseDays(dayStr) {
    const dayMap = {
        'M': 'Monday',
        'T': 'Tuesday',
        'W': 'Wednesday',
        'TH': 'Thursday',
        'F': 'Friday',
        'SAT': 'Saturday'
    };
    
    const days = [];
    
    // Handle combined days like "M-TH" or "T-F"
    if (dayStr.includes('-')) {
        const parts = dayStr.split('-');
        parts.forEach(part => {
            if (dayMap[part]) {
                days.push(dayMap[part]);
            }
        });
    } else {
        // Single day
        if (dayMap[dayStr]) {
            days.push(dayMap[dayStr]);
        }
    }
    
    return days;
}

function formatTime(militaryTime) {
    if (militaryTime.length === 4) {
        return militaryTime.slice(0, 2) + ':' + militaryTime.slice(2);
    }
    return militaryTime;
}

let addedClasses = [];

function placeClassOnSchedule(responseData) {
    console.log("Placing class:", responseData);
    
    // Extract the actual section data
    if (!responseData || !responseData.section) {
        console.error("No section data received");
        return;
    }
    
    const classObj = responseData.section;
    
    // Parse the time string
    const timeInfo = parseTimeString(classObj["Time"]);
    if (!timeInfo) {
        console.error("Could not parse time string:", classObj["Time"]);
        return;
    }
    
    console.log("Parsed time info:", timeInfo);
    
    // Create a unique identifier for this class
    const classId = `${classObj["Subject Code"]}-${classObj["Section"]}`;
    
    // Add to tracking array
    addedClasses.push({
        id: classId,
        data: classObj,
        timeInfo: timeInfo
    });
    
    // Update the courseload display
    updateCourseloadDisplay();
    
    // Map day → column number
    const columnMap = {
        "Monday": 2,
        "Tuesday": 3,
        "Wednesday": 4,
        "Thursday": 5,
        "Friday": 6,
        "Saturday": 7
    };
    
    // Calculate duration in 30-minute blocks
    const startMinutes = parseInt(timeInfo.startTime.slice(0, 2)) * 60 + parseInt(timeInfo.startTime.slice(2));
    const endMinutes = parseInt(timeInfo.endTime.slice(0, 2)) * 60 + parseInt(timeInfo.endTime.slice(2));
    const durationMinutes = endMinutes - startMinutes;
    const blocksNeeded = Math.ceil(durationMinutes / 30);
    
    console.log(`Duration: ${durationMinutes} minutes = ${blocksNeeded} blocks`);
    
    // Place the class on each day it occurs
    timeInfo.days.forEach(day => {
        let colIndex = columnMap[day];
        if (!colIndex) {
            console.error(`Day "${day}" not found in columnMap`);
            return;
        }
        
        // Get all table rows
        const rows = document.querySelectorAll("table tr");
        let startRowIndex = -1;
        
        // Find the starting row
        rows.forEach((row, index) => {
            const timeCell = row.querySelector("th");
            if (!timeCell) return;
            
            const timeRange = timeCell.innerText.trim();
            const [rowStart, rowEnd] = timeRange.split("-");
            
            // Compare start times
            const normalizedRowStart = rowStart.replace(":", "");
            const normalizedClassStart = timeInfo.startTime;
            
            if (normalizedRowStart === normalizedClassStart) {
                startRowIndex = index;
            }
        });
        
        if (startRowIndex === -1) {
            console.error(`No row found for start time: ${timeInfo.startTime} on ${day}`);
            return;
        }
        
        console.log(`Found starting row at index ${startRowIndex}, filling ${blocksNeeded} blocks`);
        
        // Fill all the blocks this class spans
        for (let blockOffset = 0; blockOffset < blocksNeeded; blockOffset++) {
            const currentRowIndex = startRowIndex + blockOffset;
            
            if (currentRowIndex >= rows.length) {
                console.warn(`Row ${currentRowIndex} out of bounds`);
                break;
            }
            
            const row = rows[currentRowIndex];
            let cells = row.querySelectorAll("td, th");
            let cell = cells[colIndex - 1];
            
            if (!cell) {
                console.log(`Creating new cell for column ${colIndex} at row ${currentRowIndex}`);
                while (row.querySelectorAll("td").length < 6) {
                    row.appendChild(document.createElement("td"));
                }
                cell = row.querySelectorAll("td")[colIndex - 2];
            }
            
            // Only add full content to the first block
            if (blockOffset === 0) {
                cell.innerHTML = `
                    <div class="class-block" data-class-id="${classId}" style="
                        background-color: #aad886;
                        padding: 5px;
                        border-radius: 5px;
                        text-align: center;
                        font-size: 11px;
                        font-weight: bold;">
                        ${classObj["Subject Code"]}<br>
                        ${classObj["Section"]}<br>
                        <span style="font-size: 10px; font-weight: normal;">
                            ${formatTime(timeInfo.startTime)}-${formatTime(timeInfo.endTime)}
                        </span><br>
                        <span style="font-size: 9px; font-weight: normal;">
                            ${classObj["Room"]}
                        </span>
                    </div>
                `;
                cell.style.backgroundColor = "#aad886";
                cell.setAttribute("rowspan", blocksNeeded);
                cell.setAttribute("data-class-id", classId);
            } else {
                // Remove subsequent cells (they're covered by rowspan)
                if (cell && cell.tagName === 'TD') {
                    cell.remove();
                }
            }
        }
    });
}

function updateCourseloadDisplay() {
    const container = document.querySelector(".rounded-text-body");
    
    // Clear existing entries (keep the header and ADD button)
    const entries = container.querySelectorAll(".rounded-text-entry");
    entries.forEach(entry => entry.remove());
    
    // Add each class to the display
    addedClasses.forEach(classInfo => {
        const wrapper = document.createElement("div");
        wrapper.className = "rounded-text-entry";
        wrapper.setAttribute("data-class-id", classInfo.id);
        
        wrapper.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="flex: 1;">
                    <b>${classInfo.data["Subject Code"]} - ${classInfo.data["Section"]}</b><br>
                    <span style="font-size: 10px;">${classInfo.data["Time"]}</span><br>
                    <span style="font-size: 10px;">${classInfo.data["Room"]}</span>
                </div>
                <button onclick="removeClass('${classInfo.id}')" style="
                    background-color: #ff6b6b;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 12px;">
                    Remove
                </button>
            </div>
        `;
        
        container.appendChild(wrapper);
    });
}

function removeClass(classId) {
    console.log("Removing class:", classId);
    
    // Remove from tracking array
    addedClasses = addedClasses.filter(c => c.id !== classId);
    
    // Remove from schedule table (all cells with this class)
    const cells = document.querySelectorAll(`td[data-class-id="${classId}"]`);
    cells.forEach(cell => {
        const rowspan = cell.getAttribute("rowspan");
        const rowspanNum = parseInt(rowspan) || 1;
        
        // Get the row this cell is in
        const row = cell.parentElement;
        const rowIndex = Array.from(row.parentElement.children).indexOf(row);
        const cellIndex = Array.from(row.children).indexOf(cell);
        
        // Clear the cell
        cell.innerHTML = "";
        cell.style.backgroundColor = "";
        cell.removeAttribute("rowspan");
        cell.removeAttribute("data-class-id");
        
        // Re-add cells that were covered by rowspan
        for (let i = 1; i < rowspanNum; i++) {
            const nextRow = row.parentElement.children[rowIndex + i];
            if (nextRow) {
                const newCell = document.createElement("td");
                // Insert at the same column position
                if (cellIndex < nextRow.children.length) {
                    nextRow.insertBefore(newCell, nextRow.children[cellIndex]);
                } else {
                    nextRow.appendChild(newCell);
                }
            }
        }
    });
    
    // Remove class blocks (the divs inside cells)
    const blocks = document.querySelectorAll(`.class-block[data-class-id="${classId}"]`);
    blocks.forEach(block => {
        block.parentElement.innerHTML = "";
        block.parentElement.style.backgroundColor = "";
    });
    
    // Update the display
    updateCourseloadDisplay();
    
    // Optionally notify the backend
    fetch("/remove_section", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ class_id: classId })
    })
    .then(res => res.json())
    .then(data => console.log("Removed from backend:", data))
    .catch(err => console.error("Error removing from backend:", err));
}