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
    // Validate request body exists (guard against redirects that drop the body)
    if (!e || !e.postData || !e.postData.contents) {
      Logger.log('doPost called with missing postData or empty body. e=' + JSON.stringify(e));
      return ContentService.createTextOutput(JSON.stringify({
        success: false,
        error: 'Missing request body (postData). Ensure you POST JSON with Content-Type: application/json and follow redirects correctly.'
      })).setMimeType(ContentService.MimeType.JSON);
    }

    // Parse JSON payload
    var data = JSON.parse(e.postData.contents);

    // Secret check (recommended)
    var expected = PropertiesService.getScriptProperties().getProperty('WEBHOOK_SECRET') || '';
    var provided = data.secret || '';
    if (!expected || provided !== expected) {
      Logger.log('Unauthorized request: secret mismatch. Provided=' + provided);
      return ContentService.createTextOutput(JSON.stringify({
        success: false,
        error: 'Unauthorized: invalid secret'
      })).setMimeType(ContentService.MimeType.JSON);
    }

    // Validate required fields
    if (!data.to || !data.subject || !data.htmlBody) {
      return ContentService.createTextOutput(JSON.stringify({
        success: false,
        error: 'Missing required fields: to, subject, htmlBody'
      })).setMimeType(ContentService.MimeType.JSON);
    }

    // Prepare email options
    var emailOptions = {
      htmlBody: data.htmlBody,
      name: data.fromName || 'AI BI Reports System'
    };

    // Download attachments if provided (attachments must be publicly accessible URLs)
    if (Array.isArray(data.attachments) && data.attachments.length) {
      var blobs = [];
      for (var i = 0; i < data.attachments.length; i++) {
        try {
          var url = data.attachments[i];
          if (!url) continue;
          var resp = UrlFetchApp.fetch(url, { muteHttpExceptions: true, followRedirects: true });
          if (resp && resp.getResponseCode && resp.getResponseCode() === 200) {
            var blob = resp.getBlob();
            // Provide a filename if possible
            var contentType = blob.getContentType();
            var filename = 'attachment_' + (i + 1);
            if (contentType) {
              if (contentType.indexOf('pdf') !== -1) filename += '.pdf';
              else if (contentType.indexOf('png') !== -1) filename += '.png';
              else if (contentType.indexOf('jpeg') !== -1 || contentType.indexOf('jpg') !== -1) filename += '.jpg';
            }
            try { blob.setName(filename); } catch (setNameErr) { /* ignore */ }
            blobs.push(blob);
          } else {
            Logger.log('Attachment fetch non-200 for URL: ' + url + ' code=' + (resp && resp.getResponseCode()));
          }
        } catch (fetchErr) {
          Logger.log('Attachment fetch error for URL: ' + data.attachments[i] + ' error=' + fetchErr.toString());
        }
      }
      if (blobs.length) {
        emailOptions.attachments = blobs;
      }
    }

    // Send email using GmailApp
    GmailApp.sendEmail(
      data.to,
      data.subject,
      'Please view this email in an HTML-capable email client.',
      emailOptions
    );

    // Log success
    Logger.log('Email sent successfully to: ' + data.to);

    // Return success response
    return ContentService.createTextOutput(JSON.stringify({
      success: true,
      message: 'Email sent successfully'
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    // Log error
    Logger.log('doPost error: ' + error.toString());

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
