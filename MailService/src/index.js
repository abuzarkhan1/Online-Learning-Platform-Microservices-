require('dotenv').config();
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const logger = require('./utils/Logger');
const mailController = require('./controller/mail');
const PORT = process.env.PORT;



const app = express();
app.use(cors());
app.use(express.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.post('/sendmail', mailController.sendMail);


app.listen(PORT, () => {
    logger.info(`Mail Service running on port ${PORT}`);
});

app.get('/health', (req, res) => {
    res.status(200).json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        service: 'Mail Service'
    });
});
