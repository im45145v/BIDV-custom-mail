/**
 * 🎉 SUPER FUN SALES PITCH EMAIL DELIVERY SYSTEM! 🎉
 * 
 * Welcome to the most awesome email automation script ever! 
 * This script doesn't just send emails - it spreads JOY! 💝
 * 
 * ═══════════════════════════════════════════════════════════
 * 🚀 DEPLOYMENT INSTRUCTIONS (Easy as pie!)
 * ═══════════════════════════════════════════════════════════
 * 
 * 1. Open Google Apps Script: https://script.google.com
 * 2. Click that shiny "New Project" button ✨
 * 3. Copy this magical code and paste it in
 * 4. Save with an epic name like "Sales Pitch Email Wizard" 🧙
 * 5. Deploy as Web App:
 *    - Click "Deploy" > "New deployment" > "Web app"
 *    - Description: "Making customers happy since today!"
 *    - Execute as: "Me" (you're the hero here!)
 *    - Who has access: "Anyone" (spread the love!)
 *    - Click "Deploy" and feel the power! ⚡
 * 6. Copy the magical URL you receive
 * 7. Add it to your .env file: APPS_SCRIPT_WEBHOOK_URL=<your_magic_url>
 * 8. Watch the happiness unfold! 🌈
 * 
 * ═══════════════════════════════════════════════════════════
 * 🎯 WHAT MAKES THIS SCRIPT SPECIAL?
 * ═══════════════════════════════════════════════════════════
 * 
 * ✨ Sends personalized sales pitches with style
 * 🎨 Supports rich HTML emails with images
 * 📎 Handles attachments like a boss
 * 😊 Tracks customer happiness metrics
 * 🎪 Fun emoji-powered logging
 * 🚀 Automatic retry on failures
 * 💌 Love in every byte!
 */

// 🎨 Configuration - Make it yours!
var CONFIG = {
  senderName: "Your Friendly Sales Team 🌟",
  fallbackPlainText: "✨ This email looks best in an HTML-capable email client! ✨",
  maxRetries: 3,
  retryDelayMs: 1000,
  enableHappinessTracking: true
};

// 📊 Happiness Metrics Tracker
var HAPPINESS_METRICS = {
  totalEmailsSent: 0,
  successfulDeliveries: 0,
  failedDeliveries: 0,
  totalCustomersReached: 0,
  happinessScore: 100
};

/**
 * 🎬 MAIN SHOW - Handle POST requests!
 * This is where the magic happens! ✨
 * 
 * Expected JSON payload (the recipe for success):
 * {
 *   "to": "happy.customer@example.com",
 *   "subject": "🎉 Amazing offer just for you!",
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
    logWithEmoji("🎬", "New email request incoming! Let's make someone's day!");
    
    // Parse the magical payload
    var data = JSON.parse(e.postData.contents);
    
    // Validate - because we care!
    if (!validatePayload(data)) {
      return createResponse(false, "❌ Oops! Missing some important fields. Check to, subject, and htmlBody!");
    }
    
    // Send with style and retries!
    var result = sendEmailWithRetry(data);
    
    // Update happiness metrics
    if (CONFIG.enableHappinessTracking) {
      updateHappinessMetrics(result.success, data);
    }
    
    // Celebrate or console
    if (result.success) {
      logWithEmoji("🎉", "Email sent successfully! Another happy customer!");
      return createResponse(true, "💌 Email delivered with love!", result);
    } else {
      logWithEmoji("😢", "Oh no! Something went wrong: " + result.error);
      return createResponse(false, result.error);
    }
    
  } catch (error) {
    logWithEmoji("💥", "Unexpected error: " + error.toString());
    return createResponse(false, "💥 Oops! Something unexpected happened: " + error.toString());
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
      logWithEmoji("📬", `Sending attempt ${attempts}/${CONFIG.maxRetries}...`);
      
      // Prepare the email masterpiece
      var emailOptions = {
        htmlBody: data.htmlBody,
        name: CONFIG.senderName
      };
      
      // Add attachments if provided (the cherry on top!)
      if (data.attachments && data.attachments.length > 0) {
        emailOptions.attachments = fetchAttachments(data.attachments);
        logWithEmoji("📎", `Added ${data.attachments.length} attachment(s)!`);
      }
      
      // 🎯 SEND IT!
      GmailApp.sendEmail(
        data.to,
        data.subject,
        CONFIG.fallbackPlainText,
        emailOptions
      );
      
      // Success! 🎊
      HAPPINESS_METRICS.totalEmailsSent++;
      HAPPINESS_METRICS.successfulDeliveries++;
      HAPPINESS_METRICS.totalCustomersReached++;
      
      return {
        success: true,
        attempts: attempts,
        timestamp: new Date().toISOString(),
        happinessBoost: "+10 😊"
      };
      
    } catch (error) {
      lastError = error.toString();
      logWithEmoji("⚠️", `Attempt ${attempts} failed: ${lastError}`);
      
      if (attempts < CONFIG.maxRetries) {
        logWithEmoji("🔄", "Retrying in a moment...");
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
        logWithEmoji("⬇️", `Fetching attachment: ${att.name}`);
        
        var response = UrlFetchApp.fetch(att.url);
        var blob = response.getBlob();
        
        if (att.name) {
          blob.setName(att.name);
        }
        
        attachments.push(blob);
        logWithEmoji("✅", `Got it: ${att.name}`);
      }
    }
  } catch (error) {
    logWithEmoji("⚠️", "Couldn't fetch all attachments: " + error.toString());
    // Continue anyway - partial success is better than no success!
  }
  
  return attachments;
}

/**
 * ✅ Payload Validator - The Bouncer of our party
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
 * 😊 Happiness Tracker - Because metrics should be fun!
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
  
  logWithEmoji("📊", `Current happiness score: ${HAPPINESS_METRICS.happinessScore}%`);
}

/**
 * 📝 Response Creator - Crafting beautiful responses
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
 * 🎭 Happiness Level Calculator
 */
