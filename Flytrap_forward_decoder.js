function bytes2HexString(bytes) {
    return Array.from(bytes) // Ensure bytes is an array
        .map(byte => byte.toString(16).padStart(2, '0')) // Convert to hex
        .join('')
        .toUpperCase(); // Ensure uppercase output
}

function Decode(port, bytes) {
    return { sensor1: bytes2HexString(bytes) };
}

// Test function to verify decoder
function main() {
    let base64 = "AmcAAA==";

    
    let bytes = Buffer.from(base64, 'base64'); // Convert base64 to byte array
    console.log("Decoded Bytes:", bytes);

    let decoded = Decode(0, bytes); // Pass bytes directly

    console.log("Output:", decoded);
}

main();
