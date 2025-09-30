require('dotenv').config();
const express = require('express');
const logger = require('./utils/logger');
const connectDB = require('./config/DB');
const bodyParser = require('body-parser');
const userRoutes = require('./routes/UserRoute');
const cors = require('cors');

const PORT = process.env.PORT;

connectDB();
const app = express();
app.use(cors());

app.use(express.json());
app.use(bodyParser.urlencoded({ extended: true }));





app.get('/health', (req, res) => {
    try {
        logger.info('Health check endpoint called');
        
        const healthStatus = {
            status: 'healthy',
            timestamp: new Date().toISOString(),
            service: 'User Service',
            uptime: process.uptime()
        };
        
        logger.debug('Health check response:', healthStatus);
        res.status(200).json(healthStatus);
    } catch (error) {
        logger.error('Health check failed:', error);
        res.status(500).json({
            status: 'error',
            message: 'Health check failed',
            timestamp: new Date().toISOString()
        });
    }
});

// Routes
app.use('/api/users', userRoutes);

app.listen(PORT, () => {
    logger.info(`User Service running on port ${PORT}`);
});

process.on('uncaughtException', (error) => {
    logger.error('Uncaught Exception:', error);
    process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
    logger.error('Unhandled Rejection at:', promise, 'reason:', reason);
    process.exit(1);
});