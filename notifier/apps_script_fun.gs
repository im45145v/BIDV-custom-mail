/**
 * SUPER SALES PITCH EMAIL DELIVERY SYSTEM
 * 
 * Welcome to the email automation script.
 * 
 * DEPLOYMENT INSTRUCTIONS
 * ==================================
 * 
 * 1. Open Google Apps Script: https://script.google.com
 * 2. Click "New Project"
 * 3. Copy this code and paste it in
 * 4. Save with a name like "Sales Pitch Email Wizard"
 * 5. Deploy as Web App:
 *    - Click "Deploy" > "New deployment" > "Web app"
 *    - Description: "Sales Pitch Email Webhook"
 *    - Execute as: "Me"
 *    - Who has access: "Anyone"
 *    - Click "Deploy"
 * 6. Copy the magical URL you receive
 * 7. Add it to your .env file: APPS_SCRIPT_WEBHOOK_URL=<your_magic_url>
 * 8. Watch the system run
 * 
 * WHAT MAKES THIS SCRIPT SPECIAL
 * ==================================
 * 
 * - Sends personalized sales pitches
 * - Supports rich HTML emails with images
 * - Handles attachments
 * - Tracks customer happiness metrics
 * - Automatic retry on failures
 */

// 🎨 Configuration - Make it yours!
var CONFIG = {
  senderName: "Your Friendly Sales Team",
  fallbackPlainText: "This email looks best in an HTML-capable email client.",
  maxRetries: 3,
  retryDelayMs: 1000,
  enableHappinessTracking: true
};

// Happiness Metrics Tracker
var HAPPINESS_METRICS = {
  totalEmailsSent: 0,
  successfulDeliveries: 0,
  failedDeliveries: 0,
  totalCustomersReached: 0,
  happinessScore: 100
};

/**
 * MAIN SHOW - Handle POST requests
 * This is where the main handler lives.
 * 
 * Expected JSON payload (the recipe for success):
 * {
 *   "to": "happy.customer@example.com",
 *   "subject": "Amazing offer just for you!",
 *   "htmlBody": "<html>Beautiful email content here</html>",
 *   "attachments": [  // Optional but awesome!
 *     {
 *       "name": "special_offer.pdf",
 *       "url": "https://example.com/file.pdf",
 *       "mimeType": "application/pdf"
 *     }
 *   ],
 *   "customerName": "John Doe",  // Optional
 *   "segment": "vip"  // Optional - helps with happiness tracking
 * }
 */
function doPost(e) {
  try {
    logWithEmoji("", "New email request incoming. Processing email request.");
    
    // Parse the magical payload
    var data = JSON.parse(e.postData.contents);
    
    // Validate - because we care!
    if (!validatePayload(data)) {
      return createResponse(false, "Missing required fields: to, subject, and htmlBody.");
    }
    
    // Send with style and retries!
    var result = sendEmailWithRetry(data);
    
    // Update happiness metrics
    if (CONFIG.enableHappinessTracking) {
      updateHappinessMetrics(result.success, data);
    }
    
    // Celebrate or console
    if (result.success) {
      logWithEmoji("", "Email sent successfully.");
      return createResponse(true, "Email delivered.", result);
    } else {
      logWithEmoji("", "Email sending failed: " + result.error);
      return createResponse(false, result.error);
    }
    
  } catch (error) {
    logWithEmoji("", "Unexpected error: " + error.toString());
    return createResponse(false, "Unexpected error: " + error.toString());
  }
}

/**
 * 📧 The Email Sender Extraordinaire!
 * Sends emails with retries and happiness sprinkled in
 */
function sendEmailWithRetry(data) {
  var attempts = 0;
  var lastError = null;
  
  while (attempts < CONFIG.maxRetries) {
    try {
      attempts++;
      logWithEmoji("", `Sending attempt ${attempts}/${CONFIG.maxRetries}...`);
      
      // Prepare the email masterpiece
      var emailOptions = {
        htmlBody: data.htmlBody,
        name: CONFIG.senderName
      };
      
      // Add attachments if provided (the cherry on top!)
      if (data.attachments && data.attachments.length > 0) {
        emailOptions.attachments = fetchAttachments(data.attachments);
        logWithEmoji("", `Added ${data.attachments.length} attachment(s)`);
      }
      
      // SEND IT
      GmailApp.sendEmail(
        data.to,
        data.subject,
        CONFIG.fallbackPlainText,
        emailOptions
      );
      
      // Success
      HAPPINESS_METRICS.totalEmailsSent++;
      HAPPINESS_METRICS.successfulDeliveries++;
      HAPPINESS_METRICS.totalCustomersReached++;
      
      return {
        success: true,
        attempts: attempts,
        timestamp: new Date().toISOString(),
        happinessBoost: "+10"
      };
      
    } catch (error) {
      lastError = error.toString();
      logWithEmoji("", `Attempt ${attempts} failed: ${lastError}`);
      
      if (attempts < CONFIG.maxRetries) {
        logWithEmoji("", "Retrying in a moment...");
        Utilities.sleep(CONFIG.retryDelayMs);
      }
    }
  }
  
  // All attempts failed 😢
  HAPPINESS_METRICS.failedDeliveries++;
  HAPPINESS_METRICS.happinessScore = Math.max(0, HAPPINESS_METRICS.happinessScore - 5);
  
  return {
    success: false,
    error: lastError,
    attempts: attempts
  };
}

