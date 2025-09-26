const nodemailer = require("nodemailer");
const logger = require("../utils/Logger");

const transporter = nodemailer.createTransport({
  host: process.env.MAIL_HOST,
  port: process.env.MAIL_PORT,
  secure: false,
  auth: {
    user: process.env.MAIL_USER,
    pass: process.env.MAIL_PASS,
  },
});

exports.sendMail = async (req, res) => {
  logger.info('Mail service endpoint hit');
  
  const { to, subject, text, html } = req.body;

  if (!to || !subject || (!text && !html)) {
    logger.warn('Missing email details:', { to, subject });
    return res.status(400).json({ 
      success: false,
      status: 'error',
      message: "Missing email details" 
    });
  }

  try {
    logger.debug('Attempting to send email', { to, subject });
    
    await transporter.sendMail({
      from: `"MyApp" <${process.env.MAIL_USER}>`,
      to,
      subject,
      text,
      html,
    });

    logger.info('Email sent successfully', { to, subject });
    res.status(200).json({ 
      success: true,
      status: 'success',
      message: "Email sent successfully" 
    });
  } catch (err) {
    logger.error('Failed to send email:', { 
      error: err.message,
      stack: err.stack,
      to,
      subject 
    });
    
    res.status(500).json({ 
      success: false,
      status: 'error',
      message: "Failed to send email", 
      error: err.message 
    });
  }
};