const joi = require('joi');

const validateRegistration = (data) => {
    const schema = joi.object({
        name: joi.string().min(3).max(30).required(),
        email: joi.string().email().required(),
        password: joi.string().min(6).required()
    });
    return schema.validate(data);
}

module.exports = {
    validateRegistration,
};