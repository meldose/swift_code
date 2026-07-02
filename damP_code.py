//
//  ContentView.swift
//  G1-Damping Watch App
//
//  Created by Midhun Eldose on 02.07.26.
//

import SwiftUI
struct ContentView: View {
    private let dampingURL = URL(string: "http://192.168.2.41:8052/api/mode/damping")!

    @State private var isSending = false

    var body: some View {
        Button("Damp") {
            Task {
                await sendDampingRequest()
            }
        }
        .font(.headline)
        .buttonStyle(.borderedProminent)
        .disabled(isSending)
        .padding()
    }

    @MainActor
    private func sendDampingRequest() async {
        guard !isSending else { return }

        isSending = true
        defer { isSending = false }

        var request = URLRequest(url: dampingURL)
        request.httpMethod = "POST"
        request.timeoutInterval = 5

        do {
            _ = try await URLSession.shared.data(for: request)
        } catch {
            print("Damping request failed: \(error.localizedDescription)")
        }
    }
}

#Preview {
    ContentView()
}
