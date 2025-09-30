const express = require('express');
const router = express.Router();
const UserCtrl = require('../controllers/UserCtrl');
const authMiddleware = require('../middlewares/auth-middleware');

router.post('/register', UserCtrl.RegisterUser);
router.post('/login', UserCtrl.LoginUser);
router.post('/forgot-password', UserCtrl.forgotPassword);
router.get('/profile', authMiddleware, UserCtrl.Profile);


module.exports = router;
