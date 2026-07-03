<<<<<<< HEAD
# G1 Mode Apps

Minimal SwiftUI code for sending mode requests to a local G1 controller from an Apple Watch or iPhone.

## What It Does

The apps show buttons for damp, zero torque, preparation, and walk modes. When tapped, each button sends one of these POST requests:

```sh
POST http://192.168.2.41:8052/api/mode/damping
POST http://192.168.2.41:8052/api/mode/preparation
POST http://192.168.2.41:8052/api/mode/walk
```

`Damp` and `Zero Torque` both use `/api/mode/damping` unless the controller has a separate zero-torque endpoint.

All buttons are temporarily disabled while a request is running to avoid duplicate taps.

## Files

- `damp_code.py` - SwiftUI `ContentView` code for the watchOS app.
- `iPhoneContentView.swift` - SwiftUI `ContentView` code for an iPhone app.

> Note: the current file contains Swift code even though its extension is `.py`. For use in Xcode, copy or rename the code to `ContentView.swift`.

## Requirements

- Xcode with watchOS support
- A watchOS SwiftUI app target
- An iOS SwiftUI app target, if using the iPhone version
- Apple Watch and controller on the same local network
- iPhone and controller on the same local network
- The controller reachable at `192.168.2.41:8052`

## Watch App Setup

Create or open a watchOS SwiftUI app, then replace `ContentView.swift` with the code from `damp_code.py`.

Because the API uses local plain HTTP, add these keys to the watch app target's `Info.plist`:

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsLocalNetworking</key>
    <true/>
</dict>
<key>NSLocalNetworkUsageDescription</key>
<string>This app connects to the local damping controller.</string>
```

## iPhone App Setup

Create or open an iOS SwiftUI app, then replace the iOS target's `ContentView.swift` with the code from `iPhoneContentView.swift`.

Because the API uses local plain HTTP, add these keys to the iPhone app target's `Info.plist`:

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsLocalNetworking</key>
    <true/>
</dict>
<key>NSLocalNetworkUsageDescription</key>
<string>This app connects to the local damping controller.</string>
```

## API Endpoint

The controller address is defined in the code here:

```swift
private let controllerBaseURL = "http://192.168.2.41:8052"
```

If your controller has a different IP address or port, update this value before building.

## Testing

You can verify the controller endpoints from a computer on the same network with:

```sh
curl -X POST http://192.168.2.41:8052/api/mode/damping
curl -X POST http://192.168.2.41:8052/api/mode/preparation
curl -X POST http://192.168.2.41:8052/api/mode/walk
```

If these curl commands fail, the watch app will not be able to reach the controller either.
=======
     1 +# G1 Damping Watch App
     2 +
     3 +Minimal SwiftUI watchOS code for sending a damping-mode request to a local G1 controller from an Apple Watch.
     4 +
     5 +## What It Does
     6 +
     7 +The app shows a single `Damp` button. When tapped, it sends:
     8 +
     9 +```sh
    10 +POST http://192.168.2.41:8052/api/mode/damping
    11 +```
    12 +
    13 +The button is temporarily disabled while the request is running to avoid duplicate taps.
    14 +
    15 +## Files
    16 +
    17 +- `damp_code.py` - SwiftUI `ContentView` code for the watchOS app.
    18 +
    19 +> Note: the current file contains Swift code even though its extension is `.py`. For use in Xcode, copy or rename the code to `ContentVi
        ew.swift`.
    20 +
    21 +## Requirements
    22 +
    23 +- Xcode with watchOS support
    24 +- A watchOS SwiftUI app target
    25 +- Apple Watch and controller on the same local network
    26 +- The controller reachable at `192.168.2.41:8052`
    27 +
    28 +## Xcode Setup
    29 +
    30 +Create or open a watchOS SwiftUI app, then replace `ContentView.swift` with the code from `damp_code.py`.
    31 +
    32 +Because the API uses local plain HTTP, add these keys to the watch app target's `Info.plist`:
    33 +
    34 +```xml
    35 +<key>NSAppTransportSecurity</key>
    36 +<dict>
    37 +    <key>NSAllowsLocalNetworking</key>
    38 +    <true/>
    39 +</dict>
    40 +<key>NSLocalNetworkUsageDescription</key>
    41 +<string>This app connects to the local damping controller.</string>
    42 +```
    43 +
    44 +## API Endpoint
    45 +
    46 +The endpoint is defined in the code here:
    47 +
    48 +```swift
    49 +private let dampingURL = URL(string: "http://192.168.2.41:8052/api/mode/damping")!
    50 +```
    51 +
    52 +If your controller has a different IP address or port, update this URL before building.
    53 +
    54 +## Testing
    55 +
    56 +You can verify the controller endpoint from a computer on the same network with:
    57 +
    58 +```sh
    59 +curl -X POST http://192.168.2.41:8052/api/mode/damping
    60 +```
    61 +
    62 +If the curl command fails, the watch app will not be able to reach the controller either.
>>>>>>> refs/remotes/origin/main
