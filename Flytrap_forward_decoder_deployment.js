const new_codec_script = `
/**
 * Entry, decoder.js
 */
function bytes2HexString(bytes) {
    return Array.from(bytes) // Ensure bytes is an array
        .map(byte => byte.toString(16).padStart(2, '0')) // Convert to hex
        .join('');
}

function Decode(port, bytes) {
    return { sensor1: bytes2HexString(bytes) };
}
`;

const jsonBody = {
  name: "LoRaForwarderHEX",
  mime: "application/javascript",
  script: new_codec_script
};

async function POST_custom_WaziGate_CODEC() {

  try {
    const POSTRequestResponse = await fetch("/codecs", {
      method: "POST",
      body: JSON.stringify(jsonBody),
      headers: {
        "Content-type" : "application/json"
      }

    });
    const POSTRequestResponseContent = await POSTRequestResponse.text();
    console.log("New codec id:", POSTRequestResponseContent);
  }
  catch (err) {
		console.error(`Error at POST_custom_WaziGate_CODEC : ${err}`);
		throw err;
	}
}

POST_custom_WaziGate_CODEC()