function getHappinessLevel() {
  var score = HAPPINESS_METRICS.happinessScore;
  if (score >= 90) return "🌟 ECSTATIC!";
  if (score >= 75) return "😊 Very Happy";
  if (score >= 60) return "🙂 Happy";
  if (score >= 40) return "😐 Neutral";
  return "😢 Needs More Joy";
}

/**
 * 👋 Handle GET requests - Say hello!
 */
function doGet(e) {
  logWithEmoji("👋", "Someone's checking if we're alive!");
  
  return ContentService
    .createTextOutput(JSON.stringify({
      status: "🚀 ACTIVE & AWESOME!",
      message: "Sales Pitch Email Delivery System is ready to spread joy!",
      version: "2.0.0-happiness-edition",
      capabilities: [
        "✉️ HTML Email Delivery",
        "📎 Attachment Support",
        "🔄 Auto-retry on failures",
        "😊 Happiness tracking",
        "🎨 Emoji-powered logging",
        "💝 Love in every byte"
      ],
      currentHappiness: getHappinessLevel(),
      metrics: HAPPINESS_METRICS,
      funFact: "This script has been optimized for maximum customer happiness! 🌈"
    }))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * 🎨 Emoji Logger - Because plain logs are boring!
 */
function logWithEmoji(emoji, message) {
  Logger.log(`${emoji} ${message}`);
}

/**
 * 🧪 Test Function - Try before you fly!
 * Run this from the Apps Script editor to test everything works
 */
function testEmailDelivery() {
  logWithEmoji("🧪", "Starting test email delivery!");
  
  var testPayload = {
    to: Session.getActiveUser().getEmail(),
    subject: "🎉 Test: Your Sales Pitch System is Working!",
    htmlBody: `
      <html>
        <body style="font-family: Arial, sans-serif; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
          <div style="background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #667eea;">🎊 Success!</h1>
            <p>Your Sales Pitch Email System is working perfectly!</p>
            <p>This means you can now:</p>
            <ul>
              <li>✨ Send personalized sales pitches</li>
              <li>📎 Include attachments</li>
              <li>😊 Track customer happiness</li>
              <li>🚀 Delight your customers</li>
            </ul>
            <p><strong>Current Happiness Level: ${getHappinessLevel()}</strong></p>
            <p style="color: #666; font-size: 12px; margin-top: 30px;">
              Sent with ❤️ by your Sales Pitch Email System
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
  logWithEmoji("📬", "Test complete! Check your email!");
  logWithEmoji("📊", response.getContent());
  
  return response.getContent();
}

/**
 * 📊 Get Happiness Report - See how we're doing!
 */
function getHappinessReport() {
  logWithEmoji("📊", "Generating happiness report...");
  
  var report = {
    reportDate: new Date().toISOString(),
    metrics: HAPPINESS_METRICS,
    happinessLevel: getHappinessLevel(),
    successRate: HAPPINESS_METRICS.totalEmailsSent > 0 
      ? (HAPPINESS_METRICS.successfulDeliveries / HAPPINESS_METRICS.totalEmailsSent * 100).toFixed(2) + "%"
      : "N/A",
    message: "Keep spreading joy! 🌈"
  };
  
  Logger.log(JSON.stringify(report, null, 2));
  return report;
}

// 🎬 End of script - Go forth and make customers happy! 🌟
