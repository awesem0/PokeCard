const functions = require("firebase-functions");
const axios = require("axios");

const { defineString } = require("firebase-functions/params");
const grokApiKey = defineString("GROK_APIKEY");

exports.generatePoem = functions.https.onCall(async (data, _context) => {   
    console.log('Received data:', data);
    const prompt = data?.prompt || data?.data?.prompt;
    console.log('Extracted prompt:', prompt);
    if (!prompt) {
        console.error('Prompt missing in data:', data);
        throw new functions.https.HttpsError(
            "invalid-argument",
            "Missing prompt"
        );
    }
              
    try {
        const apiKey = grokApiKey.value();
        if (!apiKey) {
            console.log('API key is missing in environment');
            throw new functions.https.HttpsError(
                "internal",
                "API key configuration error"
            );
        }
        console.log('Using API key:', apiKey.substring(0, 10) + '...');
        const response = await axios.post(
            "https://api.x.ai/v1/chat/completions",
            {
                model: "grok-3-latest",
                messages: [
                    {   
                        role: "system",
                        content: `You are a poetic AI. Based on the user theme
(or if vague, like just names/dates, default to a very romantic tone),
generate exactly a title (max 20 characters, full sentence) followed by
exactly 4 lines of poem (each max 44 characters) in simple layman terms
—no complex words, keep it heartfelt. Always fit the theme/tone. Output
in exact format: Title\nLine1\nLine2\nLine3\nLine4`
                    },
                    {
                        role: "user",
                        content: "Theme: " + prompt,
                    },
                ],
                max_tokens: 150,
            },
            {
                headers: {
                    "Authorization": "Bearer " + apiKey,   
                    "Content-Type": "application/json",
                },
            }
        );
    
        const poem = response.data.choices[0].message.content.trim()
            .replace(/```/g, '');
        console.log('Parsed poem:', poem);
        if (!poem) {
            throw new functions.https.HttpsError(
                "internal",
                "Empty poem response"
            );
        }
        return { poem };
    } catch (error) {
        console.error('API error:', error.message);
        throw new functions.https.HttpsError(
            "internal",
            "API call failed: " + error.message
        );
    }
});

exports.getFirebaseConfig = functions.https.onRequest((req, res) => {
    const allowedOrigins = [
        'https://grok-poem-maker-c2ef7.web.app',
        'http://127.0.0.1:5002',
        'http://localhost:5002',
        'https://awesem0.github.io'
    ];
    const origin = req.headers.origin;
    if (allowedOrigins.includes(origin)) {
        res.set('Access-Control-Allow-Origin', origin);
    } else {
        res.set('Access-Control-Allow-Origin',
                'https://grok-poem-maker-c2ef7.web.app');
    }
    res.json({
        apiKey: "AIzaSyDu3yDU8k4H59HARfzr6QlIxT52Q3aniS8",
        authDomain: "grok-poem-maker-c2ef7.firebaseapp.com",
        projectId: "grok-poem-maker-c2ef7",
        storageBucket: "grok-poem-maker-c2ef7.firebasestorage.app",
        messagingSenderId: "1031551345260",
        appId: "1:1031551345260:web:55c541d9148a687d722e49"
    });
});

exports.proxyToGoogleSheets = functions.https.onRequest(async (req, res) => {
    res.set('Access-Control-Allow-Origin', '*');
    res.set('Access-Control-Allow-Methods', 'POST');
    res.set('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.status(204).send('');
        return;
    }

    try {
        const response = await axios.post(
            'https://script.google.com/macros/s/AKfycbxYSuiZJWojDqoYNfPBLzu0b7Ai4MYrLLoP96c9K1eOLzgs_lioJNEgw1fvlhScYJ2pQA/exec',
            req.body,
            { headers: { 'Content-Type': 'application/json' } }
        );
        res.status(200).json(response.data);
    } catch (error) {
        console.error('Proxy error:', error);
        res.status(500).json({ error: 'Failed to submit to Google Sheets' });
    }
});
