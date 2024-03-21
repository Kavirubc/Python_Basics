const nodemailer = require('nodemailer');
//onst qrcode = require('qrcode');
const fs = require('fs');
const csvWriter = require('csv-write-stream');
const csvParser = require('csv-parser');

// Function to generate a unique token
function generateUniqueToken() {
    return Math.random().toString(36).substring(2, 18);
}

// Function to generate a QR code


const emailadd = 'info.noi24@gmail.com';
const emailpass = 'itms hmqt dxbw jrbu';

// Function to send an email with a QR code attachment and HTML body
async function sendEmailWithHTML(toEmail, subject, htmlBody, attachmentPath) {
    const transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            user: emailadd,
            pass: emailpass
        }
    });

    const mailOptions = {
        from: emailadd,
        to: toEmail,
        subject: subject,
        html: htmlBody,

    };

    try {
        await transporter.sendMail(mailOptions);
        console.log(`Email sent to ${toEmail}`);
    } catch (error) {
        console.error('Error sending email:', error.message);
    }
}

// Path to the CSV file containing emails and first names
const csvFilePath = 'data.csv';

// Read emails and first names from the CSV file
const emailData = [];
fs.createReadStream(csvFilePath)
    .pipe(csvParser())
    .on('data', (row) => {
        const { Email, Name } = row;
        emailData.push({ email: Email, name: Name });
    })
    .on('end', async () => {
        // Create and write to CSV file
        const csvFilename = 'tokens_and_emails.csv';
        const csvStream = csvWriter();
        csvStream.pipe(fs.createWriteStream(csvFilename));
        csvStream.write({ Token: 'Token', Email: 'Email' });

        // Iterate through emails
        for (const { email, name } of emailData) {
            // Generate a unique token for each email
            const token = generateUniqueToken();

            // Write to CSV
            csvStream.write({ Name: name, Token: token, Email: email });



            // HTML body for the email
            const subject = 'Welcome to NOI 2024 - 1st February Contest!';
            const htmlBody = `
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NOI 2024 - 1st February Contest</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #fff;
            color: #000;
            margin: 0;
            padding: 20px;
        }

        h2 {
            color: #DAA733;
        }

        p {
            margin: 15px 0;
        }

        .link {
            color: #DAA733;
            text-decoration: none;
            font-weight: bold;
        }

        .link:hover {
            text-decoration: underline;
        }

        .date-container {
            background-color: #444;
            padding: 10px;
            border-radius: 5px;
            color: #fff;
        }

        .date {
            color: #D32F2F;
        }

        button {
            background-color: #DAA733;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        button:hover {
            background-color: #997521;
        }
    </style>
</head>

<body>
    <h2>Welcome to NOI 2024 - 1st monthly Contest!</h2>
    <p>Dear ${name},</p>
    <p>Thank you for registering for the National Olympiad in Informatics (NOI) 2024.</p>
    <p>We are excited to announce the commencement of the 1st monthly Contest, which will serve as a valuable practice
        session and contribute to your qualification progress for the national finals.</p>
    <div class="date-container">
        <h3>February Contest Details:</h3>
        <ul>
            <li>Start: <span class="date">Midnight of 24th February</span></li>
            <li>End: <span class="date">Midnight of 29th February</span></li>
            <li>Platform: HackerRank</li>
            <li>
                <p>Here is the HackerRank link for the contest: <a class="link" target="\_blank"
                        href="https://www.hackerrank.com/noi-2024-feb">https://www.hackerrank.com/noi-2024-feb</a></p>
            </li>
        </ul>
        <button>Register Now</button>
    </div>
    <p>Don't miss this opportunity to sharpen your skills and prepare yourself for NOI. We appreciate your dedication
        and enthusiasm in participating.</p>
    <p>Best Regards,<br>Organizing Committee<br>National Olympiad in Informatics</p>
</body>

</html>
        `;

            // Send email with HTML body and the QR code as an attachment
            await sendEmailWithHTML(email, subject, htmlBody);
        }

        csvStream.end();
        console.log(`Tokens and emails saved to ${csvFilename}`);
    });
