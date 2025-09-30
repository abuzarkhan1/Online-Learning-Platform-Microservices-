const mongoose = require("mongoose");
const argon2 = require("argon2");

const userSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
    },
    email: {
      type: String,
      required: true,
      unique: true,
    },
    password: {
      type: String,
      required: true,
    },
    role: {
      type: String,
      enum: ["student", "instructor"],
      default: "student",
    },
  },
  { timestamps: true }
);

userSchema.pre("save", async function (next) {
  if (this.isModified("password")) {
    try {
      this.password = await argon2.hash(this.password);
    } catch (err) {
      return next(err);
    }
  }
  next();
});

userSchema.methods.verifyPassword = async function (password) {
  try {
    return await argon2.verify(this.password, password);
  } catch (err) {
    throw new Error("Password comparison failed");
  }
};

const User = mongoose.model("User", userSchema);
module.exports = User;
