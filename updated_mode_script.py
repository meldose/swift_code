//
//  ContentView.swift
//  G1-Damping Watch App
//
//  Created by Midhun Eldose on 02.07.26.
//

import Foundation
import SwiftUI

struct ContentView: View {
    private let controllerBaseURL = "http://192.168.2.41:8052"

    @State private var sendingMode: RobotMode?

    var body: some View {
        VStack(spacing: 8) {
            ForEach(RobotMode.allCases) { mode in
                Button {
                    Task {
                        await sendModeRequest(mode)
                    }
                } label: {
                    Text(sendingMode == mode ? "Sending..." : mode.title)
                        .frame(maxWidth: .infinity)
                        .minimumScaleFactor(0.75)
                }
                .font(.headline)
                .buttonStyle(.borderedProminent)
                .disabled(sendingMode != nil)
            }
        }
        .padding()
    }

    @MainActor
    private func sendModeRequest(_ mode: RobotMode) async {
        guard sendingMode == nil else { return }
        guard let url = URL(string: "\(controllerBaseURL)\(mode.path)") else { return }

        sendingMode = mode
        defer { sendingMode = nil }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.timeoutInterval = 5

        do {
            _ = try await URLSession.shared.data(for: request)
        } catch {
            print("\(mode.title) request failed: \(error.localizedDescription)")
        }
    }
}

private enum RobotMode: CaseIterable, Identifiable {
    case damp
    case zeroTorque
    case preparation
    case walk

    var id: Self { self }

    var title: String {
        switch self {
        case .damp:
            return "Damp"
        case .zeroTorque:
            return "Zero Torque"
        case .preparation:
            return "Preparation"
        case .walk:
            return "Walk"
        }
    }

    var path: String {
        switch self {
        case .damp:
            return "/api/mode/damping"
        case .zeroTorque:
            return "/api/mode/damping"
        case .preparation:
            return "/api/mode/preparation"
        case .walk:
            return "/api/mode/walk"
        }
    }
}

#Preview {
    ContentView()
}

