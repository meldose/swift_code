//
//  iPhoneContentView.swift
//  G1-Damping iPhone App
//
//  Created by Midhun Eldose on 03.07.26.
//

import Foundation
import SwiftUI

struct ContentView: View {
    private let controllerBaseURL = "http://192.168.2.41:8052"

    @State private var sendingMode: RobotMode?
    @State private var lastSucceededMode: RobotMode?
    @State private var statusMessage = "Ready"

    var body: some View {
        NavigationStack {
            VStack(alignment: .leading, spacing: 22) {
                VStack(alignment: .leading, spacing: 6) {
                    Text("G1 Mode Control")
                        .font(.largeTitle.bold())

                    Text(controllerBaseURL)
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }

                LazyVGrid(columns: gridColumns, spacing: 14) {
                    ForEach(RobotMode.allCases) { mode in
                        Button {
                            Task {
                                await sendModeRequest(mode)
                            }
                        } label: {
                            VStack(spacing: 10) {
                                Image(systemName: mode.systemImage)
                                    .font(.system(size: 30, weight: .semibold))

                                Text(sendingMode == mode ? "Sending..." : mode.title)
                                    .font(.headline)
                                    .multilineTextAlignment(.center)
                                    .minimumScaleFactor(0.75)
                            }
                            .frame(maxWidth: .infinity, minHeight: 118)
                        }
                        .buttonStyle(.borderedProminent)
                        .tint(mode.tintColor)
                        .disabled(sendingMode != nil)
                    }
                }

                HStack(spacing: 10) {
                    statusIcon

                    Text(statusMessage)
                        .font(.callout)
                        .foregroundStyle(.secondary)
                        .lineLimit(2)
                        .minimumScaleFactor(0.85)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding()
                .background(.thinMaterial, in: RoundedRectangle(cornerRadius: 8, style: .continuous))

                Spacer()
            }
            .padding()
            .navigationTitle("G1 Damping")
            .navigationBarTitleDisplayMode(.inline)
        }
    }

    private var gridColumns: [GridItem] {
        [
            GridItem(.flexible(), spacing: 14),
            GridItem(.flexible(), spacing: 14)
        ]
    }

    @ViewBuilder
    private var statusIcon: some View {
        if sendingMode != nil {
            ProgressView()
        } else if lastSucceededMode != nil {
            Image(systemName: "checkmark.circle.fill")
                .foregroundStyle(.green)
        } else {
            Image(systemName: "network")
                .foregroundStyle(.secondary)
        }
    }

    @MainActor
    private func sendModeRequest(_ mode: RobotMode) async {
        guard sendingMode == nil else { return }
        guard let url = URL(string: "\(controllerBaseURL)\(mode.path)") else {
            statusMessage = "Invalid controller URL"
            return
        }

        sendingMode = mode
        lastSucceededMode = nil
        statusMessage = "Sending \(mode.title)..."
        defer { sendingMode = nil }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.timeoutInterval = 5

        do {
            let (_, response) = try await URLSession.shared.data(for: request)

            if let httpResponse = response as? HTTPURLResponse,
               !(200...299).contains(httpResponse.statusCode) {
                statusMessage = "\(mode.title) failed: HTTP \(httpResponse.statusCode)"
                return
            }

            lastSucceededMode = mode
            statusMessage = "\(mode.title) sent"
        } catch {
            statusMessage = "\(mode.title) failed: \(error.localizedDescription)"
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

    var systemImage: String {
        switch self {
        case .damp:
            return "waveform.path.ecg"
        case .zeroTorque:
            return "power"
        case .preparation:
            return "gearshape"
        case .walk:
            return "figure.walk"
        }
    }

    var tintColor: Color {
        switch self {
        case .damp:
            return .orange
        case .zeroTorque:
            return .purple
        case .preparation:
            return .blue
        case .walk:
            return .green
        }
    }
}

#Preview {
    ContentView()
}

