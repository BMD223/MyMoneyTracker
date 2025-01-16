import SwiftUI

struct ContentView: View {
    @State private var isAddingPosition = false
    @State private var ticker = ""
    @State private var price = ""
    @State private var currency = ""
    @State private var qty = ""
    @State private var type = ""

    var body: some View {
        VStack {
            Text("Add a position")
            Button("Add Position") {
                isAddingPosition = true
            }
        }
        .sheet(isPresented: $isAddingPosition) {
            AddPositionPanel(
                ticker: $ticker,
                price: $price,
                currency: $currency,
                qty: $qty,
                type: $type,
                isPresented: $isAddingPosition
            )
        }
        .frame(width: 200, height: 200)
    }
}

struct AddPositionPanel: View {
    @Binding var ticker: String
    @Binding var price: String
    @Binding var currency: String
    @Binding var qty: String
    @Binding var type: String
    @Binding var isPresented: Bool

    var body: some View {
        Form {
            TextField("Ticker", text: $ticker)
            TextField("Price", text: $price)
            TextField("Currency", text: $currency)
            TextField("Quantity", text: $qty)
            TextField("Type", text: $type)
            HStack {
                Button("Cancel") { isPresented = false }
                Spacer()
                Button("Save") {
                    savePosition()
                    isPresented = false
                }
            }
        }
        .padding()
    }

    private func savePosition() {
        guard let url = URL(string: "http://127.0.0.1:6767/add_position") else { return }

        let positionData: [String: Any] = [
            "ticker": ticker,
            "price": Double(price) ?? 0.0,
            "currency": currency,
            "qty": Double(qty) ?? 0.0,
            "type": type
        ]
     print("Saving position with data: \(positionData)")

        do {
            let jsonData = try JSONSerialization.data(withJSONObject: positionData)
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
            request.httpBody = jsonData

            URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    print("Error saving position: \(error)")
                    return
                }

                if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 {
                    print("Position saved successfully!")
                } else {
                    print("Failed to save position.")
                }
            }.resume()
        } catch {
            print("Failed to encode position data: \(error)")
        }
    }
}

#Preview {
    ContentView()
}