/**
 * 📎 Attachment Fetcher Supreme
 * Downloads attachments from URLs (because we're fancy!)
 */
function fetchAttachments(attachmentsList) {
  var attachments = [];
  
  try {
    for (var i = 0; i < attachmentsList.length; i++) {
      var att = attachmentsList[i];
      
      if (att.url) {
        logWithEmoji("", `Fetching attachment: ${att.name}`);
        
        var response = UrlFetchApp.fetch(att.url);
        var blob = response.getBlob();
        
        if (att.name) {
          blob.setName(att.name);
        }
        
        attachments.push(blob);
        logWithEmoji("", `Fetched attachment: ${att.name}`);
      }
    }
  } catch (error) {
    logWithEmoji("", "Couldn't fetch all attachments: " + error.toString());
    // Continue anyway - partial success is better than no success!
  }
  
  return attachments;
}

/**
 * Payload Validator
 */
function validatePayload(data) {
  if (!data.to || !data.subject || !data.htmlBody) {
    return false;
  }
  
  // Email format check (basic)
  var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(data.to)) {
    return false;
  }
  
  return true;
}

/**
 * Happiness Tracker
 */
function updateHappinessMetrics(success, data) {
  if (success) {
    // Boost happiness based on customer segment
    if (data.segment === 'vip') {
      HAPPINESS_METRICS.happinessScore = Math.min(100, HAPPINESS_METRICS.happinessScore + 15);
    } else if (data.segment === 'at_risk') {
      HAPPINESS_METRICS.happinessScore = Math.min(100, HAPPINESS_METRICS.happinessScore + 20); // Extra happiness for winning back customers!
    } else {
      HAPPINESS_METRICS.happinessScore = Math.min(100, HAPPINESS_METRICS.happinessScore + 10);
    }
  }
  
  logWithEmoji("", `Current happiness score: ${HAPPINESS_METRICS.happinessScore}%`);
}

/**
 * Response Creator
 */
function createResponse(success, message, data) {
  var response = {
    success: success,
    message: message,
    timestamp: new Date().toISOString(),
    happinessLevel: getHappinessLevel()
  };
  
  if (data) {
    response.data = data;
  }
  
  if (CONFIG.enableHappinessTracking) {
    response.metrics = HAPPINESS_METRICS;
  }
  
  return ContentService
    .createTextOutput(JSON.stringify(response))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Happiness Level Calculator
 */
function getHappinessLevel() {
  var score = HAPPINESS_METRICS.happinessScore;
  if (score >= 90) return "ECSTATIC";
  if (score >= 75) return "Very Happy";
  if (score >= 60) return "Happy";
  if (score >= 40) return "Neutral";
  return "Needs More Joy";
}

/**
 * Handle GET requests - Health check
 */
function doGet(e) {
  logWithEmoji("", "Health check requested");
  
  return ContentService
    .createTextOutput(JSON.stringify({
      status: "ACTIVE",
      message: "Sales Pitch Email Delivery System is ready.",
      version: "2.0.0",
      capabilities: [
        "HTML Email Delivery",
        "Attachment Support",
        "Auto-retry on failures",
        "Happiness tracking",
        "Logging"
      ],
      currentHappiness: getHappinessLevel(),
      metrics: HAPPINESS_METRICS,
      funFact: "This script is optimized for customer delivery."
    }))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Logger helper
 */
function logWithEmoji(emoji, message) {
  // Keep signature for compatibility. Logs will not include emoji characters.
  Logger.log(message);
}

/**
 * Test Function - Try before you fly
 * Run this from the Apps Script editor to test everything works
 */
function testEmailDelivery() {
  logWithEmoji("", "Starting test email delivery");
  
  var testPayload = {
    to: Session.getActiveUser().getEmail(),
    subject: "Test: Your Sales Pitch System is Working",
    htmlBody: `
      <html>
        <body style="font-family: Arial, sans-serif; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
          <div style="background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #667eea;">Success</h1>
            <p>Your Sales Pitch Email System is working perfectly!</p>
            <p>This means you can now:</p>
            <ul>
              <li>Send personalized sales pitches</li>
              <li>Include attachments</li>
              <li>Track customer happiness</li>
              <li>Deliver emails to customers</li>
            </ul>
            <p><strong>Current Happiness Level: ${getHappinessLevel()}</strong></p>
            <p style="color: #666; font-size: 12px; margin-top: 30px;">
              Sent by your Sales Pitch Email System
            </p>
          </div>
        </body>
      </html>
    `,
    customerName: "Test User",
    segment: "vip"
  };
  
  var e = {
    postData: {
      contents: JSON.stringify(testPayload)
    }
  };
  
  var response = doPost(e);
  logWithEmoji("", "Test complete. Check your email if accessible.");
  logWithEmoji("", response.getContent());
  
  return response.getContent();
}

/**
 * Get Happiness Report
 */
function getHappinessReport() {
  logWithEmoji("", "Generating happiness report...");
  
  var report = {
    reportDate: new Date().toISOString(),
    metrics: HAPPINESS_METRICS,
    happinessLevel: getHappinessLevel(),
    successRate: HAPPINESS_METRICS.totalEmailsSent > 0 
      ? (HAPPINESS_METRICS.successfulDeliveries / HAPPINESS_METRICS.totalEmailsSent * 100).toFixed(2) + "%"
      : "N/A",
    message: "Keep improving delivery"
  };
  
  Logger.log(JSON.stringify(report, null, 2));
  return report;
}

// End of script
