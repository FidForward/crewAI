// Configuration
const API_BASE_URL = 'https://7c82-5-225-69-121.ngrok-free.app';

// Add a menu item to run the script
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Custom Menu')
    .addItem('Process Sheet', 'processSheet')
    .addToUi();
}

// Mapping of API fields to sheet column headers
const FIELD_MAPPING = {
  'linkedin_scraper': {
    'full_name': 'Full Name',
    'company': 'Company',
    'email': 'Email',
    'linkedin_url': 'LinkedIn URL'  // This is an output field
  },
  'employee_scraper': {
    'company': 'Company',
    'company_url': 'Company URL',
    'ceo_name': 'Full Name',
    'country': 'Country', 
    'employees': 'Employee names'  // This is an output field
  },
  'language_detector': {
    'full_name': 'Full Name',
    'company': 'Company',
    'email': 'Email',
    'preferred_language': 'Preferred Language'  // This is an output field
  },
  'hr_detector': {
    'ceo_name': 'Full Name',
    'company': 'Company',
    'company_url': 'Company URL',
    'hr_comment': 'HR Comment'  // This is an output field
  }
};

function processSheet() {
  Logger.log('Starting processSheet function');
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('data');
  if (!sheet) {
    Logger.log('Sheet "data" not found');
    throw new Error('Sheet "data" not found');
  }

  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  const data = sheet.getDataRange().getValues();

  Logger.log(`Processing ${data.length - 1} rows`);

  try {
    for (let row = 1; row < data.length; row++) {
      processRow(sheet, headers, data[row], row + 1);
    }
    Logger.log('Finished processing all rows');
  } catch (error) {
    Logger.log(`Error: ${error.toString()}`);
    SpreadsheetApp.getUi().alert(`Error: ${error.toString()}`);
    throw error;
  }
}

