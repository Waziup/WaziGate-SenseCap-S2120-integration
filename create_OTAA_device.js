var resp = await fetch("/devices", {
    method: "POST",
    headers: {
                'Content-Type': 'application/json'
        },
    body: JSON.stringify({
        // id: "5cde6d034b9f61" // let the server choose an id
        name: "SenseCapS2120_custom_codec",    // readable device name
        "meta": {
            "codec": "651c9cf468f319084a8c5dbe",    // change with custom codec id: wazigate.local/codecs
            "lorawan": {
              "devEUI": "2CF7F1C0443001A8",         // enter the LoRaWAN device's EUI
              "profile": "Other"                    // we will use "Other" LoRaWAN profile
            }
        },
    })
});
// the device id will be returned
var deviceId = await resp.json();
alert(`new device.id: ${deviceId}`);
