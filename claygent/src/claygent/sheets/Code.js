// Configuration
const API_BASE_URL = 'https://0f6a-79-148-212-9.ngrok-free.app';

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
    'employees': 'Employee names'  // This is an output field
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

  for (let row = 1; row < data.length; row++) {
    processRow(sheet, headers, data[row], row + 1);
  }

  Logger.log('Finished processing all rows');
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

  // Process LinkedIn scraper
  const linkedInUrlCol = headers.indexOf(FIELD_MAPPING.linkedin_scraper.linkedin_url);
  if (linkedInUrlCol !== -1) {
    Logger.log('Calling LinkedIn scraper API');
    const result = callApi('linkedin_scraper', linkedInInputs);
    Logger.log(`LinkedIn scraper result: ${JSON.stringify(result)}`);
    const cell = sheet.getRange(rowIndex, linkedInUrlCol + 1);
    const stringifiedResult = JSON.stringify(result);
    Logger.log(`Attempting to write "${stringifiedResult}" to cell (${rowIndex}, ${linkedInUrlCol + 1})`);
    cell.setValue(stringifiedResult);
    Logger.log(`Cell value after setting: ${cell.getValue()}`);
    SpreadsheetApp.flush();
    Logger.log(`Updated LinkedIn data in cell (${rowIndex}, ${linkedInUrlCol + 1}): ${stringifiedResult}`);
  } else {
    Logger.log(`LinkedIn URL column not found for row ${rowIndex}`);
  }

  // Process Employee scraper
  const employeesCol = headers.indexOf(FIELD_MAPPING.employee_scraper.employees);
  if (employeesCol !== -1) {
    Logger.log('Calling Employee scraper API');
    const result = callApi('employee_scraper', employeeInputs);
    Logger.log(`Employee scraper result: ${JSON.stringify(result)}`);
    const cell = sheet.getRange(rowIndex, employeesCol + 1);
    const stringifiedResult = JSON.stringify(result);
    Logger.log(`Attempting to write "${stringifiedResult}" to cell (${rowIndex}, ${employeesCol + 1})`);
    cell.setValue(stringifiedResult);
    Logger.log(`Cell value after setting: ${cell.getValue()}`);
    SpreadsheetApp.flush();
    Logger.log(`Updated Employees data in cell (${rowIndex}, ${employeesCol + 1}): ${stringifiedResult}`);
  } else {
    Logger.log(`Employees column not found for row ${rowIndex}`);
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
      return JSON.parse(responseText);
    } else {
      Logger.log(`API returned error code ${responseCode}: ${responseText}`);
      return null;
    }
  } catch (error) {
    Logger.log(`API Error: ${error.toString()}`);
    return null;
  }
}