function processRow(sheet, headers, rowData, rowIndex) {
  Logger.log(`Processing row ${rowIndex}`);
  const linkedInInputs = {};
  const employeeInputs = {};

  // Populate input data
  for (const [field, header] of Object.entries(FIELD_MAPPING.linkedin_scraper)) {
    const colIndex = headers.indexOf(header);
    if (colIndex !== -1 && field !== 'linkedin_url') {
      linkedInInputs[field] = rowData[colIndex];
    }
  }

  for (const [field, header] of Object.entries(FIELD_MAPPING.employee_scraper)) {
    const colIndex = headers.indexOf(header);
    if (colIndex !== -1 && field !== 'employees') {
      employeeInputs[field] = rowData[colIndex];
    }
  }

  try {
    // Process LinkedIn scraper (disabled for now)
    /*
    const linkedInUrlCol = headers.indexOf(FIELD_MAPPING.linkedin_scraper.linkedin_url);
    if (linkedInUrlCol !== -1) {
      const cell = sheet.getRange(rowIndex, linkedInUrlCol + 1);
      if (cell.isBlank()) {
        Logger.log('Calling LinkedIn scraper API');
        const result = callApi('linkedin_scraper', linkedInInputs);
        Logger.log(`LinkedIn scraper result: ${result}`);
        Logger.log(`Attempting to write "${result}" to cell (${rowIndex}, ${linkedInUrlCol + 1})`);
        cell.setValue(result);
        Logger.log(`Cell value after setting: ${cell.getValue()}`);
        SpreadsheetApp.flush();
        Logger.log(`Updated LinkedIn data in cell (${rowIndex}, ${linkedInUrlCol + 1}): ${result}`);
      } else {
        Logger.log(`LinkedIn URL cell (${rowIndex}, ${linkedInUrlCol + 1}) is already filled. Skipping.`);
      }
    } else {
      Logger.log(`LinkedIn URL column not found for row ${rowIndex}`);
    }
    */

    // Process Employee scraper
    const employeesCol = headers.indexOf(FIELD_MAPPING.employee_scraper.employees);
    if (employeesCol !== -1) {
      const cell = sheet.getRange(rowIndex, employeesCol + 1);
      if (cell.isBlank()) {
        Logger.log('Calling Employee scraper API');
        const result = callApi('employee_scraper', employeeInputs);
        Logger.log(`Employee scraper result: ${result}`);
        Logger.log(`Attempting to write "${result}" to cell (${rowIndex}, ${employeesCol + 1})`);
        cell.setValue(result);
        Logger.log(`Cell value after setting: ${cell.getValue()}`);
        SpreadsheetApp.flush();
        Logger.log(`Updated Employees data in cell (${rowIndex}, ${employeesCol + 1}): ${result}`);
      } else {
        Logger.log(`Employees cell (${rowIndex}, ${employeesCol + 1}) is already filled. Skipping.`);
      }
    } else {
      Logger.log(`Employees column not found for row ${rowIndex}`);
    }

    // Process Language detector
    const languageCol = headers.indexOf(FIELD_MAPPING.language_detector.preferred_language);
    if (languageCol !== -1) {
      const cell = sheet.getRange(rowIndex, languageCol + 1);
      if (cell.isBlank()) {
        Logger.log('Calling Language detector API');
        const result = callApi('language_detector', {
          full_name: linkedInInputs.full_name,
          company: linkedInInputs.company,
          email: linkedInInputs.email
        });
        Logger.log(`Language detector result: ${result}`);
        Logger.log(`Attempting to write "${result}" to cell (${rowIndex}, ${languageCol + 1})`);
        cell.setValue(result);
        Logger.log(`Cell value after setting: ${cell.getValue()}`);
        SpreadsheetApp.flush();
        Logger.log(`Updated Language data in cell (${rowIndex}, ${languageCol + 1}): ${result}`);
      } else {
        Logger.log(`Preferred Language cell (${rowIndex}, ${languageCol + 1}) is already filled. Skipping.`);
      }
    } else {
      Logger.log(`Preferred Language column not found for row ${rowIndex}`);
    }

    // Process HR detector
    // const hrCommentCol = headers.indexOf(FIELD_MAPPING.hr_detector.hr_comment);
    // if (hrCommentCol !== -1) {
    //   const cell = sheet.getRange(rowIndex, hrCommentCol + 1);
    //   if (cell.isBlank()) {
    //     Logger.log('Calling HR detector API');
    //     const result = callApi('hr_detector', {
    //       ceo_name: employeeInputs.ceo_name,
    //       company: employeeInputs.company,
    //       company_url: employeeInputs.company_url
    //     });
    //     Logger.log(`HR detector result: ${result}`);
    //     Logger.log(`Attempting to write "${result}" to cell (${rowIndex}, ${hrCommentCol + 1})`);
    //     cell.setValue(result);
    //     Logger.log(`Cell value after setting: ${cell.getValue()}`);
    //     SpreadsheetApp.flush();
    //     Logger.log(`Updated HR Comment data in cell (${rowIndex}, ${hrCommentCol + 1}): ${result}`);
    //   } else {
    //     Logger.log(`HR Comment cell (${rowIndex}, ${hrCommentCol + 1}) is already filled. Skipping.`);
    //   }
    // } else {
    //   Logger.log(`HR Comment column not found for row ${rowIndex}`);
    // }
  } catch (error) {
    Logger.log(`Error processing row ${rowIndex}: ${error.toString()}`);
    throw new Error(`Processing stopped at row ${rowIndex}: ${error.toString()}`);
  }
}

function callApi(endpoint, data) {
  Logger.log(`Calling API: ${endpoint} with data: ${JSON.stringify(data)}`);
  const options = {
    'method': 'post',
    'contentType': 'application/json',
    'payload': JSON.stringify(data),
    'muteHttpExceptions': true
  };

  try {
    const response = UrlFetchApp.fetch(`${API_BASE_URL}/${endpoint}`, options);
    const responseCode = response.getResponseCode();
    const responseText = response.getContentText();
    Logger.log(`API Response Code: ${responseCode}`);
    Logger.log(`API Response: ${responseText}`);
    
    if (responseCode >= 200 && responseCode < 300) {
      return responseText.trim();  // Remove any leading/trailing whitespace
    } else {
      throw new Error(`API returned error code ${responseCode}: ${responseText}`);
    }
  } catch (error) {
    Logger.log(`API Error: ${error.toString()}`);
    throw new Error(`API is not available: ${error.toString()}`);
  }
}
