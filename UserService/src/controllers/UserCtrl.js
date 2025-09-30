const logger = require("../utils/logger");
const User = require("../models/User");
const { validateRegistration } = require("../utils/validation");
const jwt = require("jsonwebtoken");
const crypto = require("crypto");
const axios = require("axios");



const RegisterUser = async (req, res) => {
  logger.info("Registration endpoint  hit");

  try {
    const { error } = validateRegistration(req.body);
    if (error) {
      logger.warn(
        "Validation error during registration:",
        error.details[0].message
      );
      return res.status(400).json({
        success: false,
        status: "error",
        message: error.details[0].message,
      });
    }

    const { name, email, password } = req.body;
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      logger.warn("Attempt to register with existing email:", email);
      return res.status(400).json({
        success: false,
        status: "error",
        message: "Email already in use",
      });
    }
    ``;
    const newUser = new User({ name, email, password });
    await newUser.save();
    logger.info("New user registered:", email);
    res.status(201).json({
      success: true,
      status: "success",
      message: "User registered successfully",
    });
  } catch (error) {
    logger.error("Error during user registration:", error);
    res.status(500).json({ message: "Internal server error" });
  }
};

const LoginUser = async (req, res) => {
  logger.info("Login endpoint hit");
  try {
    const { email, password } = req.body;
    const user = await User.findOne({ email });
    if (!user) {
      logger.warn("Login attempt with non-existent email:", email);
      return res.status(400).json({
        success: false,
        status: "error",
        message: "Invalid email or password",
      });
    }
    const isMatch = await user.verifyPassword(password);
    if (!isMatch) {
      logger.warn("Invalid password attempt for email:", email);
      return res.status(400).json({
        success: false,
        status: "error",
        message: "Invalid email or password",
      });
    }
    const token = jwt.sign(
      { id: user._id, email: user.email, name: user.name, role: user.role },
      process.env.JWT_SECRET,
      { expiresIn: "1h" }
    );
    logger.info("User logged in successfully:", email);
    res.status(200).json({
      success: true,
      status: "success",
      token,
    });
  } catch (error) {
    logger.error("Error during user login:", error);
    res.status(500).json({ message: "Internal server error" });
  }
};

const Profile = async (req, res) => {
  logger.info("Profile endpoint hit for user:", req.user.email);
  try {
    const user = await User.findById(req.user.id).select("-password");
    if (!user) {
      logger.warn("Profile request for non-existent user ID:", req.user.id);
      return res.status(404).json({
        success: false,
        status: "error",
        message: "User not found",
      });
    }
    res.status(200).json({
      success: true,
      status: "success",
      user,
    });
  } catch (error) {
    logger.error("Error fetching user profile:", error);
    res.status(500).json({ message: "Internal server error" });
  }
};

const forgotPassword = async (req, res) => {
  logger.info("Forgot Password endpoint hit");
  try {
    const { email } = req.body;
    const user = await User.findOne({ email });
    if (!user) {
      logger.warn("Forgot password attempt with non-existent email:", email);
      return res.status(400).json({
        success: false,
        status: "error",
        message: "Email not found",
      });
    }

    const resetToken = crypto.randomBytes(32).toString("hex");
    user.resetToken = resetToken;
    user.resetTokenExpiry = Date.now() + 3600000;
    await user.save();

      const resetLink = `http://localhost:3000/reset-password/${resetToken}`;

    await axios.post("http://localhost:3001/sendmail", {
      to: email,
      subject: "Password Reset Request",
      html: `<p>Hello ${user.name},</p>
             <p>Click <a href="${resetLink}">here</a> to reset your password. This link expires in 1 hour.</p>`
    });

    logger.info("Password reset requested for email:", email);
    res.status(200).json({
      success: true,
      status: "success",
      message: "Password reset link sent to email",
    });
  } catch (error) {
    logger.error("Error during forgot password process:", error);
    res.status(500).json({ message: "Internal server error" });
  }
};



module.exports = {
  RegisterUser,
  LoginUser,
  Profile,
  forgotPassword,
};
