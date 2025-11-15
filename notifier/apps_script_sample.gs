/**
 * Google Apps Script Web App for sending emails via webhook.
 * 
 * DEPLOYMENT INSTRUCTIONS:
 * 1. Open Google Apps Script: https://script.google.com
 * 2. Create a new project
 * 3. Paste this code
 * 4. Deploy as Web App:
 *    - Click "Deploy" > "New deployment"
 *    - Type: "Web app"
 *    - Execute as: "Me"
 *    - Who has access: "Anyone" (or "Anyone with Google account")
 *    - Click "Deploy"
 * 5. Copy the Web App URL
 * 6. Paste URL into .env file as APPS_SCRIPT_WEBHOOK_URL
 * 
 * PERMISSIONS:
 * - First run will request Gmail send permissions
 * - Approve the permissions to enable email sending
 */

/**
 * Handle POST requests from the Python webhook client.
 * 
 * Expected JSON payload:
 * {
 *   "to": "recipient@example.com",
 *   "subject": "Email subject",
 *   "htmlBody": "<html>...</html>",
 *   "attachments": ["https://url1.com/file.pdf"] // optional
 * }
 */
function doPost(e) {
  try {
    // Parse JSON payload
    var data = JSON.parse(e.postData.contents);
    
    // Validate required fields
    if (!data.to || !data.subject || !data.htmlBody) {
      return ContentService.createTextOutput(JSON.stringify({
        success: false,
        error: "Missing required fields: to, subject, htmlBody"
      })).setMimeType(ContentService.MimeType.JSON);
    }
    
    // Prepare email options
    var emailOptions = {
      htmlBody: data.htmlBody,
      name: "AI BI Reports System"
    };
    
    // Note: Google Apps Script doesn't support direct URL attachments
    // If you need attachments, you'd need to download them first
    // or include them as inline images in the HTML
    
    // Send email using GmailApp
    GmailApp.sendEmail(
      data.to,
      data.subject,
      "Please view this email in an HTML-capable email client.",
      emailOptions
    );
    
    // Log success
    Logger.log("Email sent successfully to: " + data.to);
    
    // Return success response
    return ContentService.createTextOutput(JSON.stringify({
      success: true,
      message: "Email sent successfully"
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    // Log error
    Logger.log("Error sending email: " + error.toString());
    
    // Return error response
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Handle GET requests (for testing).
 * Returns a simple status message.
 */
function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({
    status: "AI BI Reports Email Webhook",
    message: "POST email data to this endpoint",
    version: "1.0.0"
  })).setMimeType(ContentService.MimeType.JSON);
}

/**
 * Test function to verify the script works.
 * Run this from the Apps Script editor to test.
 */
function testEmailSending() {
  var testPayload = {
    to: Session.getActiveUser().getEmail(), // Sends to yourself
    subject: "Test Email from AI BI Reports",
    htmlBody: "<h1>Test Email</h1><p>This is a test email from the AI BI Reports system.</p>"
  };
  
  var e = {
    postData: {
      contents: JSON.stringify(testPayload)
    }
  };
  
  var response = doPost(e);
  Logger.log(response.getContent());
}
