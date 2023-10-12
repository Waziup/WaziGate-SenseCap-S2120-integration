package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
)

func main() {
	// Set the ChirpStack API endpoint and authentication credentials
	apiUrl := "http://localhost:8080/api/device-profiles"
	username := "admin"
	password := "admin"

	// Define the custom device profile
	deviceProfile := map[string]interface{}{
		"name":                     "My Custom Device Profile",
		"networkServerID":          "your-network-server-id",
		"organizationID":           "your-organization-id",
		"networkServerVersion":     "3.0.0",
		"macVersion":               "1.0.3",
		"regParamsRevision":        "A",
		"supportsJoin":             true,
		"rxDelay1":                 1,
		"rxDelay2":                 2,
		"rxDelay3":                 3,
		"rxDelay4":                 4,
		"rxFreq2":                  868300000,
		"rxFreq4":                  868500000,
		"factoryPresetFreqs":       []int{868100000, 868300000, 868500000},
		"maxEIRP":                  14,
		"maxDutyCycle":             10,
		"supportsClassB":           true,
		"supportsClassC":           true,
		"pingSlotPeriod":           32,
		"pingSlotDR":               5,
		"pingSlotFreq":             868100000,
		"supportsJoinAcceptCFList": true,
		"supports32bitFCnt":        true,
		"adrAlgorithmID":           "default",
		"installationMargin":       10,
		"rx1DROffset":              1,
		"rx2DR":                    2,
		"rx2Frequency":             869525000,
		"supportsBeacon":           true,
		"beaconFrequency":          869525000,
		"beaconDR":                 5,
		"beaconPower":              14,
		"beaconGatewayID":          "your-gateway-id",
		"classBTimeout":            30,
		"classCTimeout":            30,
		"macCommands": []map[string]interface{}{
			{
				"cid":     "LinkADRReq",
				"payload": "010203",
			},
			{
				"cid":     "DevStatusReq",
				"payload": "",
			},
		},
	}

	// Convert the device profile to JSON
	deviceProfileJson, err := json.Marshal(deviceProfile)
	if err != nil {
		panic(err)
	}

	// Send the POST request to create the custom device profile
	req, err := http.NewRequest("POST", apiUrl, bytes.NewBuffer(deviceProfileJson))
	if err != nil {
		panic(err)
	}
	req.SetBasicAuth(username, password)
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	// Check the response status code
	if resp.StatusCode == 201 {
		fmt.Println("Custom device profile created successfully")
	} else {
		fmt.Println("Error creating custom device profile:", resp.Status)
	}
}
