//
//  ContentView.swift
//  G1-Damping Watch App
//
//  Created by Midhun Eldose on 02.07.26.
//

import SwiftUI

struct ContentView: View {
    private let baseURL = URL(string: "http://192.168.2.41:8052/api/mode")!

    @State private var sendingMode: RobotMode?
    @State private var statusMessage: String?

    var body: some View {
        VStack(spacing: 8) {
            ForEach(RobotMode.allCases) { mode in
                Button {
                    Task {
                        await sendMode(mode)
                    }
                } label: {
                    Text(sendingMode == mode ? "Sending..." : mode.title)
                        .lineLimit(1)
                        .minimumScaleFactor(0.75)
                        .frame(maxWidth: .infinity)
                }
                .font(.headline)
                .buttonStyle(.borderedProminent)
                .disabled(sendingMode != nil)
            }

            if let statusMessage {
                Text(statusMessage)
                    .font(.caption2)
                    .foregroundStyle(.secondary)
                    .multilineTextAlignment(.center)
            }
        }
        .padding()
    }

    @MainActor
    private func sendMode(_ mode: RobotMode) async {
        guard sendingMode == nil else { return }

        sendingMode = mode
        statusMessage = nil
        defer { sendingMode = nil }

        var request = URLRequest(url: baseURL.appendingPathComponent(mode.pathComponent))
        request.httpMethod = "POST"
        request.timeoutInterval = 5

        do {
            let (_, response) = try await URLSession.shared.data(for: request)

            if let httpResponse = response as? HTTPURLResponse,
               200..<300 ~= httpResponse.statusCode {
                statusMessage = "\(mode.title) sent"
            } else {
                statusMessage = "\(mode.title) failed"
            }
        } catch {
            statusMessage = "\(mode.title) error"
            print("\(mode.title) request failed: \(error.localizedDescription)")
        }
    }
}

private enum RobotMode: String, CaseIterable, Identifiable {
    case damping
    case zeroTorque = "zero_torque"
    case standing
    case Walk


    var id: String {
        rawValue
    }

    var pathComponent: String {
        rawValue
    }

    var title: String {
        switch self {
        case .damping:
            return "Damp"
        case .zeroTorque:
            return "Zero Torque"
        case .standing:
            return "Standing"
        case .Walk:
            return "Walk"
        }
    }
}

#Preview {
    ContentView()
}
